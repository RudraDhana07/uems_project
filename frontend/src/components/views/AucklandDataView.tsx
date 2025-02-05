// src/components/view/AucklandDataView.tsx

import ElectricityConsumptionChart from '../visualizations/ElectricityConsumptionChart';
import { API_BASE_URL, API_ENDPOINTS } from '../../config/api';
import React, { useState, useEffect } from 'react';


interface DataRow {
  object_name: string;
  object_description?: string;
  meter_location?: string;
  reading_description?: string;
  [key: string]: string | number | undefined;
}

interface DataTableProps {
  data: DataRow[];
  title: string;
  isLoading: boolean;
}

const tableStyles = {
  container: {
    margin: '20px',
    overflowX: 'auto' as const,
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse' as const,
    border: '1px solid #ddd',
    marginBottom: '8px',
  },
  th: {
    backgroundColor: '#e6f3ff',
    padding: '8px',
    border: '1px solid #ddd',
    position: 'sticky' as const,
    top: 0,
    whiteSpace: 'nowrap' as const,
    color: '#333',
    fontWeight: 'bold',
    textAlign: 'left' as const,
    fontSize: '0.9em',
    zIndex: 1,  // Add this to ensure header stays on top
  },
  td: {
    padding: '6px 8px',
    border: '1px solid #ddd',
    fontSize: '0.9em',
    whiteSpace: 'nowrap' as const,
  },
  objectNameColumn: {
    minWidth: '320px',  // Increased from 280px
    maxWidth: '320px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  descriptionColumn: {
    minWidth: '140px',
    maxWidth: '140px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  meterLocationColumn: {
    minWidth: '320px',  // Increased from 220px
    maxWidth: '320px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  numberColumn: {
    width: '50px',
    minWidth: '50px',
    maxWidth: '50px',
    textAlign: 'right' as const,
  },
  title: {
    fontSize: '1.2em',
    marginBottom: '8px',
    color: '#333',
    padding: '8px 0',
  },
  mainTitle: {
    fontSize: '1.6em',
    color: '#222',
    padding: '15px',
  },
  error: {
    color: 'red',
    padding: '20px',
    textAlign: 'center' as const,
  },
  note: {
    fontSize: '0.85em',
    color: '#666',
    marginTop: '4px',
    marginLeft: '20px',
    marginBottom: '20px',
  }
};

