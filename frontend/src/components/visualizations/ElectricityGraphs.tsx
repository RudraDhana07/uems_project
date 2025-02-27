// src/components/visualizations/ElectricityGraphs.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';


const isValidNumber = (value: any): boolean => {
  return value !== null && 
         value !== undefined && 
         value !== '-' && 
         !isNaN(value) && 
         value !== 0;  // Exclude 0 if it's a default value
};

interface ElectricityGraphsProps {
  data: {
    ringMains: any[];
    libraries: any[];
    colleges: any[];
    science: any[];
    healthScience: any[];
    humanities: any[];
  };
}

const ElectricityGraphs: React.FC<ElectricityGraphsProps> = ({ data }) => {
  const divisions = [
    { key: 'Ring Mains', color: '#0066cc' },
    { key: 'Libraries', color: '#00cc66' },
    { key: 'Colleges', color: '#cc6600' },
    { key: 'Science', color: '#9933cc' },
    { key: 'Health Science', color: '#ff6666' },
    { key: 'Humanities', color: '#66ccff' }
  ];

  const COLORS = ['#0066cc', '#00cc66', '#cc6600', '#9933cc', '#ff6666', '#66ccff']; 

  const processedData = data.ringMains.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Ring Mains': isValidNumber(row.ring_mains_total_kwh) ? row.ring_mains_total_kwh : undefined,
    'Libraries': isValidNumber(data.libraries.find((lib: any) =>
      lib.meter_reading_year === row.meter_reading_year &&
      lib.meter_reading_month === row.meter_reading_month
    )?.libraries_total_kwh) ? data.libraries.find((lib: any) =>
      lib.meter_reading_year === row.meter_reading_year &&
      lib.meter_reading_month === row.meter_reading_month
    )?.libraries_total_kwh : undefined,
    'Colleges': isValidNumber(data.colleges.find((col: any) =>
      col.meter_reading_year === row.meter_reading_year &&
      col.meter_reading_month === row.meter_reading_month
    )?.colleges_total_kwh) ? data.colleges.find((col: any) =>
      col.meter_reading_year === row.meter_reading_year &&
      col.meter_reading_month === row.meter_reading_month
    )?.colleges_total_kwh : undefined,
    'Science': isValidNumber(data.science.find((sci: any) =>
      sci.meter_reading_year === row.meter_reading_year &&
      sci.meter_reading_month === row.meter_reading_month
    )?.science_total_kwh) ? data.science.find((sci: any) =>
      sci.meter_reading_year === row.meter_reading_year &&
      sci.meter_reading_month === row.meter_reading_month
    )?.science_total_kwh : undefined,
    'Health Science': isValidNumber(data.healthScience.find((health: any) =>
      health.meter_reading_year === row.meter_reading_year &&
      health.meter_reading_month === row.meter_reading_month
    )?.health_science_total_kwh) ? data.healthScience.find((health: any) =>
      health.meter_reading_year === row.meter_reading_year &&
      health.meter_reading_month === row.meter_reading_month
    )?.health_science_total_kwh : undefined,
    'Humanities': isValidNumber(data.humanities.find((hum: any) =>
      hum.meter_reading_year === row.meter_reading_year &&
      hum.meter_reading_month === row.meter_reading_month
    )?.humanities_total_kwh) ? data.humanities.find((hum: any) =>
      hum.meter_reading_year === row.meter_reading_year &&
      hum.meter_reading_month === row.meter_reading_month
    )?.humanities_total_kwh : undefined
  }));

  const calculateTotals = () => {
    // Calculate sums for each division based on filtered data
    const totals = {
      'Ring Mains': data.ringMains.reduce((sum, row) => sum + (Number(row.ring_mains_total_kwh) || 0), 0),
      'Libraries': data.libraries.reduce((sum, row) => sum + (Number(row.libraries_total_kwh) || 0), 0),
      'Colleges': data.colleges.reduce((sum, row) => sum + (Number(row.colleges_total_kwh) || 0), 0),
      'Science': data.science.reduce((sum, row) => sum + (Number(row.science_total_kwh) || 0), 0),
      'Health Science': data.healthScience.reduce((sum, row) => sum + (Number(row.health_science_total_kwh) || 0), 0),
      'Humanities': data.humanities.reduce((sum, row) => sum + (Number(row.humanities_total_kwh) || 0), 0)
    };
    
    // Calculate total for percentage calculation
    const grandTotal = Object.values(totals).reduce((sum, val) => sum + val, 0);
    
    // Return formatted data with percentages
    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value),
      percentage: ((Number(value) / grandTotal) * 100).toFixed(1)
    }));
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ 
          backgroundColor: 'white', 
          padding: '10px', 
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}>
          <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>{`Date: ${label}`}</p>
          {payload.map((entry: any) => (
            <p key={entry.name} style={{ 
              margin: '3px 0',
              color: entry.color
            }}>
              {`${entry.name}: ${Number(entry.value).toFixed(2)} kWh`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const CustomPieTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ 
          backgroundColor: 'white', 
          padding: '10px', 
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}>
          <p style={{ 
            margin: '0', 
            color: payload[0].payload.fill 
          }}>
            {`${payload[0].name}: ${Number(payload[0].value).toFixed(2)} kWh`}
          </p>
        </div>
      );
    }
    return null;
  };
  

  // Add data processing for Health Science breakdown
  const healthScienceData = data.healthScience.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Taieri Farm': row.taieri_farm_kwh ?? undefined,
    'Medical School': row.med_school_sub_main_kwh ?? undefined,
    'Dental School': row.dental_school_kwh ?? undefined,
    'Hunter Centre': row.hunter_centre_kwh ?? undefined,
    'Physiotherapy': row.physiotherapy_kwh ?? undefined,
    'Research Support': row.research_support_facility_kwh ?? undefined
  }));


  const healthScienceDivisions = [
    { key: 'Taieri Farm', color: '#1f77b4' },
    { key: 'Medical School', color: '#ff7f0e' },
    { key: 'Dental School', color: '#2ca02c' },
    { key: 'Hunter Centre', color: '#d62728' },
    { key: 'Physiotherapy', color: '#9467bd' },
    { key: 'Research Support', color: '#8c564b' }
  ];

  // Add calculation function for Health Science pie chart
  const calculateHealthScienceTotals = () => {
    const totals = {
      'Taieri Farm': data.healthScience.reduce((sum, row) => sum + (Number(row.taieri_farm_kwh) || 0), 0),
      'Medical School': data.healthScience.reduce((sum, row) => sum + (Number(row.med_school_sub_main_kwh) || 0), 0),
      'Dental School': data.healthScience.reduce((sum, row) => sum + (Number(row.dental_school_kwh) || 0), 0),
      'Hunter Centre': data.healthScience.reduce((sum, row) => sum + (Number(row.hunter_centre_kwh) || 0), 0),
      'Physiotherapy': data.healthScience.reduce((sum, row) => sum + (Number(row.physiotherapy_kwh) || 0), 0),
      'Research Support': data.healthScience.reduce((sum, row) => sum + (Number(row.research_support_facility_kwh) || 0), 0)
    };
    
    const grandTotal = Object.values(totals).reduce((sum, val) => sum + val, 0);
    
    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value),
      percentage: ((Number(value) / grandTotal) * 100).toFixed(1)
    }));
  };


    // Add data processing for Science breakdown
    const scienceData = data.science.map((row: any) => ({
      date: `${row.meter_reading_year}-${row.meter_reading_month}`,
      'Survey Marine': row.survey_marine_kwh ?? undefined,
      'Zoology Buildings': row.zoology_buildings_kwh ?? undefined,
      'Botany Tin Hut': row.botany_tin_hut_kwh ?? undefined,
      'Physical Education': row.physical_education_kwh ?? undefined,
      'Owheo Building': row.owheo_building_kwh ?? undefined,
      'Mellor Lab': row.mellor_laboratories_kwh ?? undefined,
      'Microbiology': row.microbiology_kwh ?? undefined,
      'Science 2': row.science_2_kwh ?? undefined,
      'Portobello Marine Lab': row.portobello_marine_lab_kwh ?? undefined,
      'Geology North': row.geology_north ?? undefined,
      'Geology South': row.geology_south ?? undefined
    }));

  const scienceDivisions = [
    { key: 'Survey Marine', color: '#1f77b4' },
    { key: 'Zoology Buildings', color: '#ff7f0e' },
    { key: 'Botany Tin Hut', color: '#2ca02c' },
    { key: 'Physical Education', color: '#d62728' },
    { key: 'Owheo Building', color: '#9467bd' },
    { key: 'Mellor Lab', color: '#8c564b' },
    { key: 'Microbiology', color: '#e377c2' },
    { key: 'Science 2', color: '#7f7f7f' },
    { key: 'Portobello Marine Lab', color: '#bcbd22' },
    { key: 'Geology North', color: '#17becf' },
    { key: 'Geology South', color: '#aec7e8' }
  ];

  // Add calculation function for Science pie chart
  const calculateScienceTotals = () => {
    const totals = {
      'Survey Marine': data.science.reduce((sum, row) => sum + (Number(row.survey_marine_kwh) || 0), 0),
      'Zoology Buildings': data.science.reduce((sum, row) => sum + (Number(row.zoology_buildings_kwh) || 0), 0),
      'Botany Tin Hut': data.science.reduce((sum, row) => sum + (Number(row.botany_tin_hut_kwh) || 0), 0),
      'Physical Education': data.science.reduce((sum, row) => sum + (Number(row.physical_education_kwh) || 0), 0),
      'Owheo Building': data.science.reduce((sum, row) => sum + (Number(row.owheo_building_kwh) || 0), 0),
      'Mellor Lab': data.science.reduce((sum, row) => sum + (Number(row.mellor_laboratories_kwh) || 0), 0),
      'Microbiology': data.science.reduce((sum, row) => sum + (Number(row.microbiology_kwh) || 0), 0),
      'Science 2': data.science.reduce((sum, row) => sum + (Number(row.science_2_kwh) || 0), 0),
      'Portobello Marine Lab': data.science.reduce((sum, row) => sum + (Number(row.portobello_marine_lab_kwh) || 0), 0),
      'Geology North': data.science.reduce((sum, row) => sum + (Number(row.geology_north) || 0), 0),
      'Geology South': data.science.reduce((sum, row) => sum + (Number(row.geology_south) || 0), 0)
    };
    
    const grandTotal = Object.values(totals).reduce((sum, val) => sum + val, 0);
    
    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value),
      percentage: ((Number(value) / grandTotal) * 100).toFixed(1)
    }));
  };

  // Add data processing for Ring Mains breakdown
  const ringMainData = data.ringMains.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Ring Main #1': row.ring_main_1_mp4889_kwh ?? undefined,
    'Ring Main #2': row.ring_main_2_kwh ?? undefined,
    'Ring Main #3': row.ring_main_3_kwh ?? undefined
  }));

  const ringMainDivisions = [
    { key: 'Ring Main #1', color: '#0066cc' },
    { key: 'Ring Main #2', color: '#00cc66' },
    { key: 'Ring Main #3', color: '#cc6600' }
  ];

  // Add calculation function for Ring Mains pie chart
  const calculateRingMainTotals = () => {
    const totals = {
      'Ring Main #1': data.ringMains.reduce((sum, row) => sum + (Number(row.ring_main_1_mp4889_kwh) || 0), 0),
      'Ring Main #2': data.ringMains.reduce((sum, row) => sum + (Number(row.ring_main_2_kwh) || 0), 0),
      'Ring Main #3': data.ringMains.reduce((sum, row) => sum + (Number(row.ring_main_3_kwh) || 0), 0)
    };
    
    const grandTotal = Object.values(totals).reduce((sum, val) => sum + val, 0);
    
    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value),
      percentage: ((Number(value) / grandTotal) * 100).toFixed(1)
    }));
  };


  // Add data processing for Libraries breakdown
  const librariesData = data.libraries.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Hocken Library': row.hocken_library_kwh ?? undefined,
    'UOCOE Robertson': row.robertson_library_kwh ?? undefined,
    'Bill Robertson': row.bill_robertson_library_msb ?? undefined,
    'Sayers Adams MSB': row.sayers_adams_msb ?? undefined,
    'ISB West': row.isb_west_excluding_shops ?? undefined,
    'Richardson': row.richardson_library_block_rising_main ?? undefined
  }));


  const librariesDivisions = [
    { key: 'Hocken Library', color: '#0066cc' },
    { key: 'UOCOE Robertson', color: '#00cc66' },
    { key: 'Bill Robertson', color: '#ff9900' },
    { key: 'Sayers Adams MSB', color: '#9933cc' },
    { key: 'ISB West', color: '#ff6666' },
    { key: 'Richardson', color: '#66ccff' }
  ];

  // Add calculation function for Libraries pie chart
  const calculateLibrariesTotals = () => {
    const totals = {
      'Hocken Library': data.libraries.reduce((sum, row) => sum + (Number(row.hocken_library_kwh) || 0), 0),
      'UOCOE Robertson': data.libraries.reduce((sum, row) => sum + (Number(row.robertson_library_kwh) || 0), 0),
      'Bill Robertson': data.libraries.reduce((sum, row) => sum + (Number(row.bill_robertson_library_msb) || 0), 0),
      'Sayers Adams MSB': data.libraries.reduce((sum, row) => sum + (Number(row.sayers_adams_msb) || 0), 0),
      'ISB West': data.libraries.reduce((sum, row) => sum + (Number(row.isb_west_excluding_shops) || 0), 0),
      'Richardson': data.libraries.reduce((sum, row) => sum + (Number(row.richardson_library_block_rising_main) || 0), 0)
    };
    
    const grandTotal = Object.values(totals).reduce((sum, val) => sum + val, 0);
    
    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value),
      percentage: ((Number(value) / grandTotal) * 100).toFixed(1)
    }));
  };


  // Add data processing for Colleges breakdown
  interface CollegeTotals {
    [key: string]: number;
  }

  // Process data for colleges
  const collegesData = data.colleges.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Castle': row.castle_college_kwh ?? undefined,
    'Hayward': row.hayward_college_kwh ?? undefined,
    'Cumberland': row.cumberland_college_kwh ?? undefined,
    'Executive Residence': row.executive_residence_kwh ?? undefined,
    'Owheo Building': row.owheo_building_kwh ?? undefined,
    'St Margarets': row.st_margarets_college_kwh ?? undefined,
    'Selwyn': row.selwyn_college_kwh ?? undefined,
    'Arana': row.arana_college_main_kwh ?? undefined,
    'Studholm': row.studholm_college_kwh ?? undefined,
    'Carrington': row.carrington_college_kwh ?? undefined,
    'Aquinas': row.aquinas_college_kwh ?? undefined,
    'Caroline Freeman': row.caroline_freeman_college_kwh ?? undefined,
    'Abbey': row.abbey_college_kwh ?? undefined
  }));


  const collegesDivisions = [
    { key: 'Castle', color: '#1f77b4' },
    { key: 'Hayward', color: '#ff7f0e' },
    { key: 'Cumberland', color: '#2ca02c' },
    { key: 'Executive Residence', color: '#d62728' },
    { key: 'Owheo Building', color: '#9467bd' },
    { key: 'St Margarets', color: '#8c564b' },
    { key: 'Selwyn', color: '#e377c2' },
    { key: 'Arana', color: '#7f7f7f' },
    { key: 'Studholm', color: '#bcbd22' },
    { key: 'Carrington', color: '#17becf' },
    { key: 'Aquinas', color: '#aec7e8' },
    { key: 'Caroline Freeman', color: '#ffbb78' },
    { key: 'Abbey', color: '#98df8a' }
  ];

  const calculateCollegesTotals = () => {
    const totals: CollegeTotals = data.colleges.reduce((acc: CollegeTotals, row: any) => {
      acc['Castle'] = (acc['Castle'] || 0) + (Number(row.castle_college_kwh) || 0);
      acc['Hayward'] = (acc['Hayward'] || 0) + (Number(row.hayward_college_kwh) || 0);
      acc['Cumberland'] = (acc['Cumberland'] || 0) + (Number(row.cumberland_college_kwh) || 0);
      acc['Executive Residence'] = (acc['Executive Residence'] || 0) + (Number(row.executive_residence_kwh) || 0);
      acc['Owheo Building'] = (acc['Owheo Building'] || 0) + (Number(row.owheo_building_kwh) || 0);
      acc['St Margarets'] = (acc['St Margarets'] || 0) + (Number(row.st_margarets_college_kwh) || 0);
      acc['Selwyn'] = (acc['Selwyn'] || 0) + (Number(row.selwyn_college_kwh) || 0);
      acc['Arana'] = (acc['Arana'] || 0) + (Number(row.arana_college_main_kwh) || 0);
      acc['Studholm'] = (acc['Studholm'] || 0) + (Number(row.studholm_college_kwh) || 0);
      acc['Carrington'] = (acc['Carrington'] || 0) + (Number(row.carrington_college_kwh) || 0);
      acc['Aquinas'] = (acc['Aquinas'] || 0) + (Number(row.aquinas_college_kwh) || 0);
      acc['Caroline Freeman'] = (acc['Caroline Freeman'] || 0) + (Number(row.caroline_freeman_college_kwh) || 0);
      acc['Abbey'] = (acc['Abbey'] || 0) + (Number(row.abbey_college_kwh) || 0);
      return acc;
    }, {});

    const grandTotal: number = Object.values(totals).reduce((sum: number, val: number) => sum + val, 0);

    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value),
      percentage: ((Number(value) / grandTotal) * 100).toFixed(1)
    }));
  };

  // Add data processing for Humanities breakdown
  const humanitiesData = data.humanities.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Education Main': row.education_main_boiler_room_kwh ?? undefined,
    'Richardson Mains': row.richardson_mains ?? undefined,
    'Arts 1': row.arts_1_submains_msb ?? undefined,
    'Albany & Leith Walk': row.albany_leith_walk ?? undefined,
    'Archway Buildings': row.archway_buildings ?? undefined
  }));


  const humanitiesDivisions = [
    { key: 'Education Main', color: '#1f77b4' },
    { key: 'Richardson Mains', color: '#ff7f0e' },
    { key: 'Arts 1', color: '#2ca02c' },
    { key: 'Albany & Leith Walk', color: '#d62728' },
    { key: 'Archway Buildings', color: '#9467bd' }
  ];

  // Add calculation function for Humanities pie chart
  const calculateHumanitiesTotals = () => {
    const totals: { [key: string]: number } = data.humanities.reduce((acc: any, row: any) => {
      acc['Education Main'] = (acc['Education Main'] || 0) + (Number(row.education_main_boiler_room_kwh) || 0);
      acc['Richardson Mains'] = (acc['Richardson Mains'] || 0) + (Number(row.richardson_mains) || 0);
      acc['Arts 1'] = (acc['Arts 1'] || 0) + (Number(row.arts_1_submains_msb) || 0);
      acc['Albany & Leith Walk'] = (acc['Albany & Leith Walk'] || 0) + (Number(row.albany_leith_walk) || 0);
      acc['Archway Buildings'] = (acc['Archway Buildings'] || 0) + (Number(row.archway_buildings) || 0);
      return acc;
    }, {});

    const grandTotal = Object.values(totals).reduce((sum: number, val: number) => sum + val, 0);

    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value),
      percentage: ((Number(value) / grandTotal) * 100).toFixed(1)
    }));
  };  


  return (
    <div style={{ padding: '20px' }}>
      {/* First Section */}
      <h2>Electricity Consumption Breakdown by Division</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <div style={{ flex: '2', minWidth: '600px', height: '500px' }}>
          <ResponsiveContainer>
            <LineChart 
              data={processedData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={60}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ 
                  value: 'Energy Consumption (kWh)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
                tickFormatter={(value) => value.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '0.9rem' }} />
              {divisions.map((division) => (
                <Line
                  key={division.key}
                  type="monotone"
                  dataKey={division.key}
                  stroke={division.color}
                  strokeWidth={2}
                  dot={{ r: 3, strokeWidth: 2, fill: "white" }}
                  activeDot={{ r: 6, strokeWidth: 0, fill: division.color }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
  
        <div style={{ flex: '1', minWidth: '300px', height: '500px' }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={calculateTotals()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                outerRadius={130}
                fill="#8884d8"
                dataKey="value"
              >
                {calculateTotals().map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
  
      {/* Ring Mains Section */}
      <h2>Ring Mains Consumption Breakdown over Time</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <div style={{ flex: '2', minWidth: '600px', height: '500px' }}>
          <ResponsiveContainer>
            <LineChart 
              data={ringMainData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={60}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ 
                  value: 'Energy Consumption (kWh)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
                tickFormatter={(value) => value.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '0.9rem' }} />
              {ringMainDivisions.map((division) => (
                <Line
                  key={division.key}
                  type="monotone"
                  dataKey={division.key}
                  stroke={division.color}
                  strokeWidth={2}
                  dot={{ r: 3, strokeWidth: 2, fill: "white" }}
                  activeDot={{ r: 6, strokeWidth: 0, fill: division.color }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: '1', minWidth: '300px', height: '500px' }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={calculateRingMainTotals()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={130}
                fill="#8884d8"
                dataKey="value"
              >
                {calculateRingMainTotals().map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={ringMainDivisions[index].color}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Libraries Section */}
      <h2>Libraries Consumption Breakdown over Time</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <div style={{ flex: '2', minWidth: '600px', height: '500px' }}>
          <ResponsiveContainer>
            <LineChart 
              data={librariesData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={60}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ 
                  value: 'Energy Consumption (kWh)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
                tickFormatter={(value) => value.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '0.9rem' }} />
              {librariesDivisions.map((division) => (
                <Line
                  key={division.key}
                  type="monotone"
                  dataKey={division.key}
                  stroke={division.color}
                  strokeWidth={2}
                  dot={{ r: 3, strokeWidth: 2, fill: "white" }}
                  activeDot={{ r: 6, strokeWidth: 0, fill: division.color }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: '1', minWidth: '300px', height: '500px' }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={calculateLibrariesTotals()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={130}
                fill="#8884d8"
                dataKey="value"
              >
                {calculateLibrariesTotals().map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={librariesDivisions[index].color}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <h2>Colleges Consumption Breakdown over Time</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <div style={{ flex: '2', minWidth: '600px', height: '500px' }}>
          <ResponsiveContainer>
            <LineChart 
              data={collegesData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={60}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ 
                  value: 'Energy Consumption (kWh)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
                tickFormatter={(value) => value.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '0.9rem' }} />
              {collegesDivisions.map((division) => (
                <Line
                  key={division.key}
                  type="monotone"
                  dataKey={division.key}
                  stroke={division.color}
                  strokeWidth={2}
                  dot={{ r: 3, strokeWidth: 2, fill: "white" }}
                  activeDot={{ r: 6, strokeWidth: 0, fill: division.color }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: '1', minWidth: '300px', height: '500px' }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={calculateCollegesTotals()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={130}
                fill="#8884d8"
                dataKey="value"
              >
                {calculateCollegesTotals().map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={collegesDivisions[index].color}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Health Science Section */}
      <h2>Health Science Consumption Breakdown over Time</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <div style={{ flex: '2', minWidth: '600px', height: '500px' }}>
          <ResponsiveContainer>
            <LineChart 
              data={healthScienceData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={60}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ 
                  value: 'Energy Consumption (kWh)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
                tickFormatter={(value) => value.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '0.9rem' }} />
              {healthScienceDivisions.map((division) => (
                <Line
                  key={division.key}
                  type="monotone"
                  dataKey={division.key}
                  stroke={division.color}
                  strokeWidth={2}
                  dot={{ r: 3, strokeWidth: 2, fill: "white" }}
                  activeDot={{ r: 6, strokeWidth: 0, fill: division.color }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
  
        <div style={{ flex: '1', minWidth: '300px', height: '500px' }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={calculateHealthScienceTotals()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={130}
                fill="#8884d8"
                dataKey="value"
              >
                {calculateHealthScienceTotals().map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={healthScienceDivisions[index].color}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Science Section */}
      <h2>Science Consumption Breakdown over Time</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <div style={{ flex: '2', minWidth: '600px', height: '500px' }}>
          <ResponsiveContainer>
            <LineChart 
              data={scienceData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={60}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ 
                  value: 'Energy Consumption (kWh)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
                tickFormatter={(value) => value.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '0.9rem' }} />
              {scienceDivisions.map((division) => (
                <Line
                  key={division.key}
                  type="monotone"
                  dataKey={division.key}
                  stroke={division.color}
                  strokeWidth={2}
                  dot={{ r: 3, strokeWidth: 2, fill: "white" }}
                  activeDot={{ r: 6, strokeWidth: 0, fill: division.color }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: '1', minWidth: '300px', height: '500px' }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={calculateScienceTotals()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={130}
                fill="#8884d8"
                dataKey="value"
              >
                {calculateScienceTotals().map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={scienceDivisions[index].color}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Humanities Section */}
      <h2>Humanities Consumption Breakdown over Time</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <div style={{ flex: '2', minWidth: '600px', height: '500px' }}>
          <ResponsiveContainer>
            <LineChart 
              data={humanitiesData}
              margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={60}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ 
                  value: 'Energy Consumption (kWh)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
                tickFormatter={(value) => value.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '0.9rem' }} />
              {humanitiesDivisions.map((division) => (
                <Line
                  key={division.key}
                  type="monotone"
                  dataKey={division.key}
                  stroke={division.color}
                  strokeWidth={2}
                  dot={{ r: 3, strokeWidth: 2, fill: "white" }}
                  activeDot={{ r: 6, strokeWidth: 0, fill: division.color }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: '1', minWidth: '300px', height: '500px' }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={calculateHumanitiesTotals()}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percentage }) => `${name}: ${percentage}%`}
                outerRadius={130}
                fill="#8884d8"
                dataKey="value"
              >
                {calculateHumanitiesTotals().map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={humanitiesDivisions[index].color}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};


export default ElectricityGraphs;