# backend/app/services/janitza_processor.py
import pandas as pd
from typing import Dict, List, Tuple
import numpy as np

class JanitzaProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = {}  # Dictionary to store data for each table
        
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load and process all Janitza data from Excel.
        Returns dictionary of processed DataFrames with standardized column names.
        """
        try:
            # Define table configurations
            table_configs = [
                ('med_data', 0, 72),
                ('freezer_room', 73, 3),
                ('uo_d4f6', 79, 227),
                ('uo_f8x', 307, 196),
                ('manual_meters', 504, 37),
                ('calculated_consumption', 549, None)  # None means read until end
            ]
            
            # Process each table
            for table_name, skiprows, nrows in table_configs:
                self.raw_data[table_name] = self._process_table(skiprows, nrows, table_name)
            
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Error loading Janitza data: {str(e)}")
    
    def _process_table(self, skiprows: int, nrows: int, table_name: str) -> pd.DataFrame:
            """Helper method to process individual tables"""
            try:
                # Read the specific range from Excel
                df = pd.read_excel(
                    self.excel_file,
                    sheet_name='Janitza data ',
                    skiprows=skiprows,
                    nrows=nrows,
                    usecols='B:AO'
                )
                
                if df.empty:
                    raise Exception(f"No data found for {table_name}")
                
                # Create new DataFrame
                new_data = pd.DataFrame()
                new_data['meter_location'] = df.iloc[:, 0]

                # For calculated_consumption table, filter out rows where meter_location is null
                if table_name == 'calculated_consumption':
                    # Filter out rows where meter_location is null or empty
                    mask = new_data['meter_location'].notna() & (new_data['meter_location'].str.strip() != '')
                    df = df[mask]  # Apply filter to original dataframe
                    new_data = new_data[mask]
                    # Reset index after filtering
                    df = df.reset_index(drop=True)
                    new_data = new_data.reset_index(drop=True)
                
                # Generate month-year combinations for column names in correct order
                date_columns = []
                for year in [2022, 2023, 2024]:
                    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    for month in months:
                        date_columns.append(f"{month}_{year}")
                for month in ['Jan', 'Feb', 'Mar']:
                    date_columns.append(f"{month}_2025")
                
                # Map data columns directly, starting from column index 1 (after meter_location)
                for i, date_col in enumerate(date_columns):
                    if i + 1 < len(df.columns):  # Check if column exists in source data
                        new_data[date_col] = df.iloc[:, i + 1]  # Start from column after meter_location
                    else:
                        new_data[date_col] = None
                
                # Handle all value validation in one pass
                for col in date_columns:
                    new_data[col] = pd.to_numeric(new_data[col], errors='coerce')
                    new_data[col] = new_data[col].where(
                        (pd.notnull(new_data[col])) & (new_data[col] >= 0),
                        None
                    )
                
                return new_data
                
            except Exception as e:
                raise Exception(f"Error processing {table_name}: {str(e)}")
    
    def validate_data(self) -> Dict:
        """
        Validate loaded data and return validation report for all tables.
        """
        if not self.raw_data:
            self.load_all_data()
            
        validation_report = {}
        for table_name, data in self.raw_data.items():
            validation_report[table_name] = {
                'total_rows': len(data),
                'columns': data.columns.tolist(),
                'missing_values': data.isnull().sum().to_dict(),
                'value_ranges': {
                    col: {
                        'min': data[col].min(),
                        'max': data[col].max(),
                        'null_count': data[col].isnull().sum()
                    }
                    for col in data.columns 
                    if col not in ['meter_location']
                }
            }
        
        return validation_report
