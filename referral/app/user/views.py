from rest_framework import generics, response, permissions, authentication, status, exceptions
from user.models import User
from django.utils.translation import gettext_lazy as _

from user.serializer import UserSerializer, SuperUserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class Login(TokenObtainPairView):
    '''
    Everyone has access
    '''
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = User.objects.get(mobile_number=request.data.get('mobile_number'))
        user_serializer = UserSerializer(data)
        return response.Response({'profile': user_serializer.data, 'token':serializer.validated_data}, status=status.HTTP_200_OK)

class Register(generics.CreateAPIView):
    '''
    Everyone has access
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile_number')
        payload = {"mobile_number":request.data.get('mobile_number'),"password":request.data.get("password")}
        if User.objects.filter(mobile_number=mobile_number).exists():
            raise exceptions.ValidationError({"mobile_number":"The mobile number is taken!"})
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data = {}
        data["mobile_number"] = mobile_number
        refresh = RefreshToken.for_user(account)
        data['token']= {
            'access_token' : str(refresh.access_token),
            'refresh_token' : str(refresh)
        }
        return response.Response(data,status=status.HTTP_201_CREATED)

class RegisterSuperUser(generics.CreateAPIView):
    '''
    Only superuser has access
    '''
    queryset = User.objects.all()
    serializer_class = SuperUserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get("password")
        serializer = self.serializer_class(data={"mobile_number":mobile_number,"password":password})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        
class UpdateProfile(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args,**kwargs):
        data = User.objects.get(mobile_number=str(request.user))
        serializer = UserSerializer(data)
        return response.Response(serializer.data,status=status.HTTP_200_OK)
    
class ManangeUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self):
        """Retrieve and return authentication user"""
        return self.request.user