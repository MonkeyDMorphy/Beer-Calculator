import pygame
import sys
import importlib
import DATA_MHH

# =========================
# EINSTELLUNGEN
# =========================
WINDOWED_SIZE = (1280, 720)
FPS = 60

BEER_NAMES = [
    "ALE",
    "HELLAS",
    "IPA",
    "SUNVALE",
    "FROSTHAVEN",
    "GRAVENFORD",
]

# Positionen im 10x10 Raster
BEER_POSITIONS = {
    "ALE": (1.2, 5.0),
    "HELLAS": (2.5, 5.0),
    "IPA": (3.8, 5.0),
    "SUNVALE": (5.1, 5.0),
    "FROSTHAVEN": (6.4, 5.0),
    "GRAVENFORD": (7.7, 5.0),
}

BEER_IMAGE_FILES = {
    "ALE": "Ale.png",
    "HELLAS": "Hellas.png",
    "IPA": "Ipa.png",
    "SUNVALE": "Sunvale.png",
    "FROSTHAVEN": "Frosthaven.png",
    "GRAVENFORD": "Gravenford.png",
}

# =========================
# BIER-NAMEN AUF DER HAUPTSEITE
# =========================
# Alles ist im gleichen 10x10-Raster wie die Bierflaschen.
# x/y = Rasterposition, nicht Pixel.
BEER_LABELS_VISIBLE = True
BEER_LABEL_FONT_SCALE = 0.035      # groesser = groessere Schrift, z.B. 0.045
BEER_LABEL_MIN_SIZE = 20
BEER_LABEL_COLOR = (0, 0, 0)       # Schriftfarbe schwarz

# Helle Flaeche hinter der Schrift, damit man sie sicher sieht.
BEER_LABEL_BOX_VISIBLE = True
BEER_LABEL_BOX_COLOR = (245, 220, 180)
BEER_LABEL_BOX_ALPHA = 230
BEER_LABEL_BOX_PADDING_X = 12
BEER_LABEL_BOX_PADDING_Y = 5
BEER_LABEL_BOX_BORDER_COLOR = (0, 0, 0)

# Positionen der Namen im 10x10-Raster.
# Damit kannst du wie bei den Bieren mit 1.4 / 5.8 usw. arbeiten.
BEER_LABEL_POSITIONS = {
    "ALE": (1.2, 7),
    "HELLAS": (2.5, 7),
    "IPA": (3.8, 7),
    "SUNVALE": (5.1, 7),
    "FROSTHAVEN": (6.4, 7),
    "GRAVENFORD": (7.7, 7),
}

BEER_DISPLAY_NAMES = {
    "ALE": "Ale",
    "HELLAS": "Hellas",
    "IPA": "IPA",
    "SUNVALE": "Sunvale",
    "FROSTHAVEN": "Frosthaven",
    "GRAVENFORD": "Gravenford",
}

# =========================
# PROGRAMM-INIT
# =========================
pygame.init()
pygame.display.set_caption("Bierrechner V2")

is_fullscreen = True
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
WIDTH, HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# =========================
# DATEN / STATE
# =========================
# Reihenfolge in DATA_MHH:
# Ale, Ipa, Hall/Hellas, Sunvale, Frosthaven, Gravenford
BEER_VALUE_INDEX = {
    "ALE": 0,
    "IPA": 1,
    "HELLAS": 2,
    "SUNVALE": 3,
    "FROSTHAVEN": 4,
    "GRAVENFORD": 5,
}

DEFAULT_PROPS = [2, 2, 2, 2, 2]
DATA_WARNINGS = []


def normalize_malz_code(code):
    """Korrigiert den bekannten Tippfehler: Malz FM ist eigentlich FW."""
    return "FW" if code == "FM" else code


def row_to_dict(row, typ):
    code = row[0]
    if typ == "malz":
        code = normalize_malz_code(code)

    values = row[1:]
    if len(values) != 6:
        raise ValueError(f"{typ.upper()} {code} hat {len(values)} Bierwerte statt 6: {row}")

    return {
        "code": code,
        "values": {
            beer: int(values[idx])
            for beer, idx in BEER_VALUE_INDEX.items()
        },
    }


