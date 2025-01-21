from django.contrib import admin
from .models import Tour, Driver, TourSchedule

# Register your models here.

admin.site.register(Tour)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
  list_display = ('name', 'vehicle', 'email', 'is_active')
  list_filter = ('is_active',)
  search_fields = ('name', 'email')

@admin.register(TourSchedule)
class TourScheduleAdmin(admin.ModelAdmin):
  list_display = ('tour', 'driver', 'date', 'time', 'capacity', 'available_seats', 'is_active')
  list_filter = ('tour', 'driver', 'date', 'is_active')
  search_fields = ('tour__title', 'driver__name')
  date_hierarchy = 'date'