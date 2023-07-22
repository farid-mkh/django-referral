from rest_framework import generics, response, status, decorators, exceptions, permissions
from django.utils.translation import gettext_lazy as _
from referral.models import Referral
from referral.serializer import ReferralSerializer
from user.models import User
# Create your views here.
class ReferralList(generics.ListAPIView):
    """
    Create and list referral codes
    """
    model = Referral
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    
class ReferralCreate(generics.CreateAPIView):
    model = Referral
    serializer_class = ReferralSerializer
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        user = payload["user"]
        serializer = self.serializer_class(data={"user":user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
@decorators.api_view(['PATCH'])
@decorators.permission_classes([permissions.IsAuthenticated])
def assign_referral_to_user(request):
    try:
        referral = Referral.objects.get(pk=request.data['referral_code'])
    except:
        raise exceptions.NotFound({"referral_code":_("Invalid referral code!")})
    if request.user in referral.invited_user.filter(is_active=True):
        raise exceptions.ValidationError({"invited_user":_("This user has already been invited!")})
    if referral.user == request.user:
        raise exceptions.ValidationError({"invited_user":_("The referral owner can't be the invited user!")})
    referral.invited_user.add(request.user)
    referral.save()
    return response.Response(status=status.HTTP_204_NO_CONTENT)
    
class ReferralRetrieveAndUpdateAndDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, retrieve and delete referral codes
    """
    model = Referral
    serializer_class = ReferralSerializer