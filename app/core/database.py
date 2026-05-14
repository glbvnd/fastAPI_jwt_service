from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings



DATABASE_URL= settings.SQLALCHEMY_DATABASE_URL

connect_args ={}
if DATABASE_URL.startswith("sqlile"):
    connect_args ={"check_same_thered": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)
Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session

    except Exception:
        session.rollback()
        raise  # just raise

    finally:
        session.close()        