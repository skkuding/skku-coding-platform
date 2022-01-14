import os
import re
from datetime import timedelta

from django.conf import settings
from django.contrib import auth
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from options.options import SysOptions
from utils.api import APIView, validate_serializer
from utils.captcha import Captcha
from utils.shortcuts import rand_str
from utils.cache import cache
from utils.constants import CacheKey
from utils.decorators import login_required
from ..models import User, UserProfile
from ..serializers import (ApplyResetPasswordSerializer, DeleteAccountSerializer, ResetPasswordSerializer, SendEmailAuthSerializer,
                           UserChangePasswordSerializer, UserLoginSerializer,
                           UserRegisterSerializer, EmailAuthSerializer, UsernameOrEmailCheckSerializer,
                           UserChangeEmailSerializer)
from ..serializers import (UserProfileSerializer,
                           EditUserProfileSerializer, ImageUploadForm, EditUserSettingSerializer, UserSerializer)
from ..tasks import send_email_async


class UserProfileAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="username",
                in_=openapi.IN_QUERY,
                description="Specific user profile with `username`",
                type=openapi.TYPE_STRING,
            ),
        ],
        opearation_description="Get user information if logged in",
        responses={200: UserProfileSerializer},
    )
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, **kwargs):
        """
        Determine whether to log in, and return user information if logged in
        """
        user = request.user
        if not user.is_authenticated:
            return self.success()
        show_real_name = False
        username = request.GET.get("username")
        try:
            if username:
                if not username == user.username:
                    return self.error("You only can get your profile")
                user = User.objects.get(username=username, is_disabled=False)
            else:
                user = request.user
                # The api returns your own information, you can return real_name
                show_real_name = True
        except User.DoesNotExist:
            return self.error("User does not exist")
        return self.success(UserProfileSerializer(user.userprofile, show_real_name=show_real_name).data)

    @swagger_auto_schema(
        request_body=EditUserProfileSerializer,
        description="Update user profile",
        responses={200: UserProfileSerializer},
    )
    @validate_serializer(EditUserProfileSerializer)
    @login_required
    def put(self, request):
        data = request.data
        user_profile = request.user.userprofile
        for k, v in data.items():
            setattr(user_profile, k, v)
        user_profile.save()
        return self.success(UserProfileSerializer(user_profile, show_real_name=True).data)


class UserSettingAPI(APIView):
    @validate_serializer(EditUserSettingSerializer)
    @login_required
    def put(self, request):
        data = request.data
        user = request.user
        setattr(user, "major", data["major"])
        user.save()
        return self.success(UserSerializer(user).data)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, **kwargs):
        """
        Determine whether to log in, and return user information if logged in
        """
        user = request.user
        if not user.is_authenticated:
            return self.success()
        username = request.GET.get("username")
        try:
            if username:
                user = User.objects.get(username=username, is_disabled=False)
            else:
                user = request.user
                # The api returns your own information, you can return real_name
        except User.DoesNotExist:
            return self.error("User does not exist")
        return self.success(UserSerializer(user).data)


