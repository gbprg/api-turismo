from django.db import models


# Create your models here.


# PASSEIOS
class Tour(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  image = models.ImageField(upload_to='tour_images/')
  status_promotion = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title
  def get_gallery_images(self):
    return self.images.all()
  
# GALERIA DE IMAGENS
class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tour_gallery/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"Image for {self.tour.title}"    
  
# MOTORISTAS
class Driver(models.Model):
  name = models.CharField(max_length=200, verbose_name='Nome')
  vehicle = models.CharField(max_length=100, verbose_name='Veículo')
  email = models.EmailField(verbose_name='Email')
  contact = models.CharField(max_length=20, verbose_name='Contato', blank=True)
  information = models.TextField(verbose_name='Informações Adicionais')
  is_active = models.BooleanField(default=True, verbose_name='Ativo')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Motorista'
    verbose_name_plural = 'Motoristas'

  def __str__(self):
    return self.name

# AGENDEMENTOS
class TourSchedule(models.Model):
    tour = models.ForeignKey(
        'Tour',
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Passeio'
    )
    driver = models.ForeignKey(
        'Driver',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Motorista'
    )
    date = models.DateField(verbose_name='Data')

    # Usar CharField para armazenar horários como uma string
    time = models.CharField(
        verbose_name='Horários',
        max_length=255,  # Limite suficiente para múltiplos horários
        blank=True,
        null=True
    )

    capacity = models.IntegerField(
        default=10,
        verbose_name='Capacidade Total'
    )
    available_seats = models.IntegerField(
        verbose_name='Assentos Disponíveis'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        unique_together = ['tour', 'driver', 'date']

    def __str__(self):
        return f"{self.tour.title} - ({self.date}) {self.time}"

    # Métodos para converter entre string e lista
    @property
    def time_list(self):
        """Retorna a lista de horários a partir da string armazenada."""
        if self.time:
            return [t.strip() for t in self.time.split(',')]
        return []

    @time_list.setter
    def time_list(self, times):
        """Define os horários a partir de uma lista."""
        if isinstance(times, list):
            self.time = ','.join(times)
        elif isinstance(times, str):
            self.time = times