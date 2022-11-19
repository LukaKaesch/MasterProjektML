# Betriebsdokumentation SeleniumWebScraping 2.0

### Generelle Beschreibung

In dieser Implementierung werden technische Zeichnungen und die dazugehörigen Tabellen von einzelnen Produkten auf der Website https://www.traceparts.com/ lokal abgespeichert.
Zusätzlich werden für alle verschiedneen Ausführungen eines Produktes die .obj Datein gespeichert und in einzelnen Ordner abgespeichert.
In jedem dieser Ordner befindet sich auch eine XML-Datei mit grundlegenden Informationen wie der URL, Artikelnummer und Hersteller.

Grundlage für die Ergebnisse sind ein Suchbegriff und die Auswahl eines Herstellers. Die Auswahl der Hersteller beschränkt sich auf Ganter und Kipp. 
Für die Suchergebnisse werden nur technische Komponeneten ausgewählt. Die Bilder/Tabellen werden in einzelnen Ordnern 
im Ordner 'images' gespeichert. Die Suche nach Produkten ist von der anschließenden Speicherung entkoppelt. Die Suchergebnisse werden in einer xml-Datei links.xml
gespeichert und für die Speicherung der Daten wird diese Datei ausgelesen.

### Voraussetzungen für den Betrieb

* Die aktuelle Version von Mozilla Firefox muss installiert sein.
* Im Verzeichnis des Projekts muss der dem eigenen Betriebssystem ensprechende geckodriver hinterlegt sein. Dieser ist hier https://github.com/mozilla/geckodriver/releases zu finden.

### Konfiguration der globalen Variablen

In main.py befinden sich einige globale Variablen, die die Grundlage für die Suche darstellen:
* EMAIL, PW: Hier sind die Login_Daten für Traceparts einzutragen. Für den Download der obj-Daten ist ein vorhandener Account notwendig.
* SEARCH_TERM: Hier ist der Suchbegriff einzugeben
* MANUFACTURER: Angabe des gewünschten Herstellers für den Suchbegriff. Möglich sind ManufacturerGanter und ManufacturerKipp
* MAX_RESULTS_PER_SEARCH_TERM: Die maximale Anzahl an gewünschten Ergebnissen für die Suche
* ITERATION_MAX_FOR_SCROLLING: Die maximale Anzahl an Scrollaktionen für die 
Suchergebnisse. Um alle möglichen Suchergebnisse zu erfassen, muss nach der 
Suche nach unten gescrollt werden, damit mehr Ergebnisse geladen werden. Falls nicht alle möglichen Suchergebnisse
erfasst werden sollen, ist damit eine Eingrenzung möglich
* CREATE_NEW_SEARCH_RESULT_LIST: Wenn eine Suche nach Produkten durchgeführt werden soll, muss hier True gesetzt sein.
Für False wird die Suche übersprungen und direkt nach dem Login mit den Produkten fortgefahren.
* APPEND_NEW_SEARCH_RESULTS_TO_EXISTING_XML = Steht diese Variable auf True werden die Suchergebnisse zu der schon vorhandenen Liste links.xml
hinzugefügt. Ansonsten wird eine neue Liste erstellt.

Weitere Anmerkungen: In main.py in der Funktion init_config() muss für die Variable options.binary_location der korrekte 
Pfad von Firefox angegeben sein!
