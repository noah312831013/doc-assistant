from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 開發用 SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./doc_assistant.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 需要
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency：每個 request 拿一個 DB session，結束後關閉"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
