import os
import re
from datetime import timedelta
from importlib import import_module

import qrcode
from django.conf import settings
from django.contrib import auth
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from otpauth import OtpAuth
from rest_framework.parsers import MultiPartParser

from problem.models import Problem
from utils.constants import ContestRuleType
from options.options import SysOptions
from utils.api import APIView, validate_serializer, CSRFExemptAPIView
from utils.captcha import Captcha
from utils.decorators import login_required
from utils.shortcuts import rand_str, img2base64, datetime2str
from ..models import User, UserProfile, AdminType
from ..serializers import (ApplyResetPasswordSerializer, ResetPasswordSerializer,
                           UserChangePasswordSerializer, UserLoginSerializer,
                           UserRegisterSerializer, EmailAuthSerializer, UsernameOrEmailCheckSerializer,
                           RankInfoSerializer, UserChangeEmailSerializer, SSOSerializer)
from ..serializers import (TwoFactorAuthCodeSerializer, UserProfileSerializer,
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


class TwoFactorAuthAPI(APIView):
    @swagger_auto_schema(operation_description="Get QR code")
    @login_required
    def get(self, request):
        """
        Get QR code
        """
        user = request.user
        if user.two_factor_auth:
            return self.error("2FA is already turned on")
        token = rand_str()
        user.tfa_token = token
        user.save()

        label = f"{SysOptions.website_name_shortcut}:{user.username}"
        image = qrcode.make(OtpAuth(token).to_uri("totp", label, SysOptions.website_name.replace(" ", "")))
        return self.success(img2base64(image))

    @swagger_auto_schema(
        request_body=TwoFactorAuthCodeSerializer,
        operation_description="Open 2FA",
    )
    @login_required
    @validate_serializer(TwoFactorAuthCodeSerializer)
    def post(self, request):
        """
        Open 2FA
        """
        code = request.data["code"]
        user = request.user
        if OtpAuth(user.tfa_token).valid_totp(code):
            user.two_factor_auth = True
            user.save()
            return self.success("Succeeded")
        else:
            return self.error("Invalid code")

    @swagger_auto_schema(
        request_body=TwoFactorAuthCodeSerializer,
        operation_description="Turn off 2FA",
    )
    @login_required
    @validate_serializer(TwoFactorAuthCodeSerializer)
    def put(self, request):
        code = request.data["code"]
        user = request.user
        if not user.two_factor_auth:
            return self.error("2FA is already turned off")
        if OtpAuth(user.tfa_token).valid_totp(code):
            user.two_factor_auth = False
            user.save()
            return self.success("Succeeded")
        else:
            return self.error("Invalid code")


class CheckTFARequiredAPI(APIView):
    @swagger_auto_schema(
        request_body=UsernameOrEmailCheckSerializer,
        operation_description="Check TFA is required",
    )
    @validate_serializer(UsernameOrEmailCheckSerializer)
    def post(self, request):
        """
        Check TFA is required
        """
        data = request.data
        result = False
        if data.get("username"):
            try:
                user = User.objects.get(username=data["username"])
                result = user.two_factor_auth
            except User.DoesNotExist:
                pass
        return self.success({"result": result})


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
        if user:
            if user.is_disabled:
                return self.error("Your account has been disabled")
            if not user.has_email_auth:
                return self.error("Your need to authenticate your email")
            if not user.two_factor_auth:
                auth.login(request, user)
                return self.success("Succeeded")

            # `tfa_code` not in post data
            if user.two_factor_auth and "tfa_code" not in data:
                return self.error("tfa_required")

            if OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                auth.login(request, user)
                return self.success("Succeeded")
            else:
                return self.error("Invalid two factor verification code")
        else:
            return self.error("Invalid username or password")


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
        if user:
            if user.two_factor_auth:
                if "tfa_code" not in data:
                    return self.error("tfa_required")
                if not OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                    return self.error("Invalid two factor verification code")
            data["new_email"] = data["new_email"].lower()
            if User.objects.filter(email=data["new_email"]).exists():
                return self.error("The email is owned by other account")
            if data["new_email"].split("@")[1] not in ("g.skku.edu", "skku.edu"):
                return self.error("Invalid domain (Use skku.edu or g.skku.edu)")
            user.email = data["new_email"]
            user.save()
            return self.success("Succeeded")
        else:
            return self.error("Wrong password")


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
        if user:
            if user.two_factor_auth:
                if "tfa_code" not in data:
                    return self.error("tfa_required")
                if not OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                    return self.error("Invalid two factor verification code")
            user.set_password(data["new_password"])
            user.save()
            return self.success("Succeeded")
        else:
            return self.error("Invalid old password")


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
        user.two_factor_auth = False
        user.set_password(data["password"])
        user.save()
        return self.success("Succeeded")


class SessionManagementAPI(APIView):
    @swagger_auto_schema(operation_description="Manage Session")
    @login_required
    def get(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_store = engine.SessionStore
        current_session = request.session.session_key
        session_keys = request.user.session_keys
        result = []
        modified = False
        for key in session_keys[:]:
            session = session_store(key)
            # session does not exist or is expiry
            if not session._session:
                session_keys.remove(key)
                modified = True
                continue

            s = {}
            if current_session == key:
                s["current_session"] = True
            s["ip"] = session["ip"]
            s["user_agent"] = session["user_agent"]
            s["last_activity"] = datetime2str(session["last_activity"])
            s["session_key"] = key
            result.append(s)
        if modified:
            request.user.save()
        return self.success(result)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="session_key",
                in_=openapi.IN_QUERY,
                description="Session Key",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        operation_description="Delete session key"
    )
    @login_required
    def delete(self, request):
        session_key = request.GET.get("session_key")
        if not session_key:
            return self.error("Parameter Error")
        request.session.delete(session_key)
        if session_key in request.user.session_keys:
            request.user.session_keys.remove(session_key)
            request.user.save()
            return self.success("Succeeded")
        else:
            return self.error("Invalid session_key")


class UserRankAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="rule",
                in_=openapi.IN_QUERY,
                description="Rule type of a contest ('ACM' or 'OI')",
                type=openapi.TYPE_STRING,
            ),
        ],
        operation_description="Get User Rank according to Rule Type"
    )
    def get(self, request):
        rule_type = request.GET.get("rule")
        if rule_type not in ContestRuleType.choices():
            rule_type = ContestRuleType.ACM
        profiles = UserProfile.objects.filter(user__admin_type=AdminType.REGULAR_USER, user__is_disabled=False) \
            .select_related("user")
        if rule_type == ContestRuleType.ACM:
            profiles = profiles.filter(submission_number__gt=0).order_by("-accepted_number", "submission_number")
        else:
            profiles = profiles.filter(total_score__gt=0).order_by("-total_score")
        return self.success(self.paginate_data(request, profiles, RankInfoSerializer))


