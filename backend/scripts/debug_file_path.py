# backend/scripts/debug_file_path.py
import os
from pathlib import Path

def debug_file_location():
    # Get the current script directory
    current_dir = Path(__file__).resolve().parent
    backend_dir = current_dir.parent
    data_dir = backend_dir / 'data'
    
    print("\nChecking directories and files:")
    print(f"Current directory: {os.getcwd()}")
    print(f"Backend directory: {backend_dir}")
    print(f"Data directory: {data_dir}")
    print(f"\nData directory exists? {data_dir.exists()}")
    
    print("\nFiles in data directory:")
    if data_dir.exists():
        for file in data_dir.iterdir():
            print(f"- {file.name}")
            
    print("\nLooking for Excel file:")
    excel_file = data_dir / '2024 campus meter readings.xlsx'
    print(f"Expected file path: {excel_file}")
    print(f"File exists? {excel_file.exists()}")

if __name__ == "__main__":
    debug_file_location()