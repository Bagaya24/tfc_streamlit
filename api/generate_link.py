from typing import List

from pydantic import BaseModel, HttpUrl, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, ForeignKey, Date

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

def search_product(nom: str):
    return session.query(Produits.nom, Produits.prix).filter(Produits.nom == nom).first()

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
    price_mapping = dict(zip(product_names, response.product_number))
    results = session.query(Produits.nom, Produits.prix).filter(Produits.nom.in_(product_names)).all()

    if results:
        final_result = [(nom, prix * price_mapping[nom]) for nom, prix in results]
        print(final_result)
        product_names = [result[0] for result in final_result]
        product_prices = [str(result[1]) for result in final_result]
        return f"http://127.0.0.1:8000/achat?noms={','.join(product_names)}&prix={','.join(product_prices)}?nombre={','.join(str(response.product_number))}"
    return None


# print(get_product_info("Je voudrais acheter un kitkat , trois pepsi et deux dove"))



session.close()


