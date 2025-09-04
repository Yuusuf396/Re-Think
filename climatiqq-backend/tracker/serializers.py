from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ImpactEntry

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        print(f"Validating registration data: {data}")
        
        # Check if passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Check password length
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        
        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        
        print("Registration data validation passed")
        return data
    
    def create(self, validated_data):
        print(f"Creating user with validated data: {validated_data}")
        try:
            validated_data.pop('password_confirm')
            user = User.objects.create_user(**validated_data)
            print(f"User created successfully: {user.username}")
            return user
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise

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