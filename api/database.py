from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration for the chat history database
CHAT_DATABASE_URL = "sqlite:///./db/historique_app.db"

# Configuration for the supermarket database
SUPERMARKET_DATABASE_URL = "mysql+pymysql://root:fazili@localhost:3306/supermarche"

# Create engines for both databases
chat_engine = create_engine(
    CHAT_DATABASE_URL, connect_args={"check_same_thread": False}
)

supermarket_engine = create_engine(
    SUPERMARKET_DATABASE_URL
)

# Create sessions for both databases
ChatSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=chat_engine)
SupermarketSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=supermarket_engine)

Base = declarative_base()
#
# # Helper functions to get database sessions
# def get_chat_db():
#     db = ChatSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# def get_supermarket_db():
#     db = SupermarketSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
