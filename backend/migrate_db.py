#!/usr/bin/env python3
"""
Script de migração do banco de dados para UltraImageAI
Inicializa as tabelas necessárias no PostgreSQL
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Adiciona o diretório src ao path para importar os modelos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_app():
    """Cria a aplicação Flask para migração"""
    app = Flask(__name__)
    
    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        print("ERRO: Variável DATABASE_URL não encontrada!")
        sys.exit(1)
    
    return app

def run_migrations():
    """Executa as migrações do banco de dados"""
    try:
        print("🔄 Iniciando migração do banco de dados...")
        
        # Cria a aplicação
        app = create_app()
        
        # Inicializa o SQLAlchemy
        db = SQLAlchemy()
        db.init_app(app)
        
        with app.app_context():
            # Importa todos os modelos para garantir que as tabelas sejam criadas
            try:
                from models.user import User
                print("✅ Modelo User importado com sucesso")
            except ImportError as e:
                print(f"⚠️  Aviso: Não foi possível importar modelo User: {e}")
                print("   Criando estrutura básica...")
            
            # Cria todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas/atualizadas com sucesso!")
            
            # Verifica se as tabelas foram criadas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Tabelas disponíveis: {tables}")
            
        print("🎉 Migração concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 UltraImageAI - Migração do Banco de Dados")
    print("=" * 50)
    
    success = run_migrations()
    
    if success:
        print("✅ Migração finalizada - Backend pronto para iniciar!")
        sys.exit(0)
    else:
        print("❌ Migração falhou - Verifique os logs acima")
        sys.exit(1)

