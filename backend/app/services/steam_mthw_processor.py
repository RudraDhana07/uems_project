# backend/app/services/steam_mthw_processor.py

import pandas as pd
from typing import Dict
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

class SteamMTHWProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = None
        
    def generate_date_sequence(self, start_date: str = '2013-10-01', periods: int = 138):
        """Generate sequence of months and years starting from Oct 2013"""
        dates = pd.date_range(start=start_date, periods=periods, freq='M')
        return pd.DataFrame({
            'month': dates.strftime('%b'),
            'year': dates.year
        })
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and process Steam and MTHW data from Excel.
        Returns processed DataFrame with standardized column names.
        """
        try:
            # Read the specific range from Excel
            df = pd.read_excel(
                self.excel_file,
                sheet_name='Steam and MTHW',
                skiprows=3,     # Skip to actual data rows
                nrows=138,      # Read 138 rows
                usecols='C:T'   # Columns C through T
            )
            
            # Generate date sequence
            date_df = self.generate_date_sequence()
            
            # Rename columns to match database model
            column_mapping = {
                df.columns[0]: 'mthw_consumption_kwh',
                df.columns[1]: 'castle_192_reading_kwh',
                df.columns[2]: 'castle_192_consumption_kwh',
                df.columns[3]: 'med_school_a_reading_kg',
                df.columns[4]: 'med_school_a_reading_kwh',
                df.columns[5]: 'med_school_a_consumption_kg',
                df.columns[6]: 'med_school_a_consumption_kwh',
                df.columns[7]: 'med_school_b_reading_kg',
                df.columns[8]: 'med_school_b_reading_kwh',
                df.columns[9]: 'med_school_b_consumption_kg',
                df.columns[10]: 'med_school_b_consumption_kwh',
                df.columns[11]: 'med_school_consumption_kg',
                df.columns[12]: 'med_school_consumption_kwh',
                df.columns[13]: 'cumberland_d401_dining_reading_kg',
                df.columns[14]: 'cumberland_d404_castle_reading_kg',
                df.columns[15]: 'cumberland_d401_d404_consumption_kg',
                df.columns[16]: 'cumberland_d401_d404_consumption_kwh',
                df.columns[17]: 'total_steam_consumption_kwh'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Replace Excel formula errors with None
            df = df.replace(['#DIV/0!', '#N/A', '#NAME?', '#NULL!', '#NUM!', '#REF!', '#VALUE!'], None)
            
            # Convert all numeric columns to float, replacing errors with None
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Combine date sequence with data
            result_df = pd.concat([date_df, df], axis=1)
            
            # Set future dates to null
            current_date = datetime.now()
            for idx, row in result_df.iterrows():
                row_date = datetime.strptime(f"{row['month']} {row['year']}", '%b %Y')
                if row_date > current_date:
                    result_df.loc[idx, df.columns] = None
            
            self.raw_data = result_df
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Error loading Steam and MTHW data: {str(e)}")
    
    def validate_data(self) -> Dict:
        """
        Validate loaded data and return validation report.
        """
        if self.raw_data is None:
            self.load_data()
            
        validation_report = {
            'total_rows': len(self.raw_data),
            'date_range': {
                'start': f"{self.raw_data['month'].iloc[0]} {self.raw_data['year'].iloc[0]}",
                'end': f"{self.raw_data['month'].iloc[-1]} {self.raw_data['year'].iloc[-1]}"
            },
            'missing_values': self.raw_data.isnull().sum().to_dict(),
            'value_ranges': {
                col: {
                    'min': self.raw_data[col].min(),
                    'max': self.raw_data[col].max(),
                    'null_count': self.raw_data[col].isnull().sum()
                }
                for col in self.raw_data.columns 
                if col not in ['month', 'year']
            }
        }
        
        return validation_report