from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import structuring
from base import get_db
from sqlalchemy.orm import Session
from function import (create_genre, get_genres, update_genre, delete_genre,create_film, get_films, update_film, delete_film)

router_websocket = APIRouter()
router_genre = APIRouter(prefix='/genres', tags=['genre'])
router_film = APIRouter(prefix='/films', tags=['film'])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)

@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"#{client_id} in the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"#{client_id} wrote: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"#{client_id} left chat")

@router_genre.post("/", response_model=structuring.Genre)
async def create_genre_route(genre_data: structuring.GenreCreate, db: Session = Depends(get_db)):
    genre = create_genre(db, genre_data)
    await notify_clients(f"{genre.name} added")
    return genre

@router_genre.get("/", response_model=List[structuring.Genre])
async def read_genres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    genre = get_genres(db, skip=skip, limit=limit)
    return genre

@router_genre.patch("/{genre_id}", response_model=structuring.Genre)
async def update_genre_route(genre_id: int, genre_data: structuring.GenreUpdate, db: Session = Depends(get_db)):
    updated_genre = update_genre(db, genre_id, genre_data)
    if updated_genre:
        await notify_clients(f"{updated_genre.name} updated")
        return updated_genre
    return {"message": "Genre not found"}

@router_genre.delete("/{genre_id}")
async def delete_genre_route(genre_id: int, db: Session = Depends(get_db)):
    deleted = delete_genre(db, genre_id)
    if deleted:
        await notify_clients(f"ID{genre_id} deleted")
        return {"message": "Genre deleted"}
    return {"message": "Genre not found"}

@router_film.post("/", response_model=structuring.Film)
async def create_film_route(schema: structuring.FilmCreate, db: Session = Depends(get_db)):
    film = create_film(db, schema)
    await notify_clients(f"{film.name} added")
    return film

@router_film.get("/", response_model=List[structuring.Film])
async def read_films(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    films = get_films(db, skip=skip, limit=limit)
    return films

@router_film.patch("/{film_id}")
async def update_film_route(film_id: int, schema: structuring.FilmUpdate, db: Session = Depends(get_db)):
    updated_film = update_film(db, film_id, schema)
    if updated_film:
        await notify_clients(f"{updated_film.name} updated")
        return updated_film
    return {"message": "Film not found"}

@router_film.delete("/{film_id}")
async def delete_film_route(film_id: int, db: Session = Depends(get_db)):
    deleted = delete_film(db, film_id)
    if deleted:
        await notify_clients(f"ID{film_id} deleted")
        return {"message": "Film deleted"}
    return {"message": "Film not found"}
