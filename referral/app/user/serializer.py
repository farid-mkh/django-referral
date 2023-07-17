from pyexpat import model
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _ 

from user.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['is_superuser','is_active','is_staff']
        extra_kwargs = {
            'password':{'write_only':True,'min_length':5},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        group = validated_data.pop("group", None)
        user = super().update(instance,validated_data)
        if group:
            user.group.add(group)
        if password:
            user.set_user(password)
        user.save()
        return user
            
class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["id",'is_superuser','is_active','is_staff']
        extra_kwargs = {
            'password':{'write_only':True,'min_length':5},
        }
        
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return User.objects.create_superuser(**validated_data)    
    

class AuthTokenSerializer(serializers.ModelSerializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False
    )

    def validate(self, attrs):
        """validate and authentication the user"""
        mobile_number = attrs.get("mobile_number")
        password = attrs.get("password")

        user = authenticate(
            request  = self.context.get("request"),
            username = mobile_number
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg,code="authentication")
        attrs['user'] = user
        return attrs
    