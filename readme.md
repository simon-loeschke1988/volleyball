
# Volleyballdatenbank

## Projektbeschreibung
In diesem Projekt sollen die Daten der Beachvolleyballturniere weltweit dargestellt werden.

## Installation
Um dieses Projekt auf deinem lokalen Entwicklungsrechner zu installieren, folge diesen Schritten:

1. Clone das Repository auf deinen Computer.
   ```sh
   git clone https://github.com/simon-loeschke1988/volleyball.git
   ```

2. Wechsle in das Projektverzeichnis.
   ```sh
   cd volleyball
   ```

3. Richte eine virtuelle Umgebung ein (optional, aber empfohlen).
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

4. Installiere die Abhängigkeiten.
   ```sh
   pip install -r requirements.txt
   ```

## Verwendung
Um das Projekt auszuführen, folge diesen Schritten:

1. Aktiviere deine virtuelle Umgebung (falls verwendet).
   ```sh
   source venv/bin/activate
   ```

2. Führe das Projekt aus.
   ```sh
   python manage.py runserver
   ```

3. Öffne deinen Webbrowser und gehe zu [http://localhost:8000/](http://localhost:8000/).

## Funktionen

### Background Worker

- Die Datenbank wird mit Background Worker über einen Celery Beat stündlich aktualisiert

### Spieler

Die Spieler können sowohl mit Namen, als auch mit Federation Code gesucht werden.

#TODO
- ...

## Verwendete Module und Technologien
- Django: Dieses Projekt basiert auf dem Django-Framework.
- Celery: Celery wird für die Aufgabenplanung verwendet.
  - Alle instanzen müssen im Projektordner starten, sonst Fehlermeldung
- POSTGRESQL (über Docker)
- Für die Verwendung von Celery ist ein Datenbroker nötig, hierfür habe ich die standardlösung verwendet: RabbitMQ
  - Hierfür ist keine spezielle Konfiguration nötig: Server starten, und fertig
- Tailwind Konfiguration: https://tailwindcss.com/docs/configuration

## Beitragsrichtlinien
Wir freuen uns über Beiträge zur Weiterentwicklung dieses Projekts. Bitte beachte unsere [Beitragsrichtlinien](CONTRIBUTING.md) für Details zur Zusammenarbeit und zum Einreichen von Änderungsvorschlägen.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen findest du in der [Lizenzdatei](LICENSE).

## Autoren
- Simon Löschke (https://github.com/simon-loeschke1988)