class ProfileProblemDisplayIDRefreshAPI(APIView):
    @swagger_auto_schema(
        operation_description="Update Solved Problem List"
    )
    @login_required
    def get(self, request):
        profile = request.user.userprofile
        acm_problems = profile.acm_problems_status.get("problems", {})
        oi_problems = profile.oi_problems_status.get("problems", {})
        ids = list(acm_problems.keys()) + list(oi_problems.keys())
        if not ids:
            return self.success()
        display_ids = Problem.objects.filter(id__in=ids, visible=True).values_list("_id", flat=True)
        id_map = dict(zip(ids, display_ids))
        for k, v in acm_problems.items():
            v["_id"] = id_map[k]
        for k, v in oi_problems.items():
            v["_id"] = id_map[k]
        profile.save(update_fields=["acm_problems_status", "oi_problems_status"])
        return self.success()


class OpenAPIAppkeyAPI(APIView):
    @swagger_auto_schema(
        operation_description="Configure whether user can use open_api. If possible, generate APIAppkey.",
    )
    @login_required
    def post(self, request):
        user = request.user
        if not user.open_api:
            return self.error("OpenAPI function is truned off for you")
        api_appkey = rand_str()
        user.open_api_appkey = api_appkey
        user.save()
        return self.success({"appkey": api_appkey})


class SSOAPI(CSRFExemptAPIView):
    @swagger_auto_schema(
        operation_description="Generate token for SSO"
    )
    @login_required
    def get(self, request):
        token = rand_str()
        request.user.auth_token = token
        request.user.save()
        return self.success({"token": token})

    @swagger_auto_schema(
        request_body=SSOSerializer,
        operation_description="Find user corresponding with SSO token"
    )
    @method_decorator(csrf_exempt)
    @validate_serializer(SSOSerializer)
    def post(self, request):
        try:
            user = User.objects.get(auth_token=request.data["token"])
        except User.DoesNotExist:
            return self.error("User does not exist")
        return self.success({"username": user.username, "avatar": user.userprofile.avatar, "admin_type": user.admin_type})
