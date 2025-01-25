// src/App.tsx

import React, { useState } from 'react';
import { Tabs, Tab, styled } from '@mui/material';
import AucklandDataView from './components/views/AucklandDataView';
import SteamMTHWDataView from './components/views/SteamMTHWDataView';
import JanitzaDataView from './components/views/JanitzaDataView';
import LTHWDataView from './components/views/LTHWDataView';
import GasDataView from './components/views/GasDataView';

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
        <StyledTab label="Auckland Data" />
        <StyledTab label="Steam & MTHW Data" />
        <StyledTab label="Janitza Data" />
        <StyledTab label="LTHW Data" />
        <StyledTab label="Gas Data" />
      </Tabs>

      {activeTab === 0 && <AucklandDataView />}
      {activeTab === 1 && <SteamMTHWDataView />}
      {activeTab === 2 && <JanitzaDataView />}
      {activeTab === 3 && <LTHWDataView />}
      {activeTab === 4 && <GasDataView />}
    </div>
  );
};

export default App;
