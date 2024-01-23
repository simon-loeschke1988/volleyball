# Stage 1: Install Node.js and build frontend assets
FROM node:latest as build-stage

# Setzen des Arbeitsverzeichnisses im Container für das Frontend-Build
WORKDIR /app

# Kopieren der package.json und package-lock.json für Node.js
COPY package*.json ./

# Installieren der Node-Abhängigkeiten
RUN npm install

# Kopieren der restlichen Frontend-Dateien und Bauen des Frontends
COPY . .
RUN npm run build

# Stage 2: Set up the Python environment
FROM python:3.12.1

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /code

# Kopieren der gebauten Frontend-Assets aus der Build-Stage
COPY --from=build-stage /app/static /code/static

# Umgebungsvariablen setzen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m ensurepip

# Virtuelle Umgebung erstellen und aktivieren
#RUN python -m venv /code/venv
#ENV PATH="/code/venv/bin:$PATH"

# Installieren von Python-Abhängigkeiten
RUN pip install --upgrade pip wheel setuptools
COPY requirements.txt /code/
RUN  pip install --no-cache-dir -r /code/requirements.txt

# Kopieren des Django-Projektcodes
COPY . /code/


# Startkommando für Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
