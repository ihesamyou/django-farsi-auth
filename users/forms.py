from django import forms
from django.contrib.auth.forms import (
    SetPasswordForm,
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
)
from .models import Profile, User


class LoginForm(AuthenticationForm):
    """
    Farsi AuthenticationForm
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'فیلد {fieldname} اجباری است.'.format(
                fieldname=field.label)}

    password = forms.CharField(label=("رمز عبور"), widget=forms.PasswordInput)
    error_messages = {
        "invalid_login": ("نام کاربری یا رمز عبور اشتباه است."),
        "inactive": ("این اکانت غیرفعال است."),
    }


class RegisterForm(UserCreationForm):
    """
    Farsi UserCreationFrom
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required':'فیلد {fieldname} اجباری است.'.format(fieldname=field.label),
                'invalid':'یک {fieldname} معتبر وارد کنید.'.format(fieldname=field.label),
            }

    password1 = forms.CharField(
        label="رمز عبور", strip=False, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور", strip=False, widget=forms.PasswordInput
    )
    error_messages = {
        "password_mismatch": ("هر دو رمز عبور باید دقیقا مثل هم باشند.")
    }

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

class PasswordChange(PasswordChangeForm):
    """
    Farsi PasswordChangeForm
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'فیلد {fieldname} اجباری است.'.format(
                fieldname=field.label)}

    old_password = forms.CharField(label=("رمز عبور فعلی"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=("رمز عبور جدید"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label=("تکرار رمز عبور جدید"), widget=forms.PasswordInput
    )
    error_messages = {
        "password_mismatch": ("هر دو رمز عبور باید دقیقا مثل هم باشند."),
        "password_incorrect": ("رمز عبور فعلی اشتباه است."),
    }


class PasswordReset(PasswordResetForm):
    """
    Farsi PasswordResetForm
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'فیلد ایمیل اجباری است.',
                'invalid':'یک ایمیل معتبر وارد کنید.',
            }


class ConfirmPasswordReset(SetPasswordForm):
    """
    Farsi SetPasswordFrom
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'فیلد {fieldname} اجباری است.'.format(
                fieldname=field.label)}

    new_password1 = forms.CharField(label=("رمز عبور جدید"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label=("تکرار رمز عبور جدید"), widget=forms.PasswordInput
    )
    error_messages = {"password_mismatch": "هر دو رمز عبور باید دقیقا مثل هم باشند."}


class UserEditForm(forms.ModelForm):
    """
    A ModelForm for editing User model information by user.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required':'فیلد {fieldname} اجباری است.'.format(fieldname=field.label),
                'invalid':'یک {fieldname} معتبر وارد کنید.'.format(fieldname=field.label),
            }

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    """
    A ModelForm for editing Profile model information by user.
    """
    photo = forms.ImageField(label=None, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ["photo", "phone", "address", "receive_updates"]
