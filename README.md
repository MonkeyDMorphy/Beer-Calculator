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

## 🖼️ Assets einrichten (WICHTIG!)

Das Programm benötigt **PNG-Bilder** in dieser Verzeichnisstruktur. Erstelle folgende Ordner und füge deine Bilder ein:

```
assets/
├── ui/                      # UI-Elemente & Hintergrund
│   ├── Home.png
│   ├── Zurueck.png
│   ├── Auge.png
│   ├── Exit.png
│   ├── reload.png
│   ├── Aroma.png
│   ├── Balken.png
│   ├── Hoch.png
│   ├── Plus.png
│   └── hintergrund.png
│
├── bier/                    # Bierflaschen (6 Sorten)
│   ├── Ale.png
│   ├── Hellas.png
│   ├── Ipa.png
│   ├── Sunvale.png
│   ├── Frosthaven.png
│   └── Gravenford.png
│
├── malz/                    # Malz-Ikonen (10 Sorten)
│   ├── BB.png
│   ├── CA.png
│   ├── CP.png
│   ├── CO.png
│   ├── DR.png
│   ├── HG.png
│   ├── SW.png
│   ├── GG.png
│   ├── BM.png
│   └── FW.png
│
├── hopfen/                  # Hopfen-Ikonen (9 Sorten)
│   ├── CD.png
│   ├── CV.png
│   ├── TF.png
│   ├── FF.png
│   ├── FW.png
│   ├── HB.png
│   ├── SH.png
│   ├── GH.png
│   └── LC.png
│
├── hefe/                    # Hefe-Ikonen (9 Sorten)
│   ├── BV.png
│   ├── FM.png
│   ├── CL.png
│   ├── RC.png
│   ├── WH.png
│   ├── YW.png
│   ├── HY.png
│   ├── WY.png
│   └── OY.png
│
├── eigenschaften/           # Eigenschafts-Ikonen (5 Sorten)
│   ├── Erfrischung.png
│   ├── Schwere.png
│   ├── Leichtigkeit.png
│   ├── Saeure.png
│   └── Suesse.png
│
└── aroma/                   # Aroma-Ikonen (4 Sorten)
    ├── Banana.png
    ├── Cherry.png
    ├── Chilli.png
    └── Wassermelone.png
```

### Quick Setup

1. Klone das Repository
2. Erstelle die `assets/` Verzeichnisstruktur wie oben
3. Füge deine PNG-Bilder in die entsprechenden Ordner ein
4. Starte das Programm!

**Hinweis:** Das Programm sucht automatisch in diesen Verzeichnissen. Fehlende Bilder werden durch farbige Platzhalter ersetzt, damit das Programm trotzdem läuft.

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
- Fehlende Bilder werden durch Platzhalter ersetzt (das Programm läuft dennoch)

## 📝 Lizenz

Privates Projekt - erstellt für Brauereiberechnung

---

**Version:** 2.0 | **Sprache:** Python | **GUI:** Pygame
