"""
Script para atualizar o esquema do banco de dados
Adiciona as colunas necessárias para a tabela processing_jobs
"""

from flask import Flask
from src.models.user import db
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def migrate_database():
    """Atualiza o esquema do banco de dados"""
    app = create_app()
    
    with app.app_context():
        try:
            # Executar comandos SQL para adicionar colunas faltantes
            db.engine.execute("""
                ALTER TABLE processing_jobs 
                ADD COLUMN IF NOT EXISTS original_filename VARCHAR(255);
            """)
            
            db.engine.execute("""
                ALTER TABLE processing_jobs 
                ADD COLUMN IF NOT EXISTS file_size INTEGER;
            """)
            
            db.engine.execute("""
                ALTER TABLE processing_jobs 
                ADD COLUMN IF NOT EXISTS replicate_prediction_id VARCHAR(255);
            """)
            
            db.engine.execute("""
                ALTER TABLE processing_jobs 
                ADD COLUMN IF NOT EXISTS error_message TEXT;
            """)
            
            db.engine.execute("""
                ALTER TABLE processing_jobs 
                ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP;
            """)
            
            print("✅ Migração do banco de dados concluída com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro na migração: {str(e)}")

if __name__ == "__main__":
    migrate_database()

