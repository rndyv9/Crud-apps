from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("postgresql://${{PGUSER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:5432/${{PGDATABASE}}")

engine = create_engine("SQLALCHEMY_DATABASE_URL")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
