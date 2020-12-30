from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# 프로필사진, 이름, 사용자이름(id), 웹사이트, 소개, 이메일, 전화번호, 성별, 비밀번호 정도 필드

class UserManager(BaseUserManager):
    def _create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('username 필드는 필수입니다.')
        # email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('username 필드는 필수입니다.')
        # email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('username 필드는 필수입니다.')
        # email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):

    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = 'F', "Female"

    username = models.CharField(
        unique=True,
        error_messages={
            'unique': '이미 존재하는 이름입니다.'
        }, max_length=20
    )
    avatar = models.ImageField(blank=True)  # TODO: upload_to 추가
    nickname = models.CharField(max_length=20, blank=True)
    site = models.TextField(blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    # phone = models.IntegerField(blank=True,) # 협의
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
