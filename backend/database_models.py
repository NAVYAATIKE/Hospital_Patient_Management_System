from sqlalchemy import Column, Integer, String, Date
from datetime import date
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Hospital(Base):
    __tablename__="patient"
    id=Column(Integer,primary_key=True,index=True)
    patient_name=Column(String,index=True)
    age=Column(Integer)
    disease=Column(String)
    admission_date=Column(Date,default=date.today)