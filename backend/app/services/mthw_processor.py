# backend/app/services/mthw_processor.py

import pandas as pd
from typing import Dict

class MTHWProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = {}

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        try:
            # Process meter reading data
            meter_reading_df = self._process_meter_reading()
            self.raw_data['meter_reading'] = meter_reading_df

            # Process consumption reading data
            consumption_reading_df = self._process_consumption_reading()
            self.raw_data['consumption_reading'] = consumption_reading_df

            return self.raw_data
        except Exception as e:
            raise Exception(f"Error loading MTHW data: {str(e)}")

    def _process_meter_reading(self) -> pd.DataFrame:
        try:
            # Read excel data for meter reading
            df = pd.read_excel(
                self.excel_file,
                sheet_name='MTHW Data',
                skiprows=30,
                nrows=32,
                usecols='A:AS'
            )

            # Initialize new dataframe for processed data
            new_data = pd.DataFrame()

            # Map basic columns
            new_data['meter_location'] = df.iloc[:, 0]  # Column A
            new_data['multiplier_for_unit'] = df.iloc[:, 6]  # Column G

            # Remove rows where meter_location is empty
            new_data = new_data.dropna(subset=['meter_location'])

            # Map monthly readings (H to AS columns)
            months = ['Nov_2021', 'Dec_2021']
            for year in range(2022, 2025):
                for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                    months.append(f"{month}_{year}")

            # Map excel columns H onwards to monthly readings
            for idx, month in enumerate(months):
                new_data[month] = df.iloc[:, 7 + idx]  # Starting from column H

            # Add empty columns for 2025
            new_data['Jan_2025'] = None
            new_data['Feb_2025'] = None
            new_data['Mar_2025'] = None

            # Convert any non-numeric values to None
            numeric_columns = [col for col in new_data.columns 
                             if col not in ['meter_location']]
            for col in numeric_columns:
                new_data[col] = pd.to_numeric(new_data[col], errors='coerce')

            return new_data

        except Exception as e:
            raise Exception(f"Error processing meter reading: {str(e)}")

    def _process_consumption_reading(self) -> pd.DataFrame:
        try:
            # Read excel data for consumption reading
            df = pd.read_excel(
                self.excel_file,
                sheet_name='MTHW Data',
                skiprows=74,
                nrows=29,
                usecols='A:AV'
            )

            # Initialize new dataframe for processed data
            new_data = pd.DataFrame()

            # Map basic columns
            new_data['meter_location'] = df.iloc[:, 0]  # Column A
            new_data['misc1'] = df.iloc[:, 1]  # Column B
            new_data['misc2'] = df.iloc[:, 2]  # Column C
            new_data['multiplier_for_unit'] = df.iloc[:, 6]  # Column G

            # Remove rows where meter_location is empty
            new_data = new_data.dropna(subset=['meter_location'])

            # Map monthly readings (H to AV columns)
            months = ['Nov_2021', 'Dec_2021']
            for year in range(2022, 2025):
                for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                    months.append(f"{month}_{year}")
            months.extend(['Jan_2025', 'Feb_2025', 'Mar_2025'])

            # Map excel columns H onwards to monthly readings
            for idx, month in enumerate(months):
                new_data[month] = df.iloc[:, 7 + idx]  # Starting from column H

            # Convert any non-numeric values to None
            numeric_columns = [col for col in new_data.columns 
                             if col not in ['meter_location', 'misc1', 'misc2']]
            for col in numeric_columns:
                new_data[col] = pd.to_numeric(new_data[col], errors='coerce')

            return new_data

        except Exception as e:
            raise Exception(f"Error processing consumption reading: {str(e)}")

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
                    if col not in ['meter_location', 'misc1', 'misc2']
                }
            }
        return validation_report
