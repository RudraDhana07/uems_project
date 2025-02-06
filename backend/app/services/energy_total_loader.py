from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..models.energy_total_models import EnergyTotalDashboard
from ..models.stream_elec_models import TotalStreamDnElectricity
from ..models.steam_mthw import SteamMTHWReading
from ..models.gas_models import GasConsumption
from ..models.lthw_models import LTHWConsumption

class EnergyTotalLoader:
    def __init__(self, db_session):
        self.session = db_session

    def load_data(self):
        try:
            # First truncate the existing table
            self.session.execute(text('TRUNCATE TABLE dbo.energy_total_dashboard RESTART IDENTITY CASCADE;'))
            self.session.commit()
            
            # Get base data from TotalStreamDnElectricity
            stream_data = self.session.query(TotalStreamDnElectricity).all()
            
            records_loaded = 0
            
            for stream_record in stream_data:
                # Get corresponding data from other tables
                month = stream_record.meter_reading_month
                year = stream_record.meter_reading_year
                
                # Get MTHW and Steam data
                mthw_steam = self.session.query(SteamMTHWReading).filter_by(
                    month=month,
                    year=year
                ).first()
                
                # Get LPG data
                lpg_data = self.session.query(GasConsumption).filter_by(
                    object_description=' Total Gas Energy - DN'
                ).first()
                
                # Get Woodchip data
                woodchip_data = self.session.query(LTHWConsumption).filter_by(
                    object_name=' Total Wood Energy - DN'
                ).first()
                
                # Get Solar data
                solar_data = self.session.query(LTHWConsumption).filter_by(
                    object_name='Total Solar Energy - DN'
                ).first()
                
                # Get the correct monthly values
                column_name = f"{month}_{year}"
                
                # Store values with None if not available 
                stream_value = (stream_record.total_stream_dn_electricity_kwh 
                                if stream_record.total_stream_dn_electricity_kwh != 0 
                                else None)
                mthw_value = mthw_steam.mthw_consumption_kwh if mthw_steam else None
                steam_value = mthw_steam.total_steam_consumption_kwh if mthw_steam else None
                lpg_value = getattr(lpg_data, column_name, None)
                woodchip_value = getattr(woodchip_data, column_name, None)
                solar_value = getattr(solar_data, column_name, None)
                
                # Calculate total only if all values are available
                if all(v is not None for v in [stream_value, mthw_value, steam_value, 
                                             lpg_value, woodchip_value, solar_value]):
                    total_kwh = float(stream_value + mthw_value + steam_value + 
                                    lpg_value + woodchip_value + solar_value)
                else:
                    total_kwh = None
                
                # Create new record
                new_record = EnergyTotalDashboard(
                    month=month,
                    year=year,
                    total_stream_dn_electricity_kwh=stream_value,
                    mthw_kwh=mthw_value,
                    steam_kwh=steam_value,
                    lpg_kwh=lpg_value,
                    woodchip_pellet_kwh=woodchip_value,
                    solar_kwh=solar_value,
                    total_kwh=total_kwh
                )
                
                self.session.add(new_record)
                records_loaded += 1
            
            self.session.commit()
            return records_loaded
            
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error loading energy total data: {str(e)}")
