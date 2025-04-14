from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List, Type
import models
from models import Categories, Marques, Fournisseurs


def insert_conversation(db: Session, session_id: str):
    is_session_exist = db.query(models.Conversation).filter(models.Conversation.session_id==session_id).first()
    if is_session_exist:
        return
    conversation = models.Conversation(session_id=session_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

def insert_messages(db: Session, session_id: str, user_query: str, ai_response: str):
    messages = models.Messages(session_id=session_id, user_query=user_query, ai_response=ai_response)
    db.add(messages)
    db.commit()
    db.refresh(messages)

def get_history(db: Session, session_id: str):
    db_messages = db.query(models.Messages).filter(models.Messages.session_id==session_id).all()
    messages = []
    for row in db_messages:
        messages.extend([
            {"role": "human", "content": row.user_query},
            {"role": "ai", "content": row.ai_response}
        ])
    return messages

# Fonctions pour les catégories
def obtenir_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Categories]]:
    """Obtenir toutes les catégories"""
    return db.query(models.Categories).offset(skip).limit(limit).all()

def obtenir_categorie(db: Session, categorie_id: int) -> models.Categories:
    """Obtenir une catégorie par son ID"""
    return db.query(models.Categories).filter(models.Categories.categorie_id == categorie_id).first()

# Fonctions pour les marques
def obtenir_marques(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Marques]]:
    """Obtenir toutes les marques"""
    return db.query(models.Marques).offset(skip).limit(limit).all()

def obtenir_marque(db: Session, marque_id: int) -> models.Marques:
    """Obtenir une marque par son ID"""
    return db.query(models.Marques).filter(models.Marques.marque_id == marque_id).first()

# Fonctions pour les fournisseurs
def obtenir_fournisseurs(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Fournisseurs]]:
    """Obtenir tous les fournisseurs"""
    return db.query(models.Fournisseurs).offset(skip).limit(limit).all()

def obtenir_fournisseur(db: Session, fournisseur_id: int) -> models.Fournisseurs:
    """Obtenir un fournisseur par son ID"""
    return db.query(models.Fournisseurs).filter(models.Fournisseurs.fournisseur_id == fournisseur_id).first()

# Fonctions CRUD pour les produits
def ajouter_produit(
    db: Session,
    nom: str,
    prix: float,
    quantité_en_stock: int,
    description: Optional[str] = None,
    categorie_id: Optional[int] = None,
    fournisseur_id: Optional[int] = None,
    marque_id: Optional[int] = None,
    date_expiration: Optional[date] = None
):
    """Ajouter un nouveau produit dans la base de données"""
    print(date_expiration)
    produit = models.Produits(
        nom=nom,
        description=description,
        prix=prix,
        quantité_en_stock=quantité_en_stock,
        categorie_id=categorie_id,
        fournisseur_id=fournisseur_id,
        marque_id=marque_id,
        date_expiration=date_expiration
    )
    db.add(produit)
    db.commit()
    db.refresh(produit)
    return produit

def obtenir_produit(db: Session, product_id: int):
    """Obtenir un produit par son ID"""
    return db.query(models.Produits).filter(models.Produits.product_id == product_id).first()

def obtenir_tous_produits(db: Session, skip: int = 0, limit: int = 100):
    """Obtenir tous les produits avec leurs relations"""
    return (
        db.query(models.Produits)
        .join(models.Categories, models.Produits.categorie_id == models.Categories.categorie_id, isouter=True)
        .join(models.Marques, models.Produits.marque_id == models.Marques.marque_id, isouter=True)
        .join(models.Fournisseurs, models.Produits.fournisseur_id == models.Fournisseurs.fournisseur_id, isouter=True)
        .offset(skip)
        .limit(limit)
        .all()
    )

def modifier_produit(
    db: Session,
    product_id: int,
    nom: Optional[str] = None,
    description: Optional[str] = None,
    prix: Optional[float] = None,
    quantité_en_stock: Optional[int] = None,
    categorie_id: Optional[int] = None,
    fournisseur_id: Optional[int] = None,
    marque_id: Optional[int] = None,
    date_expiration: Optional[date] = None
):
    """Modifier un produit existant"""
    produit = obtenir_produit(db, product_id)
    if produit:
        if nom is not None:
            produit.nom = nom
        if description is not None:
            produit.description = description
        if prix is not None:
            produit.prix = prix
        if quantité_en_stock is not None:
            produit.quantité_en_stock = quantité_en_stock
        if categorie_id is not None:
            produit.categorie_id = categorie_id
        if fournisseur_id is not None:
            produit.fournisseur_id = fournisseur_id
        if marque_id is not None:
            produit.marque_id = marque_id
        if date_expiration is not None:
            produit.date_expiration = date_expiration
        
        db.commit()
        db.refresh(produit)
    return produit

def supprimer_produit(db: Session, product_id: int):
    """Supprimer un produit par son ID"""
    produit = obtenir_produit(db, product_id)
    if produit:
        db.delete(produit)
        db.commit()
        return True
    return False
