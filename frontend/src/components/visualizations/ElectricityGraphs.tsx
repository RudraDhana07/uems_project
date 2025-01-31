// src/components/visualizations/ElectricityGraphs.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

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
    'Ring Mains': row.ring_mains_total_kwh || 0,
    'Libraries': data.libraries.find((lib: any) => 
      lib.meter_reading_year === row.meter_reading_year && 
      lib.meter_reading_month === row.meter_reading_month
    )?.libraries_total_kwh || 0,
    'Colleges': data.colleges.find((col: any) => 
      col.meter_reading_year === row.meter_reading_year && 
      col.meter_reading_month === row.meter_reading_month
    )?.colleges_total_kwh || 0,
    'Science': data.science.find((sci: any) => 
      sci.meter_reading_year === row.meter_reading_year && 
      sci.meter_reading_month === row.meter_reading_month
    )?.science_total_kwh || 0,
    'Health Science': data.healthScience.find((health: any) => 
      health.meter_reading_year === row.meter_reading_year && 
      health.meter_reading_month === row.meter_reading_month
    )?.health_science_total_kwh || 0,
    'Humanities': data.humanities.find((hum: any) => 
      hum.meter_reading_year === row.meter_reading_year && 
      hum.meter_reading_month === row.meter_reading_month
    )?.humanities_total_kwh || 0
  }));

  const calculateTotals = () => {
    const totals = {
      'Ring Mains': data.ringMains?.[0]?.ring_mains_total_kwh || 0,
      'Libraries': data.libraries?.[0]?.libraries_total_kwh || 0,
      'Colleges': data.colleges?.[0]?.colleges_total_kwh || 0,
      'Science': data.science?.[0]?.science_total_kwh || 0,
      'Health Science': data.healthScience?.[0]?.health_science_total_kwh || 0,
      'Humanities': data.humanities?.[0]?.humanities_total_kwh || 0
    };

    return Object.entries(totals).map(([name, value]) => ({
      name,
      value: Number(value)
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
    'Taieri Farm': row.taieri_farm_kwh || 0,
    'Medical School': row.med_school_sub_main_kwh || 0,
    'Dental School': row.dental_school_kwh || 0,
    'Hunter Centre': row.hunter_centre_kwh || 0,
    'Physiotherapy': row.physiotherapy_kwh || 0,
    'Research Support': row.research_support_facility_kwh || 0
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
    // Get the latest data point for pie chart
    const latestData = data.healthScience?.[0];
    const total = latestData?.health_science_total_kwh || 0;

    const totals = [
      { name: 'Taieri Farm', value: latestData?.taieri_farm_kwh || 0 },
      { name: 'Medical School', value: latestData?.med_school_sub_main_kwh || 0 },
      { name: 'Dental School', value: latestData?.dental_school_kwh || 0 },
      { name: 'Hunter Centre', value: latestData?.hunter_centre_kwh || 0 },
      { name: 'Physiotherapy', value: latestData?.physiotherapy_kwh || 0 },
      { name: 'Research Support', value: latestData?.research_support_facility_kwh || 0 }
    ];

    // Calculate percentages based on total
    return totals.map(item => ({
      ...item,
      percentage: ((item.value / total) * 100).toFixed(1)
    }));
  };


    // Add data processing for Science breakdown
  const scienceData = data.science.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Survey Marine': row.survey_marine_kwh || 0,
    'Zoology Buildings': row.zoology_buildings_kwh || 0,
    'Botany Tin Hut': row.botany_tin_hut_kwh || 0,
    'Physical Education': row.physical_education_kwh || 0,
    'Owheo Building': row.owheo_building_kwh || 0,
    'Mellor Lab': row.mellor_laboratories_kwh || 0,
    'Microbiology': row.microbiology_kwh || 0,
    'Science 2': row.science_2_kwh || 0,
    'Portobello Marine Lab': row.portobello_marine_lab_kwh || 0,
    'Geology North': row.geology_north || 0,
    'Geology South': row.geology_south || 0
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
    const latestData = data.science?.[0];
    const total = latestData?.science_total_kwh || 0;

    const totals = [
      { name: 'Survey Marine', value: latestData?.survey_marine_kwh || 0 },
      { name: 'Zoology Buildings', value: latestData?.zoology_buildings_kwh || 0 },
      { name: 'Botany Tin Hut', value: latestData?.botany_tin_hut_kwh || 0 },
      { name: 'Physical Education', value: latestData?.physical_education_kwh || 0 },
      { name: 'Owheo Building', value: latestData?.owheo_building_kwh || 0 },
      { name: 'Mellor Lab', value: latestData?.mellor_laboratories_kwh || 0 },
      { name: 'Microbiology', value: latestData?.microbiology_kwh || 0 },
      { name: 'Science 2', value: latestData?.science_2_kwh || 0 },
      { name: 'Portobello Marine Lab', value: latestData?.portobello_marine_lab_kwh || 0 },
      { name: 'Geology North', value: latestData?.geology_north || 0 },
      { name: 'Geology South', value: latestData?.geology_south || 0 }
    ];

    return totals.map(item => ({
      ...item,
      percentage: ((item.value / total) * 100).toFixed(1)
    }));
  };

  // Add data processing for Ring Mains breakdown
  const ringMainData = data.ringMains.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Ring Main #1': row.ring_main_1_mp4889_kwh || 0,
    'Ring Main #2': row.ring_main_2_kwh || 0,
    'Ring Main #3': row.ring_main_3_kwh || 0
  }));

  const ringMainDivisions = [
    { key: 'Ring Main #1', color: '#0066cc' },
    { key: 'Ring Main #2', color: '#00cc66' },
    { key: 'Ring Main #3', color: '#cc6600' }
  ];

  // Add calculation function for Ring Mains pie chart
  const calculateRingMainTotals = () => {
    const latestData = data.ringMains?.[0];
    const total = latestData?.ring_mains_total_kwh || 0;

    const totals = [
      { name: 'Ring Main #1', value: latestData?.ring_main_1_mp4889_kwh || 0 },
      { name: 'Ring Main #2', value: latestData?.ring_main_2_kwh || 0 },
      { name: 'Ring Main #3', value: latestData?.ring_main_3_kwh || 0 }
    ];

    return totals.map(item => ({
      ...item,
      percentage: ((item.value / total) * 100).toFixed(1)
    }));
  };


  // Add data processing for Libraries breakdown
  const librariesData = data.libraries.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Hocken Library': row.hocken_library_kwh || 0,
    'UOCOE Robertson': row.robertson_library_kwh || 0,
    'Bill Robertson': row.bill_robertson_library_msb || 0,
    'Sayers Adams MSB': row.sayers_adams_msb || 0,
    'ISB West': row.isb_west_excluding_shops || 0,
    'Richardson': row.richardson_library_block_rising_main || 0
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
    const latestData = data.libraries?.[0];
    const total = latestData?.libraries_total_kwh || 0;

    const totals = [
      { name: 'Hocken Library', value: latestData?.hocken_library_kwh || 0 },
      { name: 'UOCOE Robertson', value: latestData?.robertson_library_kwh || 0 },
      { name: 'Bill Robertson', value: latestData?.bill_robertson_library_msb || 0 },
      { name: 'Sayers Adams MSB', value: latestData?.sayers_adams_msb || 0 },
      { name: 'ISB West', value: latestData?.isb_west_excluding_shops || 0 },
      { name: 'Richardson', value: latestData?.richardson_library_block_rising_main || 0 }
    ];

    return totals.map(item => ({
      ...item,
      percentage: ((item.value / total) * 100).toFixed(1)
    }));
  };


  // Add data processing for Colleges breakdown
  interface CollegeTotals {
    [key: string]: number;
  }

  // Process data for colleges
  const collegesData = data.colleges.map((row: any) => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    'Castle': row.castle_college_kwh || 0,
    'Hayward': row.hayward_college_kwh || 0,
    'Cumberland': row.cumberland_college_kwh || 0,
    'Executive Residence': row.executive_residence_kwh || 0,
    'Owheo Building': row.owheo_building_kwh || 0,
    'St Margarets': row.st_margarets_college_kwh || 0,
    'Selwyn': row.selwyn_college_kwh || 0,
    'Arana': row.arana_college_main_kwh || 0,
    'Studholm': row.studholm_college_kwh || 0,
    'Carrington': row.carrington_college_kwh || 0,
    'Aquinas': row.aquinas_college_kwh || 0,
    'Caroline Freeman': row.caroline_freeman_college_kwh || 0,
    'Abbey': row.abbey_college_kwh || 0
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
    'Education Main': row.education_main_boiler_room_kwh || 0,
    'Richardson Mains': row.richardson_mains || 0,
    'Arts 1': row.arts_1_submains_msb || 0,
    'Albany & Leith Walk': row.albany_leith_walk || 0,
    'Archway Buildings': row.archway_buildings || 0
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
              <Tooltip formatter={(value: number) => [`${value.toFixed(2)} kWh`, '']} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};


export default ElectricityGraphs;