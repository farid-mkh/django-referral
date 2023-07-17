from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from referral.models import Referral
from user.models import User
from user.serializer import UserSerializer

class ReferralSerializer(ModelSerializer):    
    
    invited_user = UserSerializer(many=True)
    
    class Meta:
        model = Referral
        fields = '__all__'
        
class ReferralCreateSerializer(ModelSerializer):    
    
    invited_user = PrimaryKeyRelatedField(many=True,queryset = User.objects.all())
    
    class Meta:
        model = Referral
        fields = '__all__'