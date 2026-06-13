#----------------------------------------------------
# Bierauswirkung reihenfolge
# Ale,Ipa,Hall,Sunvale,Frosthaven,Gravenford
#----------------------------------------------------

MALZ = [
    ("BB", 35, 0, 25, 0, 12, 0),
    ("CA", 0, 20, 0, 25, 0, 30),
    ("CP", 10, 15, 0, 0, 0, 10),
    ("CO", 10, 15, 0, 0, 0, 10),
    ("DR", 10, 0, 0, 15, 0, 15),
    ("HG", 15, 0, 30, 0, 20, 0),
    ("SW", 10, 8, 30, 0, 0, 0),
    ("GG", 14, 0, 10, 29, 0, 0),
    ("BM", 20, 0, 20, 0, 12, 0),
    ("FW", 8, 0, 24, 0, 31, 0), 
]

HOPFEN = [
    ("CD", 15, 30, 0, 0, 0, 0),
    ("CV", 10, 25, 0, 0, 0, 0),
    ("TF", 15, 35, 27, 0, 0, 0),
    ("FF", 20, 0, 15, 0, 15, 0),
    ("FW", 25, 10, 10, 0, 0, 0),
    ("HB", 10, 0, 20, 0, 15, 0),
    ("SH", 11, 0, 8, 25, 0, 0),
    ("GH", 14, 0, 12, 0, 23, 0),
    ("LC", 6, 20, 10, 0, 0, 0),
]

HEFE = {
    "BV": (15, 10, 20, 0, 0, 0),
    "FM": (10, 10, 20, 0, 0, 0),
    "CL": (10, 20, 0, 0, 0, 0),
    "RC": (15, 12, 0, 0, 0, 12),
    "WH": (10, 15, 0, 0, 0, 0),
    "YW": (25, 10, 10, 0, 0, 0),
    "HY": (9, 0, 5, 34, 0, 0),
    "WY": (8, 0, 25, 0, 34, 0),
    "OY": (12, 16, 0, 0, 0, 30),
}

# Eigenschaften Reihenfolge:
# [Erfrischung, Schwere, Leichtigkeit, Saeure, Suesse]
#
# WICHTIG:
# Es gibt den Code "FW" zweimal:
# - MALZ FW
# - HOPFEN FW
# Deshalb sind die Eigenschaften nach Kategorie getrennt.
# Der alte Tippfehler MALZ "FM" wurde hier als MALZ "FW" korrigiert.

ZUTATEN = {
    "MALZ": {
        "BB": {"props": [3, 2, 2, 1, 5]},
        "CA": {"props": [2, 5, 0, 3, 1]},
        "CP": {"props": [2, 4, 1, 4, 0]},
        "CO": {"props": [2, 4, 1, 4, 0]},
        "DR": {"props": [3, 3, 3, 3, 3]},
        "HG": {"props": [4, 0, 4, 1, 3]},
        "SW": {"props": [3, 1, 5, 2, 3]},
        "GG": {"props": [4, 1, 4, 1, 3]},
        "BM": {"props": [4, 0, 3, 0, 4]},
        "FW": {"props": [5, 0, 5, 2, 3]},
    },
    "HOPFEN": {
        "CD": {"props": [3, 2, 3, 2, 3]},
        "CV": {"props": [2, 4, 1, 5, 2]},
        "TF": {"props": [3, 3, 5, 4, 0]},
        "FF": {"props": [3, 0, 4, 1, 5]},
        "FW": {"props": [1, 4, 1, 1, 2]},
        "HB": {"props": [3, 4, 1, 2, 0]},
        "SH": {"props": [4, 0, 5, 2, 4]},
        "GH": {"props": [4, 4, 4, 3, 0]},
        "LC": {"props": [1, 3, 0, 4, 2]},
    },
    "HEFE": {
        "BV": {"props": [5, 1, 4, 2, 4]},
        "FM": {"props": [2, 0, 4, 2, 4]},
        "CL": {"props": [3, 4, 2, 5, 0]},
        "RC": {"props": [1, 5, 1, 3, 4]},
        "WH": {"props": [5, 1, 3, 5, 2]},
        "YW": {"props": [2, 2, 2, 2, 2]},
        "HY": {"props": [3, 3, 4, 3, 1]},
        "WY": {"props": [4, 1, 5, 3, 1]},
        "OY": {"props": [3, 4, 1, 1, 4]},
    },
}
