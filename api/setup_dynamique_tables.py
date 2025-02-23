from  typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

load_dotenv()

def get_select_tables(conversation=None, model ="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"):
    if conversation is None:
        conversation = []
    llm = ChatTogether(model_name=model)
    def get_table_details():
        table_description = pd.read_csv("../docs/desrciption_db.csv")

        tables_details = ""
        for index, row in table_description.iterrows():
            tables_details = tables_details + "Table Name: " + row["Table Name"] + "\nTable description: " + row[
                "Description"] + "\n"
        return tables_details

    table_details = get_table_details()

    class Table(BaseModel):
        names: List[str] = Field(description="Name of the table in SQL database")

    table_prompt = f"""
            Return the tables names of all the SQL tables that MIGHT be relevant to the user question and try to understand
            the user question with his chat_history.
            table_names: 
            {table_details}
            chat_history: 
            {conversation[-6::]}
            Remember to include all the potential relevant tables, even if you don't sure.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", table_prompt),
        ("human", "{question}")
    ])

    structured_llm = llm.with_structured_output(Table)

    def get_tables(tables: List[Table]) -> List[str]:
        tables = [table for table in tables]
        return tables[0][1]

    select_tables = prompt | structured_llm | get_tables
    return select_tables
