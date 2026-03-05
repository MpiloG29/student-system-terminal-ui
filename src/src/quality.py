import pandas as pd
from config.settings import Colors


class WeatherQualityChecker:
    """Basic data quality checks for transformed weather datasets."""

    def run_checks(self, current_df: pd.DataFrame, hourly_df: pd.DataFrame, daily_df: pd.DataFrame):
        issues = []

        if current_df.empty:
            issues.append("Current weather dataset is empty")
        else:
            if current_df['recorded_at'].isna().any():
                issues.append("Missing current weather timestamps")
            if (current_df['humidity'] < 0).any() or (current_df['humidity'] > 100).any():
                issues.append("Humidity values outside 0-100 range")
            if (current_df['temperature'] < -90).any() or (current_df['temperature'] > 70).any():
                issues.append("Potentially invalid current temperature values")

        if not hourly_df.empty:
            if hourly_df['forecast_time'].isna().any():
                issues.append("Missing hourly forecast timestamps")
            if (hourly_df['temperature'] < -90).any() or (hourly_df['temperature'] > 70).any():
                issues.append("Potentially invalid hourly temperature values")

        if not daily_df.empty:
            if daily_df['forecast_date'].isna().any():
                issues.append("Missing daily forecast dates")
            if (daily_df['temperature_min'] > daily_df['temperature_max']).any():
                issues.append("Daily rows where temperature_min > temperature_max")

        if issues:
            print(f"{Colors.WARNING}⚠️ Data quality check warnings:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"{Colors.SUCCESS}✅ Data quality checks passed")

        return issues