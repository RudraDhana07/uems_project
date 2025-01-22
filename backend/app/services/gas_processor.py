# backend/app/services/gas_processor.py

import pandas as pd
from typing import Dict

class GasProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = {}

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        try:
            table_configs = [
                ('automated_meter', 27, 28, {
                    'meter_description': 'A', 
                    'icp': 'B'
                }),
                ('manual_meter', 56, 16, {
                    'meter_description': 'A', 
                    'misc1': 'E',
                    'misc2': 'F'
                }),
                ('consumption', 76, 15, {
                    'object_description': 'A', 
                    'misc': 'F'
                })
            ]

            for table_name, skiprows, nrows, columns_map in table_configs:
                self.raw_data[table_name] = self._process_table(skiprows, nrows, table_name, columns_map)
            
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Error loading Gas data: {str(e)}")

    def _process_table(self, skiprows: int, nrows: int, table_name: str, columns_map: dict) -> pd.DataFrame:
        try:
            df = pd.read_excel(
                self.excel_file,
                sheet_name='Gas Data',
                skiprows=skiprows,
                nrows=nrows
            )

            if df.empty:
                raise Exception(f"No data found for {table_name}")

            new_data = pd.DataFrame()
            
            # Map metadata columns
            for new_col, excel_col in columns_map.items():
                col_index = ord(excel_col) - ord('A')
                if col_index < len(df.columns):
                    new_data[new_col] = df.iloc[:, col_index]
                else:
                    new_data[new_col] = None

            # Generate month-year combinations
            date_columns = []
            for year in [2022, 2023, 2024]:
                for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                    date_columns.append(f"{month}_{year}")
            
            for month in ['Jan', 'Feb', 'Mar']:
                date_columns.append(f"{month}_2025")

            # Set reading start column for each table type
            if table_name == 'automated_meter':
                reading_start_idx = ord('G') - ord('A')  # Skip C to F, start from G
            elif table_name == 'manual_meter':
                reading_start_idx = ord('G') - ord('A')  # Start from G after E,F
            else:  # consumption
                reading_start_idx = ord('G') - ord('A')  # Start from G after F

            # Map reading columns
            for i, date_col in enumerate(date_columns):
                col_idx = reading_start_idx + i
                if col_idx < len(df.columns):
                    new_data[date_col] = pd.to_numeric(df.iloc[:, col_idx], errors='coerce')
                    new_data[date_col] = new_data[date_col].where(
                        (pd.notnull(new_data[date_col])) & (new_data[date_col] >= 0),
                        None
                    )
                else:
                    new_data[date_col] = None

            return new_data

        except Exception as e:
            raise Exception(f"Error processing {table_name}: {str(e)}")
