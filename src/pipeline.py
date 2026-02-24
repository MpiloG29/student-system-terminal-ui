import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now use absolute imports with the src prefix
from src.extract import WeatherExtractor
from src.transform import WeatherTransformer
from src.load import WeatherLoader
from config.settings import Colors
from datetime import datetime

class WeatherPipeline:
    """Main ETL Pipeline"""
    
    def __init__(self):
        self.extractor = WeatherExtractor()
        self.transformer = WeatherTransformer()
        self.loader = WeatherLoader()
        
    def run(self):
        """Execute the complete ETL pipeline"""
        
        start_time = datetime.now()
        
        print(f"{Colors.HEADER}")
        print("🌟" * 30)
        print("🌟  WEATHER DATA PIPELINE - ETL PROCESS  🌟")
        print("🌟" * 30)
        print(f"{Colors.RESET}\n")
        
        try:
            # EXTRACT
            print(f"{Colors.BOLD}📤 STEP 1: EXTRACTION{Colors.RESET}")
            raw_data = self.extractor.extract_all_cities()
            
            if not raw_data:
                print(f"{Colors.ERROR}No data extracted. Exiting...")
                return
            
            # TRANSFORM
            print(f"\n{Colors.BOLD}🔄 STEP 2: TRANSFORMATION{Colors.RESET}")
            current_df, hourly_df, daily_df = self.transformer.transform_all(raw_data)
            
            # LOAD
            print(f"\n{Colors.BOLD}📥 STEP 3: LOADING{Colors.RESET}")
            self.loader.load_all(current_df, hourly_df, daily_df)
            
            # Summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"\n{Colors.HEADER}{'='*60}")
            print("📊 PIPELINE EXECUTION SUMMARY")
            print(f"{'='*60}{Colors.RESET}")
            print(f"✅ Status: SUCCESS")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            print(f"🕒 Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🌍 Cities processed: {len(raw_data)}")
            print(f"\n{Colors.SUCCESS}🎉 Pipeline executed successfully!{Colors.RESET}")
            
        except Exception as e:
            print(f"\n{Colors.ERROR}❌ Pipeline failed: {str(e)}{Colors.RESET}")
            raise

if __name__ == "__main__":
    pipeline = WeatherPipeline()
    pipeline.run()
