// src/hooks/useAucklandData.ts
import { useState, useEffect } from 'react';
import { API_BASE_URL, API_ENDPOINTS } from '../config/api';

interface DataRow {
    object_name: string;
    object_description?: string;
    meter_location?: string;
    reading_description?: string;
    [key: string]: string | number | undefined;
}

export const useAucklandData = () => {
    const [data, setData] = useState<DataRow[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.electricity}`);
                const result = await response.json();
                setData(result);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred');
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, []);

    return { data, isLoading, error };
};
