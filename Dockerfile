# Usa uma imagem oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do backend para dentro do container
COPY . /app

# Atualiza o pip e instala as dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exponha a porta (Railway usa automaticamente)
EXPOSE 8000

# Comando para rodar o servidor Gunicorn apontando para seu arquivo main.py dentro do src
CMD ["gunicorn", "src.main:app", "--bind", "0.0.0.0:8000"]
