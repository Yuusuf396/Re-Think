from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ImpactEntry

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class ImpactEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactEntry
        fields = ['id', 'metric_type', 'value', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class DashboardSerializer(serializers.Serializer):
    metric_type = serializers.CharField()
    total_value = serializers.FloatField()
    entry_count = serializers.IntegerField()
    last_entry_date = serializers.DateTimeField()