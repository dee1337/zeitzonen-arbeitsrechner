# zeitzonen-arbeitsrechner

Zeitverschiebung & Arbeitszeit-Rechner

Eingabe: Stadt, Datum - Datum und Uhrzeit optional!
    Bsp1: python zeitzonen.py 'Tokyo'
    Bsp2: python zeitzonen.py 'Buenos Aires' 6.11.2026
    
Ausgabe: Zeitverschiebung, Datum/Uhrzeit in der Zielstadt und
         die deutsche Arbeitszeit (09:00-17:00) in Ortszeit der Zielstadt.

Reale Beispiele:

>> python zeitzonen.py zypern
  (gefunden via Geocoding: Κύπρος, Κύπρος - Kıbrıs)

==============================================================
  Zypern  –  Zeitzone Asia/Nicosia
==============================================================
  Zeitverschiebung zu Deutschland: +1:00 h
  Deutschland : Sa, 10.10.2026 15:45 (CEST)
  Zypern      : Sa, 10.10.2026 16:45 (EEST)

  Deutsche Arbeitszeit 09:00–17:00 entspricht vor Ort:
  ► 10:00  bis  18:00  (EEST)

  Stundenübersicht:
  Deutschland   Zypern                Einschätzung
  --------------------------------------------------------
  09:00         10:00 Sa              normale Arbeitszeit
  10:00         11:00 Sa              normale Arbeitszeit
  11:00         12:00 Sa              normale Arbeitszeit
  12:00         13:00 Sa              normale Arbeitszeit
  13:00         14:00 Sa              normale Arbeitszeit
  14:00         15:00 Sa              normale Arbeitszeit
  15:00         16:00 Sa              normale Arbeitszeit
  16:00         17:00 Sa              Randzeit
  17:00         18:00 Sa              Randzeit


  >> python zeitzonen.py 'Gran Canaria' 6.11.2026
  (gefunden via Geocoding: Gran Canaria, Canarias, España)

==============================================================
  Gran Canaria  –  Zeitzone Atlantic/Canary
==============================================================
  Zeitverschiebung zu Deutschland: -1:00 h
  Deutschland : Fr, 06.11.2026 15:46 (CET)
  Gran Canaria: Fr, 06.11.2026 14:46 (WET)

  Deutsche Arbeitszeit 09:00–17:00 entspricht vor Ort:
  ► 08:00  bis  16:00  (WET)

  Stundenübersicht:
  Deutschland   Gran Canaria          Einschätzung
  --------------------------------------------------------
  09:00         08:00 Fr              Randzeit
  10:00         09:00 Fr              normale Arbeitszeit
  11:00         10:00 Fr              normale Arbeitszeit
  12:00         11:00 Fr              normale Arbeitszeit
  13:00         12:00 Fr              normale Arbeitszeit
  14:00         13:00 Fr              normale Arbeitszeit
  15:00         14:00 Fr              normale Arbeitszeit
  16:00         15:00 Fr              normale Arbeitszeit
  17:00         16:00 Fr              normale Arbeitszeit
