from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
# Create your models here.


class User(AbstractUser):
	username = None
	mobile = models.CharField(max_length=11, unique=True)
	# email = models.EmailField(null=True, blank=True)
	otp = models.PositiveIntegerField(blank=True, null=True)
	otp_create_time = models.DateTimeField(auto_now_add=True)

	objects = UserManager()
	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'mobile'
	backend = 'account_module.model_backend.MobileBackend'


	def __str__(self):
		return f"{self.mobile}"


	class Meta:
		verbose_name = 'کاربر'
		verbose_name_plural = 'کاربران'


class Profile(models.Model):
	user_id = models.ForeignKey(User, related_name='کاربر', on_delete=models.CASCADE)
	name= models.CharField(max_length=25, verbose_name='نام')
	family = models.CharField(max_length=25, verbose_name='نام خانوادگی')
	age = models.IntegerField(verbose_name="سن")
	SEXUALITY_CHOICES=[
		("آقا", "آقا"),
		("خانوم", "خانوم")
	]
	sexuality_type = models.CharField(max_length=10, choices=SEXUALITY_CHOICES, default='آقا')
	avatar = models.ImageField(upload_to='images/avatar', null=True, blank=True)
	is_acitve = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} {self.family}"


	class Meta:
		verbose_name = 'پروفایل کاربر'
		verbose_name_plural = 'پروفایل کاربران'

