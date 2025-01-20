// frontend/src/config/api.ts

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const API_ENDPOINTS = {
    electricity: `${API_BASE_URL}/api/auckland/electricity`,
    waterCalculated: `${API_BASE_URL}/api/auckland/water-calculated`,
    water: `${API_BASE_URL}/api/auckland/water`
};