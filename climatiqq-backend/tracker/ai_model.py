#!/usr/bin/env python3
"""
Simple AI Model for Carbon Reduction Suggestions
Trained on user behavior patterns and environmental impact data
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime, timedelta

class CarbonAIModel:
    def __init__(self):
        self.model = None
        self.models = []  # Initialize models list
        self.label_encoders = {}
        self.feature_names = [
            'avg_carbon_per_day', 'avg_water_per_day', 'avg_energy_per_day',
            'total_entries', 'days_active', 'carbon_trend', 'activity_frequency',
            'high_impact_activities', 'low_impact_activities'
        ]
        
    def generate_training_data(self):
        """Generate synthetic training data based on common patterns"""
        np.random.seed(42)  # For reproducible results
        
        # Generate 1000 synthetic users with realistic patterns
        n_users = 1000
        data = []
        
        for i in range(n_users):
            # User profile
            avg_carbon = np.random.normal(15, 8)  # kg CO2/day
            avg_water = np.random.normal(150, 50)  # liters/day
            avg_energy = np.random.normal(8, 3)    # kWh/day
            total_entries = np.random.randint(5, 100)
            days_active = np.random.randint(7, 365)
            
            # Trends (positive = increasing, negative = decreasing)
            carbon_trend = np.random.normal(0, 0.5)
            activity_frequency = np.random.uniform(0.1, 1.0)
            
            # Activity patterns
            high_impact = np.random.randint(0, 10)  # car, plane, heating
            low_impact = np.random.randint(0, 20)   # walking, cycling, LED lights
            
            # Generate suggestions based on patterns
            if avg_carbon > 20:
                suggestions = ['reduce_car_usage', 'use_public_transport', 'energy_efficiency']
            elif avg_carbon > 10:
                suggestions = ['optimize_heating', 'reduce_meat_consumption', 'renewable_energy']
            else:
                suggestions = ['maintain_low_carbon', 'share_tips', 'community_engagement']
            
            # Add water-based suggestions
            if avg_water > 200:
                suggestions.extend(['shorter_showers', 'fix_leaks', 'water_efficient_appliances'])
            
            # Add energy-based suggestions
            if avg_energy > 10:
                suggestions.extend(['led_lighting', 'smart_thermostat', 'unplug_devices'])
            
            # Ensure we have at least 3 suggestions
            while len(suggestions) < 3:
                suggestions.append('general_sustainability')
            
            # Take top 3 suggestions
            suggestions = suggestions[:3]
            
            # Create feature vector
            features = [
                avg_carbon, avg_water, avg_energy, total_entries, days_active,
                carbon_trend, activity_frequency, high_impact, low_impact
            ]
            
            data.append({
                'features': features,
                'suggestions': suggestions
            })
        
        return data
    
    def train_model(self):
        """Train the AI model on synthetic data"""
        print("🤖 Training Carbon AI Model...")
        
        # Generate training data
        training_data = self.generate_training_data()
        
        # Prepare features and labels
        X = np.array([item['features'] for item in training_data])
        y = [item['suggestions'] for item in training_data]
        
        # Flatten suggestions for training
        all_suggestions = []
        for suggestions in y:
            all_suggestions.extend(suggestions)
        
        # Create label encoder for suggestions
        unique_suggestions = list(set(all_suggestions))
        self.label_encoders['suggestions'] = LabelEncoder()
        self.label_encoders['suggestions'].fit(unique_suggestions)
        
        # Train multiple models (one for each suggestion slot)
        self.models = []
        for i in range(3):  # Top 3 suggestions
            model = RandomForestClassifier(n_estimators=50, random_state=42)
            
            # Prepare labels for this slot
            slot_labels = []
            for suggestions in y:
                if len(suggestions) > i:
                    slot_labels.append(suggestions[i])
                else:
                    slot_labels.append('general_sustainability')
            
            # Encode labels
            encoded_labels = self.label_encoders['suggestions'].transform(slot_labels)
            
            # Train model
            model.fit(X, encoded_labels)
            self.models.append(model)
        
        print(f"✅ AI Model trained successfully!")
        print(f"   - {len(training_data)} training examples")
        print(f"   - {len(unique_suggestions)} unique suggestions")
        print(f"   - 3 suggestion slots")
        
        return True
    
    def predict_suggestions(self, user_data):
        """Generate personalized suggestions for a user"""
        if not self.models:
            print("❌ Model not trained. Training now...")
            self.train_model()
        
        # Prepare user features
        features = self.extract_user_features(user_data)
        X = np.array([features])
        
        # Get predictions from all models
        suggestions = []
        for i, model in enumerate(self.models):
            prediction = model.predict(X)[0]
            suggestion = self.label_encoders['suggestions'].inverse_transform([prediction])[0]
            suggestions.append(suggestion)
        
        # Remove duplicates and format
        unique_suggestions = list(dict.fromkeys(suggestions))  # Preserve order
        return self.format_suggestions(unique_suggestions[:3])
    
    def extract_user_features(self, user_data):
        """Extract features from user data"""
        entries = user_data.get('entries', [])
        
        if not entries:
            # Default features for new users
            return [10, 150, 8, 0, 1, 0, 0.5, 0, 0]
        
        # Calculate features
        carbon_entries = [e for e in entries if e.get('metric_type') == 'carbon']
        water_entries = [e for e in entries if e.get('metric_type') == 'water']
        energy_entries = [e for e in entries if e.get('metric_type') == 'energy']
        
        # Average daily values
        avg_carbon = np.mean([e.get('value', 0) for e in carbon_entries]) if carbon_entries else 10
        avg_water = np.mean([e.get('value', 0) for e in water_entries]) if water_entries else 150
        avg_energy = np.mean([e.get('value', 0) for e in energy_entries]) if energy_entries else 8
        
        # Activity patterns
        total_entries = len(entries)
        
        # Fix timezone issue for days_active calculation
        try:
            from datetime import timezone
            first_entry_date = datetime.fromisoformat(entries[0]['created_at'].replace('Z', '+00:00'))
            days_active = max(1, (datetime.now(timezone.utc) - first_entry_date).days)
        except:
            days_active = 30  # Default to 30 days if calculation fails
        
        # Trend calculation (simple)
        if len(entries) > 1:
            recent_avg = np.mean([e.get('value', 0) for e in entries[:5]])
            older_avg = np.mean([e.get('value', 0) for e in entries[-5:]])
            carbon_trend = (recent_avg - older_avg) / max(older_avg, 1)
        else:
            carbon_trend = 0
        
        activity_frequency = total_entries / max(days_active, 1)
        
        # High/low impact activities (based on descriptions)
        high_impact = len([e for e in entries if any(word in e.get('description', '').lower() 
                                                    for word in ['car', 'plane', 'heating', 'ac'])])
        low_impact = len([e for e in entries if any(word in e.get('description', '').lower() 
                                                   for word in ['walking', 'cycling', 'led', 'solar'])])
        
        return [avg_carbon, avg_water, avg_energy, total_entries, days_active,
                carbon_trend, activity_frequency, high_impact, low_impact]
    
    def format_suggestions(self, suggestions):
        """Format suggestions into user-friendly messages"""
        suggestion_messages = {
            'reduce_car_usage': {
                'title': '🚗 Reduce Car Usage',
                'message': 'Consider carpooling, public transport, or cycling for short trips. This could reduce your carbon footprint by up to 2.5 kg CO2 per day.',
                'impact': 'High',
                'effort': 'Medium'
            },
            'use_public_transport': {
                'title': '🚌 Use Public Transport',
                'message': 'Switch to buses, trains, or trams. Public transport produces 45% less CO2 than driving alone.',
                'impact': 'High',
                'effort': 'Low'
            },
            'energy_efficiency': {
                'title': '💡 Improve Energy Efficiency',
                'message': 'Upgrade to LED bulbs, use smart thermostats, and unplug devices when not in use.',
                'impact': 'Medium',
                'effort': 'Low'
            },
            'optimize_heating': {
                'title': '🌡️ Optimize Heating',
                'message': 'Lower your thermostat by 1°C to save 7% on heating costs and reduce carbon emissions.',
                'impact': 'Medium',
                'effort': 'Low'
            },
            'reduce_meat_consumption': {
                'title': '🥗 Reduce Meat Consumption',
                'message': 'Try meatless Mondays or plant-based alternatives. This can reduce your carbon footprint by up to 1.5 kg CO2 per day.',
                'impact': 'High',
                'effort': 'Medium'
            },
            'renewable_energy': {
                'title': '☀️ Switch to Renewable Energy',
                'message': 'Consider solar panels or green energy providers to power your home sustainably.',
                'impact': 'High',
                'effort': 'High'
            },
            'maintain_low_carbon': {
                'title': '🌱 Keep Up the Great Work!',
                'message': 'Your carbon footprint is already low. Share your sustainable practices with others!',
                'impact': 'Low',
                'effort': 'Low'
            },
            'share_tips': {
                'title': '📢 Share Your Tips',
                'message': 'Help others reduce their carbon footprint by sharing your sustainable lifestyle tips.',
                'impact': 'Medium',
                'effort': 'Low'
            },
            'community_engagement': {
                'title': '🤝 Community Engagement',
                'message': 'Join local environmental groups or start a sustainability challenge with friends.',
                'impact': 'Medium',
                'effort': 'Medium'
            },
            'shorter_showers': {
                'title': '🚿 Shorter Showers',
                'message': 'Reduce shower time by 2 minutes to save 10 gallons of water per shower.',
                'impact': 'Medium',
                'effort': 'Low'
            },
            'fix_leaks': {
                'title': '🔧 Fix Water Leaks',
                'message': 'A dripping faucet can waste 20 gallons of water per day. Fix leaks promptly.',
                'impact': 'Medium',
                'effort': 'Low'
            },
            'water_efficient_appliances': {
                'title': '🏠 Water-Efficient Appliances',
                'message': 'Install low-flow showerheads and water-efficient washing machines.',
                'impact': 'Medium',
                'effort': 'Medium'
            },
            'led_lighting': {
                'title': '💡 LED Lighting',
                'message': 'Replace incandescent bulbs with LEDs to save 75% on lighting energy.',
                'impact': 'Medium',
                'effort': 'Low'
            },
            'smart_thermostat': {
                'title': '📱 Smart Thermostat',
                'message': 'Install a smart thermostat to automatically optimize heating and cooling.',
                'impact': 'Medium',
                'effort': 'Medium'
            },
            'unplug_devices': {
                'title': '🔌 Unplug Devices',
                'message': 'Unplug chargers and devices when not in use to eliminate phantom energy use.',
                'impact': 'Low',
                'effort': 'Low'
            },
            'general_sustainability': {
                'title': '🌍 General Sustainability',
                'message': 'Continue making small changes every day. Every action counts towards a sustainable future.',
                'impact': 'Low',
                'effort': 'Low'
            }
        }
        
        formatted_suggestions = []
        for suggestion in suggestions:
            if suggestion in suggestion_messages:
                formatted_suggestions.append(suggestion_messages[suggestion])
            else:
                formatted_suggestions.append(suggestion_messages['general_sustainability'])
        
        return formatted_suggestions
    
    def save_model(self, filepath='carbon_ai_model.pkl'):
        """Save the trained model"""
        if self.models:
            model_data = {
                'models': self.models,
                'label_encoders': self.label_encoders,
                'feature_names': self.feature_names
            }
            joblib.dump(model_data, filepath)
            print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath='carbon_ai_model.pkl'):
        """Load a trained model"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.models = model_data['models']
            self.label_encoders = model_data['label_encoders']
            self.feature_names = model_data['feature_names']
            print(f"✅ Model loaded from {filepath}")
            return True
        return False

# Global model instance
carbon_ai_model = CarbonAIModel()

def train_and_save_model():
    """Train and save the AI model"""
    carbon_ai_model.train_model()
    carbon_ai_model.save_model()
    return carbon_ai_model

if __name__ == "__main__":
    # Train the model
    model = train_and_save_model()
    
    # Test with sample data
    test_data = {
        'entries': [
            {'metric_type': 'carbon', 'value': 25, 'description': 'Car travel to work'},
            {'metric_type': 'carbon', 'value': 15, 'description': 'Heating home'},
            {'metric_type': 'water', 'value': 200, 'description': 'Long shower'},
            {'metric_type': 'energy', 'value': 12, 'description': 'AC usage'}
        ]
    }
    
    suggestions = model.predict_suggestions(test_data)
    print("\n🎯 Sample AI Suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion['title']}")
        print(f"   {suggestion['message']}")
        print(f"   Impact: {suggestion['impact']} | Effort: {suggestion['effort']}")
        print() 