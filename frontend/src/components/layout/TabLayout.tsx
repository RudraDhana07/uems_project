// src/components/layout/TabLayout.tsx

import React, { useState } from 'react';
import AucklandDataView from '../views/AucklandDataView';
import SteamMTHWDataView from '../views/SteamMTHWDataView';

const tabStyles = {
    container: {
        minHeight: '100vh',
        backgroundColor: '#ffffff',  // Changed to white
    },
    tabBar: {
        display: 'flex',
        backgroundColor: '#f5f5f5',  // Changed to light grey
        padding: '0 20px',
        borderBottom: '1px solid #e0e0e0',
        position: 'sticky' as const,
        top: 0,
        zIndex: 1000,
    },
  tab: {
    padding: '15px 25px',
    cursor: 'pointer',
    borderBottom: '2px solid transparent',
    color: '#666',
    fontWeight: 500,
    transition: 'all 0.3s ease',
  },
  activeTab: {
    borderBottom: '2px solid #1976d2',
    color: '#1976d2',
  },
  content: {
    padding: '20px 0',
  },
  pageTitle: {
    fontSize: '24px',
    color: '#333',
    margin: '0 20px 20px',
    padding: '20px 0',
    borderBottom: '1px solid #eee',
  }
};

const TabLayout: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'auckland' | 'steam'>('auckland');

  const tabs = [
    { id: 'auckland', label: 'Auckland Campus' },
    { id: 'steam', label: 'Steam & MTHW' }
  ];

  const getTabStyle = (tabId: string) => ({
    ...tabStyles.tab,
    ...(activeTab === tabId ? tabStyles.activeTab : {})
  });

  return (
    <div style={tabStyles.container}>
      <div style={tabStyles.tabBar}>
        {tabs.map(tab => (
          <div
            key={tab.id}
            style={getTabStyle(tab.id)}
            onClick={() => setActiveTab(tab.id as 'auckland' | 'steam')}
          >
            {tab.label}
          </div>
        ))}
      </div>

      <div style={tabStyles.content}>
        {activeTab === 'auckland' ? (
          <AucklandDataView />
        ) : (
          <SteamMTHWDataView />
        )}
      </div>
    </div>
  );
};

export default TabLayout;