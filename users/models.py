from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from PIL import Image


class User(AbstractUser):
    """
    A custom User model with required email, first_name and last_name fields.
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name="نام کاربری",
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': "این نام کاربری قبلا انتخاب شده است."
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name="ایمیل",
        error_messages={"unique": "این ایمیل قبلا ثبت شده است."},
    )
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")


class Profile(models.Model):
    """
    A model to save optional information about users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(blank=True, null=True ,max_length=300, verbose_name="آدرس")
    phone_regex = RegexValidator(regex=r'\d{11}', message=("شماره همراه باید به صورت ۰۹۱۲۱۱۱۱۱۱۱ وارد شود."))
    phone = models.CharField(null=True, blank=True, unique=True, validators=[phone_regex], max_length=11, verbose_name="شماره همراه", help_text="مثال: ۰۹۱۲۱۱۱۱۱۱۱", error_messages={"unique": "این شماره قبلا ثبت شده است."})
    photo = models.ImageField(
        default="default_profile.png",
        upload_to="profile_photos",
        verbose_name="عکس پروفایل",
    )
    receive_updates = models.BooleanField(
        default=False,
        verbose_name="دریافت آپدیت ها",
        help_text="با فعال کردن این گزینه آپدیت های سایت از طریق ایمیل برای شما ارسال میشوند.",
    )
    
    # resizes profile images uploaded by users.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with Image.open(self.photo.path) as image:
            if image.height > 225 or image.width > 225:
                size = (225, 225)
                image.resize(size, Image.ANTIALIAS).save(self.photo.path)

    def __str__(self):
        return f"پروفایل {self.user.username}"
