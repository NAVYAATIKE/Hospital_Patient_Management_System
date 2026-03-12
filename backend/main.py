from fastapi import FastAPI,Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date

import database_models as database_models
from database import SessionLocal,engine
from models import HospitalCreate, HospitalResponse


database_models.Base.metadata.create_all(bind=engine)
#--------------------CREATE APP-------------------------------
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#-------------------------------CONNECTION-----------------------
#create connection to db
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
#----------------------INITIALIZING------------------------------
#initialize
def init_db():
    db=SessionLocal()

    if db.query(database_models.Hospital).count()==0:
        patients=[
            database_models.Hospital(
                patient_name="Navya",
                age=21,
                disease="Typhoid",
                admission_date=date(2026, 2, 11)
            ),
            database_models.Hospital(
                patient_name="Anusha",
                age=34,
                disease="Malaria",
                admission_date=date(2026, 2, 9)
            ),
            database_models.Hospital(
                patient_name="Soumya",
                age=45,
                disease="Common Cold",
                admission_date=date(2026, 1 ,1)
            ),
            database_models.Hospital(
                patient_name="Rama",
                age=51,
                disease="Cancer"
            ),
        ]
        db.add_all(patients)
        db.commit()

    db.close()

init_db()

#-------------------------API ENDPOINTS---------------------------
#GET all patients details
@app.get("/patients",response_model=list[HospitalResponse])
def get_all_patients(db: Session= Depends(get_db)):
    return(
        db.query(database_models.Hospital)
        .order_by(database_models.Hospital.id)
        .all()
    )


#GET patient details by id
@app.get("/patients/{patient_id}",response_model=HospitalResponse)
def get_patients_by_id(patient_id:int,db:Session=Depends(get_db)):
    patient=(
        db.query(database_models.Hospital)
        .filter(database_models.Hospital.id==patient_id)
        .first()
        )
    if not patient:
        raise HTTPException(status_code=404,detail="Patient details not found")
    return patient

#create new patient details
@app.post("/patients")
def create_patient(patient: HospitalCreate,db:Session=Depends(get_db)):
    new_patient=database_models.Hospital(**patient.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {"message":" New Patient admitted"}


#Update patient details
@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient:HospitalCreate,db: Session=Depends(get_db)):
    db_patient=(
        db.query(database_models.Hospital)
        .filter(database_models.Hospital.id==patient_id)
        .first()
    )

    if not db_patient:
        raise HTTPException(status_code=404,detail="Patient details not found")
    
    db_patient.patient_name=patient.patient_name
    db_patient.age=patient.age
    db_patient.disease=patient.disease
    db_patient.admission_date=patient.admission_date

    db.commit()
    db.refresh(db_patient)

    return {"message":"Patient Details Updated Successfully"}


#DELETE patient details
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = (
        db.query(database_models.Hospital)
        .filter(database_models.Hospital.id == patient_id)
        .first()
    )

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient details not found")

    db.delete(db_patient)
    db.commit()

    return {"message": "Patient details deleted successfully"}