class AvatarUploadAPI(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                required=True,
                type=openapi.TYPE_FILE,
            ),
        ],
    )
    @login_required
    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data["image"]
        else:
            return self.error("Invalid file content")
        if avatar.size > 2 * 1024 * 1024:
            return self.error("Picture is too large")
        suffix = os.path.splitext(avatar.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.error("Unsupported file format")

        name = rand_str(10) + suffix
        with open(os.path.join(settings.AVATAR_UPLOAD_DIR, name), "wb") as img:
            for chunk in avatar:
                img.write(chunk)
        user_profile = request.user.userprofile

        user_profile.avatar = f"{settings.AVATAR_URI_PREFIX}/{name}"
        user_profile.save()
        return self.success("Succeeded")


class UserLoginAPI(APIView):
    @swagger_auto_schema(request_body=UserLoginSerializer)
    @validate_serializer(UserLoginSerializer)
    def post(self, request):
        """
        User login api
        """
        data = request.data
        user = auth.authenticate(username=data["username"], password=data["password"])
        # None is returned if username or password is wrong
        if not user:
            return self.error("Invalid username or password")
        if user.is_disabled:
            return self.error("Your account has been disabled")
        if not user.has_email_auth:
            return self.error("Your need to authenticate your email")
        auth.login(request, user)
        return self.success("Succeeded")


class UserLogoutAPI(APIView):
    def get(self, request):
        auth.logout(request)
        return self.success()


class UsernameOrEmailCheck(APIView):
    @swagger_auto_schema(
        request_body=UsernameOrEmailCheckSerializer,
        description="Check if username or email is valid and not duplicate.\n0 means valid, 1 means duplicate, 2 means invlalid student ID or university email.",
    )
    @validate_serializer(UsernameOrEmailCheckSerializer)
    def post(self, request):
        data = request.data
        # 1 means already exist.
        # 2 means not student ID / university email
        result = {
            "username": 0,
            "email": 0
        }
        if data.get("username"):
            if User.objects.filter(username=data["username"].lower()).exists():
                result["username"] = 1
            elif not re.match(r"^20[0-9]{8}$", data["username"]):
                result["username"] = 2
        if data.get("email"):
            if User.objects.filter(email=data["email"].lower()).exists():
                result["email"] = 1
            elif data["email"].split("@")[1] not in ("g.skku.edu", "skku.edu"):
                result["email"] = 2
        return self.success(result)


class UserRegisterAPI(APIView):
    @swagger_auto_schema(request_body=UserRegisterSerializer)
    @validate_serializer(UserRegisterSerializer)
    def post(self, request):
        """
        User register api
        """
        if not SysOptions.allow_register:
            return self.error("Register function has been disabled by admin")

        data = request.data
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()

        email_auth_token = data["token"]
        token_cache_key = f"{CacheKey.auth_token_cache}:{email_auth_token}"
        email_cache_key = f"{CacheKey.auth_email_cache}:{email_auth_token}"
        auth_email = cache.get(email_cache_key)
        if not cache.get(token_cache_key):
            return self.error("Token does not exist")
        if not data["email"] == auth_email:
            return self.error("It is not authenticated email")

        if User.objects.filter(username=data["username"]).exists():
            return self.error("Username already exists")
        if not re.match(r"^20[0-9]{8}$", data["username"]):
            return self.error("Not student ID")

        user = User.objects.create(username=data["username"], email=data["email"], major=data["major"])
        user.set_password(data["password"])
        user.has_email_auth = True
        user.save()

        UserProfile.objects.create(user=user)

        cache.delete(token_cache_key)
        cache.delete(email_cache_key)
        return self.success("Succeeded")


class DeleteAccountAPI(APIView):
    @swagger_auto_schema(
        request_body=DeleteAccountSerializer,
        operation_description="Check user password",
    )
    @validate_serializer(DeleteAccountSerializer)
    @login_required
    def post(self, request):
        data = request.data
        user = auth.authenticate(username=request.user.username,
                                 email=data["email"],
                                 password=data["password"])
        if not user:
            return self.error("Invalid email or password")
        if request.user.is_super_admin():
            return self.error("super admin account cannot be deleted")
        User.objects.filter(id=request.user.id).delete()
        return self.success()


class EmailAuthAPI(APIView):
    @swagger_auto_schema(
        request_body=EmailAuthSerializer,
        operation_description="Authorize user with url sent to email",
    )
    @validate_serializer(EmailAuthSerializer)
    def post(self, request):
        email_auth_token = request.data["token"]
        token_cache_key = f"{CacheKey.auth_token_cache}:{email_auth_token}"
        email_cache_key = f"{CacheKey.auth_email_cache}:{email_auth_token}"

        if not cache.get(token_cache_key):
            return self.error("Token does not exist")
        email = cache.get(email_cache_key)

        return self.success({"email": email})


class SendEmailAuthAPI(APIView):
    @swagger_auto_schema(
        request_body=SendEmailAuthSerializer,
        operation_description="Send email to authenticate user's email for register",
    )
    @validate_serializer(SendEmailAuthSerializer)
    def post(self, request):
        if request.user.is_authenticated:
            return self.error("You have already logged in")
        data = request.data
        email = data["email"]
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("Invalid captcha")
        if User.objects.filter(email=email).exists():
            return self.error("Email already exists")
        if email.split("@")[1] not in ("g.skku.edu", "skku.edu"):
            return self.error("Invalid domain (Use skku.edu or g.skku.edu)")

        email_auth_token = rand_str()
        token_cache_key = f"{CacheKey.auth_token_cache}:{email_auth_token}"
        email_cache_key = f"{CacheKey.auth_email_cache}:{email_auth_token}"
        if cache.get(token_cache_key):
            cache.delete(token_cache_key)
        if cache.get(email_cache_key):
            cache.delete(email_cache_key)
        cache.set(token_cache_key, email_auth_token, 1200)
        cache.set(email_cache_key, email, 1200)

        render_data = {
            "username": email,
            "website_name": SysOptions.website_name,
            "link": f"{SysOptions.website_base_url}/register/{email_auth_token}"
        }
        email_html = render_to_string("email_auth.html", render_data)
        send_email_async.send(from_name=SysOptions.website_name_shortcut,
                              to_email=email,
                              to_name=email,
                              subject="Email Authentication",
                              content=email_html)

        return self.success()


class UserChangeEmailAPI(APIView):
    @swagger_auto_schema(
        request_body=UserChangeEmailSerializer,
        operation_description="Change user email",
    )
    @validate_serializer(UserChangeEmailSerializer)
    @login_required
    def post(self, request):
        data = request.data
        user = auth.authenticate(username=request.user.username, password=data["password"])
        if not user:
            return self.error("Wrong password")
        data["new_email"] = data["new_email"].lower()
        if User.objects.filter(email=data["new_email"]).exists():
            return self.error("The email is owned by other account")
        if data["new_email"].split("@")[1] not in ("g.skku.edu", "skku.edu"):
            return self.error("Invalid domain (Use skku.edu or g.skku.edu)")
        user.email = data["new_email"]
        user.save()
        return self.success("Succeeded")


class UserChangePasswordAPI(APIView):
    @swagger_auto_schema(
        request_body=UserChangePasswordSerializer,
        operation_description="Change user password",
    )
    @validate_serializer(UserChangePasswordSerializer)
    @login_required
    def post(self, request):
        """
        User change password api
        """
        data = request.data
        username = request.user.username
        user = auth.authenticate(username=username, password=data["old_password"])
        if not user:
            return self.error("Invalid old password")
        user.set_password(data["new_password"])
        user.save()
        return self.success("Succeeded")


class ApplyResetPasswordAPI(APIView):
    @swagger_auto_schema(
        request_body=ApplyResetPasswordSerializer,
        operation_description="Send link to email to reset password",
    )
    @validate_serializer(ApplyResetPasswordSerializer)
    def post(self, request):
        if request.user.is_authenticated:
            return self.error("You have already logged in, are you kidding me? ")
        data = request.data
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("Invalid captcha")
        try:
            user = User.objects.get(email__iexact=data["email"])
        except User.DoesNotExist:
            return self.error("User does not exist")
        if user.reset_password_token_expire_time and 0 < int(
                (user.reset_password_token_expire_time - now()).total_seconds()) < 20 * 60:
            return self.error("You can only reset password once per 20 minutes")
        user.reset_password_token = rand_str()
        user.reset_password_token_expire_time = now() + timedelta(minutes=20)
        user.save()
        render_data = {
            "username": user.username,
            "website_name": SysOptions.website_name,
            "link": f"{SysOptions.website_base_url}/reset-password/{user.reset_password_token}"
        }
        email_html = render_to_string("reset_password_email.html", render_data)
        send_email_async.send(from_name=SysOptions.website_name_shortcut,
                              to_email=user.email,
                              to_name=user.username,
                              subject="Reset your password",
                              content=email_html)
        return self.success("Succeeded")


class ResetPasswordAPI(APIView):
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        operation_description="Get token from email and set new password",
    )
    @validate_serializer(ResetPasswordSerializer)
    def post(self, request):
        data = request.data
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("Invalid captcha")
        try:
            user = User.objects.get(reset_password_token=data["token"])
        except User.DoesNotExist:
            return self.error("Token does not exist")
        if user.reset_password_token_expire_time < now():
            return self.error("Token has expired")
        user.reset_password_token = None
        user.set_password(data["password"])
        user.save()
        return self.success("Succeeded")
