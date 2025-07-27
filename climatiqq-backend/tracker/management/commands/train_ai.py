from django.core.management.base import BaseCommand
from tracker.ai_model import train_and_save_model
import time

class Command(BaseCommand):
    help = 'Train the carbon reduction AI model'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Training Carbon AI Model...")
        self.stdout.write("=" * 40)
        
        start_time = time.time()
        
        # Train the model
        model = train_and_save_model()
        
        end_time = time.time()
        training_time = end_time - start_time
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Training completed in {training_time:.2f} seconds!")
        )
        
        # Test the model
        self.stdout.write("\n🧪 Testing AI Model...")
        
        test_data = {
            'entries': [
                {'metric_type': 'carbon', 'value': 25, 'description': 'Car travel to work', 'created_at': '2024-01-01T10:00:00+00:00'},
                {'metric_type': 'carbon', 'value': 15, 'description': 'Heating home', 'created_at': '2024-01-01T12:00:00+00:00'},
                {'metric_type': 'water', 'value': 200, 'description': 'Long shower', 'created_at': '2024-01-01T08:00:00+00:00'},
                {'metric_type': 'energy', 'value': 12, 'description': 'AC usage', 'created_at': '2024-01-01T14:00:00+00:00'}
            ]
        }
        
        suggestions = model.predict_suggestions(test_data)
        
        self.stdout.write("\n🎯 Sample AI Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            self.stdout.write(f"{i}. {suggestion['title']}")
            self.stdout.write(f"   {suggestion['message']}")
            self.stdout.write(f"   Impact: {suggestion['impact']} | Effort: {suggestion['effort']}")
            self.stdout.write("")
        
        self.stdout.write(
            self.style.SUCCESS("🎉 AI Model is ready to use!")
        )
        self.stdout.write("\n📝 Next steps:")
        self.stdout.write("   1. Start your Django server")
        self.stdout.write("   2. The AI suggestions will be available at /api/v1/ai-suggestions/")
        self.stdout.write("   3. Users can get personalized carbon reduction advice!") 