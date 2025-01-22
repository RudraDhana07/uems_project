from flask import jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import logging
from sklearn.metrics import silhouette_score
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import logging
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
import io
import base64
from .. import db
import logging


bp = Blueprint('gas', __name__, url_prefix='/api/gas/analysis')

@app.route('/api/gas/analysis', methods=['GET'])


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def connect_to_database(db_url):
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return engine
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return None

engine = connect_to_database(db_url)


def create_plot_image(plt):
    """Helper function to convert matplotlib plot to base64 string"""
    # Save plot to a temporary buffer.
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    plt.close()  # Clear the current figure
    
    # Encode the image to base64 string
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64

def load_cleaned_data(engine):
    query = "SELECT * FROM dbo.gas_automated_meter_cleaned"
    return pd.read_sql(query, engine)

def prepare_data(df):
    numeric_cols = df.columns.difference(['meter_description'])
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df

df = load_cleaned_data(engine)
df = prepare_data(df)

def plot_monthly_trends(df):
    monthly_avg = df.iloc[:, 1:].mean()
    plt.figure(figsize=(15, 6))
    monthly_avg.plot(kind='line', marker='o')
    plt.title('Monthly Gas Consumption Trend')
    plt.xlabel('Month')
    plt.ylabel('Average Consumption')

    # Create labels for every 3 months across multiple years
    all_months = []
    for year in range(2022, 2025):
        for month in ['Jan', 'Apr', 'Jul', 'Oct']:
            all_months.append(f'{month}\n{year}')
    
    # Get positions for the labels (every 3 months)
    positions = range(0, len(monthly_avg), 3)
    # Use only the labels we need (up to Nov 2024)
    labels = all_months[:len(positions)]
    
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    gas_monthly_trends = create_plot_image(plt) = create_plot_image(plt)

    return gas_monthly_trends

