import React, { useState } from 'react';
import { Tabs, Tab, styled } from '@mui/material';
import AucklandDataView from './components/views/AucklandDataView';
import SteamMTHWDataView from './components/views/SteamMTHWDataView';
import JanitzaDataView from './components/views/JanitzaDataView';

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
          '& .MuiTabs-indicator': { // Hide the default indicator
            display: 'none',
          },
          marginBottom: '20px', // Add some spacing below tabs
        }}
      >
        <StyledTab label="Auckland Data" />
        <StyledTab label="Steam & MTHW Data" />
        <StyledTab label="Janitza Data" />
      </Tabs>

      {activeTab === 0 && <AucklandDataView />}
      {activeTab === 1 && <SteamMTHWDataView />}
      {activeTab === 2 && <JanitzaDataView />}
    </div>
  );
};

export default App;
