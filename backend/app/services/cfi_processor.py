# backend/app/services/cfi_processor.py

import pandas as pd
import numpy as np
from typing import Dict

class CfiProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = {}

    def _handle_float_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        # Replace negative values with 0 in float columns
        float_columns = df.select_dtypes(include=['float64']).columns
        for col in float_columns:
            df[col] = df[col].apply(lambda x: max(0, x) if pd.notnull(x) else 0)
        return df

    def _process_meter_data(self) -> pd.DataFrame:
        try:
            # Read meter data from Excel without usecols restriction
            df = pd.read_excel(
                self.excel_file,
                sheet_name='CfI',
                skiprows=1,
                nrows=42
            )

            if df.empty:
                raise Exception("No data found for center_for_innovation")

            # Create new DataFrame with mapped columns
            new_data = pd.DataFrame()

            # Map specific columns
            column_mapping = {
                'building_code': 'A',
                'location': 'B', 
                'meter_type': 'E',
                'meter_number': 'F',
                'digit_to_read': 'G',
                'multipier_ct_rating': 'H',
                'remark': 'I',
                'mod': 'J'
            }

            # Fill non-numeric columns with empty string if null
            for new_col, excel_col in column_mapping.items():
                col_index = ord(excel_col) - ord('A')
                if col_index < len(df.columns):
                    new_data[new_col] = df.iloc[:, col_index].fillna('')
                else:
                    new_data[new_col] = ''

            # Generate reading columns
            reading_columns = []
            # 2021-2022 readings with R1 prefix

            reading_columns.append(f"R1_Dec_2021")
            
            for year in [2022]:
                for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                    reading_columns.append(f"R1_{month}_{year}")
            
            reading_columns.append(f"R1_Jan_2023")

            # 2023-2025 readings without prefix
            for year in [2023, 2024]:
                for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                    reading_columns.append(f"{month}_{year}")

            # Add 2025 readings
            for month in ['Jan', 'Feb', 'Mar']:
                reading_columns.append(f"{month}_2025")

            # Map reading columns starting from column K
            reading_start_idx = ord('K') - ord('A')
            for i, date_col in enumerate(reading_columns):
                col_idx = reading_start_idx + i
                if col_idx < len(df.columns):
                    new_data[date_col] = pd.to_numeric(df.iloc[:, col_idx], errors='coerce').fillna(0)
                else:
                    new_data[date_col] = 0  # Set default value for missing columns

            # Filter out rows where location is empty or null
            new_data = new_data[new_data['location'].notna() & (new_data['location'] != '')]

            return new_data

        except Exception as e:
            raise Exception(f"Error processing meter data: {str(e)}")


    def _process_room_data(self) -> pd.DataFrame:
        try:
            df = pd.read_excel(
                self.excel_file,
                sheet_name='CfI',
                skiprows=57,
                nrows=73,
                usecols='A:D'
            )

            if df.empty:
                raise Exception("No data found for cfi_room_types")

            # Rename columns to match database structure
            df.columns = ['room_number', 'area_m2', 'type', 'suite']

            # Fill non-numeric columns with empty string if null
            string_columns = ['room_number', 'type', 'suite']
            for col in string_columns:
                df[col] = df[col].fillna('')

            # Fill numeric columns with 0 if null
            df['area_m2'] = pd.to_numeric(df['area_m2'], errors='coerce').fillna(0)

            # Handle negative values in area_m2
            df = self._handle_float_columns(df)

            # Filter out rows where room_number is empty or null
            df = df[df['room_number'].notna() & (df['room_number'] != '')]

            return df

        except Exception as e:
            raise Exception(f"Error processing room data: {str(e)}")

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        try:
            self.raw_data['center_for_innovation'] = self._process_meter_data()
            self.raw_data['cfi_room_types'] = self._process_room_data()
            return self.raw_data
        except Exception as e:
            raise Exception(f"Error loading CFI data: {str(e)}")
