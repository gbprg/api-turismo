from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminTourViewSet, TourListView


router = DefaultRouter()
router.register(r'admin/tours', AdminTourViewSet, basename='admin-tours')

urlpatterns = [
    path('', include(router.urls)),
    path('tours/', TourListView.as_view(), name='tour-list'),
]