def hefe_to_dict(code, values):
    if len(values) != 6:
        raise ValueError(f"HEFE {code} hat {len(values)} Bierwerte statt 6: {values}")

    return {
        "code": code,
        "values": {
            beer: int(values[idx])
            for beer, idx in BEER_VALUE_INDEX.items()
        },
    }


def get_props(kategorie, code):
    """
    Holt Eigenschaften aus DATA_MHH.ZUTATEN.
    Unterstuetzt das neue saubere Format:
        ZUTATEN["MALZ"]["FW"]
        ZUTATEN["HOPFEN"]["FW"]
        ZUTATEN["HEFE"]["FM"]
    und als Notfall auch noch das alte flache Format:
        ZUTATEN["BB"]
    """
    zutaten = getattr(DATA_MHH, "ZUTATEN", {})
    kat_key = kategorie.upper()

    daten = None

    # Neues Format mit getrennten Kategorien. Wichtig wegen FW als Malz UND Hopfen.
    if isinstance(zutaten.get(kat_key), dict):
        daten = zutaten[kat_key].get(code)

    # Altes flaches Format als Fallback.
    if daten is None:
        daten = zutaten.get(code)

    if daten is None:
        warn_key = f"{kat_key}:{code}"
        if warn_key not in DATA_WARNINGS:
            DATA_WARNINGS.append(warn_key)
        return DEFAULT_PROPS[:]

    props = daten.get("props", DEFAULT_PROPS)
    if len(props) != 5:
        print(f"WARNUNG: Eigenschaften fuer {kat_key}:{code} haben nicht 5 Werte: {props}")
        return DEFAULT_PROPS[:]

    return [int(v) for v in props]


def add_props(*prop_lists):
    return [sum(values) for values in zip(*prop_lists)]


def calc_percent(malz, hopfen, hefe, beer):
    wert = malz["values"][beer] + hopfen["values"][beer] + hefe["values"][beer]
    return max(0, min(100, int(wert)))


def calc_all_percents(malz, hopfen, hefe):
    return {beer: calc_percent(malz, hopfen, hefe, beer) for beer in BEER_NAMES}


def get_winning_beer(percentwerte):
    """
    Jede Zutatenkombination wird nur EINEM Bier zugeordnet:
    dem Bier mit dem hoechsten Prozentwert.
    Bei Gleichstand gewinnt die Reihenfolge in BEER_NAMES.
    """
    return max(BEER_NAMES, key=lambda beer: percentwerte[beer])


def generate_recipes_from_DATA_MHH():
    global DATA_WARNINGS
    DATA_WARNINGS = []

    malz_liste = [row_to_dict(row, "malz") for row in DATA_MHH.MALZ]
    hopfen_liste = [row_to_dict(row, "hopfen") for row in DATA_MHH.HOPFEN]
    hefe_liste = [hefe_to_dict(code, values) for code, values in DATA_MHH.HEFE.items()]

    generated = []

    for malz in malz_liste:
        for hopfen in hopfen_liste:
            for hefe in hefe_liste:
                combo = (malz["code"], hopfen["code"], hefe["code"])
                props = add_props(
                    get_props("MALZ", malz["code"]),
                    get_props("HOPFEN", hopfen["code"]),
                    get_props("HEFE", hefe["code"]),
                )

                percentwerte = calc_all_percents(malz, hopfen, hefe)
                winning_beer = get_winning_beer(percentwerte)

                generated.append({
                    "combo": combo,
                    "beer": (winning_beer, percentwerte[winning_beer]),
                    "props": props,
                    "percentwerte": percentwerte,
                })

    if DATA_WARNINGS:
        print("WARNUNG: Fuer diese Zutaten fehlen Eigenschaften in DATA_MHH.ZUTATEN:", ", ".join(sorted(DATA_WARNINGS)))
        print("Die UI nutzt dafuer vorerst DEFAULT_PROPS =", DEFAULT_PROPS)

    counts = {beer: 0 for beer in BEER_NAMES}
    for rezept in generated:
        counts[rezept["beer"][0]] += 1

    print(f"Rezepte aus DATA_MHH geladen: {len(generated)}")
    print("Gewinner-Rezepte je Bier:", counts)
    return generated


def load_recipes():
    importlib.reload(DATA_MHH)
    return generate_recipes_from_DATA_MHH()


