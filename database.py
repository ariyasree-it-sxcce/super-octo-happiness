from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
# --- Change these to your MySQL details ---
DB_USER     = "root"
DB_PASSWORD = "eAciMlBJoxLyEngWbrRlGvtszdIqFmlM"
DB_HOST     = "mysql.railway.internal"
DB_NAME     = "railway"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
SessionLocal = sessionmaker(bind=engine)
Base         = declarative_base()
 
 
class User(Base):
    __tablename__ = "users"
 
    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
 
 
# Creates the users table if it doesn't exist
Base.metadata.create_all(bind=engine)