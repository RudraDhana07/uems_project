import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import logging
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA

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

def load_cleaned_data(engine):
    query = "SELECT * FROM dbo.gas_automated_meter_cleaned"
    return pd.read_sql(query, engine)

def prepare_data(df):
    numeric_cols = df.columns.difference(['meter_description'])
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df

df = load_cleaned_data(engine)
df = prepare_data(df)

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
    
    
    # Perform K-means clustering with optimal k
    optimal_k = 3  # Can be adjusted based on elbow curve
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
    plt.show()
    
    # Hierarchical clustering visualization
    linkage_matrix = linkage(scaled_data, method='ward')
    plt.figure(figsize=(15, 10))
    dendrogram(linkage_matrix, labels=consumption_patterns.index, leaf_rotation=90)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Meter Description')
    plt.ylabel('Distance')
    plt.tight_layout()
    plt.show()
    
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
    plt.show()

# Call the function
try:
    perform_clustering_analysis(df)
except Exception as e:
    print(f"Error occurred: {str(e)}")