RECIPES = load_recipes()

current_screen = "home"
screen_history = []

selected_beer = None
selected_aroma = None
selected_aroma_detail = None
selected_eigenschaften = []

filtered_recipes = []
current_recipe_index = 0

up_arrow_rect = None
down_arrow_rect = None

eigenschaften = ["Erfrischung", "Schwere", "Leichtigkeit", "Saeure", "Suesse"]
eigenschaft_index = {
    "Erfrischung": 0,
    "Schwere": 1,
    "Leichtigkeit": 2,
    "Saeure": 3,
    "Suesse": 4,
}

aromen = ["Banana", "Cherry", "Chilli", "Wassermelone"]

# =========================
# HILFSFUNKTIONEN
# =========================
def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"FEHLER: Bild nicht gefunden: {path} | {e}")
        surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        surf.fill((255, 0, 255, 160))
        return surf


def load_beer_image(filename):
    # Erst korrekt aus assets/bier laden, falls nicht vorhanden als Fallback assets/ui.
    path_bier = f"assets/bier/{filename}"
    path_ui = f"assets/ui/{filename}"
    try:
        return pygame.image.load(path_bier).convert_alpha()
    except Exception:
        return load_image(path_ui)


class Background:
    def __init__(self):
        self.original = None
        self.image = None
        try:
            self.original = pygame.image.load("assets/ui/Hintergrund.png").convert()
            self.rebuild()
        except Exception:
            print("FEHLER: Hintergrundbild nicht gefunden!")

    def rebuild(self):
        if self.original:
            self.image = pygame.transform.scale(self.original, (WIDTH, HEIGHT))

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (0, 0))
        else:
            surface.fill((30, 30, 30))


class ImageButton:
    def __init__(self, image, pos_rel, scale, offset=(0, 0)):
        h = max(1, int(HEIGHT * scale))
        ratio = h / image.get_height()
        w = max(1, int(image.get_width() * ratio))

        self.image = pygame.transform.smoothscale(image, (w, h))

        grid = 10
        x = int(WIDTH * (pos_rel[0] / grid)) + offset[0]
        y = int(HEIGHT * (pos_rel[1] / grid)) + offset[1]

        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy().inflate(4, 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 1
            and self.hitbox.collidepoint(event.pos)
        )


def can_select_prop(test_name):
    if selected_beer is None:
        return False

    required = list(selected_eigenschaften)
    if test_name not in required:
        required.append(test_name)

    for r in RECIPES:
        if r["beer"][0] != selected_beer:
            continue

        ok = True
        for name in required:
            idx = eigenschaft_index[name]
            if r["props"][idx] < 10:
                ok = False
                break

        if ok:
            return True

    return False


def make_recipe_filter():
    result = []

    if selected_beer is None:
        return result

    for r in RECIPES:
        if r["beer"][0] != selected_beer:
            continue

        valid = True
        for name in selected_eigenschaften:
            idx = eigenschaft_index[name]
            if r["props"][idx] < 10:
                valid = False
                break

        if valid:
            result.append(r)

    result.sort(key=lambda x: x["beer"][1], reverse=True)
    return result


# =========================
# ASSETS LADEN
# =========================
img_home = load_image("assets/ui/Home.png")
img_back = load_image("assets/ui/Zurueck.png")
img_eye = load_image("assets/ui/Auge.png")
img_exit = load_image("assets/ui/Exit.png")
img_reload = load_image("assets/ui/reload.png")
img_aroma = load_image("assets/ui/Aroma.png")
img_confirm = load_image("assets/ui/Balken.png")
img_up = load_image("assets/ui/Hoch.png")
img_plus = load_image("assets/ui/Plus.png")

beer_images = {
    beer: load_beer_image(BEER_IMAGE_FILES[beer])
    for beer in BEER_NAMES
}

eigenschaften_icons = {
    "Erfrischung": load_image("assets/eigenschaften/Erfrischung.png"),
    "Schwere": load_image("assets/eigenschaften/Schwere.png"),
    "Leichtigkeit": load_image("assets/eigenschaften/Leichtigkeit.png"),
    "Saeure": load_image("assets/eigenschaften/Saeure.png"),
    "Suesse": load_image("assets/eigenschaften/Suesse.png"),
}

