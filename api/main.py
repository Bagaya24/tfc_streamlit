import uuid
from typing import List

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from pydantic_utils import QueryInput, QueryResponse, DetailAchat

from crud import insert_conversation, insert_messages, get_history
from langchain_utils import get_assistant_answer
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

def get_bd_historique():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput, db: Session = Depends(get_bd_historique)):
    session_id = query_input.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
    conversation = get_history(db=db, session_id=session_id)

    ai_chain = get_assistant_answer()
    ai_answer = ai_chain.invoke({
        "question": query_input.question,
        "conversation": conversation
    })
    insert_conversation(db=db, session_id=session_id)
    insert_messages(db=db, session_id=session_id, user_query=query_input.question, ai_response=ai_answer)

    return QueryResponse(answer=ai_answer, session_id=session_id)

@app.get("/achat")
def achat(noms, prix, nombre, request: Request):
    noms = noms.split(",")
    prix = prix.split(",")
    quantity = nombre.split(",")
    nombre_produit = len(noms)
    prix_total = 0
    prix_quantity = []
    for p,q in zip(prix, quantity):
        result = round(float(p) * float(q), 1)
        prix_quantity.append(result)
        prix_total += result

    return templates.TemplateResponse("index.html",
                                      {
                                          "request": request,
                                          "noms": noms,
                                          "prix": prix,
                                          "quantite": quantity,
                                          "nombre_produit": nombre_produit,
                                          "prix_total": prix_total,
                                          "prix_quantite": prix_quantity
                                      })
