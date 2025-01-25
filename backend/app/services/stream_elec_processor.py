# backend/app/services/stream_elec_processor.py

import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime, date

class StreamElecProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = {}
        
    def generate_date_columns(self) -> tuple:
        months = []
        years = []
        for year in range(2022, 2025):
            for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                months.append(month)
                years.append(year)
        # Add Jan-Mar 2025
        for month in ['Jan', 'Feb', 'Mar']:
            months.append(month)
            years.append(2025)
        return months, years

    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        try:
            # Generate month and year sequences
            months, years = self.generate_date_columns()
            
            # Load both sheets
            stream_df = pd.read_excel(self.excel_file, sheet_name='Stream Elec Data')
            janitza_df = pd.read_excel(self.excel_file, sheet_name='Janitza data ')
            
            # Process each table
            self.raw_data['ring_mains'] = self._process_ring_mains(stream_df, months, years)
            self.raw_data['libraries'] = self._process_libraries(stream_df, janitza_df, months, years)
            self.raw_data['colleges'] = self._process_colleges(stream_df, months, years)
            self.raw_data['science'] = self._process_science(stream_df, janitza_df, months, years)
            self.raw_data['health_science'] = self._process_health_science(stream_df, months, years)
            self.raw_data['humanities'] = self._process_humanities(stream_df, janitza_df, months, years)
            self.raw_data['obs_psychology'] = self._process_obs_psychology(stream_df, janitza_df, months, years)
            self.raw_data['total_stream'] = self._process_total_stream_dn(stream_df, months, years)
            self.raw_data['its_servers'] = self._process_its_servers(stream_df, janitza_df, months, years)
            self.raw_data['school_of_medicine'] = self._process_school_of_medicine(stream_df, months, years)
            self.raw_data['commerce'] = self._process_commerce(janitza_df, months, years)
            
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Error loading Stream Electricity data: {str(e)}")

    def _get_janitza_column_data(self, df: pd.DataFrame, row_index: int, 
                                start_col: str = 'C', end_col: str = 'AO') -> pd.Series:
        """Helper method to extract data from Janitza sheet for specific row"""
        # Direct mapping of column letters to indices
        column_to_index = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
            'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
            'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21,
            'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'AA': 26, 'AB': 27, 'AC': 28,
            'AD': 29, 'AE': 30, 'AF': 31, 'AG': 32, 'AH': 33, 'AI': 34,
            'AJ': 35, 'AK': 36, 'AL': 37, 'AM': 38, 'AN': 39, 'AO': 40
        }
        
        start_idx = column_to_index[start_col]
        end_idx = column_to_index[end_col]
        
        # Get the row data
        row_data = df.iloc[row_index]
        # Extract only the columns we need
        return row_data.iloc[start_idx:end_idx+1]


    def _process_ring_mains(self, df: pd.DataFrame, months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or value == ' ' or value == '':
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Read columns C:H and CE with null handling
        data['ring_main_1_mp4889_kwh'] = df.iloc[0:51, 2].apply(to_float_or_none)
        data['ring_main_1_mp4889_pf'] = df.iloc[0:51, 3].apply(to_float_or_none)
        data['ring_main_2_kwh'] = df.iloc[0:51, 4].apply(to_float_or_none)
        data['ring_main_2_pf'] = df.iloc[0:51, 5].apply(to_float_or_none)
        data['ring_main_3_kwh'] = df.iloc[0:51, 6].apply(to_float_or_none)
        data['ring_main_3_pf'] = df.iloc[0:51, 7].apply(to_float_or_none)
        data['ring_mains_total_kwh'] = df.iloc[0:51, 82].apply(to_float_or_none)
    
        return data

    def _process_libraries(self, stream_df: pd.DataFrame, janitza_df: pd.DataFrame, 
                      months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Stream Elec Data columns with null handling
        data['hocken_library_kwh'] = stream_df.iloc[0:51, 34].apply(to_float_or_none)
        data['hocken_library_pf'] = stream_df.iloc[0:51, 35].apply(to_float_or_none)
        data['robertson_library_kwh'] = stream_df.iloc[0:51, 46].apply(to_float_or_none)
        data['robertson_library_pf'] = stream_df.iloc[0:51, 47].apply(to_float_or_none)
        
        # Process Janitza data columns
        # Extract the required rows from Janitza data and transpose them
        bill_robertson_data = janitza_df.iloc[308, 2:53].reset_index(drop=True)  # C to AO
        sayers_adams_data = janitza_df.iloc[9, 2:53].reset_index(drop=True)      # C to AO
        isb_west_data = janitza_df.iloc[572, 2:53].reset_index(drop=True)        # C to AO
        richardson_data = janitza_df.iloc[256, 2:53].reset_index(drop=True)      # C to AO
        
        # Add Janitza columns with null handling
        data['bill_robertson_library_msb'] = bill_robertson_data.apply(to_float_or_none)
        data['sayers_adams_msb'] = sayers_adams_data.apply(to_float_or_none)
        data['isb_west_excluding_shops'] = isb_west_data.apply(to_float_or_none)
        data['richardson_library_block_rising_main'] = richardson_data.apply(to_float_or_none)
        
        # Total from Stream Elec Data with null handling
        data['libraries_total_kwh'] = stream_df.iloc[0:51, 83].apply(to_float_or_none)
        
        return data



    def _process_science(self, stream_df: pd.DataFrame, janitza_df: pd.DataFrame, 
                        months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Stream Elec Data columns with null handling
        data['survey_marine_kwh'] = stream_df.iloc[0:51, 16].apply(to_float_or_none)
        data['survey_marine_pf'] = stream_df.iloc[0:51, 17].apply(to_float_or_none)
        data['zoology_buildings_kwh'] = stream_df.iloc[0:51, 22].apply(to_float_or_none)
        data['zoology_buildings_pf'] = stream_df.iloc[0:51, 23].apply(to_float_or_none)
        data['botany_tin_hut_kwh'] = stream_df.iloc[0:51, 38].apply(to_float_or_none)
        data['botany_tin_hut_pf'] = stream_df.iloc[0:51, 39].apply(to_float_or_none)
        data['physical_education_kwh'] = stream_df.iloc[0:51, 40].apply(to_float_or_none)
        data['physical_education_pf'] = stream_df.iloc[0:51, 41].apply(to_float_or_none)
        data['owheo_building_kwh'] = stream_df.iloc[0:51, 44].apply(to_float_or_none)
        data['owheo_building_pf'] = stream_df.iloc[0:51, 45].apply(to_float_or_none)
        data['mellor_laboratories_kwh'] = stream_df.iloc[0:51, 52].apply(to_float_or_none)
        data['mellor_laboratories_pf'] = stream_df.iloc[0:51, 53].apply(to_float_or_none)
        data['microbiology_kwh'] = stream_df.iloc[0:51, 56].apply(to_float_or_none)
        data['microbiology_pf'] = stream_df.iloc[0:51, 57].apply(to_float_or_none)
        data['science_2_kwh'] = stream_df.iloc[0:51, 58].apply(to_float_or_none)
        data['science_2_pf'] = stream_df.iloc[0:51, 59].apply(to_float_or_none)
        data['portobello_marine_lab_kwh'] = stream_df.iloc[0:51, 76].apply(to_float_or_none)
        data['portobello_marine_lab_pf'] = stream_df.iloc[0:51, 77].apply(to_float_or_none)
        
        # Janitza data columns with null handling
        janitza_data = self._get_janitza_column_data(janitza_df, 398).apply(to_float_or_none)
        data['geology_north'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 399).apply(to_float_or_none)
        data['geology_south'] = janitza_data
        
        # Total with null handling
        data['science_total_kwh'] = stream_df.iloc[0:51, 84].apply(to_float_or_none)
        
        return data


    def _process_health_science(self, df: pd.DataFrame, months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Map columns with null handling
        data['taieri_farm_kwh'] = df.iloc[0:51, 8].apply(to_float_or_none)
        data['taieri_farm_pf'] = df.iloc[0:51, 9].apply(to_float_or_none)
        data['med_school_sub_main_kwh'] = df.iloc[0:51, 12].apply(to_float_or_none)
        data['med_school_sub_main_pf'] = df.iloc[0:51, 13].apply(to_float_or_none)
        data['dental_school_kwh'] = df.iloc[0:51, 24].apply(to_float_or_none)
        data['dental_school_pf'] = df.iloc[0:51, 25].apply(to_float_or_none)
        data['hunter_centre_kwh'] = df.iloc[0:51, 26].apply(to_float_or_none)
        data['hunter_centre_pf'] = df.iloc[0:51, 27].apply(to_float_or_none)
        data['physiotherapy_kwh'] = df.iloc[0:51, 28].apply(to_float_or_none)
        data['physiotherapy_pf'] = df.iloc[0:51, 29].apply(to_float_or_none)
        data['research_support_facility_kwh'] = df.iloc[0:51, 32].apply(to_float_or_none)
        data['research_support_facility_pf'] = df.iloc[0:51, 33].apply(to_float_or_none)
        data['health_science_total_kwh'] = df.iloc[0:51, 85].apply(to_float_or_none)
        
        return data


    def _process_humanities(self, stream_df: pd.DataFrame, janitza_df: pd.DataFrame, 
                       months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Stream Elec Data columns with null handling
        data['education_main_boiler_room_kwh'] = stream_df.iloc[0:51, 50].apply(to_float_or_none)
        data['education_main_boiler_room_pf'] = stream_df.iloc[0:51, 51].apply(to_float_or_none)
        
        # Janitza data columns with null handling
        janitza_data = self._get_janitza_column_data(janitza_df, 252).apply(to_float_or_none)
        data['richardson_mains'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 268).apply(to_float_or_none)
        data['arts_1_submains_msb'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 267).apply(to_float_or_none)
        data['albany_leith_walk'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 401).apply(to_float_or_none)
        data['archway_buildings'] = janitza_data
        
        # Total with null handling
        data['humanities_total_kwh'] = stream_df.iloc[0:51, 86].apply(to_float_or_none)
        
        return data


    def _process_obs_psychology(self, stream_df: pd.DataFrame, janitza_df: pd.DataFrame, 
                            months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Janitza data columns with null handling
        janitza_data = self._get_janitza_column_data(janitza_df, 278).apply(to_float_or_none)
        data['business_incomer_1_lower'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 279).apply(to_float_or_none)
        data['business_incomer_2_upper'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 297).apply(to_float_or_none)
        data['psychology_substation_goddard'] = janitza_data
        
        # Total with null handling
        data['obs_psychology_total_kwh'] = stream_df.iloc[0:51, 87].apply(to_float_or_none)
        
        return data


    def _process_its_servers(self, stream_df: pd.DataFrame, janitza_df: pd.DataFrame, 
                        months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Stream Elec Data columns with null handling
        data['great_king_street_kwh'] = stream_df.iloc[0:51, 36].apply(to_float_or_none)
        data['great_king_street_pf'] = stream_df.iloc[0:51, 37].apply(to_float_or_none)
        
        # Janitza data columns with null handling
        janitza_data = self._get_janitza_column_data(janitza_df, 47).apply(to_float_or_none)
        data['great_king_main_meter'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 48).apply(to_float_or_none)
        data['great_king_physiotherapy'] = janitza_data
        
        # Calculate total with proper null handling
        data['its_servers_total_kwh'] = data.apply(
            lambda row: (float(row['great_king_street_kwh'] or 0) + 
                        float(row['great_king_main_meter'] or 0) - 
                        float(row['great_king_physiotherapy'] or 0)), axis=1)
        
        return data


    def _process_commerce(self, janitza_df: pd.DataFrame, months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Janitza data columns with null handling
        janitza_data = self._get_janitza_column_data(janitza_df, 278).apply(to_float_or_none)
        data['business_incomer_1_lower'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 279).apply(to_float_or_none)
        data['business_incomer_2_upper'] = janitza_data
        
        janitza_data = self._get_janitza_column_data(janitza_df, 297).apply(to_float_or_none)
        data['psychology_substation_goddard'] = janitza_data
        
        # Calculate total with proper null handling
        data['commerce_total_kwh'] = data.apply(
            lambda row: float(row['business_incomer_1_lower'] or 0) + 
                    float(row['business_incomer_2_upper'] or 0) + 
                    float(row['psychology_substation_goddard'] or 0), axis=1)
        
        return data


    def _process_school_of_medicine(self, df: pd.DataFrame, months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Map columns with null handling
        data['school_of_medicine_chch_kwh'] = df.iloc[0:51, 80].apply(to_float_or_none)
        data['school_of_medicine_chch_pf'] = df.iloc[0:51, 81].apply(to_float_or_none)
        
        return data

    
    def _process_colleges(self, df: pd.DataFrame, months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # First set of columns with direct indices and null handling
        data['castle_college_kwh'] = df.iloc[0:51, 10].apply(to_float_or_none)
        data['castle_college_pf'] = df.iloc[0:51, 11].apply(to_float_or_none)
        data['hayward_college_kwh'] = df.iloc[0:51, 14].apply(to_float_or_none)
        data['hayward_college_pf'] = df.iloc[0:51, 15].apply(to_float_or_none)
        data['cumberland_college_kwh'] = df.iloc[0:51, 18].apply(to_float_or_none)
        data['cumberland_college_pf'] = df.iloc[0:51, 19].apply(to_float_or_none)
        data['executive_residence_kwh'] = df.iloc[0:51, 42].apply(to_float_or_none)
        data['executive_residence_pf'] = df.iloc[0:51, 43].apply(to_float_or_none)
        data['owheo_building_kwh'] = df.iloc[0:51, 44].apply(to_float_or_none)
        data['owheo_building_pf'] = df.iloc[0:51, 45].apply(to_float_or_none)
        data['st_margarets_college_kwh'] = df.iloc[0:51, 60].apply(to_float_or_none)
        data['st_margarets_college_pf'] = df.iloc[0:51, 61].apply(to_float_or_none)
        
        # BM:BX columns (indices 64-77)
        start_idx = 64  # Column BM
        column_pairs = [
            ('selwyn_college_kwh', 'selwyn_college_pf'),
            ('arana_college_main_kwh', 'arana_college_main_pf'),
            ('studholm_college_kwh', 'studholm_college_pf'),
            ('carrington_college_kwh', 'carrington_college_pf'),
            ('aquinas_college_kwh', 'aquinas_college_pf'),
            ('caroline_freeman_college_kwh', 'caroline_freeman_college_pf')
        ]
        
        for i, (kwh_col, pf_col) in enumerate(column_pairs):
            col_idx = start_idx + (i * 2)
            data[kwh_col] = df.iloc[0:51, col_idx].apply(to_float_or_none)
            data[pf_col] = df.iloc[0:51, col_idx + 1].apply(to_float_or_none)
        
        # Last columns with null handling
        data['abbey_college_kwh'] = df.iloc[0:51, 78].apply(to_float_or_none)
        data['abbey_college_pf'] = df.iloc[0:51, 79].apply(to_float_or_none)
        data['colleges_total_kwh'] = df.iloc[0:51, 84].apply(to_float_or_none)

        return data


    
    def _process_total_stream_dn(self, df: pd.DataFrame, months: list, years: list) -> pd.DataFrame:
        data = pd.DataFrame()
        data['meter_reading_month'] = months
        data['meter_reading_year'] = years
        
        # Helper function to convert values to float or None
        def to_float_or_none(value):
            if pd.isna(value) or str(value).strip() in ['', ' ']:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        # Read all columns from A to CB (columns 3 to 80)
        column_names = [
            'ring_main_1_mp4889_kwh', 'ring_main_1_mp4889_pf',
            'ring_main_2_kwh', 'ring_main_2_pf',
            'ring_main_3_kwh', 'ring_main_3_pf',
            'taieri_farm_kwh', 'taieri_farm_pf',
            'castle_college_kwh', 'castle_college_pf',
            'med_school_sub_main_kwh', 'med_school_sub_main_pf',
            'hayward_college_kwh', 'hayward_college_pf',
            'survey_marine_kwh', 'survey_marine_pf',
            'cumberland_college_kwh', 'cumberland_college_pf',
            'school_of_dentistry_kwh', 'school_of_dentistry_pf',
            'zoology_buildings_kwh', 'zoology_buildings_pf',
            'dental_school_kwh', 'dental_school_pf',
            'hunter_centre_kwh', 'hunter_centre_pf',
            'physiotherapy_kwh', 'physiotherapy_pf',
            'student_health_kwh', 'student_health_pf',
            'research_support_facility_kwh', 'research_support_facility_pf',
            'hocken_library_kwh', 'hocken_library_pf',
            'great_king_street_kwh', 'great_king_street_pf',
            'botany_tin_hut_kwh', 'botany_tin_hut_pf',
            'physical_education_kwh', 'physical_education_pf',
            'executive_residence_kwh', 'executive_residence_pf',
            'owheo_building_kwh', 'owheo_building_pf',
            'robertson_library_kwh', 'robertson_library_pf',
            'plaza_building_kwh', 'plaza_building_pf',
            'education_main_boiler_room_kwh', 'education_main_boiler_room_pf',
            'mellor_laboratories_kwh', 'mellor_laboratories_pf',
            'biochemistry_kwh', 'biochemistry_pf',
            'microbiology_kwh', 'microbiology_pf',
            'science_2_kwh', 'science_2_pf',
            'st_margarets_college_kwh', 'st_margarets_college_pf',
            'unicol_kwh', 'unicol_pf',
            'selwyn_college_kwh', 'selwyn_college_pf',
            'arana_college_main_kwh', 'arana_college_main_pf',
            'studholm_college_kwh', 'studholm_college_pf',
            'carrington_college_kwh', 'carrington_college_pf',
            'aquinas_college_kwh', 'aquinas_college_pf',
            'caroline_freeman_college_kwh', 'caroline_freeman_college_pf',
            'portobello_marine_lab_kwh', 'portobello_marine_lab_pf',
            'abbey_college_kwh', 'abbey_college_pf'
        ]
        
        # Map all columns with null handling
        for i, col_name in enumerate(column_names):
            if i < 78:  # Only process the first 78 columns (A to CB)
                data[col_name] = df.iloc[0:51, i].apply(to_float_or_none)
        
        # Add the final total column CL with null handling
        data['total_stream_dn_electricity_kwh'] = df.iloc[0:51, 88].apply(to_float_or_none)
        
        return data
