#!/usr/bin/env python3
"""
Zeitverschiebung & Arbeitszeit-Rechner
Eingabe: Stadt, Datum - Datum und Uhrzeit optional!
    Bsp1: python zeitzonen.py 'Tokyo'
    Bsp2: python zeitzonen.py 'Buenos Aires' 6.11.2026
Ausgabe: Zeitverschiebung, Datum/Uhrzeit in der Zielstadt und
         die deutsche Arbeitszeit (09:00-17:00) in Ortszeit der Zielstadt.

Nutzung:
  python zeitverschiebung.py                      (interaktiv)
  python zeitverschiebung.py Tokio 15.11.2026 10:00
  python zeitverschiebung.py "Buenos Aires"       (heute, aktuelle Uhrzeit)

Optional (für JEDE Stadt weltweit, Internet nötig):
  pip install geopy timezonefinder
Windows zusätzlich:
  pip install tzdata
"""

import sys
import unicodedata
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo, available_timezones

DE_TZ = ZoneInfo("Europe/Berlin")
ARBEIT_START = time(9, 0)
ARBEIT_ENDE = time(17, 0)

STAEDTE = {
    # Europa
    "london": "Europe/London", "dublin": "Europe/Dublin", "lissabon": "Europe/Lisbon",
    "lisbon": "Europe/Lisbon", "paris": "Europe/Paris", "madrid": "Europe/Madrid",
    "barcelona": "Europe/Madrid", "valencia": "Europe/Madrid", "rom": "Europe/Rome",
    "rome": "Europe/Rome", "mailand": "Europe/Rome", "milan": "Europe/Rome",
    "wien": "Europe/Vienna", "vienna": "Europe/Vienna", "zuerich": "Europe/Zurich",
    "zurich": "Europe/Zurich", "amsterdam": "Europe/Amsterdam", "bruessel": "Europe/Brussels",
    "brussels": "Europe/Brussels", "warschau": "Europe/Warsaw", "warsaw": "Europe/Warsaw",
    "prag": "Europe/Prague", "prague": "Europe/Prague", "stockholm": "Europe/Stockholm",
    "oslo": "Europe/Oslo", "kopenhagen": "Europe/Copenhagen", "copenhagen": "Europe/Copenhagen",
    "helsinki": "Europe/Helsinki", "athen": "Europe/Athens", "athens": "Europe/Athens",
    "istanbul": "Europe/Istanbul", "kiew": "Europe/Kyiv", "kyiv": "Europe/Kyiv",
    "moskau": "Europe/Moscow", "moscow": "Europe/Moscow", "bukarest": "Europe/Bucharest",
    # Amerika
    "new york": "America/New_York", "nyc": "America/New_York", "boston": "America/New_York",
    "washington": "America/New_York", "miami": "America/New_York", "toronto": "America/Toronto",
    "chicago": "America/Chicago", "dallas": "America/Chicago", "houston": "America/Chicago",
    "denver": "America/Denver", "phoenix": "America/Phoenix", "los angeles": "America/Los_Angeles",
    "san francisco": "America/Los_Angeles", "seattle": "America/Los_Angeles",
    "vancouver": "America/Vancouver", "mexiko-stadt": "America/Mexico_City",
    "mexico city": "America/Mexico_City", "bogota": "America/Bogota", "lima": "America/Lima",
    "caracas": "America/Caracas", "santiago": "America/Santiago",
    "santiago de chile": "America/Santiago", "buenos aires": "America/Argentina/Buenos_Aires",
    "mendoza": "America/Argentina/Mendoza", "cordoba": "America/Argentina/Cordoba",
    "sao paulo": "America/Sao_Paulo", "rio de janeiro": "America/Sao_Paulo",
    "montevideo": "America/Montevideo", "havanna": "America/Havana", "havana": "America/Havana",
    # Asien / Ozeanien / Afrika
    "dubai": "Asia/Dubai", "abu dhabi": "Asia/Dubai", "doha": "Asia/Qatar",
    "riad": "Asia/Riyadh", "riyadh": "Asia/Riyadh", "tel aviv": "Asia/Jerusalem",
    "jerusalem": "Asia/Jerusalem", "mumbai": "Asia/Kolkata", "bombay": "Asia/Kolkata",
    "delhi": "Asia/Kolkata", "neu-delhi": "Asia/Kolkata", "new delhi": "Asia/Kolkata",
    "bangalore": "Asia/Kolkata", "bengaluru": "Asia/Kolkata", "kathmandu": "Asia/Kathmandu",
    "bangkok": "Asia/Bangkok", "hanoi": "Asia/Bangkok", "ho chi minh": "Asia/Ho_Chi_Minh",
    "saigon": "Asia/Ho_Chi_Minh", "jakarta": "Asia/Jakarta", "bali": "Asia/Makassar",
    "denpasar": "Asia/Makassar", "singapur": "Asia/Singapore", "singapore": "Asia/Singapore",
    "kuala lumpur": "Asia/Kuala_Lumpur", "manila": "Asia/Manila", "hongkong": "Asia/Hong_Kong",
    "hong kong": "Asia/Hong_Kong", "peking": "Asia/Shanghai", "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai", "shenzhen": "Asia/Shanghai", "taipeh": "Asia/Taipei",
    "taipei": "Asia/Taipei", "pjoengjang": "Asia/Pyongyang", "pyongyang": "Asia/Pyongyang",
    "seoul": "Asia/Seoul", "tokio": "Asia/Tokyo", "tokyo": "Asia/Tokyo", "osaka": "Asia/Tokyo",
    "sydney": "Australia/Sydney", "melbourne": "Australia/Melbourne",
    "brisbane": "Australia/Brisbane", "perth": "Australia/Perth",
    "auckland": "Pacific/Auckland", "honolulu": "Pacific/Honolulu",
    "kairo": "Africa/Cairo", "cairo": "Africa/Cairo", "kapstadt": "Africa/Johannesburg",
    "cape town": "Africa/Johannesburg", "johannesburg": "Africa/Johannesburg",
    "nairobi": "Africa/Nairobi", "lagos": "Africa/Lagos", "casablanca": "Africa/Casablanca",
    # Deutschland
    "berlin": "Europe/Berlin", "frankfurt": "Europe/Berlin", "hannover": "Europe/Berlin",
    "muenchen": "Europe/Berlin", "hamburg": "Europe/Berlin", "koeln": "Europe/Berlin",
}

WOCHENTAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def normalisieren(text: str) -> str:
    t = text.strip().lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return " ".join(t.replace("_", " ").split())


def zeitzone_finden(stadt: str):
    key = normalisieren(stadt)
    if key in STAEDTE:
        return ZoneInfo(STAEDTE[key])
    for tz in sorted(available_timezones()):
        if normalisieren(tz.split("/")[-1]) == key or normalisieren(tz) == key:
            return ZoneInfo(tz)
    try:
        from geopy.geocoders import Nominatim
        from timezonefinder import TimezoneFinder
        ort = Nominatim(user_agent="zeitverschiebung-script").geocode(stadt, timeout=10)
        if ort:
            tz = TimezoneFinder().timezone_at(lng=ort.longitude, lat=ort.latitude)
            if tz:
                print(f"  (gefunden via Geocoding: {ort.address})")
                return ZoneInfo(tz)
    except ImportError:
        pass
    except Exception as e:
        print(f"  Geocoding-Fehler: {e}")
    return None


def offset_text(delta: timedelta) -> str:
    minuten = int(delta.total_seconds() // 60)
    vorz = "+" if minuten >= 0 else "-"
    h, m = divmod(abs(minuten), 60)
    return f"{vorz}{h}:{m:02d} h"


def fmt(dt: datetime) -> str:
    return f"{WOCHENTAGE[dt.weekday()]}, {dt:%d.%m.%Y %H:%M} ({dt.tzname()})"


def tagesmarker(ziel: datetime, de: datetime) -> str:
    diff = (ziel.date() - de.date()).days
    return "" if diff == 0 else f" [{'+' if diff > 0 else ''}{diff} Tag]"


def bewertung(stunde: int) -> str:
    if 9 <= stunde < 17:
        return "normale Arbeitszeit"
    if 7 <= stunde < 9 or 17 <= stunde < 20:
        return "Randzeit"
    if 20 <= stunde < 23 or 6 <= stunde < 7:
        return "spät/früh"
    return "Nacht!"


def datum_parsen(text: str):
    text = text.strip()
    if not text:
        return datetime.now(DE_TZ).date()
    for f in ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, f).date()
        except ValueError:
            pass
    raise ValueError("Datum bitte als TT.MM.JJJJ eingeben")


def zeit_parsen(text: str) -> time:
    text = text.strip()
    if not text:
        return datetime.now(DE_TZ).time().replace(second=0, microsecond=0)
    for f in ("%H:%M", "%H"):
        try:
            return datetime.strptime(text, f).time()
        except ValueError:
            pass
    raise ValueError("Uhrzeit bitte als HH:MM eingeben")


