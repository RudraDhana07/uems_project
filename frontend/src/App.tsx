// src/App.tsx

import React, { useState } from 'react';
import { Tabs, Tab, styled } from '@mui/material';
import AucklandDataView from './components/views/AucklandDataView';
import SteamMTHWDataView from './components/views/SteamMTHWDataView';
import JanitzaDataView from './components/views/JanitzaDataView';
import LTHWDataView from './components/views/LTHWDataView';
import GasDataView from './components/views/GasDataView';
import StreamElecDataView from './components/views/StreamElecDataView';
import CfiDataView from './components/views/CfiDataView';
import MthwDataView from './components/views/MthwDataView';
import EnergyTotalDashboard from './components/views/EnergyTotalDashboard';

// Custom styled Tab component
const StyledTab = styled(Tab)({
  backgroundColor: '#f0f0f0',
  margin: '0 5px',
  borderRadius: '4px',
  '&:hover': {
    backgroundColor: '#e0e0e0',
  },
  '&.Mui-selected': {
    backgroundColor: '#1976d2',
    color: 'white',
  },
});

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  return (
    <div>
      <Tabs 
        value={activeTab} 
        onChange={handleTabChange}
        sx={{
          '& .MuiTabs-indicator': {
            display: 'none',
          },
          marginBottom: '20px',
        }}
      >
        
        <StyledTab label="Energy Total Dashboard" />
        <StyledTab label="Stream Elec Data" />
        <StyledTab label="Steam & MTHW Data" />
        <StyledTab label="MTHW Data" />
        <StyledTab label="Janitza Data" />
        <StyledTab label="LTHW Data" />
        <StyledTab label="Gas Data" />
        <StyledTab label="Center for Innovation" />
        <StyledTab label="Auckland Data" />
      </Tabs>

      {activeTab === 0 && <EnergyTotalDashboard />}
      {activeTab === 1 && <StreamElecDataView />}
      {activeTab === 2 && <SteamMTHWDataView />}
      {activeTab === 3 && <MthwDataView />}
      {activeTab === 4 && <JanitzaDataView />}
      {activeTab === 5 && <LTHWDataView />}
      {activeTab === 6 && <GasDataView />}
      {activeTab === 7 && <CfiDataView />}
      {activeTab === 8 && <AucklandDataView />}

    </div>
  );
};

export default App;
