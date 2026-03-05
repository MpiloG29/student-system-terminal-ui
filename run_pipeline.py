#!/usr/bin/env python3
"""
Weather Data Pipeline - Main Entry Point
Run this script to execute the complete ETL pipeline
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.pipeline import WeatherPipeline
    from config.settings import Colors
    print("✅ Imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current Python path: {sys.path}")
    sys.exit(1)

def print_banner():
    """Print colorful banner"""
    banner = f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🌤️  WEATHER DATA PIPELINE - PORTFOLIO PROJECT            ║
║                                                              ║
║   Extract • Transform • Load • Visualize                    ║
║                                                              ║
║   Built with: Python • SQLite • Docker • Plotly             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
    """
    print(banner)

def main():
    """Main function"""
    print_banner()
    
    # Check if command line argument is provided
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        print(f"Running with option: {choice}")
        
        if choice == '1':
            pipeline = WeatherPipeline()
            pipeline.run()
        elif choice == '2':
            try:
                from dashboard.weather_dashboard import WeatherDashboard
                dashboard = WeatherDashboard()
                dashboard.create_dashboard()
            except ImportError as e:
                print(f"{Colors.ERROR}❌ Dashboard import error: {e}")
        elif choice == '3':
            pipeline = WeatherPipeline()
            pipeline.run()
            try:
                from dashboard.weather_dashboard import WeatherDashboard
                dashboard = WeatherDashboard()
                dashboard.create_dashboard()
            except ImportError as e:
                print(f"{Colors.ERROR}❌ Dashboard import error: {e}")
        elif choice == '4':
            print(f"{Colors.SUCCESS}👋 Goodbye!{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.ERROR}Invalid choice. Please try again.{Colors.RESET}")
        
        sys.exit(0)
    
    # Interactive mode
    while True:
        print(f"\n{Colors.BOLD}Options:{Colors.RESET}")
        print(f"{Colors.INFO}1. Run ETL Pipeline (Extract, Transform, Load)")
        print("2. Launch Dashboard")
        print("3. Run Pipeline + Dashboard")
        print("4. Exit")
        
        choice = input(f"\n{Colors.BOLD}Enter your choice (1-4): {Colors.RESET}")
        
        if choice == '1':
            pipeline = WeatherPipeline()
            pipeline.run()
            
        elif choice == '2':
            try:
                from dashboard.weather_dashboard import WeatherDashboard
                dashboard = WeatherDashboard()
                dashboard.create_dashboard()
            except ImportError as e:
                print(f"{Colors.ERROR}❌ Dashboard import error: {e}")
        elif choice == '3':
            pipeline = WeatherPipeline()
            pipeline.run()
            try:
                from dashboard.weather_dashboard import WeatherDashboard
                dashboard = WeatherDashboard()
                dashboard.create_dashboard()
            except ImportError as e:
                print(f"{Colors.ERROR}❌ Dashboard import error: {e}")
        elif choice == '4':
            print(f"{Colors.SUCCESS}👋 Goodbye!{Colors.RESET}")
            sys.exit(0)
            
        else:
            print(f"{Colors.ERROR}Invalid choice. Please try again.{Colors.RESET}")

if __name__ == "__main__":
    main()