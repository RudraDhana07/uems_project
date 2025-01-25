import React, { useState, useEffect } from 'react';
import { Tabs, Tab, CircularProgress } from '@mui/material';
import GasCollegesChart from '../visualizations/GasCollegesChart';
import GasDNCollegesChart from '../visualizations/GasDNCollegesChart';
import GasAnalysisView from './GasAnalysisView';


interface DataRow {
  meter_description?: string;
  object_description?: string;
  [key: string]: string | number | null | undefined;
}

interface DataTableProps {
  data: DataRow[];
  title: string;
  isLoading: boolean;
  tableType: 'automated' | 'manual' | 'consumption';  
}

const HIGHLIGHTED_METERS = [
  'G608,ST MARGARET\'S COLLEGE,333 LEITH',
  'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH',
  'ARANA 110 CLYDE STREET,DUNEDIN',
  'ECCLES GREAT KING STREET,UNIVERSITY OF',
  'AQUINAS 74 GLADSTONE ROAD,DUNEDIN',
  'K427,CFC EAST ABBEY COLLEGE,682 CASTLE STREET,DUNEDIN',
  'G412,SCIENCE 2 BOILER HOUSE,72 UNION PLACE'
];

const HIGHLIGHTED_CONSUMPTION = [
  ' Total Gas Energy - DN',
  'Total Gas Energy - Colleges'
];

