# Autorschaftstest

Dieses Programm untersucht einen unbekannten Text und versucht,
ihn anhand verschiedener sprachlicher Eigenschaften einem bekannten
Referenztext und damit einem Autor zuzuordnen.

Das Programm wurde im Rahmen der Abschlussaufgabe der Vorlesung
"Algorithmische Grundlagen in Python" entwickelt.


## Funktionsweise

Für einen Text werden fünf Eigenschaften berechnet:

- DWL: durchschnittliche Wortlänge
- TTR: Anzahl verschiedener Wörter / Anzahl aller Wörter
- HLR: Anzahl einmal vorkommender Wörter / Anzahl aller Wörter
- DSL: durchschnittliche Anzahl der Wörter pro Satz
- DSS: durchschnittliche Anzahl der Satzteile pro Satz

Diese fünf Werte bilden die Signatur eines Textes.

Die Signatur des eingegebenen Textes wird mit den Signaturen
bekannter Referenztexte verglichen.

Für den Vergleich werden die Unterschiede der einzelnen Werte
mit folgenden Faktoren gewichtet:

- DWL: 11
- TTR: 33
- HLR: 50
- DSL: 0.4
- DSS: 4

Je kleiner der berechnete Ähnlichkeitswert ist, desto ähnlicher
sind sich die beiden Textsignaturen.

Der Referenztext mit dem kleinsten Ähnlichkeitswert wird als
wahrscheinlichste Zuordnung ausgegeben.


## Programmstruktur
```text
autorschaftstest/
├── texte/                  # Ordner für die zu analysierende Textdateien
├── autoren.py              # Zuordnung der Textdateien zu den (besten) Autoren
├── main.py                 # Für das Starten des Programms
├── README.md               # Die Projektdokumentation
├── textanalyse.py          # Hauptmodul mit den Analysefunktionen
├── vorverarbeitung.py      # Skript für die Vorverarbeitung und Filterung der Textdateien
```

### main.py

Hauptprogramm des Autorschaftstests.

Das Programm fragt nach einer Textdatei, berechnet deren Signatur
und vergleicht sie mit den bekannten Referenztexten.


### vorverarbeitung.py

Enthält Funktionen zum Einlesen und Vorbereiten der Textdateien.

Funktionen:

- read_file()
- preprocessing()


### textanalyse_mod.py

Enthält die Funktionen zur Analyse eines Textes.

Unter anderem werden hier DWL, TTR, HLR, DSL und DSS berechnet.

Funktionen:

- get_words()
- count_words()
- count_different_words()
- count_unique_words()
- average_word_length()
- ttr()
- hlr()
- get_sentences()
- words_per_sentence()
- parts_per_sentence()
- get_signature()


### autoren.py

Enthält die Funktionen für den Vergleich der Textsignaturen.

Funktionen:

- get_author_signature()
- similarity()
- find_best_author()


### texte/

Dieser Ordner enthält die verwendeten Referenztexte und Testtexte.


## Benutzung

Das Programm wird über main.py gestartet.

Zum Beispiel:

python3 main.py

Anschließend wird nach dem Namen einer Textdatei gefragt:

Dateiname im Ordner texte: faust-test.txt

Die angegebene Datei muss sich im Ordner "texte" befinden.

Danach gibt das Programm die berechneten Eigenschaften des Textes,
die Signaturen der Referenztexte, die Ähnlichkeitswerte und die
wahrscheinlichste Zuordnung aus.


## Beispiel

Eingabe:

faust-test.txt

Ergebnis:

Wahrscheinlichste Zuordnung: Goethe (Faust)
Ähnlichkeitswert: 3.29


Ein weiterer Test mit einem Teil der "Italienischen Reise" ergab:

Wahrscheinlichste Zuordnung: Goethe (Italienische Reise)
Ähnlichkeitswert: 4.40


## Hinweis

Die Zuordnung basiert auf statistischen Eigenschaften der Texte.
Sie stellt daher keine sichere Bestimmung des Autors dar.

Insbesondere Textlänge, Textsorte und Schreibstil können die
berechneten Signaturen beeinflussen.