import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está configurada nas variáveis de ambiente.")

def run_migrations():
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as connection:
            # Criar a tabela 'users'
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(128) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            print("Tabela 'users' verificada/criada com sucesso.")

            # Criar a tabela 'processing_jobs'
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS processing_jobs (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    input_path VARCHAR(255),
                    output_path VARCHAR(255),
                    original_filename VARCHAR(255),
                    file_size INTEGER,
                    replicate_prediction_id VARCHAR(255),
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """))
            print("Tabela 'processing_jobs' verificada/criada com sucesso.")

            connection.commit() # Confirmar as alterações no banco de dados

    except Exception as e:
        print(f"Erro ao executar migrações: {e}")
        raise

if __name__ == "__main__":
    print("Executando migrações do banco de dados...")
    run_migrations()
    print("Migrações concluídas.")

