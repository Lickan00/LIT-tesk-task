from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, signup, login, verify


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/login/', login, name='login'),
    path('v1/auth/verify/', verify, name='verify'),
    path('v1/users/<int:pk>/', UserViewSet.as_view({'get': 'list'}))
]
