from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tour, TourSchedule
from .serializers import TourSerializer, TourScheduleSerializer
from django.utils.timezone import now

# Create your views here.

# Para o admin
class AdminTourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAdminUser]

# Para turistas
class TourListView(ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TourDetailView(RetrieveAPIView):  # Change to RetrieveAPIView
    queryset = Tour.objects.prefetch_related('images')
    serializer_class = TourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'pk'  # Specify lookup field

class AvailableToursSchedulesView(ListAPIView):
    serializer_class = TourScheduleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tour_id = self.kwargs['tour_id']
        date = self.request.query_params.get('date')

        queryset = TourSchedule.objects.filter(
            tour_id=tour_id,
            is_active=True,
            available_seats__gt=0,
            date__gte=now().date()
        ).select_related('tour', 'driver')

        if date:
            queryset = queryset.filter(date=date)
        
        return queryset
            
    
class BookingCreateView(APIView):
    def post(self, request):
        schedule_id = request.data.get('schedule_id')
        try:
            schedule = TourSchedule.objects.get(id=schedule_id)
            # Verificar disponibilidade
            if schedule.available_seats >= request.data.get('number_of_people', 1):
                # Processar a reserva
                # Atualizar available_seats
                schedule.available_seats -= request.data.get('number_of_people', 1)
                schedule.save()
                return Response({'message': 'Reserva realizada com sucesso'})
            return Response({'error': 'Não há assentos suficientes'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        except TourSchedule.DoesNotExist:
            return Response({'error': 'Agendamento não encontrado'}, 
                        status=status.HTTP_404_NOT_FOUND)