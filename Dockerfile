FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do backend
COPY backend/ .

# Instala as dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expõe a porta
EXPOSE 8000

# Comando para iniciar o aplicativo
# O Railway usa a variável PORT automaticamente
CMD python migrate_db.py && python main.py

