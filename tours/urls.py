from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminTourViewSet, TourListView, TourDetailView, AvailableToursSchedulesView

router = DefaultRouter()
router.register(r'admin/tours', AdminTourViewSet, basename='admin-tours')

urlpatterns = [
    path('', include(router.urls)),
    path('tours/', TourListView.as_view(), name='tour-list'),
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour-detail'),
    path('tours/<int:tour_id>/schedules/', AvailableToursSchedulesView.as_view(), name='tour-schedules'),
]
