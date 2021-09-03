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
from utils.throttling import TokenBucket
from ..decorators import login_required
from ..models import User, UserProfile
from ..serializers import (ApplyResetPasswordSerializer, ResetPasswordSerializer, UserChangeEmailForAuthSerializer,
                           UserChangePasswordSerializer, UserEmailSerializer, UserLoginSerializer,
                           UserRegisterSerializer, EmailAuthSerializer, UserResendEmailForAuthSerializer, UsernameOrEmailCheckSerializer,
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
            return self.error("You need to authenticate your email")
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
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("Invalid captcha")
        if User.objects.filter(username=data["username"]).exists():
            return self.error("Username already exists")
        if not re.match(r"^20[0-9]{8}$", data["username"]):
            return self.error("Not student ID")
        if User.objects.filter(email=data["email"]).exists():
            return self.error("Email already exists")
        if data["email"].split("@")[1] not in ("g.skku.edu", "skku.edu"):
            return self.error("Invalid domain (Use skku.edu or g.skku.edu)")
        user = User.objects.create(username=data["username"], email=data["email"], major=data["major"])
        user.set_password(data["password"])
        user.has_email_auth = False
        user.email_auth_token = rand_str()
        user.save()

        UserProfile.objects.create(user=user)

        render_data = {
            "username": user.username,
            "website_name": SysOptions.website_name,
            "link": f"{SysOptions.website_base_url}/email-auth/{user.email_auth_token}"
        }
        email_html = render_to_string("email_auth.html", render_data)
        send_email_async.send(from_name=SysOptions.website_name_shortcut,
                              to_email=user.email,
                              to_name=user.username,
                              subject="Email Authentication",
                              content=email_html)

        return self.success("Succeeded")


class EmailAuthAPI(APIView):
    @swagger_auto_schema(
        request_body=EmailAuthSerializer,
        operation_description="Authorize user with url sent to email",
    )
    @validate_serializer(EmailAuthSerializer)
    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(email_auth_token=data["token"])
        except User.DoesNotExist:
            return self.error("Token does not exist")
        user.email_auth_token = None
        user.has_email_auth = True
        user.save()
        return self.success("Succeeded")


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


class UserChangeEmailForAuthAPI(APIView):
    @swagger_auto_schema(
        request_body=UserChangeEmailForAuthSerializer,
        operation_description="Change user email for authentication",
    )
    @validate_serializer(UserChangeEmailForAuthSerializer)
    def post(self, request):
        data = request.data
        user = auth.authenticate(username=data["username"], password=data["password"])
        if not user:
            return self.error("Wrong password")
        if user.has_email_auth:
            return self.error("You already have email authenticated")
        data["email"] = data["email"].lower()
        if User.objects.filter(email=data["email"]).exists():
            return self.error("The email is owned by other account")
        if data["email"].split("@")[1] not in ("g.skku.edu", "skku.edu"):
            return self.error("Invalid domain (Use skku.edu or g.skku.edu)")
        user.email = data["email"]
        user.email_auth_token = rand_str()
        user.save()

        render_data = {
            "username": user.username,
            "website_name": SysOptions.website_name,
            "link": f"{SysOptions.website_base_url}/email-auth/{user.email_auth_token}"
        }
        email_html = render_to_string("email_auth.html", render_data)
        send_email_async.send(from_name=SysOptions.website_name_shortcut,
                              to_email=user.email,
                              to_name=user.username,
                              subject="Email Authentication",
                              content=email_html)

        return self.success("Succeeded")


class UserResendEmailForAuthAPI(APIView):
    def throttling(self, user):
        user_bucket = TokenBucket(key=str(user.id),
                                  capacity=1,
                                  fill_rate=1/60,
                                  default_capacity=1,
                                  redis_conn=cache)
        can_consume, wait = user_bucket.consume()
        if not can_consume:
            return "Please wait %d seconds" % (int(wait))

    @swagger_auto_schema(
        request_body=UserResendEmailForAuthSerializer,
        operation_description="Resend authentication email",
    )
    @validate_serializer(UserResendEmailForAuthSerializer)
    def post(self, request):
        data = request.data
        user = auth.authenticate(username=data["username"], password=data["password"])
        error = self.throttling(user)
        if error:
            return self.error(error)
        render_data = {
            "username": user.username,
            "website_name": SysOptions.website_name,
            "link": f"{SysOptions.website_base_url}/email-auth/{user.email_auth_token}"
        }
        email_html = render_to_string("email_auth.html", render_data)
        send_email_async.send(from_name=SysOptions.website_name_shortcut,
                              to_email=user.email,
                              to_name=user.username,
                              subject="Email Authentication",
                              content=email_html)

        return self.success()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="username",
                in_=openapi.IN_QUERY,
                description="Unique username of login request user",
                required=True,
                type=openapi.TYPE_STRING,
            ),
        ],
        opearation_description="Get email of login request user",
    )
    def get(self, request):
        username = request.GET.get("username")
        if username:
            user = User.objects.get(username=username)
            return self.success(UserEmailSerializer(user).data)


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
