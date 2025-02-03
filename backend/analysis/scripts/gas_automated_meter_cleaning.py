# backend/analysis/scripts/gas_automated_meter_cleaning.py

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import logging
from decouple import config, Config, RepositoryEnv
import os
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Create database connection using environment variables"""
    try:
        # Load environment variables
        current_dir = Path(os.getcwd())
        env_path = current_dir.parents[1] / '.env'
        config = Config(RepositoryEnv(env_path))
        
        # Create database URL
        db_url = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
        
        # Create engine
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return engine
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def load_meter_data(engine):
    """Load automated meter data from database"""
    try:
        query = """
            SELECT meter_description,
                   "Jan_2022", "Feb_2022", "Mar_2022", "Apr_2022", "May_2022", "Jun_2022",
                   "Jul_2022", "Aug_2022", "Sep_2022", "Oct_2022", "Nov_2022", "Dec_2022",
                   "Jan_2023", "Feb_2023", "Mar_2023", "Apr_2023", "May_2023", "Jun_2023",
                   "Jul_2023", "Aug_2023", "Sep_2023", "Oct_2023", "Nov_2023", "Dec_2023",
                   "Jan_2024", "Feb_2024", "Mar_2024", "Apr_2024", "May_2024", "Jun_2024",
                   "Jul_2024", "Aug_2024", "Sep_2024", "Oct_2024", "Nov_2024"
            FROM dbo.gas_automated_meter
        """
        df = pd.read_sql(query, engine)
        logger.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def analyze_data_quality(df, stage=""):
    """Analyze data quality metrics"""
    try:
        numeric_cols = df.columns.difference(['meter_description'])
        
        quality_stats = {
            'missing_percentage': (df[numeric_cols].isnull().sum() / len(df) * 100).round(2),
            'zero_percentage': ((df[numeric_cols] == 0).sum() / len(df) * 100).round(2)
        }
        
        logger.info(f"\n{stage} Data Analysis:")
        logger.info(f"Missing Values Percentage:\n{quality_stats['missing_percentage']}")
        logger.info(f"\nZero Values Percentage:\n{quality_stats['zero_percentage']}")
        
        return quality_stats
    except Exception as e:
        logger.error(f"Error analyzing data quality: {e}")
        raise

def preprocess_meter_readings(df):
    """Preprocess meter readings"""
    try:
        df_processed = df.copy()
        value_columns = df_processed.columns.difference(['meter_description'])
        
        # Convert to numeric and handle NULL values
        for col in value_columns:
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
        
        # Replace zeros with NaN
        df_processed[value_columns] = df_processed[value_columns].replace([0, 'NULL', None], np.nan)
        
        # Round values
        df_processed[value_columns] = df_processed[value_columns].round(2)
        
        logger.info("Zero, NULL values converted to NaN and numbers rounded")
        return df_processed
    except Exception as e:
        logger.error(f"Error preprocessing meter readings: {e}")
        raise

def handle_missing_values(df):
    """Handle missing values with multiple methods"""
    try:
        df_imputed = df.copy()
        value_columns = df_imputed.columns.difference(['meter_description'])
        
        for col in value_columns:
            # Calculate meter-specific statistics
            meter_stats = df_imputed.groupby('meter_description')[col].agg(['mean', 'std']).round(2)
            meter_stats['std'] = meter_stats['std'].fillna(0)
            
            # Forward and backward fill within meter groups
            df_imputed[col] = df_imputed.groupby('meter_description')[col].ffill()
            df_imputed[col] = df_imputed.groupby('meter_description')[col].bfill()
            
            # Handle remaining missing values with seasonal patterns
            if '_' in col:
                month = col.split('_')[0]
                year_cols = [c for c in value_columns if c.startswith(month)]
                seasonal_mean = df_imputed[year_cols].mean(axis=1).round(2)
                df_imputed[col] = df_imputed[col].fillna(seasonal_mean)
            
            # Set remaining nulls to 0
            df_imputed[col] = df_imputed[col].fillna(0)
            
        logger.info("Missing values handled successfully")
        return df_imputed
    except Exception as e:
        logger.error(f"Error handling missing values: {e}")
        raise

def save_cleaned_data(df, engine):
    """Save cleaned data to database"""
    try:
        # Drop existing table if exists
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS dbo.gas_automated_meter_cleaned"))
            conn.commit()
        
        # Save cleaned data
        df.to_sql('gas_automated_meter_cleaned', engine, schema='dbo', if_exists='replace', index=False)
        logger.info("Data saved successfully to gas_automated_meter_cleaned")
    except Exception as e:
        logger.error(f"Error saving cleaned data: {e}")
        raise

def main():
    try:
        # Connect to database
        engine = get_db_connection()
        
        # Load data
        df = load_meter_data(engine)
        
        # Initial analysis
        analyze_data_quality(df, "Initial")
        
        # Preprocess data
        df_processed = preprocess_meter_readings(df)
        
        # Handle missing values
        df_cleaned = handle_missing_values(df_processed)
        
        # Final analysis
        analyze_data_quality(df_cleaned, "Final")
        
        # Save cleaned data
        save_cleaned_data(df_cleaned, engine)
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()