aroma_icons = {
    "Banana": load_image("assets/aroma/Banana.png"),
    "Cherry": load_image("assets/aroma/Cherry.png"),
    "Chilli": load_image("assets/aroma/Chilli.png"),
    "Wassermelone": load_image("assets/aroma/Wassermelone.png"),
}

def unique_codes(seq):
    result = []
    for code in seq:
        if code not in result:
            result.append(code)
    return result


malz_icons = {
    code: load_image(f"assets/malz/{code}.png")
    for code in unique_codes(normalize_malz_code(row[0]) for row in DATA_MHH.MALZ)
}

hopfen_icons = {
    row[0]: load_image(f"assets/hopfen/{row[0]}.png")
    for row in DATA_MHH.HOPFEN
}

hefe_icons = {
    code: load_image(f"assets/hefe/{code}.png")
    for code in DATA_MHH.HEFE.keys()
}

background = Background()

# =========================
# BUTTONS BAUEN
# =========================
def rebuild_ui():
    global home_btn, back_btn, eye_btn, exit_btn, reload_btn
    global beer_buttons, aroma_btn, confirm_btn
    global eigenschaft_buttons, aroma_buttons
    global background

    background.rebuild()

    home_btn = ImageButton(img_home, (0.5, 0.8), 0.06)
    back_btn = ImageButton(img_back, (1.0, 0.8), 0.06)
    eye_btn = ImageButton(img_eye, (1.5, 0.8), 0.06)
    exit_btn = ImageButton(img_exit, (9.5, 0.5), 0.10)
    reload_btn = ImageButton(img_reload, (0.35, 9.5), 0.045)

    beer_buttons = {
        beer: ImageButton(beer_images[beer], BEER_POSITIONS[beer], 0.35)
        for beer in BEER_NAMES
    }

    aroma_btn = ImageButton(img_aroma, (9.2, 5.0), 0.20)
    confirm_btn = ImageButton(img_confirm, (5.0, 9.0), 0.05)

    eig_positions = [(4, 3), (6, 3), (3, 6), (5, 6), (7, 6)]
    eigenschaft_buttons = []
    for i, name in enumerate(eigenschaften):
        eigenschaft_buttons.append((name, ImageButton(eigenschaften_icons[name], eig_positions[i], 0.25)))

    aroma_positions = [(4, 3), (6, 3), (4, 6), (6, 6)]
    aroma_buttons = []
    for i, name in enumerate(aromen):
        aroma_buttons.append((name, ImageButton(aroma_icons[name], aroma_positions[i], 0.35)))


rebuild_ui()

# =========================
# SCREEN WECHSEL
# =========================
def go_home():
    global current_screen, selected_beer, selected_aroma, selected_aroma_detail
    global selected_eigenschaften, filtered_recipes, current_recipe_index

    current_screen = "home"
    screen_history.clear()
    selected_beer = None
    selected_aroma = None
    selected_aroma_detail = None
    selected_eigenschaften = []
    filtered_recipes = []
    current_recipe_index = 0
    print("HOME")


def toggle_fullscreen():
    global is_fullscreen, screen, WIDTH, HEIGHT

    is_fullscreen = not is_fullscreen
    pygame.display.quit()
    pygame.display.init()

    if is_fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    else:
        screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE | pygame.DOUBLEBUF)

    WIDTH, HEIGHT = screen.get_size()
    rebuild_ui()


# =========================
# DRAW-FUNKTIONEN
# =========================
def draw_highlight(rect, color):
    pygame.draw.rect(screen, color, rect, 4, border_radius=10)


def grid_pos(pos_rel):
    """Wandelt eine 10x10-Rasterposition in echte Bildschirmpixel um."""
    return (int(WIDTH * (pos_rel[0] / 10)), int(HEIGHT * (pos_rel[1] / 10)))


def draw_label_box(text, font, center):
    if not BEER_LABEL_BOX_VISIBLE:
        return

    text_surf = font.render(text, True, BEER_LABEL_COLOR)
    rect = text_surf.get_rect(center=center)
    rect.inflate_ip(BEER_LABEL_BOX_PADDING_X * 2, BEER_LABEL_BOX_PADDING_Y * 2)

    box = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    box.fill((*BEER_LABEL_BOX_COLOR, BEER_LABEL_BOX_ALPHA))
    screen.blit(box, rect)
    pygame.draw.rect(screen, BEER_LABEL_BOX_BORDER_COLOR, rect, 1, border_radius=6)


