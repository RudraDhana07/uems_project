import React, { useState, useEffect } from 'react';
import { Tabs, Tab, CircularProgress } from '@mui/material';

interface RoomTypeData {
    id: number;
    room_number: string;
    area_m2: string;
    type: string;
    suite: string;
}

interface DataRow {
    [key: string]: string | number | null | undefined;
    location?: string;
    building_code?: string;
    meter_type?: string;
    meter_number?: string;
    digit_to_read?: string;
    multipier_ct_rating?: string;
    remark?: string;
    mod?: string;
}

interface BaseTableProps {
    title: string;
    isLoading: boolean;
    searchTerm: string;
}

interface MeterTableProps extends BaseTableProps {
    data: DataRow[];
    boldLocations?: string[];
}

interface RoomTableProps extends BaseTableProps {
    data: RoomTypeData[];
}

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
        fontSize: '0.9em'
    },
    td: {
        padding: '8px',
        border: '1px solid #ddd',
        whiteSpace: 'nowrap' as const,
        fontSize: '0.9em'
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
    objectNameColumn: {
        minWidth: '320px',
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
        minWidth: '320px',
        maxWidth: '320px',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
    },
    numberColumn: {
        width: '50px',
        minWidth: '50px',
        maxWidth: '50px',
        textAlign: 'right' as const,
    }
};

const BOLD_LOCATIONS = [
    'Centre for Innovation main meters total (without Castle St houses)',
    'CfI-DB-2W', 'CfI-DB-1W', 'CfI-DB-GW',
    'CfI-DB-2E', 'CfI-DB-1E', 'CfI-DB-GE'
];

const getOrderedColumns = (data: DataRow[]): string[] => {
    if (!data.length) return [];

    const baseColumns = [
        'building_code',
        'location',
        'meter_type',
        'meter_number',
        'digit_to_read',
        'multipier_ct_rating',
        'remark',
        'mod'
    ];

    const readingColumns = [
        'R1_Dec_2021',
        ...Array.from({ length: 12 }, (_, i) => 
            `R1_${['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i]}_2022`
        ),
        'R1_Jan_2023',
        ...Array.from({ length: 12 }, (_, i) => 
            `${['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i]}_2023`
        ),
        ...Array.from({ length: 12 }, (_, i) => 
            `${['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i]}_2024`
        ),
        ...Array.from({ length: 3 }, (_, i) => 
            `${['Jan', 'Feb', 'Mar'][i]}_2025`
        )
    ];

    const availableColumns = Object.keys(data[0]).filter(col => 
        !['id', 'created_at', 'updated_at'].includes(col)
    );

    return [...baseColumns, ...readingColumns]
        .filter(col => availableColumns.includes(col));
};

const formatColumnHeader = (column: string): string => {
    const initCapsColumns = [
        'building_code', 'digit_to_read', 'location', 
        'meter_type', 'meter_number', 'mod', 
        'multipier_ct_rating', 'remark'
    ];

    if (initCapsColumns.includes(column)) {
        return column
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ');
    }
    return column;
};

const getColumnStyle = (column: string, isAltRow: boolean = false) => {
    const baseStyle = {
        ...tableStyles.td,
        backgroundColor: isAltRow ? '#f9f9f9' : '#ffffff'
    };

    if (column === 'building_code') return { ...baseStyle };
    if (column === 'location') return { ...baseStyle, ...tableStyles.meterLocationColumn };
    if (column === 'meter_type') return { ...baseStyle, ...tableStyles.descriptionColumn };
    if (column.includes('R1_') || column.match(/^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)_\d{4}$/)) {
        return { ...baseStyle, ...tableStyles.numberColumn };
    }
    return baseStyle;
};

