from flask import Blueprint, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
from sqlalchemy import create_engine
import io
import base64
import logging
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# Create Blueprint
gas_analysis = Blueprint('gas_analysis', __name__)

# Database connection parameters
DB_PARAMS = {
    'host': 'localhost',
    'database': 'uems_db',
    'user': 'admin_uems',
    'password': 'uems2025',
    'port': 5432,
    'schema': 'dbo'
}

db_url = f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['database']}"

def create_plot_image(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


@gas_analysis.route('/api/gas/analysis', methods=['GET'])
def get_gas_analysis():
    try:
        # Database connection
        engine = create_engine(db_url)
        df = pd.read_sql("SELECT * FROM dbo.gas_automated_meter_cleaned", engine)
        
        # Prepare numeric columns
        numeric_cols = df.columns.difference(['meter_description'])
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Generate all analyses
        analysis_results = {
            'monthlyTrends': {
                'plot': plot_monthly_trends(df),
                'description': 'Monthly gas consumption trends across all buildings'
            },
            'clustering': {
                'plot': perform_clustering_analysis(df),
                'description': 'Building clusters based on consumption patterns'
            },
            'anomalies': {
                'data': analyze_significant_anomalies(df),
                'plot': plot_anomaly_bars(df),
                'description': 'Buildings with significant consumption changes'
            },
            'highConsumers': {
                'plot': plot_high_gas_trends(df),
                'description': 'Highest consuming buildings analysis'
            },
            'collegeAnalysis': {
                'plot': plot_college_yearly_analysis(df),
                'description': 'College buildings consumption analysis'
            },
            'dnAnalysis': {
                'plot': plot_dn_yearly_analysis(df),
                'description': 'DN area buildings analysis'
            }
        }
        
        return jsonify(analysis_results)
        
    except Exception as e:
        logging.error(f"Error in gas analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

def plot_monthly_trends(df):
    plt.figure(figsize=(15, 6))
    monthly_avg = df.iloc[:, 1:].mean()
    monthly_avg.plot(kind='line', marker='o')
    plt.title('Monthly Gas Consumption Trend')
    plt.xlabel('Month')
    plt.ylabel('Average Consumption')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    return create_plot_image(plt)

def perform_clustering_analysis(df):
    # Prepare data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df.iloc[:, 1:])
    
    # Perform clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    
    # PCA for visualization
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1],
                         c=clusters, cmap='viridis')
    plt.title('Building Clusters based on Consumption Patterns')
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.colorbar(scatter, label='Cluster')
    plt.tight_layout()
    return create_plot_image(plt)

def analyze_significant_anomalies(df, threshold=50):
    yearly_data = df.melt(id_vars=['meter_description'])
    yearly_data['year'] = yearly_data['variable'].str.split('_').str[1]
    yearly_stats = yearly_data.groupby(['meter_description', 'year'])['value'].agg(['mean', 'std']).reset_index()
    
    # Calculate year-over-year changes
    anomalies = []
    for building in yearly_stats['meter_description'].unique():
        building_data = yearly_stats[yearly_stats['meter_description'] == building].sort_values('year')
        building_data['pct_change'] = building_data['mean'].pct_change() * 100
        significant_changes = building_data[abs(building_data['pct_change']) > threshold]
        if not significant_changes.empty:
            anomalies.append(significant_changes)
    
    return pd.concat(anomalies) if anomalies else pd.DataFrame()

def plot_anomaly_bars(df):
    anomalies = analyze_significant_anomalies(df)
    if anomalies.empty:
        return None
        
    plt.figure(figsize=(15, 8))
    sns.barplot(data=anomalies, x='meter_description', y='pct_change')
    plt.title('Significant Consumption Changes by Building')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return create_plot_image(plt)

def plot_high_gas_trends(df, top_n=5):
    yearly_totals = df.iloc[:, 1:].sum()
    top_buildings = yearly_totals.nlargest(top_n)
    
    plt.figure(figsize=(15, 8))
    top_buildings.plot(kind='bar')
    plt.title(f'Top {top_n} Highest Gas Consuming Buildings')
    plt.xlabel('Building')
    plt.ylabel('Total Consumption')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return create_plot_image(plt)

def plot_college_yearly_analysis(df):
    college_buildings = df[df['meter_description'].str.contains('COLLEGE', case=False)]
    yearly_totals = college_buildings.iloc[:, 1:].sum()
    
    plt.figure(figsize=(15, 8))
    yearly_totals.plot(kind='bar')
    plt.title('College Buildings Yearly Gas Consumption')
    plt.xlabel('Year')
    plt.ylabel('Total Consumption')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return create_plot_image(plt)

def plot_dn_yearly_analysis(df):
    dn_buildings = df[df['meter_description'].str.contains('DN|DUNEDIN', case=False)]
    yearly_totals = dn_buildings.iloc[:, 1:].sum()
    
    plt.figure(figsize=(15, 8))
    yearly_totals.plot(kind='bar')
    plt.title('DN Area Buildings Yearly Gas Consumption')
    plt.xlabel('Year')
    plt.ylabel('Total Consumption')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return create_plot_image(plt)
