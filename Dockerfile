FROM python:3.11.3-alpine3.18
LABEL maintainer="davicordeiro01012008@gmail.com"

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "project" (código Django + requirements.txt) para dentro do container.
COPY project /project

# Entra na pasta project no container (onde fica o manage.py)
WORKDIR /project  

# A porta 8000 estará disponível para conexões externas ao container
# É a porta que vamos usar para o Django.
EXPOSE 8000

# Cria o venv, instala as dependências, cria um usuário sem privilégios (duser)
# e prepara as pastas de arquivos estáticos e de mídia com as permissões dele.
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /project/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media

# Coloca o venv no PATH, assim "python" e "pip" usam o venv sem precisar ativá-lo
ENV PATH="/venv/bin:$PATH"

# Muda o usuário para duser
USER duser

# Aplica as migrations e sobe o servidor de desenvolvimento do Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]