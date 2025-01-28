# backend/app/models/cfi_models.py

from datetime import datetime
from .. import db

class CenterForInnovation(db.Model):
    __tablename__ = 'center_for_innovation'
    __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    building_code = db.Column(db.String(255))
    location = db.Column(db.String(255))
    meter_type = db.Column(db.String(255))
    meter_number = db.Column(db.String(255))
    digit_to_read = db.Column(db.String(255))
    multipier_ct_rating = db.Column(db.String(255))
    remark = db.Column(db.Text)
    mod = db.Column(db.String(255))

    # 2021 readings with R1 prefix
    R1_Dec_2021 = db.Column(db.Float)

    # 2022 readings with R1 prefix
    R1_Jan_2022 = db.Column(db.Float)
    R1_Feb_2022 = db.Column(db.Float)
    R1_Mar_2022 = db.Column(db.Float)
    R1_Apr_2022 = db.Column(db.Float)
    R1_May_2022 = db.Column(db.Float)
    R1_Jun_2022 = db.Column(db.Float)
    R1_Jul_2022 = db.Column(db.Float)
    R1_Aug_2022 = db.Column(db.Float)
    R1_Sep_2022 = db.Column(db.Float)
    R1_Oct_2022 = db.Column(db.Float)
    R1_Nov_2022 = db.Column(db.Float)
    R1_Dec_2022 = db.Column(db.Float)

    R1_Jan_2023 = db.Column(db.Float)
    # 2023 monthly readings
    Jan_2023 = db.Column(db.Float)
    Feb_2023 = db.Column(db.Float)
    Mar_2023 = db.Column(db.Float)
    Apr_2023 = db.Column(db.Float)
    May_2023 = db.Column(db.Float)
    Jun_2023 = db.Column(db.Float)
    Jul_2023 = db.Column(db.Float)
    Aug_2023 = db.Column(db.Float)
    Sep_2023 = db.Column(db.Float)
    Oct_2023 = db.Column(db.Float)
    Nov_2023 = db.Column(db.Float)
    Dec_2023 = db.Column(db.Float)

    # 2024 monthly readings
    Jan_2024 = db.Column(db.Float)
    Feb_2024 = db.Column(db.Float)
    Mar_2024 = db.Column(db.Float)
    Apr_2024 = db.Column(db.Float)
    May_2024 = db.Column(db.Float)
    Jun_2024 = db.Column(db.Float)
    Jul_2024 = db.Column(db.Float)
    Aug_2024 = db.Column(db.Float)
    Sep_2024 = db.Column(db.Float)
    Oct_2024 = db.Column(db.Float)
    Nov_2024 = db.Column(db.Float)
    Dec_2024 = db.Column(db.Float)

    # 2025 monthly readings
    Jan_2025 = db.Column(db.Float)
    Feb_2025 = db.Column(db.Float)
    Mar_2025 = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'building_code': self.building_code,
            'location': self.location,
            'meter_type': self.meter_type,
            'meter_number': self.meter_number,
            'digit_to_read': self.digit_to_read,
            'multipier_ct_rating': self.multipier_ct_rating,
            'remark': self.remark,
            'mod': self.mod,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            **{col.name: getattr(self, col.name)
               for col in self.__table__.columns
               if col.name not in ['id', 'building_code', 'location', 'meter_type',
                                 'meter_number', 'digit_to_read', 'multipier_ct_rating',
                                 'remark', 'mod', 'created_at', 'updated_at']}
        }
    

class CfiRoomTypes(db.Model):
    __tablename__ = 'cfi_room_types'
    __table_args__ = {'schema': 'dbo'}

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(255))
    area_m2 = db.Column(db.String(255))
    type = db.Column(db.String(255))
    suite = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'area_m2': self.area_m2,
            'type': self.type,
            'suite': self.suite,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }