from sqlalchemy import Column, Integer, String, DateTime, Time, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StoreStatus(Base):
    __tablename__ = 'store_data'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    store_id = Column(BigInteger, ForeignKey('store_timezone.id'), nullable=True)
    status = Column(String(50), nullable=True)
    timestamp_utc = Column(DateTime, nullable=True)

class BusinessHours(Base):
    __tablename__ = 'store_hours'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    store_id = Column(BigInteger, ForeignKey('store_timezone.id'), nullable=True)
    day = Column(Integer, nullable=True)
    start_time_local = Column(Time, nullable=True)
    end_time_local = Column(Time, nullable=True)

class StoreTimezone(Base):
    __tablename__ = 'store_timezone'
    id = Column(BigInteger, primary_key=True)
    timezone = Column(String(200), nullable=True)

