#!/usr/bin/env python3
"""
Simple AI Model for Carbon Reduction Suggestions
Rule-based system for environmental impact recommendations
"""

import os
from datetime import datetime, timedelta

class CarbonAIModel:
    def __init__(self):
        self.feature_names = [
            'avg_carbon_per_day', 'avg_water_per_day', 'avg_energy_per_day',
            'total_entries', 'days_active', 'carbon_trend', 'activity_frequency',
            'high_impact_activities', 'low_impact_activities'
        ]
        
    def predict_suggestions(self, user_data):
        """Generate suggestions based on user data using rule-based system"""
        try:
            # Extract user features
            features = self.extract_user_features(user_data)
            
            # Generate suggestions based on rules
            suggestions = self.generate_rule_based_suggestions(features)
            
            # Format suggestions
            formatted_suggestions = self.format_suggestions(suggestions)
            
            return {
                'suggestions': formatted_suggestions,
                'confidence': 0.85,
                'model_type': 'rule_based',
                'features_analyzed': features
            }
            
        except Exception as e:
            print(f"❌ Error in AI prediction: {e}")
            return {
                'suggestions': [
                    {
                        'title': 'General Sustainability',
                        'description': 'Consider reducing your overall environmental impact through daily choices.',
                        'category': 'general',
                        'impact': 'medium',
                        'difficulty': 'easy'
                    }
                ],
                'confidence': 0.5,
                'model_type': 'fallback',
                'error': str(e)
            }
    
    def extract_user_features(self, user_data):
        """Extract features from user data"""
        try:
            entries = user_data.get('entries', [])
            if not entries:
                return {
                    'avg_carbon_per_day': 0,
                    'avg_water_per_day': 0,
                    'avg_energy_per_day': 0,
                    'total_entries': 0,
                    'days_active': 0,
                    'carbon_trend': 0,
                    'activity_frequency': 0,
                    'high_impact_activities': 0,
                    'low_impact_activities': 0
                }
            
            # Calculate averages
            total_carbon = sum(entry.get('carbon_footprint', 0) for entry in entries)
            total_water = sum(entry.get('water_usage', 0) for entry in entries)
            total_energy = sum(entry.get('energy_usage', 0) for entry in entries)
            
            num_entries = len(entries)
            avg_carbon = total_carbon / num_entries if num_entries > 0 else 0
            avg_water = total_water / num_entries if num_entries > 0 else 0
            avg_energy = total_energy / num_entries if num_entries > 0 else 0
            
            # Calculate days active
            if entries:
                first_entry = min(entries, key=lambda x: x.get('created_at', ''))
                last_entry = max(entries, key=lambda x: x.get('created_at', ''))
                days_active = 30  # Default assumption
            else:
                days_active = 0
            
            # Calculate trends (simplified)
            carbon_trend = 0  # Neutral trend
            activity_frequency = num_entries / max(days_active, 1)
            
            # Count activity types
            high_impact = sum(1 for entry in entries if entry.get('carbon_footprint', 0) > 10)
            low_impact = sum(1 for entry in entries if entry.get('carbon_footprint', 0) <= 5)
            
            return {
                'avg_carbon_per_day': avg_carbon,
                'avg_water_per_day': avg_water,
                'avg_energy_per_day': avg_energy,
                'total_entries': num_entries,
                'days_active': days_active,
                'carbon_trend': carbon_trend,
                'activity_frequency': activity_frequency,
                'high_impact_activities': high_impact,
                'low_impact_activities': low_impact
            }
            
        except Exception as e:
            print(f"❌ Error extracting features: {e}")
            return {
                'avg_carbon_per_day': 0,
                'avg_water_per_day': 0,
                'avg_energy_per_day': 0,
                'total_entries': 0,
                'days_active': 0,
                'carbon_trend': 0,
                'activity_frequency': 0,
                'high_impact_activities': 0,
                'low_impact_activities': 0
            }
    
    def generate_rule_based_suggestions(self, features):
        """Generate suggestions based on rules"""
        suggestions = []
        
        avg_carbon = features.get('avg_carbon_per_day', 0)
        avg_water = features.get('avg_water_per_day', 0)
        avg_energy = features.get('avg_energy_per_day', 0)
        total_entries = features.get('total_entries', 0)
        high_impact = features.get('high_impact_activities', 0)
        low_impact = features.get('low_impact_activities', 0)
        
        # Carbon-based suggestions
        if avg_carbon > 20:
            suggestions.extend([
                'reduce_car_usage',
                'use_public_transport',
                'energy_efficiency'
            ])
        elif avg_carbon > 10:
            suggestions.extend([
                'optimize_heating',
                'reduce_meat_consumption',
                'renewable_energy'
            ])
        else:
            suggestions.extend([
                'maintain_low_carbon',
                'share_tips',
                'community_engagement'
            ])
        
        # Water-based suggestions
        if avg_water > 200:
            suggestions.extend([
                'shorter_showers',
                'fix_leaks',
                'water_efficient_appliances'
            ])
        
        # Energy-based suggestions
        if avg_energy > 10:
            suggestions.extend([
                'led_lighting',
                'smart_thermostat',
                'unplug_devices'
            ])
        
        # Activity-based suggestions
        if high_impact > low_impact:
            suggestions.extend([
                'choose_sustainable_transport',
                'reduce_high_impact_activities',
                'offset_carbon_emissions'
            ])
        
        # Engagement-based suggestions
        if total_entries < 10:
            suggestions.extend([
                'track_more_activities',
                'set_sustainability_goals',
                'join_community_challenges'
            ])
        
        # Remove duplicates and limit to top 5
        unique_suggestions = list(set(suggestions))
        return unique_suggestions[:5]
    
    def format_suggestions(self, suggestions):
        """Format suggestions into user-friendly format"""
        suggestion_templates = {
            'reduce_car_usage': {
                'title': 'Reduce Car Usage',
                'message': 'Consider walking, cycling, or public transport for short trips.',
                'impact': 'high',
                'effort': 'medium'
            },
            'use_public_transport': {
                'title': 'Use Public Transport',
                'message': 'Switch to buses, trains, or trams for your daily commute.',
                'impact': 'high',
                'effort': 'easy'
            },
            'energy_efficiency': {
                'title': 'Improve Energy Efficiency',
                'message': 'Upgrade to energy-efficient appliances and lighting.',
                'impact': 'medium',
                'effort': 'medium'
            },
            'optimize_heating': {
                'title': 'Optimize Heating',
                'message': 'Lower your thermostat and use smart heating controls.',
                'impact': 'medium',
                'effort': 'easy'
            },
            'reduce_meat_consumption': {
                'title': 'Reduce Meat Consumption',
                'message': 'Try meat-free Mondays or plant-based alternatives.',
                'impact': 'high',
                'effort': 'medium'
            },
            'renewable_energy': {
                'title': 'Switch to Renewable Energy',
                'message': 'Consider solar panels or green energy providers.',
                'impact': 'high',
                'effort': 'hard'
            },
            'maintain_low_carbon': {
                'title': 'Maintain Low Carbon Lifestyle',
                'message': 'Keep up your great work! Share your tips with others.',
                'impact': 'low',
                'effort': 'easy'
            },
            'share_tips': {
                'title': 'Share Sustainability Tips',
                'message': 'Help others by sharing your eco-friendly practices.',
                'impact': 'medium',
                'effort': 'easy'
            },
            'community_engagement': {
                'title': 'Join Community Initiatives',
                'message': 'Participate in local environmental projects.',
                'impact': 'medium',
                'effort': 'easy'
            },
            'shorter_showers': {
                'title': 'Take Shorter Showers',
                'message': 'Reduce shower time to save water and energy.',
                'impact': 'medium',
                'effort': 'easy'
            },
            'fix_leaks': {
                'title': 'Fix Water Leaks',
                'message': 'Repair dripping taps and pipes to save water.',
                'impact': 'medium',
                'effort': 'medium'
            },
            'water_efficient_appliances': {
                'title': 'Use Water-Efficient Appliances',
                'message': 'Install low-flow showerheads and efficient washing machines.',
                'impact': 'medium',
                'effort': 'medium'
            },
            'led_lighting': {
                'title': 'Switch to LED Lighting',
                'message': 'Replace traditional bulbs with energy-efficient LEDs.',
                'impact': 'medium',
                'effort': 'easy'
            },
            'smart_thermostat': {
                'title': 'Install Smart Thermostat',
                'message': 'Use smart controls to optimize heating and cooling.',
                'impact': 'medium',
                'effort': 'medium'
            },
            'unplug_devices': {
                'title': 'Unplug Unused Devices',
                'message': 'Reduce phantom energy consumption by unplugging electronics.',
                'impact': 'low',
                'effort': 'easy'
            },
            'choose_sustainable_transport': {
                'title': 'Choose Sustainable Transport',
                'message': 'Opt for walking, cycling, or electric vehicles.',
                'impact': 'high',
                'effort': 'medium'
            },
            'reduce_high_impact_activities': {
                'title': 'Reduce High-Impact Activities',
                'message': 'Limit activities with high carbon footprints.',
                'impact': 'high',
                'effort': 'medium'
            },
            'offset_carbon_emissions': {
                'title': 'Offset Carbon Emissions',
                'message': 'Support carbon offset projects to balance your impact.',
                'impact': 'high',
                'effort': 'easy'
            },
            'track_more_activities': {
                'title': 'Track More Activities',
                'message': 'Log your daily activities to better understand your impact.',
                'impact': 'low',
                'effort': 'easy'
            },
            'set_sustainability_goals': {
                'title': 'Set Sustainability Goals',
                'message': 'Create specific targets for reducing your environmental impact.',
                'impact': 'medium',
                'effort': 'easy'
            },
            'join_community_challenges': {
                'title': 'Join Community Challenges',
                'message': 'Participate in group sustainability challenges.',
                'impact': 'medium',
                'effort': 'easy'
            }
        }
        
        formatted_suggestions = []
        for suggestion in suggestions:
            if suggestion in suggestion_templates:
                formatted_suggestions.append(suggestion_templates[suggestion])
            else:
                # Fallback for unknown suggestions
                formatted_suggestions.append({
                    'title': 'General Sustainability',
                    'message': 'Consider ways to reduce your environmental impact.',
                    'impact': 'medium',
                    'effort': 'easy'
                })
        
        return formatted_suggestions

# Global instance
carbon_ai_model = CarbonAIModel() 