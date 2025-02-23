from langchain_core.prompts import MessagesPlaceholder, FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_fireworks import ChatFireworks

from setup_dynamique_few_shot_example import vectorstore

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

