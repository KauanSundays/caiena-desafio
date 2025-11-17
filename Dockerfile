# Use uma imagem base Python slim para um container menor
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o diretório de trabalho
COPY . .

# Expõe a porta que o Gunicorn irá usar
EXPOSE 8000

# Comando para iniciar a aplicação usando Gunicorn.
# 'app:app' significa: módulo 'app' e a instância do Flask chamada 'app'.
# O Gunicorn será o servidor HTTP final.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
