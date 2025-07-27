#!/usr/bin/env python3
"""
Test script for the simplified AI model
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tracker.ai_model import carbon_ai_model

def test_ai_model():
    """Test the AI model with sample data"""
    print("🧪 Testing AI Model...")
    
    # Sample user data
    sample_user_data = {
        'entries': [
            {
                'carbon_footprint': 15.5,
                'water_usage': 180,
                'energy_usage': 12.3,
                'created_at': '2024-01-15T10:00:00Z'
            },
            {
                'carbon_footprint': 8.2,
                'water_usage': 120,
                'energy_usage': 6.7,
                'created_at': '2024-01-16T10:00:00Z'
            },
            {
                'carbon_footprint': 22.1,
                'water_usage': 250,
                'energy_usage': 15.8,
                'created_at': '2024-01-17T10:00:00Z'
            }
        ]
    }
    
    try:
        # Test prediction
        result = carbon_ai_model.predict_suggestions(sample_user_data)
        
        print("✅ AI Model Test Successful!")
        print(f"Model Type: {result.get('model_type', 'unknown')}")
        print(f"Confidence: {result.get('confidence', 0)}")
        print(f"Suggestions: {len(result.get('suggestions', []))}")
        
        # Print suggestions
        for i, suggestion in enumerate(result.get('suggestions', []), 1):
            print(f"\n{i}. {suggestion.get('title', 'Unknown')}")
            print(f"   Description: {suggestion.get('description', 'No description')}")
            print(f"   Category: {suggestion.get('category', 'general')}")
            print(f"   Impact: {suggestion.get('impact', 'medium')}")
            print(f"   Difficulty: {suggestion.get('difficulty', 'easy')}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Model Test Failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_model()
    sys.exit(0 if success else 1) 