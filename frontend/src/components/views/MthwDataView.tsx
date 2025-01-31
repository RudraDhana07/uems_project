// backend/app/frontend/src/components/MthwDataView.tsx

import React, { useState, useEffect } from 'react';
import { Tabs, Tab, CircularProgress } from '@mui/material';
import MTHWConsumptionChart from '../visualizations/MTHWConsumptionChart';

interface DataRow {
    meter_location?: string;
    multiplier_for_unit?: number;
    misc1?: string;
    misc2?: string;
    [key: string]: string | number | null | undefined;
}

interface DataTableProps {
    data: DataRow[];
    title: string;
    isLoading: boolean;
    tableType: 'meter' | 'consumption';
}

const HIGHLIGHTED_METERS = [
    "St Margaret's MTHW",
    "G404, Microbiology",
    "G405, Science 3",
    "F505, Richardson Total",
    "G413, Science 2 total",
    "F419, ISB",
    "E201 Dental Steam Total",
    "F402, Union",
    "F518, Arts Building",
    "G401 Mellor Lab total"
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
    },
    tr: {
        backgroundColor: 'inherit'
    },
    trAlternate: {
        backgroundColor: '#f9f9f9'
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
        textTransform: 'capitalize' as const
    },
    td: {
        padding: '8px',
        border: '1px solid #ddd',
        whiteSpace: 'nowrap' as const
    },
    searchBox: {
        width: '60%',
        padding: '8px',
        marginBottom: '15px',
        marginLeft: '15px',
        border: '1px solid #ddd',
        borderRadius: '4px'
    }
};

const getOrderedColumns = (data: DataRow[], tableType: 'meter' | 'consumption'): string[] => {
    if (!data.length) return [];

    const baseColumns = {
        'meter': ['meter_location', 'multiplier_for_unit'],
        'consumption': ['meter_location', 'misc1', 'misc2', 'multiplier_for_unit']
    };

    const monthlyColumns = [];
    for (let year = 2021; year <= 2025; year++) {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        if (year === 2021) {
            months.splice(0, 10); // Only Nov and Dec for 2021
        }
        if (year === 2025) {
            months.splice(3); // Only Jan to Mar for 2025
        }
        monthlyColumns.push(...months.map(month => `${month}_${year}`));
    }

    return [...baseColumns[tableType], ...monthlyColumns];
};

const MTHWDataTable: React.FC<DataTableProps> = ({ data, title, isLoading, tableType }) => {
    if (isLoading) {
        return <CircularProgress />;
    }

    if (!data || data.length === 0) {
        return <div>No data available</div>;
    }

    const orderedColumns = getOrderedColumns(data, tableType);

    const formatValue = (value: any): string => {
        if (value === null || value === undefined) return '-';
        if (typeof value === 'number') {
            const numValue = Math.max(0, value); // Convert negative to 0
            return numValue.toFixed(2);
        }
        return value.toString();
    };

    const getRowStyle = (row: DataRow, index: number) => {
        const baseStyle = index % 2 === 0 ? tableStyles.tr : tableStyles.trAlternate;
        if (row.meter_location && HIGHLIGHTED_METERS.includes(row.meter_location.trim())) {
            return { ...baseStyle, backgroundColor: '#FFE9A8' };
        }
        return baseStyle;
    };

    return (
        <div style={tableStyles.container}>
            <h3>{title}</h3>
            <table style={tableStyles.table}>
                <thead>
                    <tr>
                        {orderedColumns.map((column) => (
                            <th key={column} style={tableStyles.th}>
                                {column.replace(/_/g, ' ')}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={index} style={getRowStyle(row, index)}>
                            {orderedColumns.map((column) => (
                                <td key={column} style={tableStyles.td}>
                                    <span style={{
                                        fontWeight: column === 'meter_location' && 
                                            HIGHLIGHTED_METERS.includes(row[column]?.toString().trim() || '') 
                                            ? 'bold' : 'normal'
                                    }}>
                                        {formatValue(row[column])}
                                    </span>
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const MthwDataView: React.FC = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [meterData, setMeterData] = useState<DataRow[]>([]);
    const [consumptionData, setConsumptionData] = useState<DataRow[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerms, setSearchTerms] = useState({
        meter: '',
        consumption: ''
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                const baseUrl = 'http://127.0.0.1:5001';
                const [meterResponse, consumptionResponse] = await Promise.all([
                    fetch(`${baseUrl}/api/mthw/meter`),
                    fetch(`${baseUrl}/api/mthw/consumption`)
                ]);

                const meterData = await meterResponse.json();
                const consumptionData = await consumptionResponse.json();

                setMeterData(meterData);
                setConsumptionData(consumptionData);
            } catch (error) {
                console.error('Error fetching data:', error);
                setMeterData([]);
                setConsumptionData([]);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, []);

    const filterData = (data: DataRow[], searchTerm: string) => {
        if (!searchTerm) return data;
        return data.filter(row =>
            String(row.meter_location || '').toLowerCase().includes(searchTerm.toLowerCase())
        );
    };

    return (
        <div>
            <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
                <Tab label="MTHW Meter Reading" />
                <Tab label="MTHW Consumption" />
            </Tabs>

            {activeTab === 0 && (
                <>
                    <input
                        type="text"
                        placeholder="Search by meter location..."
                        value={searchTerms.meter}
                        onChange={(e) => setSearchTerms({...searchTerms, meter: e.target.value})}
                        style={tableStyles.searchBox}
                    />
                    <MTHWDataTable
                        data={filterData(meterData, searchTerms.meter)}
                        title="MTHW Meter Reading"
                        isLoading={isLoading}
                        tableType="meter"
                    />
                </>
            )}

            {activeTab === 1 && (
                <>
                    <input
                        type="text"
                        placeholder="Search by meter location..."
                        value={searchTerms.consumption}
                        onChange={(e) => setSearchTerms({...searchTerms, consumption: e.target.value})}
                        style={tableStyles.searchBox}
                    />
                    
                    <div style={{ padding: '20px' }}>
                        {isLoading ? (
                            <CircularProgress />
                        ) : (
                            <MTHWConsumptionChart data={consumptionData} />
                        )}
                    </div>

                    <MTHWDataTable
                        data={filterData(consumptionData, searchTerms.consumption)}
                        title="MTHW Consumption"
                        isLoading={isLoading}
                        tableType="consumption"
                    />
                </>
            )}
        </div>
    );
};

export default MthwDataView;
