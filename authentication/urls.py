from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (LoginAPIView, PasswordTokenViewAPI, RegistrationAPIView,
                    RequestPasswordResetEmail, SetNewPasswordAPIView)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name="register"),
    #path('login/', LoginAPIView.as_view(), name="login"),
    path('reset-email-request/', RequestPasswordResetEmail.as_view(), name="reset-email-request"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenViewAPI.as_view(), name="password-reset-confirm"),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name="password-reset-complete"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
