# backend/app/services/weather_processor.py

import pandas as pd
import numpy as np
from datetime import datetime, time
import logging

logger = logging.getLogger(__name__)

class WeatherProcessor:
    def __init__(self, academic_calendar_df=None, weather_weights_df=None,solar_energy_df=None):
        self.working_hours = (time(8), time(18))
        self.time_blocks = {
            'morning': (time(8), time(12)),
            'afternoon': (time(12), time(16)),
            'evening': (time(16), time(20))
        }
        self.academic_calendar_df = academic_calendar_df
        self.weather_weights_df = weather_weights_df
        self.solar_energy_df = solar_energy_df

    def _calculate_weighted_score(self, day_data, season, academic_info):
        try:
            if self.weather_weights_df is None:
                logger.warning("No weather weights data available")
                return None

            # Case-insensitive season matching with strip
            season_weights = self.weather_weights_df[
                self.weather_weights_df['Season'].str.lower().str.strip() == season.lower().strip()
            ]

            if len(season_weights) == 0:
                logger.warning(f"No weights found for season: {season}")
                return None

            weights = season_weights.iloc[0]

            # Calculate base weather score using exact column names
            weather_score = (
                weights['Temp_Weight'] * day_data['Air_Temperature_C_Avg'].mean() +
                weights['radiation_Weight'] * day_data['Solar_W_Avg'].mean() +
                weights['humidity_weight'] * day_data['Relative_Humidity_Avg'].mean() +
                weights['wind_Weight'] * day_data['Wind_Speed_ms_Avg'].mean()
            )

            # Get multiplier from academic_calendar table
            if academic_info:
                multiplier = academic_info.get('final_weight', 1.0)
            else:
                multiplier = 0 # weights['term_multiplier']

            return float(weather_score * multiplier)

        except Exception as e:
            logger.error(f"Error calculating weighted score: {str(e)}")
            logger.error(f"Season: {season}")
            logger.error(f"Weather weights columns: {self.weather_weights_df.columns.tolist()}")
            return None

    def process_monthly(self, daily_df):
        """Process daily data into monthly aggregations"""
        try:
            # Create monthly aggregations without nested dictionary
            monthly_metrics = pd.DataFrame()
            
            # Group by month end
            monthly_grouped = daily_df.resample('ME')
            
            # Calculate individual metrics
            monthly_metrics['temp_mean'] = monthly_grouped['temp_mean_working'].mean()
            monthly_metrics['temp_max'] = monthly_grouped['temp_max_working'].max()
            monthly_metrics['temp_min'] = monthly_grouped['temp_min_working'].min()
            monthly_metrics['temp_std_dev'] = monthly_grouped['temp_mean_working'].std()
            monthly_metrics['radiation_total'] = monthly_grouped['global_radiation_sum'].sum()
            monthly_metrics['avg_peak_radiation'] = monthly_grouped['peak_radiation'].mean()
            monthly_metrics['humidity_mean'] = monthly_grouped['humidity_mean_working'].mean()
            monthly_metrics['rain_total'] = monthly_grouped['rain_sum_working'].sum()
            monthly_metrics['weighted_monthly_score'] = monthly_grouped['weighted_score'].mean()



            #new columns added
            # monthly_metrics['total_solar_duration'] = monthly_grouped['solar_duration_hours'].sum() #not working
            monthly_metrics['avg_wind_speed'] = monthly_grouped['wind_speed_mean'].mean()
            monthly_metrics['morning_temp_mean'] = monthly_grouped['morning_temp_mean'].mean()
            monthly_metrics['afternoon_temp_mean'] = monthly_grouped['afternoon_temp_mean'].mean()
            monthly_metrics['evening_temp_mean'] = monthly_grouped['evening_temp_mean'].mean()
            monthly_metrics['pressure_mean'] = monthly_grouped['pressure_mean_working'].mean()

            # Add Mean daily Solar energy with debugging
            if self.solar_energy_df is not None:
                logger.info("Processing solar energy data for monthly metrics")
                for month_start in monthly_metrics.index:
                    logger.debug(f"Processing month: {month_start}")
                    mask = (
                        (self.solar_energy_df['Date'].dt.year == month_start.year) &
                        (self.solar_energy_df['Date'].dt.month == month_start.month)
                    )
                    matching_records = sum(mask)
                    logger.debug(f"Found {matching_records} matching records for {month_start}")
                    
                    if matching_records > 0:
                        solar_value = self.solar_energy_df.loc[mask, 'Mean_daily_Solar_energy'].iloc[0]
                        monthly_metrics.loc[month_start, 'mean_daily_solar_energy'] = solar_value
                        logger.debug(f"Added solar energy value: {solar_value} for {month_start}")
                    else:
                        logger.warning(f"No solar energy data found for {month_start}")
            else:
                logger.warning("Solar energy DataFrame is None")
                logger.error(f"Solar energy df shape: {self.solar_energy_df.shape if self.solar_energy_df is not None else 'None'}")
                        
            # Add academic period counts if calendar data is available
            if self.academic_calendar_df is not None:
                self._add_academic_period_counts(monthly_metrics)

            return monthly_metrics

        except Exception as e:
            logger.error(f"Error processing monthly metrics: {str(e)}")
            raise

    def _add_academic_period_counts(self, monthly_metrics):
        """Add academic period day counts to monthly metrics"""
        try:
            for month_start in monthly_metrics.index:
                # Get first and last day of the month
                first_day = month_start.replace(day=1)
                last_day = (first_day + pd.offsets.MonthEnd(1))
                
                # Create mask for the month using datetime
                mask = (
                    (self.academic_calendar_df['date_id'] >= first_day) &
                    (self.academic_calendar_df['date_id'] <= last_day)
                )
                period_data = self.academic_calendar_df[mask]
                
                # Calculate actual days in month using calendar
                import calendar
                total_days = calendar.monthrange(month_start.year, month_start.month)[1]
                
                # Count days for each period type
                term_days = len(period_data[period_data['event_type'] == 'Term'])
                holiday_days = len(period_data[period_data['event_type'] == 'Holiday'])
                exam_days = len(period_data[period_data['description'] == 'Exam'])
                
                # Add counts to monthly metrics
                monthly_metrics.loc[month_start, 'term_days'] = term_days
                monthly_metrics.loc[month_start, 'holiday_days'] = holiday_days
                monthly_metrics.loc[month_start, 'exam_days'] = exam_days
                monthly_metrics.loc[month_start, 'total_days'] = total_days
                
                # Log the results
                #logger.info(
                #    f"Month {month_start.strftime('%Y-%m')}: "
                #    f"Total={total_days}, Term={term_days}, "
                #    f"Holiday={holiday_days}, Exam={exam_days}"
                #)

        except Exception as e:
            logger.error(f"Error adding academic period counts: {str(e)}")
            logger.error(f"Month being processed: {month_start}")
            raise



    def _determine_season(self, date):
        """Determine season based on month"""
        month = date.month
        if month in [12, 1, 2]:
            return 'Summer'
        elif month in [3, 4, 5]:
            return 'Autumn'
        elif month in [6, 7, 8]:
            return 'Winter'
        else:
            return 'Spring'

    def _get_academic_info(self, date):
        """Get academic calendar information for a specific date"""
        if self.academic_calendar_df is None:
            return None
            
        date_data = self.academic_calendar_df[
            self.academic_calendar_df['date_id'].dt.date == date.date()
        ]
        
        if len(date_data) == 0:
            return None
            
        return date_data.iloc[0].to_dict()

    def process_daily(self, merged_data):
        """Process merged data into daily metrics"""
        try:
            df = merged_data.copy()
            df['DATETIME'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                          format='%d/%m/%Y %H:%M:%S', 
                                          dayfirst=True)
            df = df.set_index('DATETIME')

            # Filter working hours data
            working_hours_data = df.between_time(
                self.working_hours[0],
                self.working_hours[1]
            ).copy()
            
            working_hours_data.loc[:, 'date'] = working_hours_data.index.date

            daily_metrics = []
            for date, day_data in working_hours_data.groupby('date'):
                date_dt = pd.to_datetime(date)
                season = self._determine_season(date_dt)
                academic_info = self._get_academic_info(date_dt)

                metrics = self._calculate_daily_metrics(day_data, date_dt, season, academic_info)
                daily_metrics.append(metrics)

            daily_df = pd.DataFrame(daily_metrics)
            daily_df.set_index('date_id', inplace=True)
            return daily_df

        except Exception as e:
            logger.error(f"Error processing daily metrics: {str(e)}")
            raise

    def _calculate_daily_metrics(self, day_data, date_dt, season, academic_info):
        """Calculate daily metrics for a single day"""
        metrics = {
            'date_id': date_dt,
            'temp_mean_working': day_data['Air_Temperature_C_Avg'].mean(),
            'temp_max_working': day_data['Air_Temperature_C_Avg'].max(),
            'temp_min_working': day_data['Air_Temperature_C_Avg'].min(),
            'temp_range_working': day_data['Air_Temperature_C_Avg'].max() - day_data['Air_Temperature_C_Avg'].min(),
            'global_radiation_sum': day_data['Solar_W_Avg'].sum(),
            'peak_radiation': day_data['Solar_W_Avg'].max(),
            #'solar_duration_hours': len(day_data[day_data['Solar_W_Avg'] > 100]) / 12, #not working
            'wind_speed_mean': day_data['Wind_Speed_ms_Avg'].mean(),
            'wind_direction_dominant': day_data['Wind_Direction_deg'].mode()[0],
            'max_gust_speed': day_data['Wind_Speed_ms_Max'].max(),
            'humidity_mean_working': day_data['Relative_Humidity_Avg'].mean(),
            'humidity_range_working': day_data['Relative_Humidity_Avg'].max() - day_data['Relative_Humidity_Avg'].min(),
            'pressure_mean_working': day_data['Air_Pressure_hPa_Avg'].mean(),
            'rain_sum_working': day_data['Rain_mm_Tot'].sum(),
            'season': season,
            'day_type': 'Weekend' if date_dt.weekday() >= 6 else 'Weekday',
            'academic_period': academic_info['event_type'] if academic_info else None
        }

        # Add time block metrics
        for block_name, (start, end) in self.time_blocks.items():
            block_data = day_data.between_time(start, end)
            metrics[f'{block_name}_temp_mean'] = block_data['Air_Temperature_C_Avg'].mean()
            metrics[f'{block_name}_humidity_mean'] = block_data['Relative_Humidity_Avg'].mean()

        # Calculate weighted score
        metrics['weighted_score'] = self._calculate_weighted_score(day_data, season, academic_info)

        return metrics
