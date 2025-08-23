from django.contrib import admin
from .models import ImpactEntry

# Register your models here.

@admin.register(ImpactEntry)
class ImpactEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'metric_type', 'value', 'description', 'created_at']
    list_filter = ['metric_type', 'created_at', 'user']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'
