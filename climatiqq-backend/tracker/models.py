from django.db import models

# Create your models here.
class ImpactLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=20)  # carbon, water, energy
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
