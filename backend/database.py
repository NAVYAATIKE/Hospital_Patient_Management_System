from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

db_url="postgresql://postgres:root@localhost:5432/Hospital_Patient_Management_System"

engine=create_engine(db_url)

SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)
