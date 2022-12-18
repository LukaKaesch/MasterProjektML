# Betriebsdokumentation SeleniumWebScraping 2.0

### Generelle Beschreibung

In dieser Implementierung werden obj. Dateien von einzelnen Produkten der verschiedene Produktgruppen der mechanischen Komponenten auf der
Website https://www.traceparts.com/ lokal abgespeichert.
Zusätzlich wird für jedes Produkt eine XML-Datei mit grundlegenden Informationen wie der URL, Artikelnummer und
Hersteller gespeichert.


### Voraussetzungen für den Betrieb

* Die aktuelle Version von Mozilla Firefox muss installiert sein.
* Im Verzeichnis des Projekts muss der dem eigenen Betriebssystem ensprechende geckodriver hinterlegt sein. Dieser ist
  hier https://github.com/mozilla/geckodriver/releases zu finden.

### Konfiguration der globalen Variablen

In main.py befinden sich einige globale Variablen, die die Grundlage für die Suche darstellen:

* EMAIL, PW: Hier sind die Login_Daten für Traceparts einzutragen. Für den Download der obj-Daten ist ein vorhandener
  Account notwendig.
* SEARCH_TERM: Hier ist der Suchbegriff einzugeben
* MANUFACTURER: Angabe des gewünschten Herstellers für den Suchbegriff. Möglich sind ManufacturerGanter und
  ManufacturerKipp
* CREATE_NEW_SEARCH_RESULT_LIST: Wenn eine Suche nach Produkten durchgeführt werden soll, muss hier True gesetzt sein.
  Für False wird die Suche übersprungen und direkt nach dem Login mit den Produkten fortgefahren.
* APPEND_NEW_SEARCH_RESULTS_TO_EXISTING_XML = Steht diese Variable auf True werden die Suchergebnisse zu der schon
  vorhandenen Liste links.xml
  hinzugefügt. Ansonsten wird eine neue Liste erstellt.
* AMOUNT_PER_CATEGORY: Gibt die Anzahl der zu speichernden Produkte pro Produktkategorie an.

Weitere Anmerkungen: In main.py in der Funktion init_config() muss für die Variable options.binary_location der korrekte
Pfad von Firefox angegeben sein!
