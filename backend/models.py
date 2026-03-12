from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class HospitalCreate(BaseModel):
    patient_name:str
    age:int
    disease:str
    admission_date:Optional[date]=Field(default_factory=date.today)


class HospitalResponse(HospitalCreate):
    id:int

    class Config:
        from_attributes=True


