
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta


User = get_user_model()

# class MetricType(models.TextChoices):
#     CARBON = 'carbon', 'Carbon Footprint (kg CO2)'
#     WATER = 'water', 'Water Usage (liters)'
#     ENERGY = 'energy', 'Energy Consumption (kWh)'
#     WASTE = 'waste', 'Waste Generated (kg)'
#     TRANSPORT = 'transport', 'Transport Distance (km)'
# # Create your models here.


# class ImpactCategory(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     description = models.TextField(blank=True)
#     icon = models.CharField(max_length=50, blank=True)  # For UI icons

#     class Meta:
#         verbose_name_plural = "Impact Categories"

#     def __str__(self):
#         return self.name

# class ImpactLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='impact_logs')
#     metric_type = models.CharField(max_length=20, choices=MetricType.choices)
#     category = models.ForeignKey(ImpactCategory, on_delete=models.SET_NULL, null=True, blank=True)
#     value = models.FloatField(validators=[MinValueValidator(0)])
#     unit = models.CharField(max_length=20, blank=True)  # Auto-populated based on metric_type
#     description = models.CharField(max_length=200, blank=True)
#     location = models.CharField(max_length=100, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)


#     class Meta:
#         ordering = ['-timestamp']
#         indexes = [
#             models.Index(fields=['user', 'metric_type']),
#             models.Index(fields=['timestamp']),
#         ]


class ImpactEntry(models.Model):
    """Core model - tracks user's environmental impact"""

    METRIC_CHOICES = [
        ('carbon', 'Carbon Footprint'),
        ('water', 'Water Usage'),
        ('energy', 'Energy Consumption'),
        ('digital', 'Digital Usage'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='impact_entries')
    metric_type = models.CharField(max_length=20, choices=METRIC_CHOICES)
    value = models.FloatField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Impact Entries"

    def __str__(self):
        return f"{self.user.username} - {self.metric_type}: {self.value}"
