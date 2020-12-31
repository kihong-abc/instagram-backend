from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from . import views
urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('token-auth/verify/', verify_jwt_token),
    path('token-auth/refresh/', refresh_jwt_token),
    # path('', views.ProfileListView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('login/', views.LoginView.as_view()),
]