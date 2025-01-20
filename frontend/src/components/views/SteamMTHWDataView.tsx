// src/components/views/SteamMTHWDataView.tsx
import ConsumptionTrendChart from '../visualizations/ConsumptionTrendChart';
import React, { useState, useEffect, useMemo } from 'react';

interface SteamMTHWReading {
  id: number;
  month: string;
  year: number;
  mthw_consumption_kwh: number | null;
  castle_192_reading_kwh: number | null;
  castle_192_consumption_kwh: number | null;
  med_school_a_reading_kg: number | null;
  med_school_a_reading_kwh: number | null;
  med_school_a_consumption_kg: number | null;
  med_school_a_consumption_kwh: number | null;
  med_school_b_reading_kg: number | null;
  med_school_b_reading_kwh: number | null;
  med_school_b_consumption_kg: number | null;
  med_school_b_consumption_kwh: number | null;
  med_school_consumption_kg: number | null;
  med_school_consumption_kwh: number | null;
  cumberland_d401_dining_reading_kg: number | null;
  cumberland_d404_castle_reading_kg: number | null;
  cumberland_d401_d404_consumption_kg: number | null;
  cumberland_d401_d404_consumption_kwh: number | null;
  total_steam_consumption_kwh: number | null;
}

const filterStyles = {
    filterContainer: {
      margin: '10px 0',
      display: 'flex',
      gap: '20px',
      alignItems: 'center',
    },
    select: {
      padding: '8px',
      borderRadius: '4px',
      border: '1px solid #ddd',
      minWidth: '120px',
    },
    label: {
      fontSize: '0.9em',
      color: '#333',
    }
  };

  const chartStyles = {
    container: {
      backgroundColor: '#fff',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      marginBottom: '20px'
    },
    title: {
      fontSize: '1.1em',
      marginBottom: '15px',
      color: '#333'
    }
  };

  const monthOrder = [
    'all',
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ];

  const getMonthName = (monthStr: string): string => {
    const months: { [key: string]: string } = {
      'Jan': 'January',
      'Feb': 'February',
      'Mar': 'March',
      'Apr': 'April',
      'May': 'May',
      'Jun': 'June',
      'Jul': 'July',
      'Aug': 'August',
      'Sep': 'September',
      'Oct': 'October',
      'Nov': 'November',
      'Dec': 'December'
    };
    return months[monthStr] || monthStr;
  };

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
  },
  td: {
    padding: '6px 8px',
    border: '1px solid #ddd',
    fontSize: '0.9em',
    whiteSpace: 'nowrap' as const,
    backgroundColor: '#ffffff',  // Add white background for regular cells
    },
    altRow: {
    backgroundColor: '#f9f9f9',  // Add alternate row color
    },
    numberColumn: {
    width: '100px',
    textAlign: 'right' as const,
    backgroundColor: '#ffffff',  // Add background for number columns
    },
    highlightCell: {
    backgroundColor: '#fff3e0',  // Add highlight color for specific cells
    },
  dateColumn: {
    width: '80px',
  },
  title: {
    fontSize: '1.2em',
    marginBottom: '8px',
    color: '#333',
    padding: '8px 0',
  },
  error: {
    color: 'red',
    padding: '20px',
    textAlign: 'center' as const,
  },
  mergedHeader: {
    backgroundColor: '#e6f3ff',
    padding: '8px',
    border: '1px solid #ddd',
    textAlign: 'center' as const,
    fontWeight: 'bold',
    fontSize: '0.9em',
    color: '#333',
  },
  subHeader: {
    backgroundColor: '#e6f3ff',
    padding: '8px',
    border: '1px solid #ddd',
    fontWeight: 'bold',
    fontSize: '0.9em',
    color: '#333',
    textAlign: 'center' as const,
  }
};

