// src/types/gas.ts
export interface DataRow {
    meter_description?: string;
    object_description?: string;
    icp?: string;
    misc?: string;
    misc1?: string;
    misc2?: string;
    [key: string]: string | number | null | undefined;
}