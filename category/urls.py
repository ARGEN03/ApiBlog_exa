from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]