from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, Float, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Conversation(Base):
    __tablename__ = "application_logs"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True)
    created_at = Column(TIMESTAMP, default=datetime.now())

    messages = relationship("Messages", back_populates="messages")

class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("application_logs"))
    user_query = Column(String)
    ai_response = Column(String)

    messages = relationship("Conversation", back_populates="messages")

# Supermarket Models
class Categories(Base):
    __tablename__ = "categories"
    categorie_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(50), nullable=False)
    description = Column(Text)

    produits = relationship("Produits", back_populates="categorie")

class Marques(Base):
    __tablename__ = "marques"
    marque_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(50), nullable=False)
    description = Column(Text)
    pays_origine = Column(String(50))

    produits = relationship("Produits", back_populates="marque")

class Fournisseurs(Base):
    __tablename__ = "fournisseurs"
    fournisseur_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    adresse = Column(Text)
    telephone = Column(String(20))

    produits = relationship("Produits", back_populates="fournisseur")

class Produits(Base):
    __tablename__ = "produits"
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    description = Column(Text)
    prix = Column(DECIMAL(10, 2), nullable=False)
    quantité_en_stock = Column(Integer, nullable=False)
    categorie_id = Column(Integer, ForeignKey("categories.categorie_id"))
    fournisseur_id = Column(Integer, ForeignKey("fournisseurs.fournisseur_id"))
    marque_id = Column(Integer, ForeignKey("marques.marque_id"))
    date_expiration = Column(Date)

    categorie = relationship("Categories", back_populates="produits")
    marque = relationship("Marques", back_populates="produits")
    fournisseur = relationship("Fournisseurs", back_populates="produits")
    stock_movements = relationship("Stock", back_populates="produit")

class Stock(Base):
    __tablename__ = "stock"
    stock_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("produits.product_id"))
    quantite_ajoutee = Column(Integer, nullable=False)
    date_ajout = Column(Date, nullable=False)

    produit = relationship("Produits", back_populates="stock_movements")
