#!/usr/bin/env python3
"""
Quick AI Model Training Script
Trains the carbon reduction AI model in under 1 minute
"""

import os
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from .ai_model import train_and_save_model

def main():
    print("🚀 Training Carbon AI Model...")
    print("=" * 40)
    
    start_time = time.time()
    
    # Train the model
    model = train_and_save_model()
    
    end_time = time.time()
    training_time = end_time - start_time
    
    print(f"\n✅ Training completed in {training_time:.2f} seconds!")
    
    # Test the model
    print("\n🧪 Testing AI Model...")
    
    test_data = {
        'entries': [
            {'metric_type': 'carbon', 'value': 25, 'description': 'Car travel to work', 'created_at': '2024-01-01T10:00:00+00:00'},
            {'metric_type': 'carbon', 'value': 15, 'description': 'Heating home', 'created_at': '2024-01-01T12:00:00+00:00'},
            {'metric_type': 'water', 'value': 200, 'description': 'Long shower', 'created_at': '2024-01-01T08:00:00+00:00'},
            {'metric_type': 'energy', 'value': 12, 'description': 'AC usage', 'created_at': '2024-01-01T14:00:00+00:00'}
        ]
    }
    
    suggestions = model.predict_suggestions(test_data)
    
    print("\n🎯 Sample AI Suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion['title']}")
        print(f"   {suggestion['message']}")
        print(f"   Impact: {suggestion['impact']} | Effort: {suggestion['effort']}")
        print()
    
    print("🎉 AI Model is ready to use!")
    print("\n📝 Next steps:")
    print("   1. Start your Django server")
    print("   2. The AI suggestions will be available at /api/v1/ai-suggestions/")
    print("   3. Users can get personalized carbon reduction advice!")

if __name__ == "__main__":
    main() 