from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import SignUpAPIView, UserViewSet

app_name = 'users'

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet, basename="users")
urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(), name="token"),
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('v1/', include(users_router.urls)),
]
