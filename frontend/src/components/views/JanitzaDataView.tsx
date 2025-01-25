// src/components/views/JanitzaDataView.tsx
import React, { useState, useEffect } from 'react';
import { Tabs, Tab } from '@mui/material';

interface DataRow {
  meter_location: string;
  [key: string]: string | number | undefined;
}

interface DataTableProps {
  data: DataRow[];
  title: string | React.ReactNode;
  isLoading: boolean;
}

export const tableStyles = {
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
  title: {
    fontSize: '1.2em',
    marginBottom: '15px',
    color: '#333',
    padding: '8px 0',
  },
  tabPanel: {
    padding: '20px',
    backgroundColor: '#fff',
  }
};

const formatNumber = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return '-';
  if (Math.abs(value) < 100) {
    return value.toFixed(2);
  }
  return new Intl.NumberFormat('en-NZ', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
};

export const DataTable: React.FC<DataTableProps> = ({ data, title, isLoading }) => {
  if (isLoading) return <div>Loading...</div>;
  if (!data || data.length === 0) return <div>No data available</div>;

  // Define fixed column order to match database structure
  const columnOrder = [
    'meter_location',
    'Jan_2022', 'Feb_2022', 'Mar_2022', 'Apr_2022', 'May_2022', 'Jun_2022',
    'Jul_2022', 'Aug_2022', 'Sep_2022', 'Oct_2022', 'Nov_2022', 'Dec_2022',
    'Jan_2023', 'Feb_2023', 'Mar_2023', 'Apr_2023', 'May_2023', 'Jun_2023',
    'Jul_2023', 'Aug_2023', 'Sep_2023', 'Oct_2023', 'Nov_2023', 'Dec_2023',
    'Jan_2024', 'Feb_2024', 'Mar_2024', 'Apr_2024', 'May_2024', 'Jun_2024',
    'Jul_2024', 'Aug_2024', 'Sep_2024', 'Oct_2024', 'Nov_2024', 'Dec_2024',
    'Jan_2025', 'Feb_2025', 'Mar_2025'
  ];

  // Filter out any columns that don't exist in the data
  const columns = columnOrder.filter(col =>
    Object.keys(data[0]).includes(col) &&
    !['id', 'created_at', 'updated_at'].includes(col)
  );

  return (
    <div style={tableStyles.container}>
      <div style={tableStyles.title}>{title}</div>
      <table style={tableStyles.table}>
        <thead>
          <tr>
            {columns.map(column => (
              <th key={column} style={tableStyles.th}>
                {column.replace(/_/g, ' ')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map(column => (
                <td key={column} style={tableStyles.td}>
                  {typeof row[column] === 'number' ?
                    formatNumber(row[column] as number | null | undefined) :
                    row[column] || '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const JanitzaDataView: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [medData, setMedData] = useState<DataRow[]>([]);
  const [freezerData, setFreezerData] = useState<DataRow[]>([]);
  const [uoD4F6Data, setUoD4F6Data] = useState<DataRow[]>([]);
  const [uoF8XData, setUoF8XData] = useState<DataRow[]>([]);
  const [manualMetersData, setManualMetersData] = useState<DataRow[]>([]);
  const [calculatedData, setCalculatedData] = useState<DataRow[]>([]);
  
  // Separate state for each tab's meter location filter
  const [medMeterLocation, setMedMeterLocation] = useState('');
  const [freezerMeterLocation, setFreezerMeterLocation] = useState('');
  const [uoD4F6MeterLocation, setUoD4F6MeterLocation] = useState('');
  const [uoF8XMeterLocation, setUoF8XMeterLocation] = useState('');
  const [manualMeterLocation, setManualMeterLocation] = useState('');
  const [calculatedMeterLocation, setCalculatedMeterLocation] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const baseUrl = 'http://127.0.0.1:5001';
        const [med, freezer, uoD4F6, uoF8X, manual, calculated] = await Promise.all([
          fetch(`${baseUrl}/api/janitza/med`).then(res => res.json()),
          fetch(`${baseUrl}/api/janitza/freezer`).then(res => res.json()),
          fetch(`${baseUrl}/api/janitza/uod4f6`).then(res => res.json()),
          fetch(`${baseUrl}/api/janitza/uof8x`).then(res => res.json()),
          fetch(`${baseUrl}/api/janitza/manual`).then(res => res.json()),
          fetch(`${baseUrl}/api/janitza/calculated`).then(res => res.json())
        ]);

        setMedData(med);
        setFreezerData(freezer);
        setUoD4F6Data(uoD4F6);
        setUoF8XData(uoF8X);
        setManualMetersData(manual);
        setCalculatedData(calculated);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // Utility function to get unique meter locations
  const getUniqueMeterLocations = (data: DataRow[]) => {
    const uniqueLocations = new Set(data.map(row => row.meter_location));
    return Array.from(uniqueLocations);
  };

  // Filter data based on selected meter location
  const filterDataByLocation = (data: DataRow[], selectedLocation: string) => {
    return selectedLocation
      ? data.filter(row => row.meter_location === selectedLocation)
      : data;
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
    // Reset meter location filters when changing tabs
    setMedMeterLocation('');
    setFreezerMeterLocation('');
    setUoD4F6MeterLocation('');
    setUoF8XMeterLocation('');
    setManualMeterLocation('');
    setCalculatedMeterLocation('');
  };

  
    
  return (
    <div>
      <Tabs value={activeTab} onChange={handleTabChange}>
        <Tab label="MED Meters" />
        <Tab label="Freezer" />
        <Tab label="UoD4F6" />
        <Tab label="UoF8X" />
        <Tab label="Manual Meters" />
        <Tab label="Calculated" />
      </Tabs>

      {activeTab === 0 && (
        <div style={tableStyles.tabPanel}>
          <DataTable 
            data={filterDataByLocation(medData, medMeterLocation)} 
            title={
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                <div>MED Meters</div>
                <select 
                  value={medMeterLocation}
                  onChange={(e) => setMedMeterLocation(e.target.value)}
                  style={{ marginLeft: '15px', padding: '5px' }}
                >
                  <option value="">All MED Meter Locations</option>
                  {getUniqueMeterLocations(medData).map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>
            }
            isLoading={isLoading} 
          />
        </div>
      )}

      {activeTab === 1 && (
        <div style={tableStyles.tabPanel}>
          <DataTable 
            data={filterDataByLocation(freezerData, freezerMeterLocation)} 
            title={
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                <div>Freezer</div>
                <select 
                  value={freezerMeterLocation}
                  onChange={(e) => setFreezerMeterLocation(e.target.value)}
                  style={{ marginLeft: '15px', padding: '5px' }}
                >
                  <option value="">All Freezer Meter Locations</option>
                  {getUniqueMeterLocations(freezerData).map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>
            }
            isLoading={isLoading} 
          />
        </div>
      )}

      {activeTab === 2 && (
        <div style={tableStyles.tabPanel}>
          <DataTable 
            data={filterDataByLocation(uoD4F6Data, uoD4F6MeterLocation)} 
            title={
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                <div>UoD4F6</div>
                <select 
                  value={uoD4F6MeterLocation}
                  onChange={(e) => setUoD4F6MeterLocation(e.target.value)}
                  style={{ marginLeft: '15px', padding: '5px' }}
                >
                  <option value="">All UoD4F6 Meter Locations</option>
                  {getUniqueMeterLocations(uoD4F6Data).map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>
            }
            isLoading={isLoading} 
          />
        </div>
      )}

      {activeTab === 3 && (
        <div style={tableStyles.tabPanel}>
          <DataTable 
            data={filterDataByLocation(uoF8XData, uoF8XMeterLocation)} 
            title={
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                <div>UoF8X</div>
                <select 
                  value={uoF8XMeterLocation}
                  onChange={(e) => setUoF8XMeterLocation(e.target.value)}
                  style={{ marginLeft: '15px', padding: '5px' }}
                >
                  <option value="">All UoF8X Meter Locations</option>
                  {getUniqueMeterLocations(uoF8XData).map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>
            }
            isLoading={isLoading} 
          />
        </div>
      )}

      {activeTab === 4 && (
        <div style={tableStyles.tabPanel}>
          <DataTable 
            data={filterDataByLocation(manualMetersData, manualMeterLocation)} 
            title={
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                <div>Manual Meters</div>
                <select 
                  value={manualMeterLocation}
                  onChange={(e) => setManualMeterLocation(e.target.value)}
                  style={{ marginLeft: '15px', padding: '5px' }}
                >
                  <option value="">All Manual Meter Locations</option>
                  {getUniqueMeterLocations(manualMetersData).map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>
            }
            isLoading={isLoading} 
          />
        </div>
      )}

      {activeTab === 5 && (
        <div style={tableStyles.tabPanel}>
          <DataTable 
            data={filterDataByLocation(calculatedData, calculatedMeterLocation)} 
            title={
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                <div>Calculated</div>
                <select 
                  value={calculatedMeterLocation}
                  onChange={(e) => setCalculatedMeterLocation(e.target.value)}
                  style={{ marginLeft: '15px', padding: '5px' }}
                >
                  <option value="">All Calculated Meter Locations</option>
                  {getUniqueMeterLocations(calculatedData).map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>
            }
            isLoading={isLoading} 
          />
        </div>
      )}
    </div>
  );
};

export default JanitzaDataView;