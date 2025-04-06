from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(None)

class QueryResponse(BaseModel):
    answer: str
    session_id: str

class DetailAchat(BaseModel):
    product_names : List[str] | None
    product_prices : List[float] | None

# Modèles Pydantic pour les catégories
class CategorieBase(BaseModel):
    nom: str
    description: str | None = None

class Categorie(CategorieBase):
    categorie_id: int

    class Config:
        from_attributes = True

# Modèles Pydantic pour les marques
class MarqueBase(BaseModel):
    nom: str
    description: str | None = None
    pays_origine: str | None = None

class Marque(MarqueBase):
    marque_id: int

    class Config:
        from_attributes = True

# Modèles Pydantic pour les fournisseurs
class FournisseurBase(BaseModel):
    nom: str
    adresse: str | None = None
    telephone: str | None = None
    email: str | None = None

class Fournisseur(FournisseurBase):
    fournisseur_id: int

    class Config:
        from_attributes = True

# Modèles Pydantic pour les produits
class ProduitBase(BaseModel):
    nom: str
    description: str | None = None
    prix: float
    quantité_en_stock: int
    categorie_id: int | None = None
    fournisseur_id: int | None = None
    marque_id: int | None = None
    date_expiration: datetime | None = None

class ProduitCreate(ProduitBase):
    pass

class ProduitUpdate(BaseModel):
    nom: str | None = None
    description: str | None = None
    prix: float | None = None
    quantité_en_stock: int | None = None
    categorie_id: int | None = None
    fournisseur_id: int | None = None
    marque_id: int | None = None
    date_expiration: datetime | None = None

class Produit(ProduitBase):
    product_id: int
    categorie: Optional[Categorie] = None
    marque: Optional[Marque] = None
    fournisseur: Optional[Fournisseur] = None

    class Config:
        from_attributes = True
