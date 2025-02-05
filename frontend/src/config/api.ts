// frontend/src/config/api.ts
console.log('Environment API URL:', process.env.REACT_APP_API_URL);
console.log('Final API URL:', process.env.REACT_APP_API_URL || 'http://localhost:5001');

export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

export const API_ENDPOINTS = {
    electricity: '/api/auckland/electricity',
    waterCalculated: '/api/auckland/water-calculated',
    water: '/api/auckland/water'
};
