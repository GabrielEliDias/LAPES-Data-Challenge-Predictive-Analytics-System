# 1. Imagem base com Python 3.9 slim (leve)
FROM python:3.11-slim

# 2. Define o diretório de trabalho no container
WORKDIR /app

# 3. Copia os arquivos do seu projeto para o container
COPY . .

# 4. Instala dependências a partir do requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --resume-retries 5 -r requirements.txt

# 5. Expõe a porta que o Jupyter usará
EXPOSE 8888

# 6. Comando padrão ao rodar o container
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
