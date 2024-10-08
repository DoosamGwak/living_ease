from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError


class PasswordValidator:
    def validate_password_check(self, password, password2):
        if password != password2:
            raise ValidationError(
                {"msg": "비밀번호가 일치하지 않습니다. 다시 입력해주세요."}
            )


class CustomProfileDeleteValidator:
    def validate_refresh(self, refresh):
        data = self.context["request"].data
        if not "refresh" in data:
            raise ValidationError({"msg": "refresh_token 값을 입력해주세요."})
        try:
            refresh_token = RefreshToken(data["refresh"])
            refresh_token.blacklist()
        except TokenError:
            raise ValidationError(
                {"msg": "refresh_token값이 유효하지 않습니다. 다시 입력해주세요"}
            )
        return refresh

    def validate_check_password(self, password):
        user = self.context["request"].user
        if not user.check_password(password):
            raise ValidationError(
                {"msg": "비밀번호가 일치하지 않습니다. 다시 입력해주세요."}
            )


class OldPasswordValidator:
    def validate_old_password(self, old_password):
        user = self.context["request"].user
        if not user.check_password(old_password):
            raise ValidationError(
                {"msg": "비밀번호가 일치하지 않습니다. 다시 입력해주세요."}
            )
