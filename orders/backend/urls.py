from django.urls import path
from .views import RegisterAccount, user_activate

app_name = 'backend'
urlpatterns = [
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/activate/<str:sign>/', user_activate, name='register-activate'),
    # path('user/register/confirm/<str:sign>/', user_activate, name='register-activate'),

]