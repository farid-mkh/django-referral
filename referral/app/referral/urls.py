from django.urls import path
from referral.views import ReferralList,ReferralCreate,ReferralRetrieve,assign_referral_to_user


urlpatterns = [
    path('',ReferralList.as_view(),name="referral-list"),
    path('create',ReferralCreate.as_view(),name="referral-create"),
    path('assign',assign_referral_to_user,name="referral-assign"),
    path('<str:pk>', ReferralRetrieve.as_view(), name="referral-detail"),
]