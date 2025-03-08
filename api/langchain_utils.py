from langchain_core.prompts import MessagesPlaceholder, FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain.chains import create_sql_query_chain, create_retrieval_chain
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_fireworks import ChatFireworks
from operator import itemgetter

from langchain_groq import ChatGroq

from generate_link import get_product_info
from setup_dynamique_few_shot_example import vectorstore
from setup_dynamique_tables import get_select_tables
from db_utils import get_db

select_tables = get_select_tables()
db = get_db()
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=3,
    input_keys=["input"]
)

example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}\nSQLQuery:"),
            ("ai", "{query}"),
        ]
    )
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    input_variables=["input", "top_k"],
)

generate_sql_prompt = ChatPromptTemplate.from_messages(
    [
            ("system", """
                You are a MySQL expert of the schema below. Given an input question, create a syntactically correct MySQL 
                query  that answer to the input question. You can order the results to return the most informative data in 
                the database.Never query for all columns from a table. You must query only the columns that are needed to
                answer the question.Pay attention to use only the column names you can see in the tables below. Be careful 
                to not query for columns that do not exist, use only the columns of the table, don't try to create on. 
                Also, pay attention to which column is in which table.Pay 
                attention to use CURDATE() function to get the current date, if the question 
                involves "today". You'll write the the SQL query and nothing else.
                Here is the relevant table info:{table_info}
                DO NOT ANSWER SOMETHING ELSE IF IS NOT A SQL QUERY.
                HERE IS SOME EXAMPLE THAT YOU WILL REFER TO ANSWER THE USER'S QUESTION:
            """),
            few_shot_prompt,
            ("system", "pay attention to see the conversation history before answer, here the conversation history:"),
            MessagesPlaceholder("conversation"),
            ("human", "{input}")
        ]
)
answer_prompt = ChatPromptTemplate.from_template(
        """
        Vous êtes un assistant pour les clients du supermarché Ruvunda à Goma, qui aide les clients avec les achats. 
        Vous aidez les clients à trouver des produits ou des informations dans la base de données du magasin. Soyez
        poli, chaleureux et clair dans vos réponses, en donnant seulement les informations essentielles mais en 
        proposant au client qu'il puisse demander plus de détails.
        Instructions spécifiques :
        Si le résultat de la requête SQL est null, répondez uniquement par :
        "Veuillez reformuler votre question, s'il vous plaît."
        ou
        "Nous n'avons pas ce produit."
        La devise de la monnaie du supermarché est le dollars américain $
        (Choisissez la réponse la plus adaptée au contexte de la conversation, mais ne proposez pas les deux en même temps.)
        Si le lien de paiement (link) est None, ne mentionnez aucun lien dans votre réponse. Ne parlez pas d'un potentiel
        lien de paiement.
        Si le lien de paiement est disponible (link n'est pas None), assurez-vous de remplacer les espaces dans le lien 
        par %20 pour qu'il soit valide. Présentez-le sous la forme :
        [ici](lien_sans_espaces)
        Exemple :
        Avec espace : http://127.0.0.1:8000/achat?noms=Coca-Cola Zero?prix=3.00
        Sans espace : http://127.0.0.1:8000/achat?noms=Coca-Cola%20Zero?prix=3.00
        Format de la réponse : Vous pouvez acheter ce produit [ici](http://127.0.0.1:8000/achat?noms=Coca-Cola%20Zero?prix=3.00).

        Ne saluez le client qu'au début de la conversation. Ensuite, assurez-vous que vos réponses restent cohérentes
        avec le contexte de la conversation.
        Conversation : {conversation}
        Question du client : {question}
        Requête SQL : {query}
        Résultat SQL : {result}
        Lien pour acheter : {link}
         """
    )

def get_assistant_answer(model: str = "llama-3.3-70b-versatile"):
    llm = ChatGroq(model_name=model)
    execute_query = QuerySQLDatabaseTool(db=db)
    generate_query = create_sql_query_chain(llm, db, generate_sql_prompt)
    answer_chain = answer_prompt | llm | StrOutputParser()
    return (RunnablePassthrough.assign(tables_names_to_use=select_tables)
         | RunnablePassthrough.assign(query=generate_query).assign(result=itemgetter("query") | execute_query) |
          RunnablePassthrough.assign(link = get_product_info) | answer_chain)

# a = get_assistant_answer()
# print(a.invoke({
#     "question": "Bonjour, je vais acheter un kitkat",
#     "conversation": []
# }))
