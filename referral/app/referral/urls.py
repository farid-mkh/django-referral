from django.urls import path
from referral.views import ReferralList,ReferralCreate,ReferralRetrieveAndUpdateAndDelete,assign_referral_to_user


urlpatterns = [
    path('',ReferralList.as_view(),name="referral-list"),
    path('create',ReferralCreate.as_view(),name="referral-create"),
    path('assign',assign_referral_to_user,name="referral-assign"),
    path('<str:pk>', ReferralRetrieveAndUpdateAndDelete.as_view(), name="referral-detail-update-delete"),
]