# backend/app/services/auckland_calculated_water_processor.py
import pandas as pd
from typing import Dict
import numpy as np

class AucklandCalculatedWaterProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and process Auckland calculated water consumption data from Excel.
        Returns processed DataFrame with standardized column names.
        """
        try:
            # Read the specific range from Excel including column A for meter_location
            df = pd.read_excel(
                self.excel_file,
                sheet_name='AKL-WLG-CHC',
                skiprows=39,     # Skip to actual data rows
                nrows=4,         # Only read 4 rows
                usecols='A:AQ'   # Columns A through AQ (including A for meter_location)
            )
            
            if df.empty:
                raise Exception("No data found in the specified Excel range")
            
            # Create new DataFrame
            new_data = pd.DataFrame()
            
            # Get meter location from column A
            new_data['meter_location'] = df.iloc[:, 0]  # First column (A)
            new_data['object_name'] = df.iloc[:, 1]     # Second column (B)
            new_data['object_description'] = df.iloc[:, 2]  # Third column (C)
            
            # Generate month-year combinations for column names
            date_columns = ['Dec_2021']
            for year in [2022, 2023, 2024]:
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for month in months:
                    date_columns.append(f"{month}_{year}")
            for month in ['Jan', 'Feb', 'Mar']:
                date_columns.append(f"{month}_2025")
            
            # Map data directly from source columns to target columns
            data_cols = df.iloc[:, 3:]  # Skip first 3 columns
            
            # Map each column maintaining order
            for i, date_col in enumerate(date_columns):
                if i < len(data_cols.columns):
                    new_data[date_col] = data_cols.iloc[:, i]
                else:
                    new_data[date_col] = None
            
            # Handle all value validation in one pass
            for col in date_columns:
                new_data[col] = pd.to_numeric(new_data[col], errors='coerce')
                new_data[col] = new_data[col].where(
                    (pd.notnull(new_data[col])) & (new_data[col] >= 0),
                    None
                )
            
            self.raw_data = new_data
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Error loading Auckland Calculated Water data: {str(e)}")
    
    def validate_data(self) -> Dict:
        """
        Validate loaded data and return validation report.
        """
        if self.raw_data is None:
            self.load_data()
            
        validation_report = {
            'total_rows': len(self.raw_data),
            'columns': self.raw_data.columns.tolist(),
            'missing_values': self.raw_data.isnull().sum().to_dict(),
            'value_ranges': {
                col: {
                    'min': self.raw_data[col].min(),
                    'max': self.raw_data[col].max(),
                    'null_count': self.raw_data[col].isnull().sum()
                }
                for col in self.raw_data.columns 
                if col not in ['object_name', 'object_description', 'meter_location']
            }
        }
        
        return validation_report
