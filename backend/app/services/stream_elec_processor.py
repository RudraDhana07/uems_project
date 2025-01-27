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
        # Calculate total with proper null handling
        data['ring_mains_total_kwh'] = data.apply(
            lambda row: float(row['ring_main_1_mp4889_kwh'] or 0) + 
                    float(row['ring_main_2_kwh'] or 0) + 
                    float(row['ring_main_3_kwh'] or 0), axis=1)
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
        
        # Calculate total with proper null handling
        data['libraries_total_kwh'] = data.apply(
            lambda row: float(row['hocken_library_kwh'] or 0) + 
                    float(row['robertson_library_kwh'] or 0) + 
                    float(row['bill_robertson_library_msb'] or 0)+
                    float(row['sayers_adams_msb'] or 0) + 
                    float(row['isb_west_excluding_shops'] or 0) +
                    float(row['richardson_library_block_rising_main'] or 0), axis=1)
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
        
        geology_north_data = janitza_df.iloc[398, 2:53].reset_index(drop=True)  # C to AO
        geology_south_data = janitza_df.iloc[399, 2:53].reset_index(drop=True)  # C to AO

        # Add Janitza columns with null handling
        data['geology_north'] = geology_north_data.apply(to_float_or_none)
        data['geology_south'] = geology_south_data.apply(to_float_or_none)
        
        # Calculate total with proper null handling
        data['science_total_kwh'] = data.apply(
            lambda row: float(row['survey_marine_kwh'] or 0) + 
                    float(row['zoology_buildings_kwh'] or 0) + 
                    float(row['botany_tin_hut_kwh'] or 0) +
                    float(row['physical_education_kwh'] or 0) + 
                    float(row['owheo_building_kwh'] or 0) +
                    float(row['mellor_laboratories_kwh'] or 0) + 
                    float(row['microbiology_kwh'] or 0) + 
                    float(row['science_2_kwh'] or 0) +
                    float(row['portobello_marine_lab_kwh'] or 0) + 
                    float(row['geology_north'] or 0) +
                    float(row['geology_south'] or 0), axis=1)
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
        
         # Calculate total with proper null handling
        data['health_science_total_kwh'] = data.apply(
            lambda row: float(row['taieri_farm_kwh'] or 0) + 
                    float(row['med_school_sub_main_kwh'] or 0) + 
                    float(row['dental_school_kwh'] or 0) +
                    float(row['hunter_centre_kwh'] or 0) + 
                    float(row['physiotherapy_kwh'] or 0) +
                    float(row['research_support_facility_kwh'] or 0), axis=1)
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
        
        richardson_data = janitza_df.iloc[252, 2:53].reset_index(drop=True)  # C to AO
        arts_1_data = janitza_df.iloc[268, 2:53].reset_index(drop=True)     # C to AO
        albany_data = janitza_df.iloc[267, 2:53].reset_index(drop=True)     # C to AO
        archway_data = janitza_df.iloc[401, 2:53].reset_index(drop=True)    # C to AO

        # Add Janitza columns with null handling
        data['richardson_mains'] = richardson_data.apply(to_float_or_none)
        data['arts_1_submains_msb'] = arts_1_data.apply(to_float_or_none)
        data['albany_leith_walk'] = albany_data.apply(to_float_or_none)
        data['archway_buildings'] = archway_data.apply(to_float_or_none)
        
        # Total with null handling
        data['humanities_total_kwh'] = stream_df.iloc[0:51, 87].apply(to_float_or_none)

         # Calculate total with proper null handling
        data['humanities_total_kwh'] = data.apply(
            lambda row: float(row['education_main_boiler_room_kwh'] or 0) + 
                    float(row['richardson_mains'] or 0) + 
                    float(row['arts_1_submains_msb'] or 0)+
                    float(row['albany_leith_walk'] or 0) + 
                    float(row['archway_buildings'] or 0), axis=1)
        
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
        
        # Process Janitza data columns
        # Extract the required rows from Janitza data and transpose them
        business_incomer_1_data = janitza_df.iloc[278, 2:53].reset_index(drop=True)  # C to AO
        business_incomer_2_data = janitza_df.iloc[279, 2:53].reset_index(drop=True)  # C to AO
        psychology_data = janitza_df.iloc[297, 2:53].reset_index(drop=True)          # C to AO
        
        # Add Janitza columns with null handling
        data['business_incomer_1_lower'] = business_incomer_1_data.apply(to_float_or_none)
        data['business_incomer_2_upper'] = business_incomer_2_data.apply(to_float_or_none)
        data['psychology_substation_goddard'] = psychology_data.apply(to_float_or_none)
        
        # Calculate total as sum of the three values with null handling
        data['obs_psychology_total_kwh'] = data.apply(
            lambda row: float(row['business_incomer_1_lower'] or 0) + 
                    float(row['business_incomer_2_upper'] or 0) + 
                    float(row['psychology_substation_goddard'] or 0), axis=1)
        
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
        
        # Process Janitza data columns
        # Extract the required rows from Janitza data and transpose them
        great_king_main_data = janitza_df.iloc[47, 2:53].reset_index(drop=True)  # C to AO
        great_king_phys_data = janitza_df.iloc[48, 2:53].reset_index(drop=True)  # C to AO
        
        # Add Janitza columns with null handling
        data['great_king_main_meter'] = great_king_main_data.apply(to_float_or_none)
        data['great_king_physiotherapy'] = great_king_phys_data.apply(to_float_or_none)
        
        # Calculate total with proper null handling
        data['its_servers_total_kwh'] = data.apply(
            lambda row: float(row['great_king_street_kwh'] or 0) + 
                    float(row['great_king_main_meter'] or 0) - 
                    float(row['great_king_physiotherapy'] or 0), axis=1)
        
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
        
        # Process Janitza data columns
        # Extract the required rows from Janitza data and transpose them
        business_incomer_1_data = janitza_df.iloc[278, 2:53].reset_index(drop=True)  # C to AO
        business_incomer_2_data = janitza_df.iloc[279, 2:53].reset_index(drop=True)  # C to AO
        psychology_data = janitza_df.iloc[297, 2:53].reset_index(drop=True)          # C to AO
        
        # Add Janitza columns with null handling
        data['business_incomer_1_lower'] = business_incomer_1_data.apply(to_float_or_none)
        data['business_incomer_2_upper'] = business_incomer_2_data.apply(to_float_or_none)
        data['psychology_substation_goddard'] = psychology_data.apply(to_float_or_none)
        
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
        
        # Calculate total with proper null handling
        data['colleges_total_kwh'] = data.apply(
            lambda row: float(row['castle_college_kwh'] or 0) + 
                    float(row['hayward_college_kwh'] or 0) + 
                    float(row['cumberland_college_kwh'] or 0) +
                    float(row['executive_residence_kwh'] or 0) + 
                    float(row['owheo_building_kwh'] or 0) +
                    float(row['st_margarets_college_kwh'] or 0) + 
                    float(row['selwyn_college_kwh'] or 0) + 
                    float(row['arana_college_main_kwh'] or 0) + 
                    float(row['studholm_college_kwh'] or 0) +
                    float(row['carrington_college_kwh'] or 0) + 
                    float(row['aquinas_college_kwh'] or 0) + 
                    float(row['caroline_freeman_college_kwh'] or 0) +
                    float(row['abbey_college_kwh'] or 0), axis=1)
        
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
        
        # Column mappings with their Excel indices
        column_mappings = {
            'ring_main_1_mp4889_kwh': 2, 'ring_main_1_mp4889_pf': 3,
            'ring_main_2_kwh': 4, 'ring_main_2_pf': 5,
            'ring_main_3_kwh': 6, 'ring_main_3_pf': 7,
            'taieri_farm_kwh': 8, 'taieri_farm_pf': 9,
            'castle_college_kwh': 10, 'castle_college_pf': 11,
            'med_school_sub_main_kwh': 12, 'med_school_sub_main_pf': 13,
            'hayward_college_kwh': 14, 'hayward_college_pf': 15,
            'survey_marine_kwh': 16, 'survey_marine_pf': 17,
            'cumberland_college_kwh': 18, 'cumberland_college_pf': 19,
            'school_of_dentistry_kwh': 20, 'school_of_dentistry_pf': 21,
            'zoology_buildings_kwh': 22, 'zoology_buildings_pf': 23,
            'dental_school_kwh': 24, 'dental_school_pf': 25,
            'hunter_centre_kwh': 26, 'hunter_centre_pf': 27,
            'physiotherapy_kwh': 28, 'physiotherapy_pf': 29,
            'student_health_kwh': 30, 'student_health_pf': 31,
            'research_support_facility_kwh': 32, 'research_support_facility_pf': 33,
            'hocken_library_kwh': 34, 'hocken_library_pf': 35,
            'great_king_street_kwh': 36, 'great_king_street_pf': 37,
            'botany_tin_hut_kwh': 38, 'botany_tin_hut_pf': 39,
            'physical_education_kwh': 40, 'physical_education_pf': 41,
            'executive_residence_kwh': 42, 'executive_residence_pf': 43,
            'owheo_building_kwh': 44, 'owheo_building_pf': 45,
            'robertson_library_kwh': 46, 'robertson_library_pf': 47,
            'plaza_building_kwh': 48, 'plaza_building_pf': 49,
            'education_main_boiler_room_kwh': 50, 'education_main_boiler_room_pf': 51,
            'mellor_laboratories_kwh': 52, 'mellor_laboratories_pf': 53,
            'biochemistry_kwh': 54, 'biochemistry_pf': 55,
            'microbiology_kwh': 56, 'microbiology_pf': 57,
            'science_2_kwh': 58, 'science_2_pf': 59,
            'st_margarets_college_kwh': 60, 'st_margarets_college_pf': 61,
            'unicol_kwh': 62, 'unicol_pf': 63,
            'selwyn_college_kwh': 64, 'selwyn_college_pf': 65,
            'arana_college_main_kwh': 66, 'arana_college_main_pf': 67,
            'studholm_college_kwh': 68, 'studholm_college_pf': 69,
            'carrington_college_kwh': 70, 'carrington_college_pf': 71,
            'aquinas_college_kwh': 72, 'aquinas_college_pf': 73,
            'caroline_freeman_college_kwh': 74, 'caroline_freeman_college_pf': 75,
            'portobello_marine_lab_kwh': 76, 'portobello_marine_lab_pf': 77,
            'abbey_college_kwh': 78, 'abbey_college_pf': 79
        }
        
        # Map all columns with correct indices and null handling
        for col_name, idx in column_mappings.items():
            data[col_name] = df.iloc[0:51, idx].apply(to_float_or_none)
        
        # Calculate total by summing all _kwh columns
        kwh_columns = [col for col in data.columns if col.endswith('_kwh')]
        data['total_stream_dn_electricity_kwh'] = data[kwh_columns].sum(axis=1, skipna=True)
    
        return data