const formatNumber = (value: number | null): string => {
  if (value === null || value === undefined || isNaN(value)) return '-';
  if (Math.abs(value) < 0.01) return '0';
  return new Intl.NumberFormat('en-NZ', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(value);
};

const getColumnStyle = (column: string, isAltRow: boolean) => {
    const baseStyle = {
      ...tableStyles.td,
      backgroundColor: isAltRow ? '#f9f9f9' : '#ffffff'
    };
  
    // Add array of columns that should have light yellow background
    const highlightColumns = [
      'castle_192_consumption_kwh',
      'med_school_consumption_kwh',
      'cumberland_d401_d404_consumption_kwh',
      'total_steam_consumption_kwh'
    ];
  
    // Check if column should be highlighted
    if (highlightColumns.includes(column)) {
      return {
        ...baseStyle,
        ...tableStyles.numberColumn,
        backgroundColor: '#fffde7'  // Light yellow color
      };
    }
  
    if (column === 'month' || column === 'year') {
      return { ...baseStyle, ...tableStyles.dateColumn };
    }
    if (column.includes('consumption') || column.includes('reading')) {
      return { ...baseStyle, ...tableStyles.numberColumn, backgroundColor: isAltRow ? '#f9f9f9' : '#ffffff' };
    }
    return baseStyle;
  };

const SteamMTHWDataView: React.FC = () => {
  const [data, setData] = useState<SteamMTHWReading[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [yearFilter, setYearFilter] = useState<string>('all');
  const [monthFilter, setMonthFilter] = useState<string>('all');
  
  const uniqueYears = useMemo(() => {
    if (!data.length) return [];
    return Array.from(new Set(data.map(row => row.year))).sort((a, b) => b - a);
  }, [data]);

  const filteredData = useMemo(() => {
    return data.filter(row => {
      const matchesYear = yearFilter === 'all' || row.year.toString() === yearFilter;
      const matchesMonth = monthFilter === 'all' || getMonthName(row.month) === monthFilter;
      return matchesYear && matchesMonth;
    });
  }, [data, yearFilter, monthFilter]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const baseUrl = 'http://127.0.0.1:5001';
        const response = await fetch(`${baseUrl}/api/steam-mthw/readings`);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to fetch data');
        }

        const result = await response.json();
        const cleanedData = result.map((row: any) => {
          const cleanRow = { ...row };
          Object.keys(cleanRow).forEach(key => {
            if (key !== 'id' && key !== 'month' && key !== 'year') {
              const value = cleanRow[key];
              cleanRow[key] = value === null || value === undefined || isNaN(value) ? null : parseFloat(value);
            }
          });
          return cleanRow;
        });
        setData(cleanedData);
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

  if (isLoading) {
    return <div style={{ padding: '20px' }}>Loading...</div>;
  }

  if (!data || data.length === 0) {
    return <div style={{ padding: '20px' }}>No data available</div>;
  }


  return (
    <div style={tableStyles.container}>
      <h2 style={tableStyles.title}>Steam and MTHW Data</h2>
       {/* Add Chart Section */}
        <div style={chartStyles.container}>
        <h3 style={chartStyles.title}>Consumption Trends Over Time (in kWh)</h3>
        {filteredData.length > 0 && <ConsumptionTrendChart data={filteredData} />}
        </div>
        
      <div style={filterStyles.filterContainer}>
        <div>
          <label style={filterStyles.label}>Year: </label>
          <select 
            style={filterStyles.select}
            value={yearFilter}
            onChange={(e) => setYearFilter(e.target.value)}
          >
            <option value="all">All Years</option>
            {uniqueYears.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>
        <div>
          <label style={filterStyles.label}>Month: </label>
          <select
            style={filterStyles.select}
            value={monthFilter}
            onChange={(e) => setMonthFilter(e.target.value)}
            >
            <option value="all">All Months</option>
            {monthOrder.slice(1).map(month => (
                <option key={month} value={month}>{month}</option>
            ))}
            </select>
        </div>
      </div>

      <table style={tableStyles.table}>
        <thead>
          <tr>
            <th style={tableStyles.mergedHeader} rowSpan={2}>Month</th>
            <th style={tableStyles.mergedHeader} rowSpan={2}>Year</th>
            <th style={tableStyles.mergedHeader} rowSpan={2}>MTHW Consumption kWh</th>
            <th style={tableStyles.mergedHeader} colSpan={2}>Castle 192</th>
            <th style={tableStyles.mergedHeader} colSpan={4}>Med School Line A</th>
            <th style={tableStyles.mergedHeader} colSpan={4}>Med School Line B</th>
            <th style={tableStyles.mergedHeader} colSpan={2}>Med School Total</th>
            <th style={tableStyles.mergedHeader} colSpan={4}>Cumberland</th>
            <th style={tableStyles.mergedHeader} rowSpan={2}>Total Steam Consumption kWh</th>
          </tr>
          <tr>
            <th style={tableStyles.subHeader}>Reading kWh</th>
            <th style={tableStyles.subHeader}>Consumption kWh</th>
            
            <th style={tableStyles.subHeader}>Reading kg</th>
            <th style={tableStyles.subHeader}>Reading kWh</th>
            <th style={tableStyles.subHeader}>Consumption kg</th>
            <th style={tableStyles.subHeader}>Consumption kWh</th>
            
            <th style={tableStyles.subHeader}>Reading kg</th>
            <th style={tableStyles.subHeader}>Reading kWh</th>
            <th style={tableStyles.subHeader}>Consumption kg</th>
            <th style={tableStyles.subHeader}>Consumption kWh</th>
            
            <th style={tableStyles.subHeader}>Consumption kg</th>
            <th style={tableStyles.subHeader}>Consumption kWh</th>
            
            <th style={tableStyles.subHeader}>D401 Reading kg</th>
            <th style={tableStyles.subHeader}>D404 Reading kg</th>
            <th style={tableStyles.subHeader}>Consumption kg</th>
            <th style={tableStyles.subHeader}>Consumption kWh</th>
          </tr>
        </thead>
        <tbody>
         {filteredData.map((row, index) => (
            <tr key={index}>
           <td style={getColumnStyle('month', index % 2 !== 0)}>{getMonthName(row.month)}</td>
            <td style={getColumnStyle('year', index % 2 !== 0)}>{row.year}</td>
            <td style={getColumnStyle('mthw_consumption_kwh', index % 2 !== 0)}>{formatNumber(row.mthw_consumption_kwh)}</td>
            <td style={getColumnStyle('castle_192_reading_kwh', index % 2 !== 0)}>{formatNumber(row.castle_192_reading_kwh)}</td>
            <td style={getColumnStyle('castle_192_consumption_kwh', index % 2 !== 0)}>{formatNumber(row.castle_192_consumption_kwh)}</td>
            <td style={getColumnStyle('med_school_a_reading_kg', index % 2 !== 0)}>{formatNumber(row.med_school_a_reading_kg)}</td>
            <td style={getColumnStyle('med_school_a_reading_kwh', index % 2 !== 0)}>{formatNumber(row.med_school_a_reading_kwh)}</td>
            <td style={getColumnStyle('med_school_a_consumption_kg', index % 2 !== 0)}>{formatNumber(row.med_school_a_consumption_kg)}</td>
            <td style={getColumnStyle('med_school_a_consumption_kwh', index % 2 !== 0)}>{formatNumber(row.med_school_a_consumption_kwh)}</td>
            <td style={getColumnStyle('med_school_b_reading_kg', index % 2 !== 0)}>{formatNumber(row.med_school_b_reading_kg)}</td>
            <td style={getColumnStyle('med_school_b_reading_kwh', index % 2 !== 0)}>{formatNumber(row.med_school_b_reading_kwh)}</td>
            <td style={getColumnStyle('med_school_b_consumption_kg', index % 2 !== 0)}>{formatNumber(row.med_school_b_consumption_kg)}</td>
            <td style={getColumnStyle('med_school_b_consumption_kwh', index % 2 !== 0)}>{formatNumber(row.med_school_b_consumption_kwh)}</td>
            <td style={getColumnStyle('med_school_consumption_kg', index % 2 !== 0)}>{formatNumber(row.med_school_consumption_kg)}</td>
            <td style={getColumnStyle('med_school_consumption_kwh', index % 2 !== 0)}>{formatNumber(row.med_school_consumption_kwh)}</td>
            <td style={getColumnStyle('cumberland_d401_dining_reading_kg', index % 2 !== 0)}>{formatNumber(row.cumberland_d401_dining_reading_kg)}</td>
            <td style={getColumnStyle('cumberland_d404_castle_reading_kg', index % 2 !== 0)}>{formatNumber(row.cumberland_d404_castle_reading_kg)}</td>
            <td style={getColumnStyle('cumberland_d401_d404_consumption_kg', index % 2 !== 0)}>{formatNumber(row.cumberland_d401_d404_consumption_kg)}</td>
            <td style={getColumnStyle('cumberland_d401_d404_consumption_kwh', index % 2 !== 0)}>{formatNumber(row.cumberland_d401_d404_consumption_kwh)}</td>
            <td style={getColumnStyle('total_steam_consumption_kwh', index % 2 !== 0)}>{formatNumber(row.total_steam_consumption_kwh)}</td>
            </tr>
        ))}
        </tbody>
      </table>
    </div>
  );
};

export default SteamMTHWDataView;
