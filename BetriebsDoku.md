# Betriebsdokumentation SeleniumWebScraping 1.0

### Generelle Beschreibung

In dieser Implementierung werden technische Zeichnungen und die dazugehörigen Tabellen auf der Website https://www.traceparts.com/ lokal abgespeichert. 
Grundlage für die Ergebnisse sind ein Suchbegriff und die Auswahl eines Hertsellers. Die Auswahl der Hersteller beschränkt sich auf Ganter und Kipp. 
Für die Suchergebnisse werden nur technische Komponeneten ausgewählt. Die Bilder/tabellen werden in einzelnen Ordnern 
im ordner 'images' gespeichert.

### Voraussetzungen für den Betrieb

* Die aktuelle Version von Mozilla Firefox muss installiert sein.
* Im Verzeichnis des Projekts muss der dem eigenen Betriebssystem ensprechende geckodriver hinterlegt sein. Dieser ist hier https://github.com/mozilla/geckodriver/releases zu finden.

### Konfiguration der globalen Variablen

In main.py befinden sich einige globale Variablen, die die Grundlage für die Suche darstellen:
* SEARCH_TERM: Hier ist der Suchbegriff einzugeben
* MANUFACTURER: Angabe des gewünschten Herstellers für den Suchbegriff. Möglich sind ManufacturerGanter und ManufacturerKipp
* MAX_RESULTS_PER_SEARCH_TERM: Die maximale Anzahl an gewünschten Ergebnissen für die SUche
* ITERATION_MAX_FOR_SCROLLING: Die maximale Anzahl an Scrollaktionen für die 
Suchergebnisse. Um alle möglichen Suchergebnisse zu erfassen, muss nach der 
Suche nach unten gescrollt werden, damit mehr Ergebnisse geladen werden. Falls nicht alle möglichen Suchergebnisse
erfasst werden sollen, ist damit eine Eingrenzung möglich
