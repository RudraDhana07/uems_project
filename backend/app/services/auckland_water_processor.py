# backend/app/services/auckland_water_processor.py
import pandas as pd
from typing import Dict
import numpy as np

class AucklandWaterProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = None
        self.READING_DESCRIPTION = "(From Desigo CC System2) The values from the monthly report are unreliable the water meters drop to 0 and back to value"
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and process Auckland water consumption data from Excel.
        Returns processed DataFrame with standardized column names.
        """
        try:
            # Read the specific range from Excel
            df = pd.read_excel(
                self.excel_file,
                sheet_name='AKL-WLG-CHC',
                skiprows=46,     # Skip to actual data rows
                usecols='B:AQ'   # Columns B through AQ
            )
            
            # Keep the first two columns as they are
            new_data = pd.DataFrame()
            new_data['object_name'] = df.iloc[:, 0]
            new_data['object_description'] = df.iloc[:, 1]
            
            # Generate month-year combinations for column names
            date_columns = []
            
            # Add Dec 2021
            date_columns.append('Dec_2021')
            
            # Add months for 2022-2024
            for year in [2022, 2023, 2024]:
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for month in months:
                    date_columns.append(f"{month}_{year}")
            
            # Add months for 2025 (Jan through Mar)
            for month in ['Jan', 'Feb', 'Mar']:
                date_columns.append(f"{month}_2025")
            
            # Map available numeric data to date columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            available_numeric_data = df[numeric_cols]
            
            # Add each month column, mapping data where available and using None for future months
            for i, date_col in enumerate(date_columns):
                if i < len(available_numeric_data.columns):
                    new_data[date_col] = available_numeric_data.iloc[:, i]
                else:
                    new_data[date_col] = None
            
            # Add reading description
            new_data['reading_description'] = self.READING_DESCRIPTION
            
            # Replace any invalid values with None
            for col in date_columns:
                new_data[col] = pd.to_numeric(new_data[col], errors='coerce')
            
            self.raw_data = new_data
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Error loading Auckland Water data: {str(e)}")
    
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
                if col not in ['object_name', 'object_description', 'reading_description']
            }
        }
        
        return validation_report