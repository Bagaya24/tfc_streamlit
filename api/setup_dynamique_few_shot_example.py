from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

example_few_shot = [
    {
        "input": "Pouvez vous me donner votre adresse?",
        "query": "SELECT 'Boulevard Kalema, Q. Les volcans, Commune de Goma, juste en diagonale avec Kin marche' AS message"
    },

    {
        "input": "Bonjour",
        "query": "SELECT 'Bonjour ! Bienvenue dans notre supermarché Ruvunga.' AS message"
    },
    {
        "input": "Votre horaire de travail",
        "query": "SELECT 'Du lundi au vendredi nous ouvrons de 7h à 20h, samedi dès 11h à 20h et dimanche dès 9h à 19h.' AS message"
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
        "query": """SELECT nom, description, prix FROM supermarche.produits WHERE categorie_id = (SELECT categorie_id 
                    FROM supermarche.categories WHERE nom IN ("Alimentaire", "Boulangerie", "Viandes", "Fruits et 
                    Légumes", "Charcuterie"))"""
    },
    {
        "input": "Ça coûte combien",
        "query": 'SELECT prix FROM produits WHERE nom LIKE "%Coca%"'
    },
    {
        "input": "Bonjour, je cherche du pain",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom = "Boulangerie" AND p.nom LIKE "%pain%"'
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
    },
    {
        "input": "je cherche une chaussure",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom LIKE "%Chaussure%"'
    },
    {
        "input": "je cherche un appareil electronique",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom LIKE "%electronique%"'
    },
    {
        "input": "Bonjour, je cherche une television",
        "query": 'SELECT nom, description, prix FROM supermarche.produits WHERE description LIKE "%télévision%" or nom LIKE "%television%";'
    },
    {
        "input": "C'est quoi le blender le moins chere",
        "query": "SELECT nom, prix FROM produits WHERE description LIKE '%blender%' ORDER BY prix ASC LIMIT 1"
    },
    {
        "input": "Quel saucisse irait le mieux avec le pain complet?",
        "query": 'SELECT nom, description, prix FROM supermarche.produits WHERE description LIKE "%saucisse%";'
    },
    {
        "input": "Pouvez vous avoir du pain et du fromage?",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom IN ("Boulangerie", "Produits laitiers")'
    },
    {
        "input": "Avez vous de la viande?",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom = "viandes"'
    },
    {
        "input": "Je cherche un jus",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom LIKE "%boisson%" AND p.nom LIKE "%jus%"'
    },
    {
        "input": "Avez vous de produits pour faire un petit déjeuner ?",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom = "boulangerie" or c.nom = "produits laitiers" or c.nom = "charcuterie"'
    },
    {
        "input": "Je voudrai faire un jus multi fruit",
        "query": 'SELECT p.nom, p.description, p.prix FROM supermarche.produits p JOIN supermarche.categories c ON p.categorie_id = c.categorie_id WHERE c.nom = "fruits et legumes"'
    }
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}\n"),
    ("ai", "{query}")
])

embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
to_vectorize = [" ".join(examples.values()) for examples in example_few_shot]
vectorstore = Chroma.from_texts(to_vectorize, embedding, metadatas=example_few_shot)

