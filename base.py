from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


SQLALCHEMY_DATABASE_URL = "sqlite:///sql.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    films = relationship('Film', back_populates='genre')

class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship('Genre', back_populates='films')