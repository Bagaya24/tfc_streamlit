import os
import uuid

from typing import List
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from pydantic_utils import QueryResponse, QueryInput, Produit, ProduitCreate, ProduitUpdate, Categorie, Marque, \
    Fournisseur
from crud import (
    insert_conversation, insert_messages, get_history,
    ajouter_produit, obtenir_produit, obtenir_tous_produits,
    modifier_produit, supprimer_produit,
    obtenir_categories, obtenir_marques, obtenir_fournisseurs
)

from langchain_utils import get_assistant_answer
from database import ChatSessionLocal, SupermarketSessionLocal, chat_engine
import models

models.Base.metadata.create_all(bind=chat_engine)

def get_bd_historique():
    db = ChatSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_supermarche():
    db = SupermarketSessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Configuration des dossiers statiques et des templates
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "api\static")
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), r"api\templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes pour les pages
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index_maj.html", {"request": request})

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
    return {"answer": ai_answer, "session_id": session_id}

# Route pour achat
@app.get("/achat")
def achat(noms, prix, nombre, request: Request):
    noms = noms.split(",")
    prix_unitaire = prix.split(",")
    quantity = nombre.split(",")
    nombre_produit = len(noms)
    prix_total = 0
    prix_total_par_produit = []
    for p,q in zip(prix_unitaire, quantity):
        result = round(float(p) * float(q), 1)
        prix_total_par_produit.append(result)
        prix_total += result
    return templates.TemplateResponse("index_paiement.html",
                                      {
                                          "request": request,
                                          "noms": noms,
                                          "prix_unitaire": prix_unitaire,
                                          "quantite": quantity,
                                          "nombre_produit": nombre_produit,
                                          "prix_total": prix_total,
                                          "prix_total_par_produit": prix_total_par_produit
                                      })

# Routes pour les catégories
@app.get("/api/categories", response_model=List[Categorie])
def lire_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_supermarche)):
    """Obtenir la liste de toutes les catégories"""
    categories = obtenir_categories(db, skip=skip, limit=limit)
    return categories

# Routes pour les marques
@app.get("/api/marques", response_model=List[Marque])
def lire_marques(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_supermarche)):
    """Obtenir la liste de toutes les marques"""
    marques = obtenir_marques(db, skip=skip, limit=limit)
    return marques

# Routes pour les fournisseurs
@app.get("/api/fournisseurs", response_model=List[Fournisseur])
def lire_fournisseurs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_supermarche)):
    """Obtenir la liste de tous les fournisseurs"""
    fournisseurs = obtenir_fournisseurs(db, skip=skip, limit=limit)
    return fournisseurs

# Routes pour la gestion des produits
@app.get("/api/produits", response_model=List[Produit])
def lire_produits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_supermarche)):
    """Obtenir la liste de tous les produits"""
    produits = obtenir_tous_produits(db, skip=skip, limit=limit)
    return produits

@app.get("/api/produits/{product_id}", response_model=Produit)
def lire_produit(product_id: int, db: Session = Depends(get_db_supermarche)):
    """Obtenir un produit spécifique par son ID"""
    produit = obtenir_produit(db, product_id=product_id)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit

@app.post("/api/produits", response_model=Produit)
def creer_produit(produit: ProduitCreate, db: Session = Depends(get_db_supermarche)):
    """Créer un nouveau produit"""
    return ajouter_produit(
        db=db,
        nom=produit.nom,
        description=produit.description,
        prix=produit.prix,
        quantité_en_stock=produit.quantité_en_stock,
        categorie_id=produit.categorie_id,
        fournisseur_id=produit.fournisseur_id,
        marque_id=produit.marque_id,
        date_expiration=produit.date_expiration
    )

@app.put("/api/produits/{product_id}", response_model=Produit)
def update_produit(product_id: int, produit: ProduitUpdate, db: Session = Depends(get_db_supermarche)):
    """Mettre à jour un produit"""
    produit_modifie = modifier_produit(
        db=db,
        product_id=product_id,
        nom=produit.nom,
        description=produit.description,
        prix=produit.prix,
        quantité_en_stock=produit.quantité_en_stock,
        categorie_id=produit.categorie_id,
        fournisseur_id=produit.fournisseur_id,
        marque_id=produit.marque_id,
        date_expiration=produit.date_expiration
    )
    if produit_modifie is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit_modifie

@app.delete("/api/produits/{product_id}")
def effacer_produit(product_id: int, db: Session = Depends(get_db_supermarche)):
    """Supprimer un produit"""
    success = supprimer_produit(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"message": "Produit supprimé avec succès"}
