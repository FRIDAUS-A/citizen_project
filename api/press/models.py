from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin
from press.managers import CustomUserManager
import uuid

class Press(AbstractUser, PermissionsMixin):
	"""
	Press Table
	"""
	name = models.CharField(max_length=255, blank=False)
	press_id = models.CharField(max_length=255, primary_key=True, blank=False, default=str(uuid.uuid4()))
	phone_number = models.CharField(max_length=255, blank=False, unique=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)

	groups = models.ManyToManyField(Group, related_name='press_groups')
	user_permissions = models.ManyToManyField(Permission, 
	related_name='press_user_permissions')

	username = None
	email = models.EmailField('email address', unique=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()
	date_of_birth = models.DateField(blank=True, null=True)
	
	
	def __str__(self):
		"""
		Citizen string representation
		"""
		return self.email
	
class PressPost(models.Model):
	post_id = models.CharField(max_length=255, primary_key=True, blank=False, default=str(uuid.uuid4()))
	title = models.CharField(max_length=255, blank=False)
	content = models.TextField()
	press_id = models.ForeignKey('Press', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)