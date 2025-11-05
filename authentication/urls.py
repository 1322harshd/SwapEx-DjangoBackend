from django.urls import path
from .views import StudentSignUpView, CustomTokenObtainPairView, forgot_password_view, give_trust_badge, current_user_profile, deduct_wallet, add_money_to_wallet

urlpatterns = [
    path('signup/', StudentSignUpView.as_view(), name='student-signup'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),  
    path('give-trust-badge/', give_trust_badge, name='give-trust-badge'),
    path('me/', current_user_profile, name='current-user-profile'),
    path('wallet/deduct/', deduct_wallet, name='wallet-deduct'),
    path('wallet/add/', add_money_to_wallet, name='wallet-add'),
]


