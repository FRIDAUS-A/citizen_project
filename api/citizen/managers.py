from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime
import uuid
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_citizen(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        if 'first_name' not in extra_fields:
            raise ValueError('First name must be added')
        
        if 'last_name' not in extra_fields:
            raise ValueError('Last name must be added')
        extra_fields['created_at'] = datetime.now()
        extra_fields['updated_at'] = datetime.now()
        extra_fields['citizen_id'] = uuid.uuid4()
        extra_fields.setdefault('groups', False)
        extra_fields.setdefault('user_permissions', False)
        citizen = self.model(email=email, **extra_fields)
        citizen.set_password(password)
        citizen.save()
        return citizen
    def create_supercitizen(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_citizen(email, password, **extra_fields)