from rest_framework import serializers
from press.models import Press
from django.contrib.auth import authenticate
from rest_framework import serializers


class PressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
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
        model = Press
        fields = '__all__' # Add more fields as needed

    def create(self, validated_data):
        """
        Create and return a new user instance with the validated data.
        """
        press = Press.objects.create_press(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            created_at=validated_data.get('created_at'),
            updated_at=validated_data.get('updated_at'),
            press_id=validated_data.get('citizen_id'),
            groups=validated_data.get('groups'),
            user_permissions=validated_data.get('user_permission'),
        )
        return press