def draw_beer_label(beer, font):
    label = BEER_DISPLAY_NAMES.get(beer, beer)
    center = grid_pos(BEER_LABEL_POSITIONS.get(beer, BEER_POSITIONS[beer]))

    draw_label_box(label, font, center)

    text_surf = font.render(label, True, BEER_LABEL_COLOR)
    text_rect = text_surf.get_rect(center=center)
    screen.blit(text_surf, text_rect)


def draw_home():
    # Bierbilder zeichnen
    for beer in BEER_NAMES:
        beer_buttons[beer].draw(screen)

    # Biernamen im 10x10-Raster zeichnen
    if BEER_LABELS_VISIBLE:
        font_size = max(BEER_LABEL_MIN_SIZE, int(HEIGHT * BEER_LABEL_FONT_SCALE))
        font = pygame.font.SysFont(None, font_size, bold=True)
        for beer in BEER_NAMES:
            draw_beer_label(beer, font)

    aroma_btn.draw(screen)

    if selected_beer in beer_buttons:
        draw_highlight(beer_buttons[selected_beer].rect, (255, 230, 0))

    if selected_aroma == "Aroma":
        draw_highlight(aroma_btn.rect, (0, 200, 255))


def draw_aroma():
    for name, btn in aroma_buttons:
        btn.draw(screen)
        if selected_aroma_detail == name:
            draw_highlight(btn.rect, (0, 200, 255))


def draw_eigenschaften():
    for name, btn in eigenschaft_buttons:
        btn.draw(screen)

        if name in selected_eigenschaften:
            draw_highlight(btn.rect, (0, 255, 150))
        elif not can_select_prop(name):
            draw_highlight(btn.rect, (80, 80, 80))


