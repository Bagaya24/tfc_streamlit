from typing import List

from pydantic import BaseModel, HttpUrl, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, ForeignKey, Date, or_

from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:fazili@localhost:3306/supermarche"
Base = declarative_base()

llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
# llm = ChatOllama(model="llama3.2:latest")
class Produits(Base):
    __tablename__ = "Produits"
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    prix = Column(DECIMAL(10, 2), nullable=False)
    quantité_en_stock = Column(Integer, nullable=False)
    categorie_id = Column(Integer, ForeignKey("Categories.categorie_id"))
    date_expiration = Column(Date, nullable=True)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()


class ProductsLink(BaseModel):
    is_purchase: bool = Field(
        description="True if the user wants to buy, False if they are just asking for information")
    product_names: List[str]| None = Field(description="The names of the products")
    product_number: List[int] | None = Field(description="The number of each products")
    # product_price: int = Field(description="The price of the product in the database")

product_prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Determine if the user wants to buy a product or is just asking for information.
        If they want to buy, return 'is_purchase': True and the product name.
        If they are just asking, return 'is_purchase': False and no product details.
        Here some examples: 
        question: avez vous un produit?
        ai answer: False
        question: Combien coute tel produit?
        ai answer: False
        question: Je voudrais tel produit
        ai answer: False
        question: Je voudrais acheter tel produit
        ai answer: True
        question: Je voudrais prendre tel produit
        ai answer: True
    """),
    ("human", "{question}")
])

structured_output = llm.with_structured_output(ProductsLink)
prompt_with_output = product_prompt | structured_output

def get_product_info(question):
    response = prompt_with_output.invoke({"question": question})
    print(response)
    if not response.is_purchase:
        return None
    product_names = response.product_names
    if product_names is None:
        return None

    results = session.query(Produits.nom, Produits.prix).filter(or_(*(Produits.nom.like(f"%{product_name}%") for product_name in product_names))).all()
    print(results)
    if results:

        product_names = [result[0] for result in results]
        product_prices = [str(result[1]) for result in results]
        product_quantity = [str(quantity) for quantity in response.product_number]

        return f"http://127.0.0.1:8000/achat?noms={','.join(product_names)}&prix={','.join(product_prices)}&nombre={','.join(product_quantity)}"
    return None


# print(get_product_info("Je voudrais acheter un kit, deux iphone"))



session.close()


