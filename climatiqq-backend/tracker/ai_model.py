#!/usr/bin/env python3
"""
Custom AI Recommendation Engine for Environmental Impact Analysis

This module implements a rule-based AI system that analyzes user environmental data
and generates personalized sustainability recommendations. The system uses expert
knowledge encoded in rules to provide actionable advice for reducing environmental impact.

Key Components:
1. Feature Extraction: Analyzes user data patterns and calculates relevant metrics
2. Rule-Based Decision Making: Applies environmental expertise through intelligent thresholds
3. Recommendation Generation: Creates personalized sustainability suggestions
4. Response Formatting: Structures output for frontend consumption

Author: [Your Name]
Date: [Current Date]
"""

import os
from datetime import datetime, timedelta

class CarbonAIModel:
    """
    Rule-based AI model for generating environmental sustainability recommendations.
    
    This class implements an expert system that analyzes user environmental data
    and provides personalized suggestions for reducing carbon footprint, water usage,
    and energy consumption. It uses predefined rules based on environmental science
    and sustainability best practices.
    
    Attributes:
        feature_names (list): Names of features extracted from user data
    """
    
    def __init__(self):
        # Define the features that will be extracted and analyzed from user data
        self.feature_names = [
            'avg_carbon_per_day',      # Average daily carbon footprint
            'avg_water_per_day',       # Average daily water usage
            'avg_energy_per_day',      # Average daily energy consumption
            'total_entries',           # Total number of environmental entries logged
            'days_active',             # Number of days user has been active
            'carbon_trend',            # Trend in carbon usage over time
            'activity_frequency',      # How often user logs activities
            'high_impact_activities',  # Count of high-impact activities
            'low_impact_activities'    # Count of low-impact activities
        ]
        
    def predict_suggestions(self, user_data):
        """
        Main method to generate personalized sustainability recommendations.
        
        This is the primary interface for the AI model. It takes user environmental
        data, extracts relevant features, applies rule-based logic, and returns
        formatted recommendations.
        
        Args:
            user_data (dict): Dictionary containing user's environmental data
                - entries (list): List of environmental impact entries
                - Each entry should have: carbon_footprint, water_usage, energy_usage, created_at
        
        Returns:
            dict: Structured response containing:
                - suggestions (list): List of recommendation objects
                - confidence (float): Confidence level of recommendations (0.0-1.0)
                - model_type (str): Type of AI model used
                - features_analyzed (dict): Features extracted from user data
                - error (str): Error message if something goes wrong
        """
        try:
            # Step 1: Extract numerical features from user data
            features = self.extract_user_features(user_data)
            
            # Step 2: Apply rule-based logic to generate suggestions
            suggestions = self.generate_rule_based_suggestions(features)
            
            # Step 3: Format suggestions into user-friendly structure
            formatted_suggestions = self.format_suggestions(suggestions)
            
            # Return successful response with extracted features for transparency
            return {
                'suggestions': formatted_suggestions,
                'confidence': 0.85,  # High confidence for rule-based system
                'model_type': 'rule_based',
                'features_analyzed': features
            }
            
        except Exception as e:
            print(f"❌ Error in AI prediction: {e}")
            # Return fallback suggestions if something goes wrong
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
                'confidence': 0.5,  # Lower confidence for fallback
                'model_type': 'fallback',
                'error': str(e)
            }
    
    def extract_user_features(self, user_data):
        """
        Extract and calculate relevant features from user environmental data.
        
        This method processes raw user data to calculate meaningful metrics that
        the AI system can use to make decisions. It handles edge cases and
        provides default values when data is insufficient.
        
        Args:
            user_data (dict): Raw user data containing environmental entries
        
        Returns:
            dict: Dictionary of calculated features:
                - avg_carbon_per_day: Average daily carbon footprint
                - avg_water_per_day: Average daily water usage
                - avg_energy_per_day: Average daily energy consumption
                - total_entries: Number of entries logged
                - days_active: Estimated days of activity
                - carbon_trend: Trend in carbon usage (simplified)
                - activity_frequency: Entries per day
                - high_impact_activities: Count of high-impact activities
                - low_impact_activities: Count of low-impact activities
        """
        try:
            entries = user_data.get('entries', [])
            if not entries:
                # Return default values if no data available
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
            
            # Calculate total values across all entries
            total_carbon = sum(entry.get('carbon_footprint', 0) for entry in entries)
            total_water = sum(entry.get('water_usage', 0) for entry in entries)
            total_energy = sum(entry.get('energy_usage', 0) for entry in entries)
            
            # Calculate averages (avoid division by zero)
            num_entries = len(entries)
            avg_carbon = total_carbon / num_entries if num_entries > 0 else 0
            avg_water = total_water / num_entries if num_entries > 0 else 0
            avg_energy = total_energy / num_entries if num_entries > 0 else 0
            
            # Calculate days active (simplified - could be enhanced with actual date analysis)
            if entries:
                first_entry = min(entries, key=lambda x: x.get('created_at', ''))
                last_entry = max(entries, key=lambda x: x.get('created_at', ''))
                days_active = 30  # Default assumption - could be calculated from actual dates
            else:
                days_active = 0
            
            # Calculate simplified trends (placeholder for future enhancement)
            carbon_trend = 0  # Neutral trend - could be enhanced with time-series analysis
            activity_frequency = num_entries / max(days_active, 1)  # Entries per day
            
            # Categorize activities by impact level
            # High impact: carbon footprint > 10 kg CO2
            # Low impact: carbon footprint <= 5 kg CO2
            high_impact = sum(1 for entry in entries if entry.get('carbon_footprint', 0) > 10)
            low_impact = sum(1 for entry in entries if entry.get('carbon_footprint', 0) <= 5)
            
            # Return all calculated features
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
            # Return safe default values on error
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
        """
        Apply rule-based logic to generate sustainability recommendations.
        
        This method implements the core AI logic using environmental science principles
        and sustainability best practices. It analyzes user patterns and applies
        appropriate rules to generate relevant suggestions.
        
        The rules are based on:
        - Carbon footprint thresholds (high: >20, medium: >10, low: <=10)
        - Water usage patterns (high: >200L)
        - Energy consumption (high: >10kWh)
        - User engagement levels
        - Activity impact distribution
        
        Args:
            features (dict): Extracted features from user data
        
        Returns:
            list: List of suggestion keys (e.g., 'reduce_car_usage', 'led_lighting')
        """
        suggestions = []
        
        # Extract feature values for rule evaluation
        avg_carbon = features.get('avg_carbon_per_day', 0)
        avg_water = features.get('avg_water_per_day', 0)
        avg_energy = features.get('avg_energy_per_day', 0)
        total_entries = features.get('total_entries', 0)
        high_impact = features.get('high_impact_activities', 0)
        low_impact = features.get('low_impact_activities', 0)
        
        # RULE 1: Carbon-based suggestions based on daily carbon footprint
        if avg_carbon > 20:
            # High carbon users: Focus on major lifestyle changes
            suggestions.extend([
                'reduce_car_usage',        # Transportation is major carbon source
                'use_public_transport',    # Alternative to private vehicles
                'energy_efficiency'        # Improve home energy efficiency
            ])
        elif avg_carbon > 10:
            # Medium carbon users: Focus on optimization and diet changes
            suggestions.extend([
                'optimize_heating',        # Heating/cooling optimization
                'reduce_meat_consumption', # Diet changes for sustainability
                'renewable_energy'         # Consider green energy options
            ])
        else:
            # Low carbon users: Focus on maintenance and community engagement
            suggestions.extend([
                'maintain_low_carbon',     # Keep up good practices
                'share_tips',             # Help others learn
                'community_engagement'     # Join environmental initiatives
            ])
        
        # RULE 2: Water-based suggestions for high water users
        if avg_water > 200:
            # High water usage: Focus on water conservation
            suggestions.extend([
                'shorter_showers',         # Reduce shower time
                'fix_leaks',              # Repair water leaks
                'water_efficient_appliances' # Use water-saving devices
            ])
        
        # RULE 3: Energy-based suggestions for high energy users
        if avg_energy > 10:
            # High energy usage: Focus on energy efficiency
            suggestions.extend([
                'led_lighting',            # Switch to energy-efficient lighting
                'smart_thermostat',       # Use smart temperature controls
                'unplug_devices'          # Reduce phantom energy consumption
            ])
        
        # RULE 4: Activity-based suggestions based on impact distribution
        if high_impact > low_impact:
            # User has more high-impact activities: Focus on reducing major impacts
            suggestions.extend([
                'choose_sustainable_transport',    # Alternative transportation
                'reduce_high_impact_activities',  # Limit high-carbon activities
                'offset_carbon_emissions'         # Carbon offset programs
            ])
        
        # RULE 5: Engagement-based suggestions for new users
        if total_entries < 10:
            # New users: Focus on building tracking habits
            suggestions.extend([
                'track_more_activities',      # Encourage regular logging
                'set_sustainability_goals',   # Goal setting for motivation
                'join_community_challenges'   # Community engagement
            ])
        
        # Remove duplicate suggestions and limit to top 5 for user experience
        unique_suggestions = list(set(suggestions))
        return unique_suggestions[:5]
    
    def format_suggestions(self, suggestions):
        """
        Convert suggestion keys into user-friendly recommendation objects.
        
        This method takes the raw suggestion keys from the rule engine and
        formats them into structured objects that the frontend can easily
        display. Each suggestion includes a title, message, impact level,
        and effort required.
        
        Args:
            suggestions (list): List of suggestion keys from rule engine
        
        Returns:
            list: List of formatted suggestion objects with:
                - title: Human-readable suggestion title
                - message: Detailed explanation of the suggestion
                - impact: Expected environmental impact (high/medium/low)
                - effort: Required effort to implement (easy/medium/hard)
        """
        # Comprehensive template library for all possible suggestions
        # Each template includes title, message, impact level, and effort required
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
        
        # Convert suggestion keys to formatted objects
        formatted_suggestions = []
        for suggestion in suggestions:
            if suggestion in suggestion_templates:
                # Use the predefined template
                formatted_suggestions.append(suggestion_templates[suggestion])
            else:
                # Fallback for unknown suggestions (shouldn't happen with current rules)
                formatted_suggestions.append({
                    'title': 'General Sustainability',
                    'message': 'Consider ways to reduce your environmental impact.',
                    'impact': 'medium',
                    'effort': 'easy'
                })
        
        return formatted_suggestions

# Global instance of the AI model for easy access throughout the application
# This instance is imported and used by views.py to generate recommendations
carbon_ai_model = CarbonAIModel() 