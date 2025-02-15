import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv(override=True)

# Codificar a senha para URL
db_password = quote_plus(os.getenv('DB_PASSWORD'))

# Construir a URL do banco de dados
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{db_password}" \
               f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Criação da engine
engine = create_engine(DATABASE_URL, echo=True)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)