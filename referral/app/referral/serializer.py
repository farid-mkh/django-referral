from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from referral.models import Referral
from user.models import User
from user.serializer import UserSerializer

class ReferralSerializer(ModelSerializer):    
    
    invited_user = UserSerializer(many=True,required=False)
    
    class Meta:
        model = Referral
        fields = '__all__'
