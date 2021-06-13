# Use a imagem oficial como imagem principal.
FROM python:3.9

LABEL maintainer='Boa_Vista_SCPC'

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y unzip xvfb libxi6 libgconf-2-4

# Usado para containers fora do Gitlab BVS
#RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

# Executa o comando dentro do sistema de arquivos de imagem.
RUN pip install google-cloud-storage
RUN pip install requests

# Cria o diretório de trabalho
RUN mkdir -p /usr/src/app

# Define o diretório de trabalho.
WORKDIR /usr/src/app

# Copia os arquivos do host para o sistema de arquivos de imagem.
COPY . /usr/src/app

EXPOSE 8080

# Executa o comando especificado dentro do contêiner.
CMD python3 bot_ibama.py
