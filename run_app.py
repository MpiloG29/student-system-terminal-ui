#!/usr/bin/env python3
"""Non-interactive runner for ETL and dashboard generation."""

import argparse
import os
import shutil

from dashboard.weather_dashboard import WeatherDashboard
from src.pipeline import WeatherPipeline


def main():
    parser = argparse.ArgumentParser(description="Run weather pipeline and/or dashboard generation.")
    parser.add_argument(
        "--mode",
        choices=["pipeline", "dashboard", "all"],
        default="all",
        help="What to run (default: all).",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where dashboard HTML will be copied when generated.",
    )
    args = parser.parse_args()

    if args.mode in {"pipeline", "all"}:
        WeatherPipeline().run()

    if args.mode in {"dashboard", "all"}:
        dashboard_path = WeatherDashboard().create_dashboard()
        if dashboard_path and args.output_dir:
            os.makedirs(args.output_dir, exist_ok=True)
            target_path = os.path.join(args.output_dir, "weather_dashboard.html")
            shutil.copyfile(dashboard_path, target_path)
            print(f"Dashboard exported to: {target_path}")


if __name__ == "__main__":
    main()