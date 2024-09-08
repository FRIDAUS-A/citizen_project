from rest_framework import serializers
from press.models import Press, PressPost
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import Group


class PressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ['name', 'email', 'phone_number', 'press_id']


class PressPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressPost
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
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    class Meta:
        model = Press
        fields = '__all__' # Add more fields as needed

    def create(self, validated_data):
        """
        Create and return a new user instance with the validated data.
        """
        groups_data = validated_data.pop('groups', [])
        permissions_data = validated_data.pop('user_permissions', [])
        press = Press.objects.create_press(
            **validated_data)
        """
            email=validated_data['email'],
            password=validated_data['password'],
            #groups=validated_data['groups'],
            phone_number=validated_data.get('phone_number'),
            created_at=validated_data.get('created_at'),
            updated_at=validated_data.get('updated_at'),
            press_id=validated_data.get('press_id'),
            user_permissions=validated_data.get('user_permission'),
            """
        press.groups.set(groups_data)
        press.user_permissions.set(permissions_data)
        return press