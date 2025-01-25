# backend/app/models/stream_elec_models.py

from datetime import datetime
from .. import db

class RingMainsStream(db.Model):
    __tablename__ = 'ring_mains_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    ring_main_1_mp4889_kwh = db.Column(db.Float)
    ring_main_1_mp4889_pf = db.Column(db.Float)
    ring_main_2_kwh = db.Column(db.Float)
    ring_main_2_pf = db.Column(db.Float)
    ring_main_3_kwh = db.Column(db.Float)
    ring_main_3_pf = db.Column(db.Float)
    ring_mains_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }

class LibrariesStream(db.Model):
    __tablename__ = 'libraries_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    hocken_library_kwh = db.Column(db.Float)
    hocken_library_pf = db.Column(db.Float)
    robertson_library_kwh = db.Column(db.Float)
    robertson_library_pf = db.Column(db.Float)
    bill_robertson_library_msb = db.Column(db.Float)
    sayers_adams_msb = db.Column(db.Float)
    isb_west_excluding_shops = db.Column(db.Float)
    richardson_library_block_rising_main = db.Column(db.Float)
    libraries_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }

class CollegesStream(db.Model):
    __tablename__ = 'colleges_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    castle_college_kwh = db.Column(db.Float)
    castle_college_pf = db.Column(db.Float)
    hayward_college_kwh = db.Column(db.Float)
    hayward_college_pf = db.Column(db.Float)
    cumberland_college_kwh = db.Column(db.Float)
    cumberland_college_pf = db.Column(db.Float)
    executive_residence_kwh = db.Column(db.Float)
    executive_residence_pf = db.Column(db.Float)
    owheo_building_kwh = db.Column(db.Float)
    owheo_building_pf = db.Column(db.Float)
    st_margarets_college_kwh = db.Column(db.Float)
    st_margarets_college_pf = db.Column(db.Float)
    selwyn_college_kwh = db.Column(db.Float)
    selwyn_college_pf = db.Column(db.Float)
    arana_college_main_kwh = db.Column(db.Float)
    arana_college_main_pf = db.Column(db.Float)
    studholm_college_kwh = db.Column(db.Float)
    studholm_college_pf = db.Column(db.Float)
    carrington_college_kwh = db.Column(db.Float)
    carrington_college_pf = db.Column(db.Float)
    aquinas_college_kwh = db.Column(db.Float)
    aquinas_college_pf = db.Column(db.Float)
    caroline_freeman_college_kwh = db.Column(db.Float)
    caroline_freeman_college_pf = db.Column(db.Float)
    abbey_college_kwh = db.Column(db.Float)
    abbey_college_pf = db.Column(db.Float)
    colleges_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }

class ScienceStream(db.Model):
    __tablename__ = 'science_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    survey_marine_kwh = db.Column(db.Float)
    survey_marine_pf = db.Column(db.Float)
    zoology_buildings_kwh = db.Column(db.Float)
    zoology_buildings_pf = db.Column(db.Float)
    botany_tin_hut_kwh = db.Column(db.Float)
    botany_tin_hut_pf = db.Column(db.Float)
    physical_education_kwh = db.Column(db.Float)
    physical_education_pf = db.Column(db.Float)
    owheo_building_kwh = db.Column(db.Float)
    owheo_building_pf = db.Column(db.Float)
    mellor_laboratories_kwh = db.Column(db.Float)
    mellor_laboratories_pf = db.Column(db.Float)
    microbiology_kwh = db.Column(db.Float)
    microbiology_pf = db.Column(db.Float)
    science_2_kwh = db.Column(db.Float)
    science_2_pf = db.Column(db.Float)
    portobello_marine_lab_kwh = db.Column(db.Float)
    portobello_marine_lab_pf = db.Column(db.Float)
    geology_north = db.Column(db.Float)
    geology_south = db.Column(db.Float)
    science_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }

class HealthScienceStream(db.Model):
    __tablename__ = 'health_science_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    taieri_farm_kwh = db.Column(db.Float)
    taieri_farm_pf = db.Column(db.Float)
    med_school_sub_main_kwh = db.Column(db.Float)
    med_school_sub_main_pf = db.Column(db.Float)
    dental_school_kwh = db.Column(db.Float)
    dental_school_pf = db.Column(db.Float)
    hunter_centre_kwh = db.Column(db.Float)
    hunter_centre_pf = db.Column(db.Float)
    physiotherapy_kwh = db.Column(db.Float)
    physiotherapy_pf = db.Column(db.Float)
    research_support_facility_kwh = db.Column(db.Float)
    research_support_facility_pf = db.Column(db.Float)
    health_science_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }

class HumanitiesStream(db.Model):
    __tablename__ = 'humanities_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    education_main_boiler_room_kwh = db.Column(db.Float)
    education_main_boiler_room_pf = db.Column(db.Float)
    richardson_mains = db.Column(db.Float)
    arts_1_submains_msb = db.Column(db.Float)
    albany_leith_walk = db.Column(db.Float)
    archway_buildings = db.Column(db.Float)
    humanities_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }
    

class ObsPsychologyStream(db.Model):
    __tablename__ = 'obs_psychology_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    business_incomer_1_lower = db.Column(db.Float)
    business_incomer_2_upper = db.Column(db.Float)
    psychology_substation_goddard = db.Column(db.Float)
    obs_psychology_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }

