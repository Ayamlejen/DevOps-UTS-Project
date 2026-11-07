import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Membaca konfigurasi dari file .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL belum diatur di file .env")

# Membuat koneksi ke PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Membuat session database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base untuk model database
Base = declarative_base()


# Fungsi untuk menguji koneksi
def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Hasil koneksi:", result.scalar())
        print("PostgreSQL berhasil terhubung!")