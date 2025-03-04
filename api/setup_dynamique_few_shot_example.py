from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

example_few_shot = [
    {
        "input": "Bonjour",
        "query": 'SELECT *  FROM categories '
    },
    {
        "input": 'Quel sont les marques de produits que vous avez?',
        "query": 'SELECT nom FROM marques',
    },
    {
        "input": 'Avez vous un téléphone?',
        "query": 'SELECT nom FROM produits WHERE description LIKE "%téléphone%" OR description LIKE "%smartphone%";'
    },
    {
        "input": "Avez un produit de la marque nike?",
        "query": 'SELECT produits.nom AS product_name, produits.description AS product_description, produits.prix,'
                 'marques.nom AS brand_name FROM  supermarche.produits JOIN supermarche.marques ON '
                 'produits.marque_id = marques.marque_id WHERE marques.nom = "nike";'
    },
    {
        "input": "lequel de chocolat est le moin chère ",
        "query": 'SELECT nom, prix FROM supermarche.produits WHERE description LIKE "%chocolat%" ORDER BY prix ASC LIMIT 1'
    },
    {
        "input": "dites moi son prix",
        "query": 'SELECT prix FROM supermarche.produits WHERE nom LIKE "%nom_du_produit%" or description LIKE "%nom_produit%"'
    },
    {
        "input": "Je vais en acheter 3",
        "query": 'SELECT prix * 3, nom FROM supermarche.produits WHERE nom LIKE "%nom_du_produit%" or description LIKE "%nom_produit%"'
    },
    {
        "input": "J'ai faim",
        "query": 'SELECT nom, description, prix FROM supermarche.produits WHERE categorie_id = (SELECT categorie_id FROM supermarche.categories WHERE nom = "Alimentaire")'
    },
    {
        "input": "Ça coûte combien",
        "query": 'SELECT prix FROM produits WHERE nom LIKE "%Coca%"'
    },
    {
        "input": "Bonjour, je cherche du pain",
        "query": 'SELECT nom, description, prix FROM produits WHERE categorie_id = (SELECT categorie_id FROM categories WHERE nom = "Alimentaire")'
    },
    {
        "input": "en prenant le parfum, le bracelet et la télé, ça va coûter combien?",
        "query": "SELECT SUM(prix) FROM produits WHERE nom IN ('Chanel N°5', 'Cartier bracelet', 'Sony TV 4K');"
    },
    {
        "input": "je vais prendre le chips et deux coca",
        "query": "SELECT prix FROM produits WHERE nom LIKE '%Lay\'s Chips%' OR nom LIKE '%Coca-Cola%"
    },
    {
        "input": "je voudrais une boisson",
        "query": 'SELECT nom, description, prix FROM supermarche.produits WHERE categorie_id = (SELECT categorie_id FROM categories WHERE nom = "Boissons")'
    },
    {
        "input": "je vais prendre une télé avec 3 oreo alors",
        "query": 'SELECT SUM(prix * quantite) AS total_prix FROM(SELECT prix,1 AS quantite FROM produits where '
                 'nom="Sony TV 4K"  union all select prix, 3 AS quantite from produits where nom = "Oreo Biscuits") as '
                 'sous_requete;'
    },
    {
        "input": "quel boisson pouvez vous me proposer",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON'
                 ' p.categorie_id = c.categorie_id WHERE c.nom LIKE "%boisson%"'
    }
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}\n"),
    ("ai", "{query}")
])

embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
to_vectorize = [" ".join(examples.values()) for examples in example_few_shot]
vectorstore = Chroma.from_texts(to_vectorize, embedding, metadatas=example_few_shot)

