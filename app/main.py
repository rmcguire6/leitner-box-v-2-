from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Card(BaseModel):
    subject: str
    question: str
    answer: str
    is_active: bool = True

@app.get("/")
async def root():
    return {"message": "Welcome to Leitner Box"}


@app.get('/cards')
def get_cards(db: Session= Depends(get_db)):
    cards = db.query(models.Card).all()
    return {"data": cards}

@app.post("/cards", status_code=status.HTTP_201_CREATED)
def create_card(card: Card, db: Session = Depends(get_db)):
    new_card = models.Card(**card.dict())
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return{"data": new_card}

@app.get('/cards/{id}')
def get_card(id:int, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.card_id == id).first()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} was not found")
    return {"card": card}

@app.delete('/cards/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_card(id:int, db: Session = Depends(get_db)):
    card_query = db.query(models.Card).filter(models.Card.card_id == id)
    if card_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} does not exist")
    card_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/cards/{id}')
def update_card(id:int, card: Card,  db: Session = Depends(get_db)):
    card_query = db.query(models.Card).filter(models.Card.card_id == id)
    found_card = card_query.first()
    if found_card == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"card with id {id} does not exist")
    card_query.update(card.dict(), synchronize_session=False)
    db.commit()
    return {'message': card_query.first()}