from langchain_community.utilities import SQLDatabase


def get_db(db_uri: str = "mysql+pymysql://root:fazili@localhost:3306/supermarche"):
    return SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=2, include_tables=["marques", "produits", "categories", "stock"])

d = get_db()
