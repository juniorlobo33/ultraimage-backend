FROM python:3.12-slim

WORKDIR /app/backend  # <--- MUDANÇA AQUI: Define o diretório de trabalho dentro da pasta 'backend'

COPY backend .         # <--- MUDANÇA AQUI: Copia o conteúdo da pasta 'backend' para o WORKDIR

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

# O comando CMD agora assume que está dentro de /app/backend
# Então, o caminho para main.py é src/main.py
CMD ["gunicorn", "src.main:app", "--bind", "0.0.0.0:${PORT}"]
