#!/usr/bin/env python3
"""
Weather Data Pipeline - Main Entry Point
Run this script to execute the complete ETL pipeline
"""

import sys
import os
from src.pipeline import WeatherPipeline
from dashboard.weather_dashboard import WeatherDashboard
from config.settings import Colors

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
║   Built with: Python • PostgreSQL • Docker • Plotly         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
    """
    print(banner)

def main():
    """Main function"""
    print_banner()
    
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
            dashboard = WeatherDashboard()
            dashboard.create_dashboard()
            
        elif choice == '3':
            pipeline = WeatherPipeline()
            pipeline.run()
            
            dashboard = WeatherDashboard()
            dashboard.create_dashboard()
            
        elif choice == '4':
            print(f"{Colors.SUCCESS}👋 Goodbye!{Colors.RESET}")
            sys.exit(0)
            
        else:
            print(f"{Colors.ERROR}Invalid choice. Please try again.{Colors.RESET}")

if __name__ == "__main__":
    main()