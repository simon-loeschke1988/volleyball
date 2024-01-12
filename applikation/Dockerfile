# Python-Image als Basis
FROM python:3.12.1

# Umgebungsvariablen setzen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Arbeitsverzeichnis im Container
WORKDIR /code

# Python-Abhängigkeiten installieren
COPY requirements.txt /code/
# Virtuelle Umgebung erstellen und aktivieren
RUN python -m venv /code/venv
ENV PATH="/code/venv/bin:$PATH"

# Python-Abhängigkeiten installieren
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Node.js installieren
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Node.js-Abhängigkeiten installieren
COPY package.json package-lock.json /code/
RUN npm install

# Projektcode kopieren
COPY . /code/

# Django-Startkommando
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
