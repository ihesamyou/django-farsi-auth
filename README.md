# Farsi validation errors for django auth forms

Django authentication forms customized to show validation errors in farsi.<br>
Custom validators are used to validate passwords.<br>
A live example of this app is implemented on https://ihosseinu.info/register.<br><br>

![farsi-forms](https://user-images.githubusercontent.com/86075967/150630151-dd85e501-510b-4b7b-85d1-c8f768dacd97.png)
<br><br>

## Note
You should use and install this app before running makemigrations and migrate command.<br>
This is because we use a custom User model.<br>
More information about why we should not define a custom User model midproject is available on <a href="https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project">Django Documentation</a>.


# Installation<br>
<ul>
<li>Install dependencies in requirements.txt</li>
<li>Create a new django project (django-admin startproject project).</li>
<li>Copy and paste users folder in the root directory of your project.</li>
<li>Make these changes in settings.py:</li><br>


```
INSTALLED_APPS = [
  ...,
  'users.apps.UsersConfig',
  ]
  
  
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "users.validators.FarsiUserAttributeSimilarityValidator",
    },
    {
        "NAME": "users.validators.FarsiMinimumLengthValidator",
    },
    {
        "NAME": "users.validators.FarsiCommonPasswordValidator",
    },
    {
        "NAME": "users.validators.FarsiNumericPasswordValidator",
    },
]


AUTH_USER_MODEL = "users.User"
  
# media settings for profile pictures
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
  
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "profile-edit"  # Change this base on your project
LOGOUT_REDIRECT_URL = "login"        # Change this base on your project

# email settings for reset password email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "email host"
EMAIL_PORT = port
EMAIL_HOST_USER = "email"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_TLS = True
```
  
<li>Include users urls in project urls.py:</li><br>

```
  
from django.contrib im is set toport admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
  
```
  
<li>Lastly create a media folder and add a default_profile.png file there. you can change the name of this file in users/models.py</li></ul>
<br>

Note: by default html form validation is set to novalidate. If you want to remove this behavior, remove novalidate from forms in templates.<br><br>

# list of errors:
<ul>
  <li>فیلد {fieldname} الزامی است.</li><br>
  <li>این نام کاربری قبلا انتخاب شده است.</li><br>
  <li>این ایمیل قبلا ثبت شده است.</li><br>
  <li>نام کاربری یا رمز عبور اشتباه است.</li><br>
  <li>این اکانت غیرفعال است.</li><br>
  <li>رمز عبور باید دارای حداقل {min_length} کاراکتر باشد.</li><br>
  <li>رمز عبور شما به {field.verbose_name} بسیار شبیه است.</li><br>
  <li>رمز عبور بیش از حد ساده است.</li><br>
  <li>رمز عبور نمیتواند فقط از اعداد باشد.</li><br>
  <li>شماره همراه باید به صورت ۰۹۱۲۱۱۱۱۱۱۱ وارد شود.</li><br>
  <li>این شماره قبلا ثبت شده است.</li><br>
  <li>هر دو رمز عبور باید دقیقا مثل هم باشند.</li><br>
  <li>رمز عبور فعلی اشتباه است.</li><br>
</ul>