class TotalStreamDnElectricity(db.Model):
    __tablename__ = 'total_stream_dn_electricity'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    # Ring Mains
    ring_main_1_mp4889_kwh = db.Column(db.Float)
    ring_main_1_mp4889_pf = db.Column(db.Float)
    ring_main_2_kwh = db.Column(db.Float)
    ring_main_2_pf = db.Column(db.Float)
    ring_main_3_kwh = db.Column(db.Float)
    ring_main_3_pf = db.Column(db.Float)
    
    # Buildings and Facilities
    taieri_farm_kwh = db.Column(db.Float)
    taieri_farm_pf = db.Column(db.Float)
    castle_college_kwh = db.Column(db.Float)
    castle_college_pf = db.Column(db.Float)
    med_school_sub_main_kwh = db.Column(db.Float)
    med_school_sub_main_pf = db.Column(db.Float)
    hayward_college_kwh = db.Column(db.Float)
    hayward_college_pf = db.Column(db.Float)
    survey_marine_kwh = db.Column(db.Float)
    survey_marine_pf = db.Column(db.Float)
    cumberland_college_kwh = db.Column(db.Float)
    cumberland_college_pf = db.Column(db.Float)
    school_of_dentistry_kwh = db.Column(db.Float)
    school_of_dentistry_pf = db.Column(db.Float)
    zoology_buildings_kwh = db.Column(db.Float)
    zoology_buildings_pf = db.Column(db.Float)
    dental_school_kwh = db.Column(db.Float)
    dental_school_pf = db.Column(db.Float)
    hunter_centre_kwh = db.Column(db.Float)
    hunter_centre_pf = db.Column(db.Float)
    physiotherapy_kwh = db.Column(db.Float)
    physiotherapy_pf = db.Column(db.Float)
    student_health_kwh = db.Column(db.Float)
    student_health_pf = db.Column(db.Float)
    research_support_facility_kwh = db.Column(db.Float)
    research_support_facility_pf = db.Column(db.Float)
    hocken_library_kwh = db.Column(db.Float)
    hocken_library_pf = db.Column(db.Float)
    great_king_street_kwh = db.Column(db.Float)
    great_king_street_pf = db.Column(db.Float)
    botany_tin_hut_kwh = db.Column(db.Float)
    botany_tin_hut_pf = db.Column(db.Float)
    physical_education_kwh = db.Column(db.Float)
    physical_education_pf = db.Column(db.Float)
    executive_residence_kwh = db.Column(db.Float)
    executive_residence_pf = db.Column(db.Float)
    owheo_building_kwh = db.Column(db.Float)
    owheo_building_pf = db.Column(db.Float)
    robertson_library_kwh = db.Column(db.Float)
    robertson_library_pf = db.Column(db.Float)
    plaza_building_kwh = db.Column(db.Float)
    plaza_building_pf = db.Column(db.Float)
    education_main_boiler_room_kwh = db.Column(db.Float)
    education_main_boiler_room_pf = db.Column(db.Float)
    mellor_laboratories_kwh = db.Column(db.Float)
    mellor_laboratories_pf = db.Column(db.Float)
    biochemistry_kwh = db.Column(db.Float)
    biochemistry_pf = db.Column(db.Float)
    microbiology_kwh = db.Column(db.Float)
    microbiology_pf = db.Column(db.Float)
    science_2_kwh = db.Column(db.Float)
    science_2_pf = db.Column(db.Float)
    st_margarets_college_kwh = db.Column(db.Float)
    st_margarets_college_pf = db.Column(db.Float)
    unicol_kwh = db.Column(db.Float)
    unicol_pf = db.Column(db.Float)
    selwyn_college_kwh = db.Column(db.Float)
    selwyn_college_pf = db.Column(db.Float)
    arana_college_main_kwh = db.Column(db.Float)
    arana_college_main_pf = db.Column(db.Float)
    studholm_college_kwh = db.Column(db.Float)
    studholm_college_pf = db.Column(db.Float)
    carrington_college_kwh = db.Column(db.Float)
    carrington_college_pf = db.Column(db.Float)
    aquinas_college_kwh = db.Column(db.Float)
    aquinas_college_pf = db.Column(db.Float)
    caroline_freeman_college_kwh = db.Column(db.Float)
    caroline_freeman_college_pf = db.Column(db.Float)
    portobello_marine_lab_kwh = db.Column(db.Float)
    portobello_marine_lab_pf = db.Column(db.Float)
    abbey_college_kwh = db.Column(db.Float)
    abbey_college_pf = db.Column(db.Float)
    
    # Total
    total_stream_dn_electricity_kwh = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }
    

class ItsServersStream(db.Model):
    __tablename__ = 'its_servers_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    great_king_street_kwh = db.Column(db.Float)
    great_king_street_pf = db.Column(db.Float)
    great_king_main_meter = db.Column(db.Float)
    great_king_physiotherapy = db.Column(db.Float)
    its_servers_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }
    

class SchoolOfMedicineChChStream(db.Model):
    __tablename__ = 'school_of_medicine_chch_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    school_of_medicine_chch_kwh = db.Column(db.Float)
    school_of_medicine_chch_pf = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }

class CommerceStream(db.Model):
    __tablename__ = 'commerce_stream'
    __table_args__ = {'schema': 'dbo'}
    
    id = db.Column(db.Integer, primary_key=True)
    meter_reading_month = db.Column(db.String(255))
    meter_reading_year = db.Column(db.Integer)
    business_incomer_1_lower = db.Column(db.Float)
    business_incomer_2_upper = db.Column(db.Float)
    psychology_substation_goddard = db.Column(db.Float)
    commerce_total_kwh = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_reading_month': self.meter_reading_month,
            'meter_reading_year': self.meter_reading_year,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
            for col in self.__table__.columns
            if col.name not in ['id', 'meter_reading_month', 'meter_reading_year', 'created_at', 'updated_at']}
        }