def draw_recipe():
    global up_arrow_rect, down_arrow_rect

    if not filtered_recipes:
        font = pygame.font.SysFont(None, 50)
        text = font.render("Keine Rezepte gefunden", True, (0, 0, 0))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, rect)
        return

    recipe = filtered_recipes[current_recipe_index]
    malz, hopfen, hefe = recipe["combo"]
    beer, percent = recipe["beer"]

    y_title = 100
    y_icons = HEIGHT // 2
    y_count = int(HEIGHT * 0.75)

    # Pfeile
    arrow_size = 60
    img_up_scaled = pygame.transform.smoothscale(img_up, (arrow_size, arrow_size))
    up_arrow_rect = img_up_scaled.get_rect(center=(WIDTH // 2, 50))

    img_down_scaled = pygame.transform.rotate(img_up_scaled, 180)
    down_arrow_rect = img_down_scaled.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    if current_recipe_index > 0:
        screen.blit(img_up_scaled, up_arrow_rect)

    if current_recipe_index < len(filtered_recipes) - 1:
        screen.blit(img_down_scaled, down_arrow_rect)

    # Rezept-Elemente
    elements = [("malz", malz), ("plus", None), ("hopfen", hopfen)]

    if selected_aroma_detail:
        elements.append(("plus", None))
        elements.append(("aroma", selected_aroma_detail))

    elements.append(("plus", None))
    elements.append(("hefe", hefe))

    base_size = 240
    gap = 140
    total_width = gap * (len(elements) - 1)
    start_x = (WIDTH // 2) - (total_width // 2)

    for i, (typ, value) in enumerate(elements):
        if typ == "malz":
            img = malz_icons.get(value, img_plus)
        elif typ == "hopfen":
            img = hopfen_icons.get(value, img_plus)
        elif typ == "hefe":
            img = hefe_icons.get(value, img_plus)
        elif typ == "aroma":
            img = aroma_icons.get(value, img_plus)
        else:
            img = img_plus

        w, h = img.get_size()
        scale = base_size / max(w, h)

        if typ == "plus":
            scale *= 0.5

        img_scaled = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
        rect = img_scaled.get_rect(center=(start_x + i * gap, y_icons))
        screen.blit(img_scaled, rect)

    font_big = pygame.font.SysFont(None, 50)
    text = font_big.render(f"{beer} {percent}%", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, y_title))
    screen.blit(text, rect)

    font_small = pygame.font.SysFont(None, 40)
    text = font_small.render(f"{current_recipe_index + 1}/{len(filtered_recipes)}", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, y_count))
    screen.blit(text, rect)


def draw_top_ui():
    home_btn.draw(screen)
    back_btn.draw(screen)
    eye_btn.draw(screen)
    exit_btn.draw(screen)
    reload_btn.draw(screen)

    if current_screen in ("home", "aroma", "eigenschaften"):
        confirm_btn.draw(screen)


# =========================
# EVENT-FUNKTIONEN
# =========================
def handle_mouse_click(event):
    global RECIPES, current_screen, selected_beer, selected_aroma, selected_aroma_detail
    global selected_eigenschaften, filtered_recipes, current_recipe_index

    # Globale Buttons
    if reload_btn.is_clicked(event):
        RECIPES = load_recipes()
        print("DATA_MHH neu geladen 🔄")
        return

    if home_btn.is_clicked(event):
        go_home()
        return

    if back_btn.is_clicked(event):
        if screen_history:
            current_screen = screen_history.pop()
            print("BACK →", current_screen)
        return

    if eye_btn.is_clicked(event):
        toggle_fullscreen()
        return

    if exit_btn.is_clicked(event):
        pygame.quit()
        sys.exit()

    # Home: Bierauswahl
    if current_screen == "home":
        for beer, btn in beer_buttons.items():
            if btn.is_clicked(event):
                selected_beer = None if selected_beer == beer else beer
                print("Bier:", selected_beer)
                return

        if selected_beer and aroma_btn.is_clicked(event):
            if selected_aroma == "Aroma":
                selected_aroma = None
                selected_aroma_detail = None
            else:
                selected_aroma = "Aroma"
            return

    # Aroma-Auswahl
    if current_screen == "aroma":
        for name, btn in aroma_buttons:
            if btn.is_clicked(event):
                selected_aroma_detail = None if selected_aroma_detail == name else name
                print("Aroma:", selected_aroma_detail)
                return

    # Eigenschaften-Auswahl
    if current_screen == "eigenschaften":
        for name, btn in eigenschaft_buttons:
            if btn.is_clicked(event):
                if name in selected_eigenschaften:
                    selected_eigenschaften.remove(name)
                elif can_select_prop(name):
                    selected_eigenschaften.append(name)
                print("Eigenschaften:", selected_eigenschaften)
                return

    # Rezept-Pfeile
    if current_screen == "rezept":
        if up_arrow_rect and current_recipe_index > 0 and up_arrow_rect.collidepoint(event.pos):
            current_recipe_index -= 1
            return

        if down_arrow_rect and current_recipe_index < len(filtered_recipes) - 1 and down_arrow_rect.collidepoint(event.pos):
            current_recipe_index += 1
            return

    # Bestätigen
    if confirm_btn.is_clicked(event):
        if current_screen == "home":
            if selected_beer is None:
                print("Bitte Bier wählen")
                return

            selected_eigenschaften = []
            screen_history.append(current_screen)
            current_screen = "aroma" if selected_aroma else "eigenschaften"
            return

        if current_screen == "aroma":
            if selected_aroma_detail is None:
                print("Bitte Aroma wählen")
                return

            screen_history.append(current_screen)
            current_screen = "eigenschaften"
            return

        if current_screen == "eigenschaften":
            filtered_recipes = make_recipe_filter()
            current_recipe_index = 0
            screen_history.append(current_screen)
            current_screen = "rezept"

            print("Bier:", selected_beer)
            print("Eigenschaften:", selected_eigenschaften)
            print("Rezepte:", len(filtered_recipes))
            return


# =========================
# HAUPTSCHLEIFE
# =========================
print("INIT:", current_screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE and not is_fullscreen:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)
            rebuild_ui()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            handle_mouse_click(event)

    background.draw(screen)

    if current_screen == "home":
        draw_home()
    elif current_screen == "aroma":
        draw_aroma()
    elif current_screen == "eigenschaften":
        draw_eigenschaften()
    elif current_screen == "rezept":
        draw_recipe()

    draw_top_ui()

    pygame.display.flip()
    clock.tick(FPS)
