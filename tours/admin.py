from django.contrib import admin
from .models import Tour, Driver, TourSchedule, TourImage

# Register your models here.
class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 3  # Allows adding multiple images

class TourAdmin(admin.ModelAdmin):
    inlines = [TourImageInline]

admin.site.register(Tour, TourAdmin)

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