const tableStyles = {
    container: {
      margin: '20px',
      overflowX: 'auto' as const,
      backgroundColor: '#fff',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse' as const,
      border: '1px solid #ddd',
      marginBottom: '8px',
    },
    tr: {
      backgroundColor: 'inherit'
    },
    th: {
      backgroundColor: '#e6f3ff',
      padding: '12px 8px',
      border: '1px solid #ddd',
      position: 'sticky' as const,
      top: 0,
      whiteSpace: 'nowrap' as const,
      color: '#333',
      fontWeight: 'bold',
      textAlign: 'left' as const,
      fontSize: '0.8em'
    },
    td: {
      padding: '8px',
      border: '1px solid #ddd',
      whiteSpace: 'nowrap' as const,
      fontSize: '0.8em'
    },
    tabPanel: {
      padding: '20px',
      backgroundColor: '#fff',
    },
    searchBox: {
      width: '60%',
      padding: '8px',
      marginBottom: '15px',
      marginLeft: '15px',
      border: '1px solid #ddd',
      borderRadius: '4px',
      fontSize: '14px'
    },
    analysisContainer: {
      padding: '20px',
      display: 'grid',
      gap: '20px',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))'
    },
    chartSection: {
      backgroundColor: '#fff',
      padding: '15px',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    },
    chartsContainer: {
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '20px',
        marginBottom: '20px',
        padding: '15px',
        backgroundColor: '#fff',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }

  };


  const getOrderedColumns = (data: DataRow[], tableType: 'automated' | 'manual' | 'consumption'): string[] => {
    if (!data.length) return [];
    
  /// Define column order based on model structure with proper typing
  const baseColumns: Record<'automated' | 'manual' | 'consumption', string[]> = {
    'automated': ['meter_description', 'icp'],
    'manual': ['meter_description', 'misc1', 'misc2'],
    'consumption': ['object_description', 'misc']
  };
  
  // Get monthly columns in order
  const years = ['2022', '2023', '2024', '2025'];
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    const monthlyColumns = years.flatMap(year => 
      months.map(month => `${month}_${year}`)
    );
    
    return [...baseColumns[tableType], ...monthlyColumns];
  }; 

  const GasDataTable: React.FC<DataTableProps> = ({ data, title, isLoading, tableType }) => {
    if (isLoading) {
      return <CircularProgress />;
    }
  
    if (!data || data.length === 0) {
      return <div>No data available</div>;
    }

    type Column = string;
  
    const columns: Column[] = Object.keys(data[0] || {});

    const orderedColumns = getOrderedColumns(data, tableType);

 
  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'number') {
      return value.toFixed(2).replace(/\.?0+$/, '');
    }
    return value.toString();
  };

  const getRowStyle = (row: DataRow) => {
    if (tableType === 'automated' && row.meter_description) {
      return HIGHLIGHTED_METERS.includes(row.meter_description) ? 
        { ...tableStyles.tr, backgroundColor: '#FFE9A8' } : 
        tableStyles.tr;
    }
    
    if (tableType === 'consumption' && row.object_description) {
      return HIGHLIGHTED_CONSUMPTION.includes(row.object_description) ? 
        { ...tableStyles.tr, backgroundColor: '#FFE9A8' } : 
        tableStyles.tr;
    }
    
    return tableStyles.tr;
  };

  return (
    <div>
      <h2>{title}</h2>
      <table style={tableStyles.table}>
        <thead>
          <tr>
            {columns.map((column: Column) => (
              <th key={column} style={tableStyles.th}>
                {column.replace(/_/g, ' ')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
        {data.map((row: DataRow, index: number) => (
            <tr key={index} style={getRowStyle(row)}>
              {orderedColumns.map((column: string) => (
                <td key={column} style={tableStyles.td}>
                  {formatValue(row[column])}
                  </td>
                ))}
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

const GasDataView: React.FC = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [automatedData, setAutomatedData] = useState<DataRow[]>([]);
    const [manualData, setManualData] = useState<DataRow[]>([]);
    const [consumptionData, setConsumptionData] = useState<DataRow[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [analysisData, setAnalysisData] = useState<any>(null);
    const [searchTerms, setSearchTerms] = useState({
      automated: '',
      manual: '',
      consumption: ''
    });

    useEffect(() => {
      const fetchData = async () => {
        try {
          setIsLoading(true);
          const baseUrl = 'http://127.0.0.1:5001';
          
          const responses = await Promise.all([
            fetch(`${baseUrl}/api/gas/automated`),
            fetch(`${baseUrl}/api/gas/manual`),
            fetch(`${baseUrl}/api/gas/consumption`),
            fetch(`${baseUrl}/api/gas/analysis`)
          ].map(async (request) => {
            const response = await request;
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          }));
    
          const [automated, manual, consumption, analysis] = responses;
          
          setAutomatedData(automated || []);
          setManualData(manual || []);
          setConsumptionData(consumption || []);
          setAnalysisData(analysis || null);
        } catch (error) {
          console.error('Error fetching data:', error);
          // Set empty defaults
          setAutomatedData([]);
          setManualData([]);
          setConsumptionData([]);
          setAnalysisData(null);
        } finally {
          setIsLoading(false);
        }
      };
    
      fetchData();
    }, []);

    useEffect(() => {
      console.log('Analysis Data:', analysisData);
      console.log('Loading State:', isLoading);
    }, [analysisData, isLoading]);

  const filterData = (data: DataRow[], searchTerm: string, field: string) => {
    if (!searchTerm) return data;
    return data.filter(row =>
      String(row[field] || '').toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  return (
    <div style={tableStyles.container}>
      <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
        <Tab label="Automated Meters" />
        <Tab label="Manual Meters" />
        <Tab label="Consumption Data" />
        <Tab label="Data Insight and Analysis" />
      </Tabs>

      {activeTab === 0 && (
        <div style={tableStyles.tabPanel}>
          
          <div style={tableStyles.chartsContainer}>
            <GasCollegesChart 
              data={automatedData} 
            />
            <GasDNCollegesChart 
              automatedData={automatedData}
              consumptionData={consumptionData}
            />
          </div>
          
          <input
            type="text"
            placeholder="Search automated meters..."
            value={searchTerms.automated}
            onChange={(e) => setSearchTerms({...searchTerms, automated: e.target.value})}
            style={tableStyles.searchBox}
          />

          <GasDataTable
                data={filterData(automatedData, searchTerms.automated, 'meter_description')}
                title="Automated Meters"
                isLoading={isLoading}
                tableType="automated"
          />
          
        </div>
      )}

      {activeTab === 1 && (
        <div style={tableStyles.tabPanel}>
          <input
            type="text"
            placeholder="Search manual meters..."
            value={searchTerms.manual}
            onChange={(e) => setSearchTerms({...searchTerms, manual: e.target.value})}
            style={tableStyles.searchBox}
          />
          <GasDataTable
            data={filterData(manualData, searchTerms.manual, 'meter_description')}
            title="Manual Meters"
            isLoading={isLoading}
            tableType="manual"
          />
        </div>
      )}

      {activeTab === 2 && (
        <div style={tableStyles.tabPanel}>
          <input
            type="text"
            placeholder="Search consumption data..."
            value={searchTerms.consumption}
            onChange={(e) => setSearchTerms({...searchTerms, consumption: e.target.value})}
            style={tableStyles.searchBox}
          />
          <GasDataTable
            data={filterData(consumptionData, searchTerms.consumption, 'object_description')}
            title="Consumption Data"
            isLoading={isLoading}
            tableType="consumption"
          />
        </div>
      )}

        {activeTab === 3 && (
                <div style={tableStyles.tabPanel}>
                    <GasAnalysisView 
                        data={analysisData} 
                        isLoading={isLoading}
                    />
                </div>
        )}
    </div>
  );
};

export default GasDataView;
