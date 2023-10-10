# Volleyball-Projekt

Dieses Projekt soll daten aus der XML-API des Volleyballverbands holen, und in einer nutzbaren UI-verwenden.


# Changelog

## 10/10/2023

### Aufsetzen der Datenbank
Datenbank ist POSTGRESQL

- Bisherige Tabelle: Player
- **ACHTUNG:** Anderes Passwort für Production setzen, educational purpose only
- Datenmodellierung für Spieler initialisiert
- Vorteil gegenüber SQLITE: geringere Ladezeiten, mehr Performance, Usermanagement

### Zwei neue Management Commands

- import_player führt den Import der Spieler direkt in die Datenbank durch

```Python
python manage.py import_player
````

- db_wipe setzt die Datenbank **KOMPLETT ZURÜCK**

```Python
python manage.py db_wipe
````

### Frontend

Die Seite "Spieler" zeigt jetzt eine komplette Liste aller Spieler. **Achtung**: möglicherweise lange Ladezeiten.

### Hilfsdateien

- request_tester.py soll alle Requests testen und in eine *.xml-Datei schreiben. Hilft beim Debugging, falls Daten mal wieder nicht gefunden werden.
