from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.task import  create_users_from_git_filter


class GithubUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
            Creates and saves a User with the given username, email and password.
        """
        user = self.model(login=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(login, password, **extra_fields)


class GithubUser(AbstractBaseUser, PermissionsMixin):

    login = models.CharField('Login', blank=False, db_index=True, max_length=255, unique=True)
    email = models.CharField('Email', blank=True, db_index=True, max_length=255,null=True)
    is_staff = models.BooleanField('Staff Status', default=False, help_text='Designates', db_index=True)
    followers_url = models.CharField('Followers URL', max_length=255, blank=True)
    following_url = models.CharField('Following URL', max_length=255, blank=True)
    company = models.CharField('Company', max_length=255, blank=True, null=True)
    name = models.CharField('Name', max_length=255, blank=True, null=True)
    location = models.CharField('Location', max_length=255, blank=True, null=True)
    gists_url = models.CharField('Gists URL', max_length=255, blank=True, null=True)
    received_events_url = models.CharField('Received events URL', max_length=255, blank=True, null=True)
    url = models.CharField('URL', max_length=255, blank=True, null=True)
    type = models.CharField('Type', max_length=255, blank=True, null=True)
    score = models.DecimalField('Score', decimal_places=6, max_digits=10, blank=True, null=True)
    avatar_url = models.CharField('Avatar URL', max_length=255, blank=True, null=True)
    events_url = models.CharField('Events URL', max_length=255, blank=True, null=True)
    gravatar_id = models.CharField('Gravatar ID', max_length=255, blank=True, null=True)
    organizations_url = models.CharField('Organizations URL', max_length=255, blank=True, null=True)
    starred_url = models.CharField('Starred URL', max_length=255, blank=True, null=True)
    html_url = models.CharField('Html URL', max_length=255, blank=True, null=True)
    subscriptions_url = models.CharField('Subscriptions URL', max_length=255, blank=True, null=True)
    site_admin = models.BooleanField('Siteadmin', default=False, null=True)
    repos_url = models.CharField('Repos URL', max_length=255, blank=True, null=True)
    bio = models.CharField('Bio', max_length=255, blank=True, null=True)
    blog = models.CharField('Blog', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField('Created At', blank=True, null=True)

    followers = models.IntegerField('Followers', null=True)
    following = models.IntegerField('Following', null=True)
    hireable = models.BooleanField('Hireable', default=False, null=True)
    public_gists = models.CharField('Public Gist', max_length=255, blank=True, null=True)
    public_repos = models.CharField('Public Gist', max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField('Created At', blank=True, null=True)

    node_id = models.CharField('Node id', max_length=255, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)
    modified_date = models.DateTimeField('Modified Date', auto_now=True)

    objects = GithubUserManager()
    USERNAME_FIELD = 'login'


class ApiSearchDetail(models.Model):

    query_params = models.CharField('Query params', blank=True, max_length=255)
    api_response = models.TextField('Api response')
    response_processed = models.BooleanField('Processed', default=False)
    created_date = models.DateTimeField('Created Date', auto_now_add=True)


@receiver(post_save, sender=ApiSearchDetail)
def update_remaining_limits(sender, instance, **kwargs):
    create_users_from_git_filter.delay(instance.pk)

