from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("postgresql://postgres:NrOLNHfnetSjnzsERltXlqzKDwCzTnCn@postgres.railway.internal:5432/railway")

engine = create_engine("SQLALCHEMY_DATABASE_URL")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
