from django.urls import path

from ..views.oj import (ApplyResetPasswordAPI, ResetPasswordAPI,
                        UserChangePasswordAPI, UserRegisterAPI, EmailAuthAPI, UserChangeEmailAPI,
                        UserLoginAPI, UserLogoutAPI, UsernameOrEmailCheck,
                        AvatarUploadAPI, TwoFactorAuthAPI, UserProfileAPI,
                        UserRankAPI, CheckTFARequiredAPI, SessionManagementAPI,
                        ProfileProblemDisplayIDRefreshAPI, OpenAPIAppkeyAPI, SSOAPI, UserSettingAPI)

from utils.captcha.views import CaptchaAPIView

urlpatterns = [
    path("login/", UserLoginAPI.as_view(), name="user_login_api"),
    path("logout/", UserLogoutAPI.as_view(), name="user_logout_api"),
    path("register/", UserRegisterAPI.as_view(), name="user_register_api"),
    path("email_auth/", EmailAuthAPI.as_view(), name="email_auth_api"),
    path("change_password/", UserChangePasswordAPI.as_view(), name="user_change_password_api"),
    path("change_email/", UserChangeEmailAPI.as_view(), name="user_change_email_api"),
    path("apply_reset_password/", ApplyResetPasswordAPI.as_view(), name="apply_reset_password_api"),
    path("reset_password/", ResetPasswordAPI.as_view(), name="reset_password_api"),
    path("captcha/", CaptchaAPIView.as_view(), name="show_captcha"),
    path("check_username_or_email/", UsernameOrEmailCheck.as_view(), name="check_username_or_email"),
    path("profile/", UserProfileAPI.as_view(), name="user_profile_api"),
    path("user/", UserSettingAPI.as_view(), name="user_setting_api"),
    path("profile/fresh_display_id/", ProfileProblemDisplayIDRefreshAPI.as_view(), name="display_id_fresh"),
    path("upload_avatar/", AvatarUploadAPI.as_view(), name="avatar_upload_api"),
    path("tfa_required/", CheckTFARequiredAPI.as_view(), name="tfa_required_check"),
    path("two_factor_auth/", TwoFactorAuthAPI.as_view(), name="two_factor_auth_api"),
    path("user_rank/", UserRankAPI.as_view(), name="user_rank_api"),
    path("sessions/", SessionManagementAPI.as_view(), name="session_management_api"),
    path("open_api_appkey/", OpenAPIAppkeyAPI.as_view(), name="open_api_appkey_api"),
    path("sso/", SSOAPI.as_view(), name="sso_api")
]
