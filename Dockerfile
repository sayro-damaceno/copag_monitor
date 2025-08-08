FROM python:3.11-slim

# Instalar dependências do Chrome
RUN apt-get update && apt-get install -y \
  wget unzip gnupg curl chromium chromium-driver

# Copiar arquivos do projeto
WORKDIR /app
COPY . .

# Instalar pacotes Python
RUN pip install --no-cache-dir -r requirements.txt

# Executar o script
CMD ["python", "monitor.py"]
