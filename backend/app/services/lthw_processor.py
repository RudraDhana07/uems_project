# backend/app/services/lthw_processor.py

import pandas as pd
from typing import Dict

class LTHWProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = {}

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        try:
            table_configs = [
                ('automated_meter', 27, 27, {'object_name': 'A', 'object_description': 'B',
                                           'company': 'D', 'identifier': 'E', 'notes': 'F'}),
                ('manual_meter', 55, 6, {'object_name': 'A', 'meter_location': 'B',
                                       'company': 'D', 'identifier': 'E', 'notes': 'F'}),
                ('consumption', 64, 40, {'object_name': 'A', 'notes': 'D',
                                       'comments': 'E', 'misc': 'F'})
            ]

            for table_name, skiprows, nrows, columns_map in table_configs:
                self.raw_data[table_name] = self._process_table(skiprows, nrows, table_name, columns_map)
            
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Error loading LTHW data: {str(e)}")

    def _process_table(self, skiprows: int, nrows: int, table_name: str, columns_map: dict) -> pd.DataFrame:
        try:
            df = pd.read_excel(
                self.excel_file,
                sheet_name='LTHW Data',
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

            # Map reading columns starting from column G
            reading_start_idx = ord('G') - ord('A')
            for i, date_col in enumerate(date_columns):
                col_idx = reading_start_idx + i
                if col_idx < len(df.columns):
                    new_data[date_col] = pd.to_numeric(df.iloc[:, col_idx], errors='coerce')
                    # Handle negative values
                    new_data[date_col] = new_data[date_col].where(
                        (pd.notnull(new_data[date_col])) & (new_data[date_col] >= 0),
                        None
                    )
                else:
                    new_data[date_col] = None

            return new_data

        except Exception as e:
            raise Exception(f"Error processing {table_name}: {str(e)}")

    def validate_data(self) -> Dict:
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
                    if col not in ['object_name', 'object_description', 'meter_location',
                                 'company', 'identifier', 'notes', 'comments', 'misc']
                }
            }

        return validation_report