def perform_clustering_analysis(df):
    # Create mapping dictionary for shorter names
    name_mapping = {
        'F512,INFORMATION TECHNOLOGY BLDG,270 LEITH': 'F512',
        'G60X,UNIVERSITY COLLEGE 1,315 LEITH': 'G60X',
        'K308 CFC 911 CUMBERLAND STREET,DUNEDIN': 'K308',
        'K427,CFC EAST ABBEY COLLEGE,682 CASTLE STREET,DUNEDIN': 'K427',
        'D206, MEDICAL SCHOOL (HERCUS) HANOVER': 'D206',
        'G404,CAMPUS (MICROBIOLOGY),720 CUMBERLAND': 'G404',
        'F940 PLAZA BUILDING,132 ANZAC AVENUE,FORSYTH': 'F940',
        'F603,PROPERTY SERVICES BLDG,111 ALBANY': 'F603',
        'F62X,PSYCHOLOGY (WILLIAM JAMES BLDG),275': 'F62X',
        'G412,SCIENCE 2 BOILER HOUSE,72 UNION PLACE': 'G412',
        'F405,SMITHELL\'S GYMNASIUM,690 CUMBERLAND': 'F405',
        'G608,ST MARGARET\'S COLLEGE,333 LEITH': 'G608',
        'F916,COLLEGE OF EDUCATION BOILER HOUSE,151': 'F916',
        'F402,UNIVERSITY UNION BUILDING,660': 'F402',
        'E902,HOCKEN LIBRARY,90 ANZAC AVENUE,DUNEDIN': 'E902',
        'F516/17,HUMANITIES,97-99/ALBANY': 'F516/17',
        'F204,IT DEPT,444 GREAT KING STREET,DUNEDIN': 'F204',
        'E208/12,ZOOLOGY (BENHAM BLDG),346 GREAT KING': 'E208',
        'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH': 'G601',
        'E213,PARKER BUILDING,344 GREAT KING': 'E213',
        'ARANA 110 CLYDE STREET,DUNEDIN': 'ARANA',
        'DENTAL 310 GREAT KING STREET,DUNEDIN NORTH,DUNEDIN': 'DENTAL',
        'ECCLES GREAT KING STREET,UNIVERSITY OF': 'ECCLES',
        'MARSH STUDY CENTRE,CASTLE STREET,DUNEDIN': 'MARSH',
        'CHILDCARE CENTRE,563 CASTLE STREET,DUNEDIN': 'CHILDCARE',
        'PHYSIO BUILDING, 325 GREAT KING ST': 'PHYSIO',
        'AQUINAS 74 GLADSTONE ROAD,DUNEDIN': 'AQUINAS',
        '56A TE AWE AWE STREET,HOKOWHITU,PALMERSTON NORTH': '56A'
    }

    # Create a copy of the dataframe with simplified names
    df_simplified = df.copy()
    df_simplified['meter_description'] = df_simplified['meter_description'].map(name_mapping)
    
    # Continue with the rest of the clustering analysis using df_simplified
    consumption_patterns = df_simplified.set_index('meter_description')
    
    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(consumption_patterns)
    
    # Determine optimal number of clusters using elbow method
    inertias = []
    silhouette_scores = []
    K = range(2, 6)
    
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled_data)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(scaled_data, kmeans.labels_))
    
    # Plot elbow curve
    '''plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(K, inertias, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    
    # Plot silhouette scores
    plt.subplot(1, 2, 2)
    plt.plot(K, silhouette_scores, 'rx-')
    plt.xlabel('k')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score vs k')
    plt.tight_layout()
    plt.show()
    '''
    
    # Perform K-means clustering with optimal k
    optimal_k = 3  
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    
    # Add cluster labels to original data
    consumption_patterns['Cluster'] = clusters
    
    # Perform PCA for visualization
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)
    
    # Plot clustering results using PCA
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], 
                         c=clusters, cmap='viridis')
    plt.title('Meter Clusters based on Consumption Patterns')
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')

    # Add meter descriptions as annotations
    for i, meter in enumerate(consumption_patterns.index):
        plt.annotate(meter, (pca_result[i, 0], pca_result[i, 1]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.colorbar(scatter, label='Cluster')
    plt.tight_layout()
    
    gas_clustering_analysis = create_plot_image(plt) = create_plot_image(plt)

    #return gas_clustering_analysis
    
    
    '''# Hierarchical clustering visualization
    linkage_matrix = linkage(scaled_data, method='ward')
    plt.figure(figsize=(15, 10))
    dendrogram(linkage_matrix, labels=consumption_patterns.index, leaf_rotation=90)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Meter Description')
    plt.ylabel('Distance')
    plt.tight_layout()
    plt.show()
    '''
    # Calculate and display cluster characteristics
    cluster_stats = pd.DataFrame()
    print("\nDetailed Cluster Memberships:")
    print("=" * 50)
    for i in range(optimal_k):
        cluster_meters = consumption_patterns[consumption_patterns['Cluster'] == i]
        print(f"\nCluster {i} Members:")
        print("-" * 30)
        for meter in cluster_meters.index:
            print(f"- {meter}")
        print(f"Total members in Cluster {i}: {len(cluster_meters)}")
        print("=" * 50)
    
    # Calculate average consumption patterns for each cluster
    plt.figure(figsize=(15, 6))
    for i in range(optimal_k):
        cluster_data = consumption_patterns[consumption_patterns['Cluster'] == i]
        mean_pattern = cluster_data.drop('Cluster', axis=1).mean()
        plt.plot(mean_pattern.index, mean_pattern.values, 
                label=f'Cluster {i}', marker='o')
    
    plt.title('Average Consumption Patterns by Cluster')
    plt.xlabel('Month')
    plt.ylabel('Average Consumption')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    Avg_gas_consumption = create_plot_image(plt)

    #return gas_clustering_analysis

def analyze_significant_anomalies(df, threshold_percentage=50):
    """
    Analyze and display only buildings with significant consumption changes
    threshold_percentage: percentage change to consider as anomaly (default 50%)
    """
    # Create yearly averages for each meter
    yearly_data = df.melt(
        id_vars=['meter_description'],
        var_name='Month_Year',
        value_name='Consumption'
    )
    
    # Extract year from Month_Year column
    yearly_data['Year'] = yearly_data['Month_Year'].apply(lambda x: x.split('_')[1])
    
    # Calculate yearly statistics
    yearly_stats = yearly_data.groupby(['meter_description', 'Year'])['Consumption'].agg([
        'mean', 'std', 'min', 'max'
    ]).reset_index()
    
    # Function to calculate percentage change and identify anomalies
    def identify_anomalies(group):
        # Calculate percentage change from previous year
        group = group.sort_values('Year')
        group['pct_change'] = group['mean'].pct_change() * 100
        
        # Calculate overall statistics
        mean_consumption = group['mean'].mean()
        
        # Identify years with significant changes
        significant_changes = abs(group['pct_change']) > threshold_percentage
        
        # Also check for absolute deviation from mean
        absolute_deviation = abs((group['mean'] - mean_consumption) / mean_consumption * 100)
        significant_deviation = absolute_deviation > threshold_percentage
        
        return group[significant_changes | significant_deviation]
    
    # Identify buildings with anomalies
    anomalies_by_building = {}
    for meter in yearly_stats['meter_description'].unique():
        meter_data = yearly_stats[yearly_stats['meter_description'] == meter]
        anomalies = identify_anomalies(meter_data)
        if not anomalies.empty:
            anomalies_by_building[meter] = anomalies
    
    if not anomalies_by_building:
        print(f"No buildings found with consumption changes greater than {threshold_percentage}%")
        return
    
    # Print and plot only buildings with anomalies
    print(f"\nBuildings with Significant Consumption Changes (>{threshold_percentage}%):")
    print("=" * 80)
    
    for meter, anomaly_data in anomalies_by_building.items():
        print(f"\n{meter}")
        print("-" * 50)
        
        # Get full data for plotting
        full_meter_data = yearly_stats[yearly_stats['meter_description'] == meter]
        
        # Print statistical summary
        summary_table = pd.DataFrame({
            'Year': full_meter_data['Year'],
            'Mean Consumption': full_meter_data['mean'].round(2),
            'Percentage Change': full_meter_data['mean'].pct_change() * 100
        }).fillna('-')
        print(summary_table.to_string(index=False))
        
        '''# Plotting
        plt.figure(figsize=(12, 6))
        
        # Plot all years
         plt.plot(full_meter_data['Year'], full_meter_data['mean'], 
                marker='o', label='Yearly Average', color='blue')
        
        # Highlight anomaly years
         plt.scatter(anomaly_data['Year'], anomaly_data['mean'],
                   color='red', s=100, label='Anomaly')
        
        # Add error bands
         plt.fill_between(full_meter_data['Year'], 
                        full_meter_data['mean'] - full_meter_data['std'],
                        full_meter_data['mean'] + full_meter_data['std'],
                        alpha=0.2, color='blue')
        
         plt.title(f'Consumption Pattern with Anomalies: {meter}')
         plt.xlabel('Year')
         plt.ylabel('Average Consumption')
         plt.legend()
         plt.grid(True)
         plt.xticks(rotation=45)
         plt.tight_layout()
         plt.show()
        '''

        # print("\nDetailed Anomaly Information:")
        for _, row in anomaly_data.iterrows():
            pct_change = row['pct_change'] if not pd.isna(row['pct_change']) else 'Initial Year'
            if isinstance(pct_change, str):
                print(f"Year {row['Year']}: Mean Consumption = {row['mean']:.2f}")
            else:
                print(f"Year {row['Year']}: Mean Consumption = {row['mean']:.2f} " +
                      f"(Change: {pct_change:.1f}%)")
        print("=" * 80)

# Call the function with desired threshold
analyze_significant_anomalies(df, threshold_percentage=50)

def plot_high_gas_trends(df, buildinglist):
    # Filter data for colleges and create a copy
    college_data = df[df['meter_description'].isin(buildinglist)].copy()
    
    # Create mapping for shorter names
    name_mapping = {
        'ECCLES GREAT KING STREET,UNIVERSITY OF':'ECCLES',
        'F940 PLAZA BUILDING,132 ANZAC AVENUE,FORSYTH':'F940'
    }
    
    # Replace long names with short names
    college_data['meter_description'] = college_data['meter_description'].map(name_mapping)
    
    # Melt the dataframe to convert from wide to long format
    melted_data = pd.melt(college_data, 
                         id_vars=['meter_description'],
                         var_name='date',
                         value_name='consumption')
    
    # Convert date column to datetime
    #melted_data['date'] = pd.to_datetime(melted_data['date'], format='%b_%Y')
    
    # Create line plot
    plt.figure(figsize=(15, 8))
    sns.lineplot(data=melted_data, 
                x='date',
                y='consumption',
                hue='meter_description'#, 
                #marker='o',
                #markersize=8
                )
    
    plt.title('ECCLES and F940 University Plaza Consumption Trends (2022-2024)', fontsize=12, pad=15)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Gas Energy Consumption', fontsize=10)
    plt.xticks(rotation=45)
    plt.legend(title='Building')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    high_gas_consumption = create_plot_image(plt)

    #return high_gas_consumption

# Define buildinglist
buildinglist = [
    'ECCLES GREAT KING STREET,UNIVERSITY OF',
    'F940 PLAZA BUILDING,132 ANZAC AVENUE,FORSYTH'
]

# Call the function
plot_high_gas_trends(df, buildinglist)


def plot_college_yearly_analysis(df, buildinglist):
    # Filter data for colleges and create a copy
    college_data = df[df['meter_description'].isin(buildinglist)].copy()
    
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
    
    # Replace long names with short names
    college_data['meter_description'] = college_data['meter_description'].map(name_mapping)
    
    # Create year columns for grouping
    year_cols = {
        '2022': [col for col in college_data.columns if '2022' in col],
        '2023': [col for col in college_data.columns if '2023' in col],
        '2024': [col for col in college_data.columns if '2024' in col]
    }
    
    # Calculate yearly sums for each building
    yearly_sums = pd.DataFrame()
    for year, cols in year_cols.items():
        yearly_sums[year] = college_data.groupby('meter_description')[cols].sum().sum(axis=1)
    
    # Calculate percentages
    yearly_percentages = yearly_sums.div(yearly_sums.sum()) * 100

    colors = ['#4394E5', '#87BB62', '#876FD4'] 
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Plot 1: Yearly Total Consumption
    yearly_sums.plot(kind='bar', ax=ax1, color=colors)
    ax1.set_title('Yearly Total Gas Consumption by College')
    ax1.set_xlabel('College')
    ax1.set_ylabel('Total Consumption')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.0f', padding=3)

    # Plot 2: Percentage Contribution
    yearly_percentages.plot(kind='bar', ax=ax2, color=colors)
    ax2.set_title('Percentage Contribution to Total Gas Consumption')
    ax2.set_xlabel('College')
    ax2.set_ylabel('Percentage (%)')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add percentage labels on bars
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.1f%%', padding=3)
    
    plt.tight_layout()
    college_gas_consumption = create_plot_image(plt)

    #return college_gas_consumption
    
    # Print detailed summary
    '''print("\nYearly Consumption Summary:")
    print(yearly_sums.round(2))
    print("\nPercentage Contribution Summary:")
    print(yearly_percentages.round(2))
    '''
    
# Define buildinglist
buildinglist = [
    'G60X,UNIVERSITY COLLEGE 1,315 LEITH',
    'K308 CFC 911 CUMBERLAND STREET,DUNEDIN',
    'K427,CFC EAST ABBEY COLLEGE,682 CASTLE STREET,DUNEDIN',
    'G608,ST MARGARET\'S COLLEGE,333 LEITH',
    'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH',
    'ARANA 110 CLYDE STREET,DUNEDIN',
    'AQUINAS 74 GLADSTONE ROAD,DUNEDIN'
]
# Call the function
plot_college_yearly_analysis(df, buildinglist)

def plot_dn_yearly_analysis(df, buildinglist_DN):
    # Filter data for colleges and create a copy
    college_data = df[df['meter_description'].isin(buildinglist_DN)].copy()
    
    # Create mapping for shorter names
    name_mapping = {
        'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH': 'G601',
        'E213,PARKER BUILDING,344 GREAT KING':'E213',
        'ARANA 110 CLYDE STREET,DUNEDIN':'ARANA',
        'DENTAL 310 GREAT KING STREET,DUNEDIN NORTH,DUNEDIN':'DENTAL',
        'ECCLES GREAT KING STREET,UNIVERSITY OF':'ECCLES',
        'MARSH STUDY CENTRE,CASTLE STREET,DUNEDIN':'MARSH',
        'CHILDCARE CENTRE,563 CASTLE STREET,DUNEDIN':'CHILDCARE',
        'PHYSIO BUILDING, 325 GREAT KING ST':'PHYSIO',
        'AQUINAS 74 GLADSTONE ROAD,DUNEDIN':'AQUINAS',
        '56A TE AWE AWE STREET,HOKOWHITU,PALMERSTON NORTH':'56A'
    }
    
    # Replace long names with short names
    college_data['meter_description'] = college_data['meter_description'].map(name_mapping)
    
    # Create year columns for grouping
    year_cols = {
        '2022': [col for col in college_data.columns if '2022' in col],
        '2023': [col for col in college_data.columns if '2023' in col],
        '2024': [col for col in college_data.columns if '2024' in col]
    }
    
    # Calculate yearly sums for each building
    yearly_sums = pd.DataFrame()
    for year, cols in year_cols.items():
        yearly_sums[year] = college_data.groupby('meter_description')[cols].sum().sum(axis=1)
    
    # Calculate percentages
    yearly_percentages = yearly_sums.div(yearly_sums.sum()) * 100

    colors = ['#115f9a', '#22a7f0', '#a6d75b'] 
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(20, 8), height_ratios=[1, 1])
    
    '''# Plot 1: Yearly Total Consumption
    yearly_sums.plot(kind='bar', ax=ax1, color=colors)
    ax1.set_title('Yearly Total Gas Consumption by DN')
    ax1.set_xlabel('DN')
    ax1.set_ylabel('Total Consumption')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.0f', padding=3)
    '''
    # Plot 2: Percentage Contribution
    yearly_percentages.plot(kind='bar', ax=ax2, color=colors)
    ax2.set_title('Percentage Contribution to Total Gas Consumption DN')
    ax2.set_xlabel('DN')
    ax2.set_ylabel('Percentage (%)')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add percentage labels on bars
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.1f%%', padding=3)
    
    plt.tight_layout()
    #plt.show()
    
    # Print detailed summary
    #print("\nYearly Consumption Summary:")
    #print(yearly_sums.round(2))
    print("\nPercentage Contribution Summary:")
    print(yearly_percentages.round(2))

    DN_gas_consumption = create_plot_image(plt)

    #return DN_gas_consumption


# Define buildinglist_DN
buildinglist_DN = [
'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH',
'E213,PARKER BUILDING,344 GREAT KING',
'ARANA 110 CLYDE STREET,DUNEDIN',
'DENTAL 310 GREAT KING STREET,DUNEDIN NORTH,DUNEDIN',
'ECCLES GREAT KING STREET,UNIVERSITY OF',
'MARSH STUDY CENTRE,CASTLE STREET,DUNEDIN',
'CHILDCARE CENTRE,563 CASTLE STREET,DUNEDIN',
'PHYSIO BUILDING, 325 GREAT KING ST',
'AQUINAS 74 GLADSTONE ROAD,DUNEDIN',
'56A TE AWE AWE STREET,HOKOWHITU,PALMERSTON NORTH'
]
# Call the function
plot_dn_yearly_analysis(df, buildinglist_DN)


def plot_anomaly_bars(df, anomaly_buildings):
    # Create dictionary for simplified names
    name_mapping = {
        'CHILDCARE CENTRE,563 CASTLE STREET,DUNEDIN': 'CHILDCARE',
        'DENTAL 310 GREAT KING STREET,DUNEDIN NORTH,DUNEDIN': 'DENTAL',
        'F402,UNIVERSITY UNION BUILDING,660': 'F402',
        'F62X,PSYCHOLOGY (WILLIAM JAMES BLDG),275': 'F62X',
        'F916,COLLEGE OF EDUCATION BOILER HOUSE,151': 'F916',
        'G412,SCIENCE 2 BOILER HOUSE,72 UNION PLACE': 'G412',
        'G608,ST MARGARET\'S COLLEGE,333 LEITH': 'G608',
        'G60X,UNIVERSITY COLLEGE 1,315 LEITH': 'G60X',
        'MARSH STUDY CENTRE,CASTLE STREET,DUNEDIN': 'MARSH'
    }
    
    # Prepare data
    yearly_data = df[df['meter_description'].isin(anomaly_buildings)].melt(
        id_vars=['meter_description'],
        var_name='Month_Year',
        value_name='Consumption'
    )
    
    # Extract year and simplify names
    yearly_data['Year'] = yearly_data['Month_Year'].apply(lambda x: x.split('_')[1])
    yearly_data['Simple_Name'] = yearly_data['meter_description'].map(name_mapping)
    
    # Calculate yearly averages
    yearly_avg = yearly_data.groupby(['Simple_Name', 'Year'])['Consumption'].mean().reset_index()
    
    # Create figure
    plt.figure(figsize=(15, 8))
    
    # Set width of bars and positions of the bars
    barWidth = 0.25
    
    # Set position of bar on X axis
    buildings = sorted(yearly_avg['Simple_Name'].unique())
    r1 = np.arange(len(buildings))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    
    # Create bars with borders
    colors = {
        '2022': {'fill': '#4169E1', 'edge': '#2B4595'},  # Royal Blue with darker edge
        '2023': {'fill': '#228B22', 'edge': '#165916'},  # Forest Green with darker edge
        '2024': {'fill': '#FF4500', 'edge': '#B33000'}   # Orange Red with darker edge
    }
    
    for i, year in enumerate(['2022', '2023', '2024']):
        year_data = yearly_avg[yearly_avg['Year'] == year]
        year_values = [year_data[year_data['Simple_Name'] == building]['Consumption'].values[0] 
                      if len(year_data[year_data['Simple_Name'] == building]) > 0 
                      else 0 
                      for building in buildings]
        
        positions = [r1, r2, r3][i]
        plt.bar(positions, year_values, width=barWidth, label=f'Year {year}', 
                color=colors[year]['fill'], 
                edgecolor=colors[year]['edge'],  # Add border color
                linewidth=1.5,                   # Border width
                alpha=0.7)
    
    # Add labels and customize the plot
    plt.xlabel('Building', fontsize=12, labelpad=15)
    plt.ylabel('Average Yearly Consumption', fontsize=12)
    plt.title('Yearly Consumption Patterns for Buildings (2022-2024) with Change > 50%', 
              fontsize=14, pad=20)
    
    # Add xticks on the middle of the group bars
    plt.xticks([r + barWidth for r in range(len(buildings))], 
               buildings, rotation=45, ha='right')
    
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.3, axis='y')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return create_plot_image(plt)

# Define the buildings list
anomaly_buildings = [
    'CHILDCARE CENTRE,563 CASTLE STREET,DUNEDIN',
    'DENTAL 310 GREAT KING STREET,DUNEDIN NORTH,DUNEDIN',
    'F402,UNIVERSITY UNION BUILDING,660',
    'F62X,PSYCHOLOGY (WILLIAM JAMES BLDG),275',
    'F916,COLLEGE OF EDUCATION BOILER HOUSE,151',
    'G412,SCIENCE 2 BOILER HOUSE,72 UNION PLACE',
    'G608,ST MARGARET\'S COLLEGE,333 LEITH',
    'G60X,UNIVERSITY COLLEGE 1,315 LEITH',
    'MARSH STUDY CENTRE,CASTLE STREET,DUNEDIN'
]

# Call the function and show the plot
plt = plot_anomaly_bars(df, anomaly_buildings)


def get_gas_analysis():
    try:
        # Database connection
        engine = create_engine(db_url)
        
        analysis_results = {
            
        }
        
        return jsonify(analysis_results)
        
    except Exception as e:
        logging.error(f"Error in gas analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500