def auswerten(stadt: str, datum, uhrzeit) -> None:
    tz = zeitzone_finden(stadt)
    if tz is None:
        print(f"\n✗ Stadt '{stadt}' nicht gefunden. Tipp: englischen Namen probieren "
              f"oder 'pip install geopy timezonefinder' für weltweite Suche.\n")
        return

    de = datetime.combine(datum, uhrzeit, tzinfo=DE_TZ)
    ziel = de.astimezone(tz)
    delta = ziel.utcoffset() - de.utcoffset()

    print("\n" + "=" * 62)
    print(f"  {stadt.title()}  –  Zeitzone {tz.key}")
    print("=" * 62)
    print(f"  Zeitverschiebung zu Deutschland: {offset_text(delta)}")
    print(f"  Deutschland : {fmt(de)}")
    print(f"  {stadt.title():<12}: {fmt(ziel)}{tagesmarker(ziel, de)}")

    de_start = datetime.combine(datum, ARBEIT_START, tzinfo=DE_TZ)
    de_ende = datetime.combine(datum, ARBEIT_ENDE, tzinfo=DE_TZ)
    z_start, z_ende = de_start.astimezone(tz), de_ende.astimezone(tz)

    print("\n  Deutsche Arbeitszeit 09:00–17:00 entspricht vor Ort:")
    print(f"  ► {z_start:%H:%M}{tagesmarker(z_start, de_start)}  bis  "
          f"{z_ende:%H:%M}{tagesmarker(z_ende, de_ende)}  ({z_start.tzname()})")

    print("\n  Stundenübersicht:")
    print(f"  {'Deutschland':<14}{stadt.title()[:20]:<22}Einschätzung")
    print("  " + "-" * 56)
    t = de_start
    while t <= de_ende:
        o = t.astimezone(tz)
        print(f"  {t:%H:%M}{'':<9}{o:%H:%M} {WOCHENTAGE[o.weekday()]}"
              f"{tagesmarker(o, t):<14}{bewertung(o.hour)}")
        t += timedelta(hours=1)

    if (de_start.utcoffset() != (de_start + timedelta(days=14)).utcoffset()
            or z_start.utcoffset() != (z_start + timedelta(days=14)).utcoffset()):
        print("\n  ⚠ In den nächsten 14 Tagen gibt es eine Zeitumstellung – "
              "die Verschiebung ändert sich!")
    print()

"""
def main() -> None:
    if len(sys.argv) > 1:
        stadt = sys.argv[1]
        datum = datum_parsen(sys.argv[2] if len(sys.argv) > 2 else "")
        uhrzeit = zeit_parsen(sys.argv[3] if len(sys.argv) > 3 else "")
        auswerten(stadt, datum, uhrzeit)
        return

    print("Zeitverschiebungs-Rechner (Enter ohne Stadt = Beenden)")
    while True:
        stadt = input("\nStadt: ").strip()
        if not stadt:
            break
        try:
            datum = datum_parsen(input("Datum (TT.MM.JJJJ, Enter = heute): "))
            uhrzeit = zeit_parsen(input("Uhrzeit in DE (HH:MM, Enter = jetzt): "))
        except ValueError as e:
            print(f"✗ {e}")
            continue
        auswerten(stadt, datum, uhrzeit)
"""

def eingabe_zerlegen(text: str):
    """Zerlegt 'Stadt [TT.MM.JJJJ] [HH:MM]' - Datum und Uhrzeit sind optional."""
    teile = text.split()
    datum, uhrzeit = None, None
    if len(teile) > 1 and ":" in teile[-1]:
        try:
            uhrzeit = zeit_parsen(teile[-1])
            teile.pop()
        except ValueError:
            pass
    if len(teile) > 1:
        try:
            datum = datum_parsen(teile[-1])
            teile.pop()
        except ValueError:
            pass
    stadt = " ".join(teile)
    return stadt, datum or datum_parsen(""), uhrzeit or zeit_parsen("")


def main() -> None:
    if len(sys.argv) > 1:
        auswerten(*eingabe_zerlegen(" ".join(sys.argv[1:])))
        return

    print("Zeitverschiebungs-Rechner")
    print("Eingabe: Stadt [TT.MM.JJJJ] [HH:MM]  - z. B. 'Tokio' oder "
          "'Buenos Aires 15.11.2026 10:00'")
    print("Nur Stadt = heute/jetzt. Leere Eingabe = Beenden.")
    while True:
        try:
            zeile = input("\nStadt [Datum] ").strip()
        except EOFError:
            break
        if not zeile:
            break
        auswerten(*eingabe_zerlegen(zeile))

if __name__ == "__main__":
    main()

