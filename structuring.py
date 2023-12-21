from typing import Optional
from pydantic import BaseModel, ConfigDict

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreUpdate(GenreBase):
    name: Optional[str] = None

class Genre(GenreBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class FilmBase(BaseModel):
    name: str
    genre_id: int

class FilmCreate(FilmBase):
    pass

class FilmUpdate(FilmBase):
    name: Optional[str] = None
    genre_id: Optional[int] = None

class Film(FilmBase):
    model_config = ConfigDict(from_attributes=True)
    id: int