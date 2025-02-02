// frontend/src/components/views/StreamElecDataView.tsx

import React, { useState, useEffect } from 'react';
import { Tabs, Tab, CircularProgress } from '@mui/material';
import EnergyUsageChart from '../visualizations/EnergyUsageChart';
import ElectricityGraphs from '../visualizations/ElectricityGraphs';
import { StreamElecDataRow } from '../../types/streamElecData';



interface ColumnGroup {
    title: string;
    subColumns: {
        key: string;
        label: string;
    }[];
}

interface ChartConfig {
    columns: {
      key: string;
      name: string;
      color: string;
    }[];
  }
 

  const ringMainsGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'Ring Main #1 MP4889',
        subColumns: [
            { key: 'ring_main_1_mp4889_kwh', label: 'kWh' },
            { key: 'ring_main_1_mp4889_pf', label: 'PF' }
        ]
    },
    {
        title: 'Ring Main #2',
        subColumns: [
            { key: 'ring_main_2_kwh', label: 'kWh' },
            { key: 'ring_main_2_pf', label: 'PF' }
        ]
    },
    {
        title: 'Ring Main #3',
        subColumns: [
            { key: 'ring_main_3_kwh', label: 'kWh' },
            { key: 'ring_main_3_pf', label: 'PF' }
        ]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'ring_mains_total_kwh', label: 'kWh' }]
    }
];

const librariesGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'E902 Hocken Library',
        subColumns: [
            { key: 'hocken_library_kwh', label: 'kWh' },
            { key: 'hocken_library_pf', label: 'PF' }
        ]
    },
    {
        title: 'F813 UOCOE Robertson Library',
        subColumns: [
            { key: 'robertson_library_kwh', label: 'kWh' },
            { key: 'robertson_library_pf', label: 'PF' }
        ]
    },
    {
        title: 'F813 Bill Robertson Library',
        subColumns: [{ key: 'bill_robertson_library_msb', label: 'MSB' }]
    },
    {
        title: 'D203 Sayers',
        subColumns: [{ key: 'sayers_adams_msb', label: 'Adams MSB' }]
    },
    {
        title: 'F419 ISB West',
        subColumns: [{ key: 'isb_west_excluding_shops', label: 'Excluding Shops' }]
    },
    {
        title: 'F505 Richardson Library',
        subColumns: [{ key: 'richardson_library_block_rising_main', label: 'Block Rising Main' }]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'libraries_total_kwh', label: 'kWh' }]
    }
];

const collegesGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'C405 192 Castle College',
        subColumns: [
            { key: 'castle_college_kwh', label: 'kWh' },
            { key: 'castle_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'D402 Hayward College',
        subColumns: [
            { key: 'hayward_college_kwh', label: 'kWh' },
            { key: 'hayward_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'D40X Cumberland College',
        subColumns: [
            { key: 'cumberland_college_kwh', label: 'kWh' },
            { key: 'cumberland_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'F711 Executive Residence',
        subColumns: [
            { key: 'executive_residence_kwh', label: 'kWh' },
            { key: 'executive_residence_pf', label: 'PF' }
        ]
    },
    {
        title: 'F812 UOCOE Owheo Building',
        subColumns: [
            { key: 'owheo_building_kwh', label: 'kWh' },
            { key: 'owheo_building_pf', label: 'PF' }
        ]
    },
    {
        title: 'G608 St Margarets College',
        subColumns: [
            { key: 'st_margarets_college_kwh', label: 'kWh' },
            { key: 'st_margarets_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'H41X Selwyn College',
        subColumns: [
            { key: 'selwyn_college_kwh', label: 'kWh E2' },
            { key: 'selwyn_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'H633 Arana College',
        subColumns: [
            { key: 'arana_college_main_kwh', label: 'kWh' },
            { key: 'arana_college_main_pf', label: 'PF' }
        ]
    },
    {
        title: 'H71X Studholm College',
        subColumns: [
            { key: 'studholm_college_kwh', label: 'kWh E2' },
            { key: 'studholm_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'J126 Carrington College',
        subColumns: [
            { key: 'carrington_college_kwh', label: 'kWh' },
            { key: 'carrington_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'J14X Aquinas College',
        subColumns: [
            { key: 'aquinas_college_kwh', label: 'kWh' },
            { key: 'aquinas_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'J303 Caroline Freeman College',
        subColumns: [
            { key: 'caroline_freeman_college_kwh', label: 'kWh' },
            { key: 'caroline_freeman_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'K427 Abbey College',
        subColumns: [
            { key: 'abbey_college_kwh', label: 'kWh' },
            { key: 'abbey_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'colleges_total_kwh', label: 'kWh' }]
    }
];

const scienceGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'D403 Survey & Marine',
        subColumns: [
            { key: 'survey_marine_kwh', label: 'kWh' },
            { key: 'survey_marine_pf', label: 'PF' }
        ]
    },
    {
        title: 'E212 Zoology Buildings',
        subColumns: [
            { key: 'zoology_buildings_kwh', label: 'kWh' },
            { key: 'zoology_buildings_pf', label: 'PF' }
        ]
    },
    {
        title: 'F315 Botany Tin Hut',
        subColumns: [
            { key: 'botany_tin_hut_kwh', label: 'kWh' },
            { key: 'botany_tin_hut_pf', label: 'PF' }
        ]
    },
    {
        title: 'F325 Physical Education',
        subColumns: [
            { key: 'physical_education_kwh', label: 'kWh' },
            { key: 'physical_education_pf', label: 'PF' }
        ]
    },
    {
        title: 'F812 UOCOE Owheo Building',
        subColumns: [
            { key: 'owheo_building_kwh', label: 'kWh' },
            { key: 'owheo_building_pf', label: 'PF' }
        ]
    },
    {
        title: 'G401 Mellor Laboratories',
        subColumns: [
            { key: 'mellor_laboratories_kwh', label: 'kWh' },
            { key: 'mellor_laboratories_pf', label: 'PF' }
        ]
    },
    {
        title: 'G404 Microbiology',
        subColumns: [
            { key: 'microbiology_kwh', label: 'kWh' },
            { key: 'microbiology_pf', label: 'PF' }
        ]
    },
    {
        title: 'G413 Science 2',
        subColumns: [
            { key: 'science_2_kwh', label: 'kWh' },
            { key: 'science_2_pf', label: 'PF' }
        ]
    },
    {
        title: 'J960 Portobello Marine Lab',
        subColumns: [
            { key: 'portobello_marine_lab_kwh', label: 'kWh' },
            { key: 'portobello_marine_lab_pf', label: 'PF' }
        ]
    },
    {
        title: 'G505 Geology',
        subColumns: [
            { key: 'geology_north', label: 'North' },
            { key: 'geology_south', label: 'South' }
        ]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'science_total_kwh', label: 'kWh' }]
    }
];

const healthScienceGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'A161 Taieri Farm',
        subColumns: [
            { key: 'taieri_farm_kwh', label: 'kWh' },
            { key: 'taieri_farm_pf', label: 'PF' }
        ]
    },
    {
        title: 'D20X Med School Sub Main',
        subColumns: [
            { key: 'med_school_sub_main_kwh', label: 'kWh' },
            { key: 'med_school_sub_main_pf', label: 'PF' }
        ]
    },
    {
        title: 'E214 Otago Dental School',
        subColumns: [
            { key: 'dental_school_kwh', label: 'kWh' },
            { key: 'dental_school_pf', label: 'PF' }
        ]
    },
    {
        title: 'E301 Hunter Centre',
        subColumns: [
            { key: 'hunter_centre_kwh', label: 'kWh' },
            { key: 'hunter_centre_pf', label: 'PF' }
        ]
    },
    {
        title: 'E305 Physiotherapy',
        subColumns: [
            { key: 'physiotherapy_kwh', label: 'kWh' },
            { key: 'physiotherapy_pf', label: 'PF' }
        ]
    },
    {
        title: 'E325 Research Support Facility',
        subColumns: [
            { key: 'research_support_facility_kwh', label: 'kWh' },
            { key: 'research_support_facility_pf', label: 'PF' }
        ]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'health_science_total_kwh', label: 'kWh' }]
    }
];

const humanitiesGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'F9XX College of Education main',
        subColumns: [
            { key: 'education_main_boiler_room_kwh', label: 'kWh' },
            { key: 'education_main_boiler_room_pf', label: 'PF' }
        ]
    },
    {
        title: 'F505 Richardson',
        subColumns: [{ key: 'richardson_mains', label: 'Mains' }]
    },
    {
        title: 'F518 Arts 1',
        subColumns: [{ key: 'arts_1_submains_msb', label: 'Submains MSB' }]
    },
    {
        title: 'Albany & Leith Walk',
        subColumns: [{ key: 'albany_leith_walk', label: 'F516 97, F517 99 Albany, F513 262 Leith Walk' }]
    },
    {
        title: 'G506/07 Archway',
        subColumns: [{ key: 'archway_buildings', label: 'Buildings (incl. Allen & Marama Hall)' }]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'humanities_total_kwh', label: 'kWh' }]
    }
];

const obsPsychologyGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'F614 School of Business',
        subColumns: [
            { key: 'business_incomer_1_lower', label: 'Incomer 1 (Lower floors)' },
            { key: 'business_incomer_2_upper', label: 'Incomer 2 (Upper floors)' }
        ]
    },
    {
        title: 'F618 Psychology',
        subColumns: [{ key: 'psychology_substation_goddard', label: 'Substation - Goddard' }]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'obs_psychology_total_kwh', label: 'kWh' }]
    }
];

const totalStreamGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'Ring Main #1 MP4889',
        subColumns: [
            { key: 'ring_main_1_mp4889_kwh', label: 'kWh' },
            { key: 'ring_main_1_mp4889_pf', label: 'PF' }
        ]
    },
    {
        title: 'Ring Main #2',
        subColumns: [
            { key: 'ring_main_2_kwh', label: 'kWh' },
            { key: 'ring_main_2_pf', label: 'PF' }
        ]
    },
    {
        title: 'Ring Main #3',
        subColumns: [
            { key: 'ring_main_3_kwh', label: 'kWh' },
            { key: 'ring_main_3_pf', label: 'PF' }
        ]
    },
    {
        title: 'A161 Taieri Farm',
        subColumns: [
            { key: 'taieri_farm_kwh', label: 'kWh' },
            { key: 'taieri_farm_pf', label: 'PF' }
        ]
    },
    {
        title: 'C405 192 Castle College',
        subColumns: [
            { key: 'castle_college_kwh', label: 'kWh' },
            { key: 'castle_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'D20X Med School Sub Main',
        subColumns: [
            { key: 'med_school_sub_main_kwh', label: 'kWh' },
            { key: 'med_school_sub_main_pf', label: 'PF' }
        ]
    },
    {
        title: 'D402 Hayward College',
        subColumns: [
            { key: 'hayward_college_kwh', label: 'kWh' },
            { key: 'hayward_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'D403 Survey & Marine',
        subColumns: [
            { key: 'survey_marine_kwh', label: 'kWh' },
            { key: 'survey_marine_pf', label: 'PF' }
        ]
    },
    {
        title: 'D40X Cumberland College',
        subColumns: [
            { key: 'cumberland_college_kwh', label: 'kWh' },
            { key: 'cumberland_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'E201 School of Dentistry',
        subColumns: [
            { key: 'school_of_dentistry_kwh', label: 'kWh' },
            { key: 'school_of_dentistry_pf', label: 'PF' }
        ]
    },
    {
        title: 'E212 Zoology Buildings',
        subColumns: [
            { key: 'zoology_buildings_kwh', label: 'kWh' },
            { key: 'zoology_buildings_pf', label: 'PF' }
        ]
    },
    {
        title: 'E214 Otago Dental School',
        subColumns: [
            { key: 'dental_school_kwh', label: 'kWh' },
            { key: 'dental_school_pf', label: 'PF' }
        ]
    },
    {
        title: 'E301 Hunter Centre',
        subColumns: [
            { key: 'hunter_centre_kwh', label: 'kWh' },
            { key: 'hunter_centre_pf', label: 'PF' }
        ]
    },
    {
        title: 'E305 Physiotherapy',
        subColumns: [
            { key: 'physiotherapy_kwh', label: 'kWh' },
            { key: 'physiotherapy_pf', label: 'PF' }
        ]
    },
    {
        title: 'E308 Student Health',
        subColumns: [
            { key: 'student_health_kwh', label: 'kWh' },
            { key: 'student_health_pf', label: 'PF' }
        ]
    },
    {
        title: 'E325 Research Support Facility',
        subColumns: [
            { key: 'research_support_facility_kwh', label: 'kWh' },
            { key: 'research_support_facility_pf', label: 'PF' }
        ]
    },
    {
        title: 'E902 Hocken Library',
        subColumns: [
            { key: 'hocken_library_kwh', label: 'kWh' },
            { key: 'hocken_library_pf', label: 'PF' }
        ]
    },
    {
        title: 'F204 444 Great King Street',
        subColumns: [
            { key: 'great_king_street_kwh', label: 'kWh' },
            { key: 'great_king_street_pf', label: 'PF' }
        ]
    },
    {
        title: 'F315 Botany Tin Hut',
        subColumns: [
            { key: 'botany_tin_hut_kwh', label: 'kWh' },
            { key: 'botany_tin_hut_pf', label: 'PF' }
        ]
    },
    {
        title: 'F325 Physical Education',
        subColumns: [
            { key: 'physical_education_kwh', label: 'kWh' },
            { key: 'physical_education_pf', label: 'PF' }
        ]
    },
    {
        title: 'F711 Executive Residence',
        subColumns: [
            { key: 'executive_residence_kwh', label: 'kWh' },
            { key: 'executive_residence_pf', label: 'PF' }
        ]
    },
    {
        title: 'F812 UOCOE Owheo Building',
        subColumns: [
            { key: 'owheo_building_kwh', label: 'kWh' },
            { key: 'owheo_building_pf', label: 'PF' }
        ]
    },
    {
        title: 'F813 UOCOE Robertson Library',
        subColumns: [
            { key: 'robertson_library_kwh', label: 'kWh' },
            { key: 'robertson_library_pf', label: 'PF' }
        ]
    },
    {
        title: 'F940 Plaza Building',
        subColumns: [
            { key: 'plaza_building_kwh', label: 'kWh' },
            { key: 'plaza_building_pf', label: 'PF' }
        ]
    },
    {
        title: 'F9XX College of Education main',
        subColumns: [
            { key: 'education_main_boiler_room_kwh', label: 'kWh' },
            { key: 'education_main_boiler_room_pf', label: 'PF' }
        ]
    },
    {
        title: 'G401 Mellor Laboratories',
        subColumns: [
            { key: 'mellor_laboratories_kwh', label: 'kWh' },
            { key: 'mellor_laboratories_pf', label: 'PF' }
        ]
    },
    {
        title: 'G403 Biochemistry',
        subColumns: [
            { key: 'biochemistry_kwh', label: 'kWh' },
            { key: 'biochemistry_pf', label: 'PF' }
        ]
    },
    {
        title: 'G404 Microbiology',
        subColumns: [
            { key: 'microbiology_kwh', label: 'kWh' },
            { key: 'microbiology_pf', label: 'PF' }
        ]
    },
    {
        title: 'G413 Science 2',
        subColumns: [
            { key: 'science_2_kwh', label: 'kWh' },
            { key: 'science_2_pf', label: 'PF' }
        ]
    },
    {
        title: 'G608 St Margarets College',
        subColumns: [
            { key: 'st_margarets_college_kwh', label: 'kWh' },
            { key: 'st_margarets_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'G60X UNICOL',
        subColumns: [
            { key: 'unicol_kwh', label: 'kWh' },
            { key: 'unicol_pf', label: 'PF' }
        ]
    },
    {
        title: 'H41X Selwyn College',
        subColumns: [
            { key: 'selwyn_college_kwh', label: 'kWh E2' },
            { key: 'selwyn_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'H633 Arana College main',
        subColumns: [
            { key: 'arana_college_main_kwh', label: 'kWh' },
            { key: 'arana_college_main_pf', label: 'PF' }
        ]
    },
    {
        title: 'H71X Studholm College',
        subColumns: [
            { key: 'studholm_college_kwh', label: 'kWh E2' },
            { key: 'studholm_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'J126 Carrington College',
        subColumns: [
            { key: 'carrington_college_kwh', label: 'kWh' },
            { key: 'carrington_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'J14X Aquinas College',
        subColumns: [
            { key: 'aquinas_college_kwh', label: 'kWh' },
            { key: 'aquinas_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'J303 Caroline Freeman College',
        subColumns: [
            { key: 'caroline_freeman_college_kwh', label: 'kWh' },
            { key: 'caroline_freeman_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'J960 Portobello Marine Lab',
        subColumns: [
            { key: 'portobello_marine_lab_kwh', label: 'kWh' },
            { key: 'portobello_marine_lab_pf', label: 'PF' }
        ]
    },
    {
        title: 'K427 Abbey College',
        subColumns: [
            { key: 'abbey_college_kwh', label: 'kWh' },
            { key: 'abbey_college_pf', label: 'PF' }
        ]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'total_stream_dn_electricity_kwh', label: 'kWh' }]
    }
];

const itsServersGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'F204 444 Great King Street',
        subColumns: [
            { key: 'great_king_street_kwh', label: 'kWh' },
            { key: 'great_king_street_pf', label: 'PF' }
        ]
    },
    {
        title: 'E305 325 Great King',
        subColumns: [
            { key: 'great_king_main_meter', label: 'Main Meter' },
            { key: 'great_king_physiotherapy', label: 'Physiotherapy' }
        ]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'its_servers_total_kwh', label: 'kWh' }]
    }
];

const schoolOfMedicineGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'XC01 UoO School of Medicine ChCh',
        subColumns: [
            { key: 'school_of_medicine_chch_kwh', label: 'kWh' },
            { key: 'school_of_medicine_chch_pf', label: 'PF' }
        ]
    }
];

const commerceGroups: ColumnGroup[] = [
    {
        title: 'Month',
        subColumns: [{ key: 'meter_reading_month', label: '' }]
    },
    {
        title: 'Year',
        subColumns: [{ key: 'meter_reading_year', label: '' }]
    },
    {
        title: 'F614 School of Business',
        subColumns: [
            { key: 'business_incomer_1_lower', label: 'Incomer 1 (Lower floors)' },
            { key: 'business_incomer_2_upper', label: 'Incomer 2 (Upper floors)' }
        ]
    },
    {
        title: 'F618 Psychology',
        subColumns: [{ key: 'psychology_substation_goddard', label: 'Substation - Goddard' }]
    },
    {
        title: 'Total',
        subColumns: [{ key: 'commerce_total_kwh', label: 'kWh' }]
    }
];  


const columnGroups = {
    ringMains: ringMainsGroups,
    libraries: librariesGroups,
    colleges: collegesGroups,
    science: scienceGroups,
    healthScience: healthScienceGroups,
    humanities: humanitiesGroups,
    obsPsychology: obsPsychologyGroups,
    totalStream: totalStreamGroups,
    itsServers: itsServersGroups,
    schoolOfMedicine: schoolOfMedicineGroups,
    commerce: commerceGroups
};

// Finally define the mapping types
type ColumnGroupsMapping = typeof columnGroups;
type ChartConfigsMapping = {
    [K in keyof typeof columnGroups]: ChartConfig;
};


const tableStyles = {
    container: {
        margin: '20px',
        overflowX: 'auto' as const,
        backgroundColor: '#fff',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    },
    table: {
        width: '100%',
        borderCollapse: 'collapse' as const,
        border: '2px solid #ccc',
        marginBottom: '8px'
    },
    mainHeader: {
        backgroundColor: '#d1e9ff',
        padding: '12px 8px',
        border: '2px solid #ccc',
        borderBottom: '2px solid #999',
        position: 'sticky' as const,
        top: 0,
        whiteSpace: 'nowrap' as const,
        fontSize: '0.9rem',
        fontWeight: 'bold',
        textAlign: 'center' as const
    },
    subHeader: {
        backgroundColor: '#e6f3ff',
        padding: '8px 4px',
        border: '1px solid #ccc',
        borderTop: '2px solid #999',
        position: 'sticky' as const,
        top: '43px',
        whiteSpace: 'nowrap' as const,
        fontSize: '0.85rem',
        textAlign: 'center' as const
    },
    td: {
        padding: '6px 4px',
        border: '1px solid #ddd',
        whiteSpace: 'nowrap' as const,
        textAlign: 'right' as const,
        fontSize: '0.9rem'
    },
    valueCell: {
        backgroundColor: '#fff',
        transition: 'background-color 0.2s'
    }
};


const chartConfigs: Partial<ChartConfigsMapping> = {
    ringMains: {
      columns: [
        { key: 'ring_main_1_mp4889_kwh', name: 'Ring Main #1 MP4889', color: '#0066cc' },
        { key: 'ring_main_2_kwh', name: 'Ring Main #2', color: '#00cc66' },
        { key: 'ring_main_3_kwh', name: 'Ring Main #3', color: '#cc6600' },
        { key: 'ring_mains_total_kwh', name: 'Total', color: '#ff0000' }
      ]
    },
    libraries: {
        columns: [
          { key: 'hocken_library_kwh', name: 'Hocken Library', color: '#0066cc' },
          { key: 'robertson_library_kwh', name: 'UOCOE Robertson Library', color: '#00cc66' },
          { key: 'bill_robertson_library_msb', name: 'Bill Robertson Library MSB', color: '#ff9900' },
          { key: 'sayers_adams_msb', name: 'Sayers Adams MSB', color: '#9933cc' },
          { key: 'isb_west_excluding_shops', name: 'ISB West', color: '#ff6666' },
          { key: 'richardson_library_block_rising_main', name: 'Richardson Library', color: '#66ccff' },
          { key: 'libraries_total_kwh', name: 'Total', color: '#ff0000' }
        ]
      },
      colleges: {
        columns: [
          { key: 'castle_college_kwh', name: 'Castle College', color: '#1f77b4' },
          { key: 'hayward_college_kwh', name: 'Hayward College', color: '#ff7f0e' },
          { key: 'cumberland_college_kwh', name: 'Cumberland College', color: '#2ca02c' },
          { key: 'executive_residence_kwh', name: 'Executive Residence', color: '#d62728' },
          { key: 'owheo_building_kwh', name: 'Owheo Building', color: '#9467bd' },
          { key: 'st_margarets_college_kwh', name: 'St Margarets College', color: '#8c564b' },
          { key: 'selwyn_college_kwh', name: 'Selwyn College', color: '#e377c2' },
          { key: 'arana_college_main_kwh', name: 'Arana College', color: '#7f7f7f' },
          { key: 'studholm_college_kwh', name: 'Studholm College', color: '#bcbd22' },
          { key: 'carrington_college_kwh', name: 'Carrington College', color: '#17becf' },
          { key: 'aquinas_college_kwh', name: 'Aquinas College', color: '#aec7e8' },
          { key: 'caroline_freeman_college_kwh', name: 'Caroline Freeman College', color: '#ffbb78' },
          { key: 'abbey_college_kwh', name: 'Abbey College', color: '#98df8a' },
          { key: 'colleges_total_kwh', name: 'Total', color: '#ff0000' }
        ]
    },
    science: {
        columns: [
          { key: 'survey_marine_kwh', name: 'Survey Marine', color: '#1f77b4' },
          { key: 'zoology_buildings_kwh', name: 'Zoology Buildings', color: '#ff7f0e' },
          { key: 'botany_tin_hut_kwh', name: 'Botany Tin Hut', color: '#2ca02c' },
          { key: 'physical_education_kwh', name: 'Physical Education', color: '#d62728' },
          { key: 'owheo_building_kwh', name: 'Owheo Building', color: '#9467bd' },
          { key: 'mellor_laboratories_kwh', name: 'Mellor Laboratories', color: '#8c564b' },
          { key: 'microbiology_kwh', name: 'Microbiology', color: '#e377c2' },
          { key: 'science_2_kwh', name: 'Science 2', color: '#7f7f7f' },
          { key: 'portobello_marine_lab_kwh', name: 'Portobello Marine Lab', color: '#bcbd22' },
          { key: 'geology_north', name: 'Geology North', color: '#17becf' },
          { key: 'geology_south', name: 'Geology South', color: '#aec7e8' },
          { key: 'science_total_kwh', name: 'Total', color: '#ff0000' }
        ]
    },
    healthScience: {
        columns: [
          { key: 'taieri_farm_kwh', name: 'Taieri Farm', color: '#1f77b4' },
          { key: 'med_school_sub_main_kwh', name: 'Medical School', color: '#ff7f0e' },
          { key: 'dental_school_kwh', name: 'Dental School', color: '#2ca02c' },
          { key: 'hunter_centre_kwh', name: 'Hunter Centre', color: '#d62728' },
          { key: 'physiotherapy_kwh', name: 'Physiotherapy', color: '#9467bd' },
          { key: 'research_support_facility_kwh', name: 'Research Support Facility', color: '#8c564b' },
          { key: 'health_science_total_kwh', name: 'Total', color: '#ff0000' }
        ]
    },
    humanities: {
        columns: [
          { key: 'education_main_boiler_room_kwh', name: 'Education Main', color: '#1f77b4' },
          { key: 'richardson_mains', name: 'Richardson Mains', color: '#ff7f0e' },
          { key: 'arts_1_submains_msb', name: 'Arts 1', color: '#2ca02c' },
          { key: 'albany_leith_walk', name: 'Albany & Leith Walk', color: '#d62728' },
          { key: 'archway_buildings', name: 'Archway Buildings', color: '#9467bd' },
          { key: 'humanities_total_kwh', name: 'Total', color: '#ff0000' }
        ]
      },
      obsPsychology: {
        columns: [
          { key: 'business_incomer_1_lower', name: 'Business Lower Floors', color: '#1f77b4' },
          { key: 'business_incomer_2_upper', name: 'Business Upper Floors', color: '#ff7f0e' },
          { key: 'psychology_substation_goddard', name: 'Psychology Goddard', color: '#2ca02c' },
          { key: 'obs_psychology_total_kwh', name: 'Total', color: '#ff0000' }
        ]
      },
      itsServers: {
        columns: [
          { key: 'great_king_street_kwh', name: 'Great King Street', color: '#1f77b4' },
          { key: 'great_king_main_meter', name: 'Great King Main', color: '#ff7f0e' },
          { key: 'great_king_physiotherapy', name: 'Great King Physiotherapy', color: '#2ca02c' },
          { key: 'its_servers_total_kwh', name: 'Total', color: '#ff0000' }
        ]
      },
      schoolOfMedicine: {
        columns: [
          { key: 'school_of_medicine_chch_kwh', name: 'School of Medicine ChCh', color: '#1f77b4' }
        ]
      },
      commerce: {
        columns: [
          { key: 'business_incomer_1_lower', name: 'Business Lower Floors', color: '#1f77b4' },
          { key: 'business_incomer_2_upper', name: 'Business Upper Floors', color: '#ff7f0e' },
          { key: 'psychology_substation_goddard', name: 'Psychology Goddard', color: '#2ca02c' },
          { key: 'commerce_total_kwh', name: 'Total', color: '#ff0000' }
        ]
      },
      totalStream: {
        columns: [
          { key: 'ring_main_1_mp4889_kwh', name: 'Ring Main #1 MP4889', color: '#1f77b4' },
          { key: 'ring_main_2_kwh', name: 'Ring Main #2', color: '#ff7f0e' },
          { key: 'ring_main_3_kwh', name: 'Ring Main #3', color: '#2ca02c' },
          { key: 'taieri_farm_kwh', name: 'Taieri Farm', color: '#d62728' },
          { key: 'castle_college_kwh', name: 'Castle College', color: '#9467bd' },
          { key: 'med_school_sub_main_kwh', name: 'Medical School', color: '#8c564b' },
          { key: 'hayward_college_kwh', name: 'Hayward College', color: '#e377c2' },
          { key: 'survey_marine_kwh', name: 'Survey Marine', color: '#7f7f7f' },
          { key: 'cumberland_college_kwh', name: 'Cumberland College', color: '#bcbd22' },
          { key: 'school_of_dentistry_kwh', name: 'School of Dentistry', color: '#17becf' },
          { key: 'zoology_buildings_kwh', name: 'Zoology Buildings', color: '#aec7e8' },
          { key: 'dental_school_kwh', name: 'Dental School', color: '#ffbb78' },
          { key: 'hunter_centre_kwh', name: 'Hunter Centre', color: '#98df8a' },
          { key: 'physiotherapy_kwh', name: 'Physiotherapy', color: '#ff9896' },
          { key: 'student_health_kwh', name: 'Student Health', color: '#c5b0d5' },
          { key: 'research_support_facility_kwh', name: 'Research Support Facility', color: '#c49c94' },
          { key: 'hocken_library_kwh', name: 'Hocken Library', color: '#f7b6d2' },
          { key: 'great_king_street_kwh', name: 'Great King Street', color: '#c7c7c7' },
          { key: 'botany_tin_hut_kwh', name: 'Botany Tin Hut', color: '#dbdb8d' },
          { key: 'physical_education_kwh', name: 'Physical Education', color: '#9edae5' },
          { key: 'executive_residence_kwh', name: 'Executive Residence', color: '#393b79' },
          { key: 'owheo_building_kwh', name: 'Owheo Building', color: '#637939' },
          { key: 'robertson_library_kwh', name: 'Robertson Library', color: '#8c6d31' },
          { key: 'plaza_building_kwh', name: 'Plaza Building', color: '#843c39' },
          { key: 'education_main_boiler_room_kwh', name: 'Education Main Boiler Room', color: '#7b4173' },
          { key: 'mellor_laboratories_kwh', name: 'Mellor Laboratories', color: '#5254a3' },
          { key: 'biochemistry_kwh', name: 'Biochemistry', color: '#637939' },
          { key: 'microbiology_kwh', name: 'Microbiology', color: '#8c6d31' },
          { key: 'science_2_kwh', name: 'Science 2', color: '#bd9e39' },
          { key: 'st_margarets_college_kwh', name: 'St Margarets College', color: '#ad494a' },
          { key: 'unicol_kwh', name: 'UNICOL', color: '#a55194' },
          { key: 'selwyn_college_kwh', name: 'Selwyn College', color: '#6b6ecf' },
          { key: 'arana_college_main_kwh', name: 'Arana College', color: '#b5cf6b' },
          { key: 'studholm_college_kwh', name: 'Studholm College', color: '#e7ba52' },
          { key: 'carrington_college_kwh', name: 'Carrington College', color: '#d6616b' },
          { key: 'aquinas_college_kwh', name: 'Aquinas College', color: '#ce6dbd' },
          { key: 'caroline_freeman_college_kwh', name: 'Caroline Freeman College', color: '#9c9ede' },
          { key: 'portobello_marine_lab_kwh', name: 'Portobello Marine Lab', color: '#cedb9c' },
          { key: 'abbey_college_kwh', name: 'Abbey College', color: '#e7cb94' },
          { key: 'total_stream_dn_electricity_kwh', name: 'Total', color: '#ff0000' }
        ]
      }      
  };

  const DataTable: React.FC<{
    data: StreamElecDataRow[];
    title: string;
    isLoading: boolean;
    tableType: keyof typeof columnGroups;
  }> = ({ data, title, isLoading, tableType }) => {
    if (isLoading) {
      return <CircularProgress />;
    }

    if (!data || data.length === 0) {
        return <div>No data available</div>;
    }

    const getColumnGroups = (): ColumnGroup[] => {
        switch (tableType) {
            case 'ringMains':
                return ringMainsGroups;
            case 'libraries':
                return librariesGroups;
            case 'colleges':
                return collegesGroups;
            case 'science':
                return scienceGroups;
            case 'healthScience':
                return healthScienceGroups;
            case 'humanities':
                return humanitiesGroups;
            case 'obsPsychology':
                return obsPsychologyGroups;
            case 'totalStream':
                return totalStreamGroups;
            case 'itsServers':
                return itsServersGroups;
            case 'schoolOfMedicine':
                return schoolOfMedicineGroups;
            case 'commerce':
                return commerceGroups;
            default:
                return [];
        }
    };
    
    const columnGroups = getColumnGroups();

    
    
    
    // Add this formatValue function
    const formatValue = (value: any): string => {
        if (value === null || value === undefined) return '-';
        if (typeof value === 'number') {
            return value.toFixed(2).replace(/\.?0+$/, '');
        }
        return value.toString();
    };

    return (
        <div style={tableStyles.container}>
        
            <h3>{title}</h3>
            {chartConfigs[tableType] && (
            <EnergyUsageChart 
              data={data} 
              columns={chartConfigs[tableType]!.columns} 
            />
          )}
            <table style={tableStyles.table}>
                <thead>
                    {/* Main header row with merged cells */}
                    <tr>
                        {columnGroups.map((group, index) => (
                            <th 
                                key={`group-${index}`}
                                colSpan={group.subColumns.length}
                                style={tableStyles.mainHeader}
                            >
                                {group.title}
                            </th>
                        ))}
                    </tr>
                    {/* Sub-header row for kWh/PF labels */}
                    <tr>
                        {columnGroups.flatMap(group => 
                            group.subColumns.map((subCol, index) => (
                                <th 
                                    key={`subheader-${index}`}
                                    style={tableStyles.subHeader}
                                >
                                    {subCol.label}
                                </th>
                            ))
                        )}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            {columnGroups.flatMap(group => 
                                group.subColumns.map((subCol, colIndex) => (
                                    <td 
                                        key={`${rowIndex}-${subCol.key}-${colIndex}`}
                                        style={{
                                            ...tableStyles.td,
                                            ...tableStyles.valueCell,
                                            backgroundColor: rowIndex % 2 === 0 ? '#f9f9f9' : '#fff'
                                        }}
                                    >
                                        {formatValue(row[subCol.key])}
                                    </td>
                                ))
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};



const StreamElecDataView: React.FC = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedYear, setSelectedYear] = useState<number | null>(null);
    const [selectedMonth, setSelectedMonth] = useState<number | null>(null);
    const [data, setData] = useState({
        ringMains: [],
        libraries: [],
        colleges: [],
        science: [],
        healthScience: [],
        humanities: [],
        obsPsychology: [],
        totalStream: [],
        itsServers: [],
        schoolOfMedicine: [],
        commerce: []
    });

    const [error, setError] = useState<string | null>(null);
    
    const filterData = (dataArray: any[]) => {
        if (!Array.isArray(dataArray)) return [];
        return dataArray.filter(item => {
            const itemYear = Number(item.meter_reading_year);
            // Convert month name to number (e.g., "January" -> 1)
            const itemMonth = new Date(Date.parse(`${item.meter_reading_month} 1, 2022`)).getMonth() + 1;
            
            return (selectedYear === null || itemYear === selectedYear) && 
                   (selectedMonth === null || itemMonth === selectedMonth);
        });
    };

    const handleYearChange = (value: string) => {
        setSelectedYear(value === 'all' ? null : parseInt(value));
    };
    
    const handleMonthChange = (value: string) => {
        setSelectedMonth(value === 'all' ? null : parseInt(value));
    };

    const FilterControls = () => (
        <div style={{ margin: '20px', display: 'flex', gap: '20px' }}>
            <div>
                <label>Year: </label>
                <select 
                    value={selectedYear?.toString() || 'all'}
                    onChange={(e) => handleYearChange(e.target.value)}
                    style={{ padding: '5px', marginLeft: '10px' }}
                >
                    <option value="all">All Years</option>
                    {Array.from({ length: 6 }, (_, i) => 2022 + i).map(year => (
                        <option key={year} value={year.toString()}>{year}</option>
                    ))}
                </select>
            </div>
            <div>
                <label>Month: </label>
                <select 
                    value={selectedMonth?.toString() || 'all'}
                    onChange={(e) => handleMonthChange(e.target.value)}
                    style={{ padding: '5px', marginLeft: '10px' }}
                >
                    <option value="all">All Months</option>
                    {Array.from({ length: 12 }, (_, i) => i + 1).map(month => (
                        <option key={month} value={month.toString()}>
                            {new Date(2022, month - 1).toLocaleString('default', { month: 'long' })}
                        </option>
                    ))}
                </select>
            </div>
        </div>
    );
    


    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                setError(null);
                const baseUrl = 'http://127.0.0.1:5001';
                const endpoints = [
                    'ring-mains',
                    'libraries',
                    'colleges',
                    'science',
                    'health-science',
                    'humanities',
                    'obs-psychology',
                    'total-stream',
                    'its-servers',
                    'school-of-medicine',
                    'commerce'
                ];

                const responses = await Promise.all(
                    endpoints.map(async endpoint => {
                        const response = await fetch(`${baseUrl}/api/stream-elec/${endpoint}`);
                        if (!response.ok) {
                            throw new Error(`Failed to fetch ${endpoint} data`);
                        }
                        return response.json();
                    })
                );

                setData({
                    ringMains: responses[0] || [],
                    libraries: responses[1] || [],
                    colleges: responses[2] || [],
                    science: responses[3] || [],
                    healthScience: responses[4] || [],
                    humanities: responses[5] || [],
                    obsPsychology: responses[6] || [],
                    totalStream: responses[7] || [],
                    itsServers: responses[8] || [],
                    schoolOfMedicine: responses[9] || [],
                    commerce: responses[10] || []
                });
            } catch (error) {
                console.error('Error fetching stream electricity data:', error);
                setError('Failed to fetch data. Please try again later.');
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [selectedYear, selectedMonth]);

    return (
        <div>
            <FilterControls />
            {error && (
                <div style={{ color: 'red', margin: '20px' }}>
                    {error}
                </div>
            )}
            <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}
                variant="scrollable"
                scrollButtons="auto"
                allowScrollButtonsMobile
                sx={{
                '.MuiTab-root': {
                    fontSize: '2 rem',
                    minWidth: 'auto',
                    padding: '6px 12px',
                    textTransform: 'none'
                },
                '.MuiTabs-scrollButtons': {
                    '&.Mui-disabled': {
                    opacity: 0.3
                    }
                }
                }}
            >
                <Tab label="Ring Mains" />
                <Tab label="Libraries" />
                <Tab label="Colleges" />
                <Tab label="Science" />
                <Tab label="Health Science" />
                <Tab label="Humanities" />
                <Tab label="OBS Psychology" />
                <Tab label="Total Stream" />
                <Tab label="ITS Servers" />
                <Tab label="School of Medicine" />
                <Tab label="Commerce" />
                <Tab label="Electricity Graphs" />
            </Tabs>

            {activeTab === 0 && <DataTable data={filterData(data.ringMains)} title="Ring Mains Stream" isLoading={isLoading} tableType="ringMains" />}
            {activeTab === 1 && <DataTable data={filterData(data.libraries)} title="Libraries Stream" isLoading={isLoading} tableType="libraries" />}
            {activeTab === 2 && <DataTable data={filterData(data.colleges)} title="Colleges Stream" isLoading={isLoading} tableType="colleges" />}
            {activeTab === 3 && <DataTable data={filterData(data.science)} title="Science Stream" isLoading={isLoading} tableType="science" />}
            {activeTab === 4 && <DataTable data={filterData(data.healthScience)} title="Health Science Stream" isLoading={isLoading} tableType="healthScience" />}
            {activeTab === 5 && <DataTable data={filterData(data.humanities)} title="Humanities Stream" isLoading={isLoading} tableType="humanities" />}
            {activeTab === 6 && <DataTable data={filterData(data.obsPsychology)} title="OBS Psychology Stream" isLoading={isLoading} tableType="obsPsychology" />}
            {activeTab === 7 && <DataTable data={filterData(data.totalStream)} title="Total Stream DN Electricity" isLoading={isLoading} tableType="totalStream" />}
            {activeTab === 8 && <DataTable data={filterData(data.itsServers)} title="ITS Servers Stream" isLoading={isLoading} tableType="itsServers" />}
            {activeTab === 9 && <DataTable data={filterData(data.schoolOfMedicine)} title="School of Medicine Stream" isLoading={isLoading} tableType="schoolOfMedicine" />}
            {activeTab === 10 && <DataTable data={filterData(data.commerce)} title="Commerce Stream" isLoading={isLoading} tableType="commerce" />}
            {activeTab === 11 && (
                <ElectricityGraphs 
                    data={{
                    ringMains: filterData(data.ringMains),
                    libraries: filterData(data.libraries),
                    colleges: filterData(data.colleges),
                    science: filterData(data.science),
                    healthScience: filterData(data.healthScience),
                    humanities: filterData(data.humanities)
                    }} 
                />
            )}
        </div>
    );
};

export default StreamElecDataView;
