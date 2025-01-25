// src/components/views/LTHWDataView.tsx

import React, { useState, useEffect } from 'react';
import { Tabs, Tab, CircularProgress } from '@mui/material';
import LTHWConsumptionChart from '../visualizations/LTHWConsumptionChart';

interface DataRow {
    object_name: string;
    [key: string]: string | number | null | undefined;
}

interface DataTableProps {
    data: DataRow[];
    title: string;
    isLoading: boolean;
}

// Styles object
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
    tr: {
        backgroundColor: 'inherit'
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

const HIGHLIGHTED_BOILERS = [
    'F622 Psychology wood boiler (IP 10.81.146.160)',
    'F916 College of Education wood boiler (10.81.147.145)',
    'H538 Childcare boiler (IP 10.81.149.14)',
    'H633 Arana Boiler (IP 10.81.148.22)',
    'J122 Carrington Jenkins boiler',
    'XI01 Invercargill Boiler (IP 10.85.4.21)'
];

// Function to format column header
const formatColumnHeader = (column: string): string => {
    return column
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
};

// LTHW-specific DataTable component
const LTHWDataTable: React.FC<DataTableProps> = ({ data, title, isLoading }) => {
    if (isLoading) {
        return <CircularProgress />;
    }

    if (!data || data.length === 0) {
        return <div>No data available</div>;
    }

    const formatValue = (value: any, column: string): string => {
        if (value === null || value === undefined) return '-';
    
        // Columns that should not have decimal formatting
        const noDecimalColumns = ['misc', 'identifier'];
        
        if (typeof value === 'number' && !noDecimalColumns.includes(column.toLowerCase())) {
            // For numeric columns (monthly readings), format to 2 decimal places if needed
            const strValue = value.toString();
            if (strValue.includes('.')) {
                return Number(value).toFixed(2).replace(/\.?0+$/, '');
            }
        }
        return value.toString();
    };

    // Define column order for each table type based on title
    const getOrderedColumns = (title: string, allColumns: string[]): string[] => {
        // Define metadata columns based on table type
        let metadataColumns: string[];
        if (title.includes("Automated Meters")) {
            metadataColumns = [
                'object_name',
                'object_description',
                'company',
                'identifier',
                'notes'
            ];
        } else if (title.includes("Manual Meters")) {
            metadataColumns = [
                'object_name',
                'meter_location',
                'company',
                'identifier',
                'notes'
            ];
        } else {
            metadataColumns = [
                'object_name',
                'notes',
                'comments',
                'misc'
            ];
        }
    
        // Hardcoded month-year columns in specific order
        const monthYearColumns = [
            'Jan_2022', 'Feb_2022', 'Mar_2022', 'Apr_2022', 'May_2022', 'Jun_2022',
            'Jul_2022', 'Aug_2022', 'Sep_2022', 'Oct_2022', 'Nov_2022', 'Dec_2022',
            'Jan_2023', 'Feb_2023', 'Mar_2023', 'Apr_2023', 'May_2023', 'Jun_2023',
            'Jul_2023', 'Aug_2023', 'Sep_2023', 'Oct_2023', 'Nov_2023', 'Dec_2023',
            'Jan_2024', 'Feb_2024', 'Mar_2024', 'Apr_2024', 'May_2024', 'Jun_2024',
            'Jul_2024', 'Aug_2024', 'Sep_2024', 'Oct_2024', 'Nov_2024', 'Dec_2024',
            'Jan_2025', 'Feb_2025', 'Mar_2025'
        ];
    
        // Return combined columns in order
        return [...metadataColumns, ...monthYearColumns];
    };

    // Get all columns except id, created_at, and updated_at
    const allColumns = Object.keys(data[0]).filter(
        col => !['id', 'created_at', 'updated_at'].includes(col)
    );

    // Get ordered columns based on table type
    const orderedColumns = getOrderedColumns(title, allColumns);

    return (
        <div style={tableStyles.container}>
            <h2 style={tableStyles.title}>{title}</h2>
            <table style={tableStyles.table}>
            <thead>
                <tr>
                    {orderedColumns.map((column) => (
                        <th key={column} style={tableStyles.th}>
                            {formatColumnHeader(column)}
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {data.map((row, rowIndex) => (
                    <tr 
                        key={rowIndex}
                        style={{
                            ...tableStyles.tr,
                            backgroundColor: title.includes("Consumption Values") && 
                                HIGHLIGHTED_BOILERS.includes(row.object_name) 
                                ? '#ffebb5' 
                                : 'inherit'
                        }}
                    >
                        {orderedColumns.map((column) => (
                            <td key={`${rowIndex}-${column}`} style={tableStyles.td}>
                                {formatValue(row[column], column)}
                            </td>
                        ))}
                    </tr>
                ))}
            </tbody>
            </table>
        </div>
    );
};


const LTHWDataView: React.FC = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [automatedData, setAutomatedData] = useState<DataRow[]>([]);
    const [manualData, setManualData] = useState<DataRow[]>([]);
    const [consumptionData, setConsumptionData] = useState<DataRow[]>([]);
    
    const [automatedObjectName, setAutomatedObjectName] = useState('');
    const [manualObjectName, setManualObjectName] = useState('');
    const [consumptionObjectName, setConsumptionObjectName] = useState('');
    
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                const baseUrl = 'http://127.0.0.1:5001';
                const [automated, manual, consumption] = await Promise.all([
                    fetch(`${baseUrl}/api/lthw/automated`).then(res => res.json()),
                    fetch(`${baseUrl}/api/lthw/manual`).then(res => res.json()),
                    fetch(`${baseUrl}/api/lthw/consumption`).then(res => res.json())
                ]);

                setAutomatedData(automated);
                setManualData(manual);
                setConsumptionData(consumption);
            } catch (error) {
                console.error('Error fetching LTHW data:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, []);

    const getUniqueObjectNames = (data: DataRow[]) => {
        const uniqueNames = new Set(data.map(row => row.object_name));
        return Array.from(uniqueNames);
    };

    const filterDataByObjectName = (data: DataRow[], selectedName: string) => {
        return selectedName
            ? data.filter(row => row.object_name === selectedName)
            : data;
    };

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setActiveTab(newValue);
        setAutomatedObjectName('');
        setManualObjectName('');
        setConsumptionObjectName('');
    };

    return (
        <div style={tableStyles.container}>
            <Tabs value={activeTab} onChange={handleTabChange}>
                <Tab label="Consumption Values" />
                <Tab label="Automated Meters" />
                <Tab label="Manual Meters" />
            </Tabs>
    
            {activeTab === 0 && (
                <div>
                    <LTHWConsumptionChart data={consumptionData} />
                    <select
                        value={consumptionObjectName}
                        onChange={(e) => setConsumptionObjectName(e.target.value)}
                        style={{ marginLeft: '15px', padding: '5px' }}
                    >
                        <option value="">All Consumption Values</option>
                        {getUniqueObjectNames(consumptionData).map(name => (
                            <option key={name} value={name}>{name}</option>
                        ))}
                    </select>
                    <LTHWDataTable
                        data={filterDataByObjectName(consumptionData, consumptionObjectName)}
                        title="LTHW Consumption Values"
                        isLoading={isLoading}
                    />
                </div>
            )}
    
            {activeTab === 1 && (
                <div>
                    <select
                        value={automatedObjectName}
                        onChange={(e) => setAutomatedObjectName(e.target.value)}
                        style={{ marginLeft: '15px', padding: '5px' }}
                    >
                        <option value="">All Automated Meters</option>
                        {getUniqueObjectNames(automatedData).map(name => (
                            <option key={name} value={name}>{name}</option>
                        ))}
                    </select>
                    <LTHWDataTable
                        data={filterDataByObjectName(automatedData, automatedObjectName)}
                        title="LTHW Automated Meters"
                        isLoading={isLoading}
                    />
                </div>
            )}
    
            {activeTab === 2 && (
                <div>
                    <select
                        value={manualObjectName}
                        onChange={(e) => setManualObjectName(e.target.value)}
                        style={{ marginLeft: '15px', padding: '5px' }}
                    >
                        <option value="">All Manual Meters</option>
                        {getUniqueObjectNames(manualData).map(name => (
                            <option key={name} value={name}>{name}</option>
                        ))}
                    </select>
                    <LTHWDataTable
                        data={filterDataByObjectName(manualData, manualObjectName)}
                        title="LTHW Manual Meters"
                        isLoading={isLoading}
                    />
                </div>
            )}
        </div>
    );
};

export default LTHWDataView;
