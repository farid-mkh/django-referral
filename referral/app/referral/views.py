from rest_framework import generics, response, status, decorators, exceptions
from django.utils.translation import gettext_lazy as _
from referral.models import Referral
from referral.serializer import ReferralSerializer,ReferralCreateSerializer
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
def assign_referral_to_user(request):
    referral = Referral.objects.get(pk=request.data['referral_code'])
    invited_user = User.objects.get(pk=request.data['invited_user'])
    if invited_user in referral.invited_user.filter(is_active=True):
        raise exceptions.ValidationError({"invited_user":_("This user has already been invited!")})
    if referral.user == invited_user:
        raise exceptions.ValidationError({"invited_user":_("The referral owner can't be the invited user!")})
    referral.invited_user.add(invited_user)
    referral.save()
    return response.Response('done', status=status.HTTP_200_OK)
    
    
class ReferralRetrieveAndUpdateAndDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, retrieve and delete referral codes
    """
    model = Referral
    serializer_class = ReferralSerializer