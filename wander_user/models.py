from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from wander_core.models import BaseModel
from .exceptions import UserAlreadyExist


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username=None, email=None, password=None):
        """Create and return a `User` with an email, username and password."""
        if not any([username, email]):
            raise TypeError('Users must have one of them to input: username, email.')

        if self.model.objects.all().filter(username=username).exists():
            raise UserAlreadyExist("username already used.")

        if self.model.objects.all().filter(email=self.normalize_email(email)).exists():
            raise UserAlreadyExist("email already used.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, email=None):
        """
        Create and return a `User` with superuser powers.

        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    用户名或者邮箱加密码登录
    """
    username_validator = UnicodeUsernameValidator()

    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField('username',
                                max_length=150,
                                unique=True,
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                validators=[username_validator],
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                }, db_index=True, null=True)

    email = models.EmailField(db_index=True, max_length=255, unique=True,
                              null=True)

    nickname = models.CharField('nickname', max_length=300, blank=True, null=True)

    # 一般不要删除用户！ 而是将本字段设置为False
    is_active = models.BooleanField('active',
                                    default=True,
                                    help_text=
                                    'Designates whether this user should be treated as active. '
                                    'Unselect this instead of deleting accounts.')

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # falsed.
    is_staff = models.BooleanField('staff status',
                                   default=False,
                                   help_text='Designates whether the user can log into this admin site.')

    # More fields required by Django when specifying a custom user model.
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        if self.username:
            return self.username
        elif self.email:
            return self.email
        else:
            return 'unknown username'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class Profile(BaseModel):
    """
    User类用户不太重要的档案信息
    """
    # As mentioned, there is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField('wander_user.User', on_delete=models.CASCADE)

    # Each user profile will have a field where they can tell other users
    # something about themselves. This field will be empty when the user
    # creates their account, so we specify `blank=True`.
    bio = models.TextField(blank=True)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. Similar to `bio`, this field is not required. It may be blank.
    image = models.URLField(blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username
