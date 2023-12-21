from sqlalchemy.orm import Session
import structuring
from base import Genre, Film

def create_genre(db: Session, schema: structuring.GenreCreate):
    db_genre = Genre(**schema.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genres(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Genre).offset(skip).limit(limit).all()

def update_genre(db: Session, genre_id: int, genre_data: structuring.GenreUpdate | dict):
    db_genre = db.query(Genre).filter_by(id=genre_id).first()
    genre_data = genre_data if isinstance(genre_data, dict) else genre_data.model_dump()

    if db_genre:
        for key, value in genre_data.items():
            if hasattr(db_genre, key):
                setattr(db_genre, key, value)
        db.commit()
        db.refresh(db_genre)
    return db_genre

def delete_genre(db: Session, genre_id: int):
    db_genre = db.query(Genre).filter_by(id=genre_id).first()
    if db_genre:
        db.delete(db_genre)
        db.commit()
        return True
    return False

def create_film(db: Session, schema: structuring.FilmCreate):
    db_film = Film(**schema.model_dump())
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film

def get_films(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Film).offset(skip).limit(limit).all()

def update_film(db: Session, film_id: int, film_data: structuring.FilmUpdate | dict):
    db_film = db.query(Film).filter_by(id=film_id).first()
    film_data = film_data if isinstance(film_data, dict) else film_data.model_dump()

    if db_film:
        for key, value in film_data.items():
            if hasattr(db_film, key):
                setattr(db_film, key, value)
        db.commit()
        db.refresh(db_film)
        return db_film
    return None

def delete_film(db: Session, film_id: int):
    db_film = db.query(Film).filter_by(id=film_id).first()
    if db_film:
        db.delete(db_film)
        db.commit()
        return True
    return False
