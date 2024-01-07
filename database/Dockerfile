FROM postgres:latest

# Setzen der Umgebungsvariablen
ENV POSTGRES_USER=volley
ENV POSTGRES_PASSWORD=volley
ENV POSTGRES_DB=volley

# Port 5432 freigeben
EXPOSE 5432

# Kopieren des Initialisierungsskripts in das Docker-Image
COPY init.sql /docker-entrypoint-initdb.d/
