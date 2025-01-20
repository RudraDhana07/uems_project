# backend/check_db.py
from app import create_app, db
from sqlalchemy import text
from app.models.auckland_electricity import AucklandElectricityCalculatedConsumption
from app.models.auckland_water import AucklandWaterCalculatedConsumption, AucklandWaterConsumption

def check_database():
    app = create_app()
    with app.app_context():
        try:
            # Test database connection using text()
            db.session.execute(text('SELECT 1'))
            print("✓ Database connection successful")
            
            # Check if tables exist and count records
            electricity_count = db.session.query(AucklandElectricityCalculatedConsumption).count()
            water_calc_count = db.session.query(AucklandWaterCalculatedConsumption).count()
            water_count = db.session.query(AucklandWaterConsumption).count()
            
            print("\nRecord counts:")
            print(f"Electricity Calculated Consumption: {electricity_count}")
            print(f"Water Calculated Consumption: {water_calc_count}")
            print(f"Water Consumption: {water_count}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("\nPlease check:")
            print("1. Is PostgreSQL running?")
            print("2. Is the database 'uems_db' created?")
            print("3. Is your DATABASE_URL in .env correct?")
            print(f"Current error: {str(e)}")

if __name__ == "__main__":
    check_database()