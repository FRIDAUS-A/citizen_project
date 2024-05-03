from rest_framework import serializers
from citizen.models import Citizen, Address
from django.contrib.auth import authenticate
from rest_framework import serializers

class CitizenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Citizen
		fields = ['first_name', 'last_name', 'email', 'phone_number']

class AddressSerializer(serializers.Serializer):
	class Meta:
		model = Address
		fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                return user
            else:
                raise serializers.ValidationError("Incorrect email or password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        return user

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Citizen
        fields = '__all__' # Add more fields as needed

    def create(self, validated_data):
        """
        Create and return a new user instance with the validated data.
        """
        citizen = Citizen.objects.create_citizen(
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data.get('date_of_birth'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            created_at=validated_data.get('created_at'),
            updated_at=validated_data.get('updated_at'),
            nin_number=validated_data.get('nin_number'),
            citizen_id=validated_data.get('citizen_id')
        )
        return citizen