const MeterReadingsTable: React.FC<MeterTableProps> = ({ data, title, isLoading, searchTerm }) => {
    if (isLoading) {
        return <CircularProgress />;
    }

    if (!data || data.length === 0) {
        return <div>No data available</div>;
    }

    const columns = getOrderedColumns(data);

    const formatValue = (value: any): string => {
        if (value === null || value === undefined) return '-';
        if (typeof value === 'number') {
            const positiveValue = Math.max(0, value);
            return positiveValue.toFixed(2).replace(/\.?0+$/, '');
        }
        return value.toString();
    };

    return (
        <div style={tableStyles.container}>
            <h3>{title}</h3>
            <table style={tableStyles.table}>
                <thead>
                    <tr>
                        {columns.map((column) => (
                            <th key={column} style={tableStyles.th}>
                                {formatColumnHeader(column)}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={index} style={{
                            backgroundColor: index % 2 === 0 ? '#f9f9f9' : '#ffffff'
                        }}>
                            {columns.map((column) => (
                                <td key={column} style={{
                                    ...getColumnStyle(column, index % 2 !== 0),
                                    fontWeight: (column === 'location' && 
                                        BOLD_LOCATIONS.includes(row[column]?.toString() || '')) 
                                        ? 'bold' : 'normal'
                                }}>
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

const RoomTypesTable: React.FC<RoomTableProps> = ({ data, isLoading, searchTerm }) => {
    if (isLoading) {
        return <CircularProgress />;
    }

    const columns = ['room_number', 'area_m2', 'type', 'suite'];

    // Filter data based on search term
    const filteredData = data.filter(row =>
        row.room_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
        row.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        row.suite.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div style={tableStyles.container}>
            <table style={tableStyles.table}>
                <thead>
                    <tr>
                        {columns.map((column) => (
                            <th key={column} style={tableStyles.th}>
                                {column.split('_').map(word => 
                                    word.charAt(0).toUpperCase() + word.slice(1)
                                ).join(' ')}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {filteredData.map((row, index) => (
                        <tr key={index} style={{
                            backgroundColor: index % 2 === 0 ? '#f9f9f9' : '#ffffff'
                        }}>
                            {columns.map((column) => (
                                <td key={column} style={tableStyles.td}>
                                    {row[column as keyof RoomTypeData]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const CfiDataView: React.FC = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [meterData, setMeterData] = useState<DataRow[]>([]);
    const [roomData, setRoomData] = useState<RoomTypeData[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerms, setSearchTerms] = useState({
        meter: '',
        room: ''
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                const baseUrl = 'http://127.0.0.1:5001';
                const [meterResponse, roomResponse] = await Promise.all([
                    fetch(`${baseUrl}/api/cfi/meter`),
                    fetch(`${baseUrl}/api/cfi/rooms`)
                ]);

                if (!meterResponse.ok || !roomResponse.ok) {
                    throw new Error('Failed to fetch data');
                }

                const [meterData, roomData] = await Promise.all([
                    meterResponse.json(),
                    roomResponse.json()
                ]);

                setMeterData(meterData);
                setRoomData(roomData);
            } catch (error) {
                console.error('Error fetching CFI data:', error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, []);

    const filterMeterData = (data: DataRow[]) => {
        return data.filter(row =>
            row.location?.toString().toLowerCase().includes(searchTerms.meter.toLowerCase())
        );
    };

    return (
        <div>
            <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
                <Tab label="Meter Readings" />
                <Tab label="Room Types" />
            </Tabs>

            {activeTab === 0 && (
                <>
                    <input
                        type="text"
                        placeholder="Search by location..."
                        value={searchTerms.meter}
                        onChange={(e) => setSearchTerms({...searchTerms, meter: e.target.value})}
                        style={tableStyles.searchBox}
                    />
                    <MeterReadingsTable
                        data={filterMeterData(meterData)}
                        title="Center for Innovation Meter Readings"
                        isLoading={isLoading}
                        searchTerm={searchTerms.meter}
                        boldLocations={BOLD_LOCATIONS}
                    />
                </>
            )}

            {activeTab === 1 && (
                <>
                    <input
                        type="text"
                        placeholder="Search room types..."
                        value={searchTerms.room}
                        onChange={(e) => setSearchTerms({...searchTerms, room: e.target.value})}
                        style={tableStyles.searchBox}
                    />
                    <RoomTypesTable
                        data={roomData}
                        title="CFI Room Types"
                        isLoading={isLoading}
                        searchTerm={searchTerms.room}
                    />
                </>
            )}
        </div>
    );
};

export default CfiDataView;