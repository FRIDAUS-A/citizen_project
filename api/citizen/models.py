from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from citizen.managers import CustomUserManager
import uuid

class Citizen(AbstractUser):
	"""
	Citizen Table
	"""
	#first_name = models.CharField(max_length=128, blank=False)
	#last_name = models.CharField(max_length=128, blank=False)
	#email = models.EmailField(max_length=128, blank=False, unique=True)
	#password = models.CharField(max_length=128, blank=False)
	citizen_id = models.CharField(max_length=255, primary_key=True, blank=False)
	phone_number = models.CharField(max_length=255, blank=False, unique=True)
	address_id = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
	nin_number = models.CharField(max_length=20, blank=True)
	date_of_birth = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now_add=True, null=True)
	

	groups = models.ManyToManyField(Group, related_name='citizen_groups')
	user_permissions = models.ManyToManyField(Permission, related_name='citizen_user_permissions')

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


class Address(models.Model):
	"""
	Address Table
	"""
	address_id = models.CharField(max_length=255, blank=False, primary_key=True, )
	street = models.CharField(max_length=255, blank=True)
	state = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=255, blank=True)
	zip_code = models.CharField(max_length=255, blank=True)
	
	def __str__(self):
		"""
		Address string representation
		"""
		return Address.citizen.first_name + " " + Address.citizen.last_name