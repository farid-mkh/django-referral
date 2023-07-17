from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

from user.views import UserList, UserDetail, Register, RegisterSuperUser, UpdateProfile, Login
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
## urls: root/api-auth/
urlpatterns = [
    path("users/",UserList.as_view(),name="users-list"),
    path("me/",UserDetail.as_view(),name="user-detail"),
    ##
    path('register/',Register.as_view(),name="register"),
    path('create-admin/',RegisterSuperUser.as_view(),name="create-admin"),
    path('update-profile/',UpdateProfile.as_view(),name="update-profile"),
    ## jwt
    path('login', Login.as_view(), name='token_obtain_pair'),## access_token expire time: 5 min, refresh_token: 24h
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'), 
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]