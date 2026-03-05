from config.settings import Colors

class WeatherQualityChecker:
    """Check data quality for weather pipeline"""
    
    def __init__(self):
        print(f"{Colors.INFO}🔍 Initializing Quality Checker...")
    
    def run_checks(self, current_df, hourly_df, daily_df):
        """Run all quality checks on the transformed data"""
        print(f"{Colors.HEADER}{'='*60}")
        print("🧪 DATA QUALITY CHECKS")
        print(f"{'='*60}{Colors.RESET}\n")
        
        all_checks_passed = True
        
        # Check current weather data
        if not current_df.empty:
            print(f"{Colors.INFO}📊 Checking current weather data...")
            current_checks = self._check_current_weather(current_df)
            all_checks_passed = all_checks_passed and current_checks
        else:
            print(f"{Colors.WARNING}⚠️ No current weather data to check")
        
        # Check hourly forecast data
        if not hourly_df.empty:
            print(f"{Colors.INFO}📊 Checking hourly forecast data...")
            hourly_checks = self._check_hourly_forecast(hourly_df)
            all_checks_passed = all_checks_passed and hourly_checks
        else:
            print(f"{Colors.WARNING}⚠️ No hourly forecast data to check")
        
        # Check daily forecast data
        if not daily_df.empty:
            print(f"{Colors.INFO}📊 Checking daily forecast data...")
            daily_checks = self._check_daily_forecast(daily_df)
            all_checks_passed = all_checks_passed and daily_checks
        else:
            print(f"{Colors.WARNING}⚠️ No daily forecast data to check")
        
        # Final result
        if all_checks_passed:
            print(f"\n{Colors.SUCCESS}✅ All quality checks passed!{Colors.RESET}")
        else:
            print(f"\n{Colors.WARNING}⚠️ Some quality checks failed{Colors.RESET}")
        
        return all_checks_passed
    
    def _check_current_weather(self, df):
        """Check current weather data quality"""
        checks_passed = True
        total_rows = len(df)
        
        print(f"  Total records: {total_rows}")
        
        # Check for missing values
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            print(f"{Colors.WARNING}    ⚠️ Found {missing_values} missing values{Colors.RESET}")
            checks_passed = False
        else:
            print(f"{Colors.SUCCESS}    ✅ No missing values{Colors.RESET}")
        
        # Check temperature range (reasonable values)
        if 'temperature' in df.columns:
            extreme_temps = df[~df['temperature'].between(-50, 50)].shape[0]
            if extreme_temps > 0:
                print(f"{Colors.WARNING}    ⚠️ Found {extreme_temps} extreme temperatures{Colors.RESET}")
                checks_passed = False
            else:
                print(f"{Colors.SUCCESS}    ✅ Temperatures in reasonable range{Colors.RESET}")
        
        # Check humidity range
        if 'humidity' in df.columns:
            invalid_humidity = df[~df['humidity'].between(0, 100)].shape[0]
            if invalid_humidity > 0:
                print(f"{Colors.WARNING}    ⚠️ Found {invalid_humidity} invalid humidity values{Colors.RESET}")
                checks_passed = False
            else:
                print(f"{Colors.SUCCESS}    ✅ Humidity values valid{Colors.RESET}")
        
        return checks_passed
    
    def _check_hourly_forecast(self, df):
        """Check hourly forecast data quality"""
        checks_passed = True
        total_rows = len(df)
        
        print(f"  Total records: {total_rows}")
        
        # Check for missing values
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            print(f"{Colors.WARNING}    ⚠️ Found {missing_values} missing values{Colors.RESET}")
            checks_passed = False
        else:
            print(f"{Colors.SUCCESS}    ✅ No missing values{Colors.RESET}")
        
        # Check precipitation probability range
        if 'precipitation_probability' in df.columns:
            invalid_prob = df[~df['precipitation_probability'].between(0, 100)].shape[0]
            if invalid_prob > 0:
                print(f"{Colors.WARNING}    ⚠️ Found {invalid_prob} invalid probability values{Colors.RESET}")
                checks_passed = False
            else:
                print(f"{Colors.SUCCESS}    ✅ Precipitation probabilities valid{Colors.RESET}")
        
        return checks_passed
    
    def _check_daily_forecast(self, df):
        """Check daily forecast data quality"""
        checks_passed = True
        total_rows = len(df)
        
        print(f"  Total records: {total_rows}")
        
        # Check for missing values
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            print(f"{Colors.WARNING}    ⚠️ Found {missing_values} missing values{Colors.RESET}")
            checks_passed = False
        else:
            print(f"{Colors.SUCCESS}    ✅ No missing values{Colors.RESET}")
        
        # Check temperature max/min relationship
        if 'temperature_max' in df.columns and 'temperature_min' in df.columns:
            invalid_temp = df[df['temperature_max'] < df['temperature_min']].shape[0]
            if invalid_temp > 0:
                print(f"{Colors.WARNING}    ⚠️ Found {invalid_temp} records where max < min{Colors.RESET}")
                checks_passed = False
            else:
                print(f"{Colors.SUCCESS}    ✅ Temperature relationships valid{Colors.RESET}")
        
        return checks_passed