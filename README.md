# 🍺 Bierrechner V2

Ein interaktives Python-Programm zur Berechnung und Auswahl von Bierrezepten basierend auf Zutaten (Malz, Hopfen, Hefe) und Geschmackseigenschaften.

## 📋 Features

- **Interaktive GUI** mit Pygame - benutzerfreundliche Bedienung
- **6 verschiedene Biersorten:** ALE, HELLAS, IPA, SUNVALE, FROSTHAVEN, GRAVENFORD
- **Rezeptgenerator** - kombiniert Zutaten automatisch
- **Eigenschaftsfilter** - Filterung nach Geschmacksmerkmalen:
  - Erfrischung
  - Schwere
  - Leichtigkeit
  - Säure
  - Süße
- **Aromen** - optionale Aroma-Auswahl (Banana, Cherry, Chilli, Wassermelone)
- **Responsive Design** - Fullscreen- und Fenster-Modus

## 🎯 Verwendung

### Start des Programms

```bash
python Bierrechner_V2.py
```

### Bedienung

1. **Startseite**: Wähle ein Bier durch Klick auf die Bierflaschen aus
2. **(Optional) Aroma**: Bestätige eine Aromawahl (z.B. Banana, Cherry, etc.)
3. **Eigenschaften**: Wähle die gewünschten Geschmackseigenschaften
4. **Rezepte**: Durchblättere verfügbare Rezepte mit Pfeilen oben/unten

### Steuerung

- **Mausklick** auf Buttons zum Interagieren
- **HOME** - zur Startseite zurück
- **ZURÜCK** - einen Schritt rückwärts
- **AUGE** - zwischen Fullscreen und Fenster-Modus wechseln
- **RELOAD** - Rezeptdaten neu laden
- **EXIT** - Programm beenden

## 📁 Projektstruktur

```
Beer-Calculator/
├── Bierrechner_V2.py    # Hauptprogramm (GUI + Logik)
├── DATA_MHH.py          # Zutaten-Datenbank
└── README.md            # Diese Datei
```

### Assets (erforderlich)

Das Programm benötigt folgende Verzeichnisstruktur für Bilder:

```
assets/
├── ui/                  # UI-Buttons und Hintergrund
├── bier/               # Bierflaschen-Bilder
├── malz/               # Malz-Ikonen
├── hopfen/             # Hopfen-Ikonen
├── hefe/               # Hefe-Ikonen
├── eigenschaften/      # Eigenschafts-Ikonen
└── aroma/              # Aroma-Ikonen
```

## 🔧 Anforderungen

- **Python 3.7+**
- **Pygame** - für die grafische Benutzeroberfläche

### Installation der Abhängigkeiten

```bash
pip install pygame
```

## 📊 Datenformat (DATA_MHH.py)

- **MALZ** - Liste von Malzsorten mit Codes und Bierauswirkungen
- **HOPFEN** - Liste von Hopfensorten mit Codes und Bierauswirkungen
- **HEFE** - Dictionary von Hefesorten mit Codes und Bierauswirkungen
- **ZUTATEN** - Eigenschaftswerte für jede Zutat:
  - [Erfrischung, Schwere, Leichtigkeit, Säure, Süße]

## 🐛 Bekannte Besonderheiten

- Der Code "FW" existiert sowohl bei Malz als auch bei Hopfen (separate Verwaltung in ZUTATEN)
- Der alte Tippfehler "FM" bei Malz wird automatisch in "FW" korrigiert
- Fehlende Zutaten in der ZUTATEN-Datenbank nutzen Standard-Eigenschaftswerte

## 📝 Lizenz

Privates Projekt - erstellt für Brauereiberechnung

---

**Version:** 2.0 | **Sprache:** Python | **GUI:** Pygame
