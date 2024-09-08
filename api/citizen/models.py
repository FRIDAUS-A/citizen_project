from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, Permission
from citizen.managers import CustomUserManager
import uuid

#from press import models

class Citizen(AbstractBaseUser):
	citizen_id = models.CharField(max_length=255, primary_key=True, blank=False)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30, blank=False)
	last_name=models.CharField(max_length=30, blank=False)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_press = models.BooleanField(default=False)
	phone_number = models.CharField(max_length=255, blank=False, unique=True)
	address = models.TextField()
	nin_number = models.CharField(max_length=20, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	USERNAME_FIELD = 'email'
	objects = CustomUserManager()

	def __str__(self):
		"""
		Citizen string representation
		"""
		return self.email
	
	"""
	groups = models.ManyToManyField(Group, related_name='citizen_groups')
	user_permissions = models.ManyToManyField(Permission, related_name='citizen_user_permissions')
	"""