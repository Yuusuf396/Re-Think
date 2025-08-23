
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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
