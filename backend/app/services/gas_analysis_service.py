# backend/app/services/gas_analysis_service.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

class GasAnalysisService:
    def __init__(self, db):
        self.db = db
        self.n_clusters = 3
        self.anomaly_threshold = 50
        self.buildinglist = [
            'G60X,UNIVERSITY COLLEGE 1,315 LEITH',
            'K308 CFC 911 CUMBERLAND STREET,DUNEDIN',
            'K427,CFC EAST ABBEY COLLEGE,682 CASTLE STREET,DUNEDIN',
            'G608,ST MARGARET\'S COLLEGE,333 LEITH',
            'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH',
            'ARANA 110 CLYDE STREET,DUNEDIN',
            'AQUINAS 74 GLADSTONE ROAD,DUNEDIN'
        ]

    def get_analysis_data(self):
        try:
            with self.db.session.begin():
                query = "SELECT * FROM dbo.gas_automated_meter_cleaned"
                result = self.db.session.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                
                if df.empty:
                    logger.error("No data found in database")
                    return {"error": "No data found in database"}

                logger.info(f"Raw data shape: {df.shape}")
                cleaned_data = self._preprocess_data(df)
                logger.info(f"Cleaned data shape: {cleaned_data.shape}")
                
                if cleaned_data.shape[0] < self.n_clusters:
                    return {"error": f"Not enough valid data points for {self.n_clusters} clusters"}

                cluster_results, consumption_patterns = self._perform_clustering(cleaned_data)
                anomalies = self._analyze_anomalies(cleaned_data)

                college_consumption = self.get_college_yearly_analysis(cleaned_data)

                response = {
                    'cluster_results': cluster_results,
                    'consumption_patterns': consumption_patterns,
                    'anomaly_analysis': {
                        'anomalies': anomalies,
                        'threshold': self.anomaly_threshold
                    },
                    'college_consumption': college_consumption
                }
                
                logger.info(f"Analysis complete. Found {len(anomalies)} anomalies")
                return response

        except Exception as e:
            logger.exception("Error in gas analysis")
            raise


    def _preprocess_data(self, df):
        try:
            # Get relevant columns
            reading_cols = [col for col in df.columns 
                          if any(yr in col for yr in ['2022', '2023', '2024']) 
                          and '_' in col]
            
            # Select columns and create working copy
            analysis_df = df[['meter_description'] + reading_cols].copy()
            
            # Convert readings to numeric
            for col in reading_cols:
                analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')
            
            # Remove rows where all readings are NaN
            analysis_df = analysis_df.dropna(subset=reading_cols, how='all')
            
            # Fill remaining NaN values with 0
            analysis_df[reading_cols] = analysis_df[reading_cols].fillna(0)
            
            # Remove rows with all zeros
            mask = (analysis_df[reading_cols] != 0).any(axis=1)
            analysis_df = analysis_df[mask]
            
            logger.info(f"Processed data shape: {analysis_df.shape}")
            return analysis_df

        except Exception as e:
            logger.exception("Error in preprocessing:")
            raise

    def _perform_clustering(self, df):
        try:
            features = df.drop('meter_description', axis=1)
            
            # Scale the features
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(features)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=min(self.n_clusters, len(df)), random_state=42)
            clusters = kmeans.fit_predict(scaled_data)
            
            cluster_results = []
            consumption_patterns = []
            
            for i in range(kmeans.n_clusters):
                cluster_mask = clusters == i
                cluster_meters = df[cluster_mask]['meter_description'].tolist()
                
                cluster_results.append({
                    'cluster_id': i,
                    'meters': cluster_meters,
                    'size': len(cluster_meters)
                })
                
                pattern_data = features[cluster_mask].mean()
                consumption_patterns.append({
                    'cluster_id': i,
                    'consumption_pattern': pattern_data.to_dict()
                })
            
            return cluster_results, consumption_patterns

        except Exception as e:
            logger.exception("Error in clustering:")
            raise

    def _analyze_anomalies(self, df):  
            try:
                anomalies = []
                # Get columns for each year
                year_cols = {
                    '2022': [col for col in df.columns if '2022' in col and '_' in col],
                    '2023': [col for col in df.columns if '2023' in col and '_' in col],
                    '2024': [col for col in df.columns if '2024' in col and '_' in col]
                }
                
                for meter in df['meter_description'].unique():
                    meter_data = df[df['meter_description'] == meter]
                    
                    # Calculate yearly means
                    yearly_means = {}
                    # Calculate mean for each year
                    if year_cols['2022']:
                        yearly_means['2022'] = meter_data[year_cols['2022']].sum(axis=1).iloc[0] / 12
                    if year_cols['2023']:
                        yearly_means['2023'] = meter_data[year_cols['2023']].sum(axis=1).iloc[0] / 12
                    if year_cols['2024']:
                        yearly_means['2024'] = meter_data[year_cols['2024']].sum(axis=1).iloc[0] / 11  # 11 months for 2024
                    
                    # Check 2023 vs 2022
                    if '2022' in yearly_means and '2023' in yearly_means:
                        if yearly_means['2022'] > 0:
                            pct_change = ((yearly_means['2023'] - yearly_means['2022']) / yearly_means['2022']) * 100
                            if abs(pct_change) > self.anomaly_threshold:
                                anomalies.append({
                                    'meter': meter,
                                    'year': '2023',
                                    'value': round(yearly_means['2023'], 2),
                                    'previous_value': round(yearly_means['2022'], 2),
                                    'percent_change': round(pct_change, 2)
                                })
                    
                    # Check 2024 vs 2023
                    if '2023' in yearly_means and '2024' in yearly_means:
                        if yearly_means['2023'] > 0:
                            pct_change = ((yearly_means['2024'] - yearly_means['2023']) / yearly_means['2023']) * 100
                            if abs(pct_change) > self.anomaly_threshold:
                                anomalies.append({
                                    'meter': meter,
                                    'year': '2024',
                                    'value': round(yearly_means['2024'], 2),
                                    'previous_value': round(yearly_means['2023'], 2),
                                    'percent_change': round(pct_change, 2)
                                })
                
                return sorted(anomalies, key=lambda x: (x['meter'], x['year']))
                
            except Exception as e:
                logger.exception("Error in anomaly analysis")
                raise

    def get_college_yearly_analysis(self, df):
        try:
            # Create mapping for shorter names
            name_mapping = {
                'G60X,UNIVERSITY COLLEGE 1,315 LEITH': 'G60X',
                'K308 CFC 911 CUMBERLAND STREET,DUNEDIN': 'K308',
                'K427,CFC EAST ABBEY COLLEGE,682 CASTLE STREET,DUNEDIN': 'K427',
                'G608,ST MARGARET\'S COLLEGE,333 LEITH': 'G608',
                'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH': 'G601',
                'ARANA 110 CLYDE STREET,DUNEDIN': 'Arana',
                'AQUINAS 74 GLADSTONE ROAD,DUNEDIN': 'Aquinas'
            }
            
            college_data = df[df['meter_description'].isin(self.buildinglist)].copy()
            college_data['meter_description'] = college_data['meter_description'].map(name_mapping)
            
            year_cols = {
                '2022': [col for col in college_data.columns if '2022' in col],
                '2023': [col for col in college_data.columns if '2023' in col],
                '2024': [col for col in college_data.columns if '2024' in col]
            }
            
            yearly_data = []
            for building in self.buildinglist:
                building_data = {
                    'name': name_mapping[building],
                    '2022': round(college_data[college_data['meter_description'] == name_mapping[building]][year_cols['2022']].sum().sum(), 2),
                    '2023': round(college_data[college_data['meter_description'] == name_mapping[building]][year_cols['2023']].sum().sum(), 2),
                    '2024': round(college_data[college_data['meter_description'] == name_mapping[building]][year_cols['2024']].sum().sum(), 2)
                }
                yearly_data.append(building_data)
            
            return yearly_data
            
        except Exception as e:
            logger.exception("Error in college yearly analysis")
            raise