const formatNumber = (value: number | null): string => {
  if (value === null || value === undefined) return '-';
  if (Math.abs(value) < 100) {
    return value.toFixed(2);
  }
  return new Intl.NumberFormat('en-NZ', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
};

const formatColumnHeader = (column: string): string => {
  if (column === 'object_name') return 'Object Name';
  if (column === 'object_description') return 'Description';
  if (column === 'meter_location') return 'Meter Location';
  if (column === 'reading_description') return 'Reading Description';
  
  if (column.includes('_20')) {
    const [month, year] = column.split('_');
    return `${month} ${year}`;
  }
  return column.replace(/_/g, ' ');
};

const getColumnStyle = (column: string, isAltRow: boolean = false, isHeader: boolean = false) => {
  const baseStyle = {
    ...tableStyles.td,
    backgroundColor: isHeader ? '#e6f3ff' : isAltRow ? '#f9f9f9' : '#ffffff'
  };

  if (column === 'object_name') {
    return { ...baseStyle, ...tableStyles.objectNameColumn };
  }
  if (column === 'object_description') {
    return { ...baseStyle, ...tableStyles.descriptionColumn };
  }
  if (column === 'meter_location') {
    return { ...baseStyle, ...tableStyles.meterLocationColumn };
  }
  if (column.includes('_20')) {
    return { ...baseStyle, ...tableStyles.numberColumn };
  }
  return baseStyle;
};

const LoadingTable: React.FC<{ title: string }> = ({ title }) => (
  <div style={tableStyles.container}>
    <h2 style={tableStyles.title}>{title}</h2>
    <div>Loading...</div>
  </div>
);

const EmptyTable: React.FC<{ title: string }> = ({ title }) => (
  <div style={tableStyles.container}>
    <h2 style={tableStyles.title}>{title}</h2>
    <div>No data available</div>
  </div>
);

const DataTable: React.FC<DataTableProps> = ({ data, title, isLoading }) => {
  if (isLoading) {
    return <LoadingTable title={title} />;
  }

  if (!data || data.length === 0) {
    return <EmptyTable title={title} />;
  }

  const columnOrder = [
    'object_name',
    'object_description',
    'meter_location',
    'reading_description',
    'Dec_2021',
    'Jan_2022', 'Feb_2022', 'Mar_2022', 'Apr_2022', 'May_2022', 'Jun_2022',
    'Jul_2022', 'Aug_2022', 'Sep_2022', 'Oct_2022', 'Nov_2022', 'Dec_2022',
    'Jan_2023', 'Feb_2023', 'Mar_2023', 'Apr_2023', 'May_2023', 'Jun_2023',
    'Jul_2023', 'Aug_2023', 'Sep_2023', 'Oct_2023', 'Nov_2023', 'Dec_2023',
    'Jan_2024', 'Feb_2024', 'Mar_2024', 'Apr_2024', 'May_2024', 'Jun_2024',
    'Jul_2024', 'Aug_2024', 'Sep_2024', 'Oct_2024', 'Nov_2024', 'Dec_2024',
    'Jan_2025', 'Feb_2025', 'Mar_2025'
  ];

  const columns = columnOrder.filter(col =>
    Object.keys(data[0]).includes(col) &&
    !['id', 'created_at', 'updated_at'].includes(col) &&
    !(title === "Water Consumption" && col === 'reading_description')
  );
  

  return (
    <div style={tableStyles.container}>
      <h2 style={tableStyles.title}>{title}</h2>
      <table style={tableStyles.table}>
      <thead>
        <tr>
          {columns.map((column: string) => (
            <th key={column} style={{ ...tableStyles.th, ...getColumnStyle(column, false, true) }}>
              {formatColumnHeader(column)}
            </th>
          ))}
        </tr>
      </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column} style={getColumnStyle(column, index % 2 !== 0)}>
                {typeof row[column] === 'number' ? formatNumber(row[column] as number) : row[column] || '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {title === "Water Consumption" && (
        <div style={tableStyles.note}>
          ** (From Desigo CC System2) The values from the monthly report are unreliable. The water meters drop to 0 and back to value
        </div>
      )}
    </div>
  );
};

const AucklandDataView: React.FC = () => {
  const [electricityData, setElectricityData] = useState<DataRow[]>([]);
  const [waterCalculatedData, setWaterCalculatedData] = useState<DataRow[]>([]);
  const [waterData, setWaterData] = useState<DataRow[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        console.log('Fetching from:', `${API_BASE_URL}${API_ENDPOINTS.electricity}`);

        const [electricityRes, waterCalcRes, waterRes] = await Promise.all([
          fetch(`${API_BASE_URL}${API_ENDPOINTS.electricity}`),
          fetch(`${API_BASE_URL}${API_ENDPOINTS.waterCalculated}`),
          fetch(`${API_BASE_URL}${API_ENDPOINTS.water}`)
        ]);

        console.log('Response status:', {
          electricity: electricityRes.status,
          waterCalc: waterCalcRes.status,
          water: waterRes.status
        });

        const [electricityData, waterCalcData, waterData] = await Promise.all([
          electricityRes.json(),
          waterCalcRes.json(),
          waterRes.json()
        ]);

        setElectricityData(electricityData);
        setWaterCalculatedData(waterCalcData);
        setWaterData(waterData);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (error) {
    return <div style={tableStyles.error}>Error: {error}</div>;
  }

  return (
    <div>
      <h1 style={tableStyles.mainTitle}>Auckland Campus Data</h1>
      {!isLoading && !error && (
        <div style={tableStyles.container}>
          <h2 style={tableStyles.title}>Electricity Consumption Trend</h2>
          <ElectricityConsumptionChart data={electricityData} />
        </div>
      )}
      <DataTable
        data={electricityData}
        title="Electricity Consumption"
        isLoading={isLoading}
      />
      <DataTable
        data={waterCalculatedData}
        title="Water Calculated Consumption"
        isLoading={isLoading}
      />
      <DataTable
        data={waterData}
        title="Water Consumption"
        isLoading={isLoading}
      />
    </div>
  );
};

export default AucklandDataView;
