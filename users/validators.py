import re
from difflib import SequenceMatcher
from django.core.exceptions import (
    FieldDoesNotExist,
    ValidationError,
)
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.utils.translation import gettext as _, ngettext


class FarsiMinimumLengthValidator:
    """
    Validate whether the password is of a minimum length. Errors are wrriten in farsi.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "رمز عبور باید دارای حداقل %(min_length)d کاراکتر باشد.",
                    "رمز عبور باید دارای حداقل %(min_length)d کاراکتر باشد.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return (
            ngettext(
                "رمز عبور باید دارای حداقل %(min_length)d کاراکتر باشد.",
                "رمز عبور باید دارای حداقل %(min_length)d کاراکتر باشد.",
                self.min_length,
            )
            % {"min_length": self.min_length}
        )


class FarsiUserAttributeSimilarityValidator:
    """
    Validate whether the password is sufficiently different from the user's
    attributes. Errors are wrriten in farsi.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """

    DEFAULT_USER_ATTRIBUTES = ("username", "first_name", "last_name", "email")

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r"\W+", value) + [value]
            for value_part in value_parts:
                if (
                    SequenceMatcher(
                        a=password.lower(), b=value_part.lower()
                    ).quick_ratio()
                    >= self.max_similarity
                ):
                    try:
                        verbose_name = str(
                            user._meta.get_field(attribute_name).verbose_name
                        )
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("رمز عبور شما به %(verbose_name)s بسیار شبیه است."),
                        code="password_too_similar",
                        params={"verbose_name": verbose_name},
                    )

    def get_help_text(self):
        return _("رمز عبور نباید بیش از حد به اطلاعات شخصی شما شبیه باشد.")


class FarsiCommonPasswordValidator(CommonPasswordValidator):
    """
    Validate whether the password is a common password. Errors are wrriten in farsi.
    """

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("رمز عبور بیش از حد ساده است."),
                code="password_too_common",
            )

    def get_help_text(self):
        return _("رمز عبور نباید بیش از حد ساده و معمول باشد.")


class FarsiNumericPasswordValidator:
    """
    Validate whether the password is alphanumeric. Errors are wrriten in farsi.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("رمز عبور نمیتواند فقط از اعداد باشد."),
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return _("رمز عبور نمیتواند فقط از اعداد باشد.")
