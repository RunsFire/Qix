from typing import List
from Interface.buttons import MenuButton, OptionButton
from Interface.const import COLORS, QIX_LOGO_PATH, WIDTH, HEIGHT
from Interface.utils import read_input
from fltk import image, rectangle, texte, ligne, touche, donne_ev, type_ev, abscisse_souris, ordonnee_souris, mise_a_jour, efface


def create_options_menu_ui() -> None:
    """Create the static UI elements for the options menu."""
    rectangle(0, 0, WIDTH, HEIGHT, COLORS["background"], COLORS["background"], 1, "bg")
    img_height = 80
    image(WIDTH//2,125, QIX_LOGO_PATH, ancrage="center", tag="im", largeur=int(img_height * (414/188)), hauteur=img_height)
    
    # Draw section frames
    rectangle(65, 200, 335, 735, COLORS["accent"], epaisseur=3, tag="cadre")
    texte(200, 245, "Divers", COLORS["accent"], "center", tag="titre")
    ligne(65, 290, 335, 290, COLORS["accent"], 3, "ligne")

    rectangle(365, 200, 635, 735, COLORS["accent"], epaisseur=3, tag="cadre")
    texte(500, 245, "Configuration des ennemis", COLORS["accent"], "center", tag="titre")
    ligne(365, 290, 635, 290, COLORS["accent"], 3, "ligne")

    rectangle(665, 200, 935, 435, "#45FFCA", epaisseur=3, tag="cadre")
    texte(800, 230, "Incrémentation", "#45FFCA", "center", tag="titre")
    texte(800, 260, "par niveau", "#45FFCA", "center", tag="titre")
    ligne(665, 290, 935, 290, "#45FFCA", 3, "ligne")

    rectangle(665, 445, 935, 735, "#45FFCA", epaisseur=3, tag="cadre")
    texte(800, 475, "Incrémentation", "#45FFCA", "center", tag="titre")
    texte(800, 505, "par X niveaux", "#45FFCA", "center", tag="titre")
    ligne(665, 535, 935, 535, "#45FFCA", 3, "ligne")


def create_options_input_buttons() -> List[OptionButton]:
    """Create all option input buttons for the left side."""
    buttons = [
        OptionButton(75, 300, "Nombre d'obstacles", "obstacles", "nombre_obstacles"),
        OptionButton(75, 375, "Nombre de bonus", "pommes", "nombre_pommes"),
        OptionButton(75, 450, "Nombre de vies", "vies", "nombre_vies"),
        OptionButton(75, 525, "Niveau initial", "nivInit", "nb_niveau"),
        OptionButton(75, 600, "Vitesse lente", "vitLent", "nombre_JoueurSpd(n)"),
        OptionButton(75, 675, "Vitesse rapide", "vitRap", "nombre_JoueurSpd(f)")
    ]
    return buttons


def create_options_input_buttons_right() -> List[OptionButton]:
    """Create all option input buttons for the right side."""
    buttons = [
        OptionButton(375, 300, "Vitesse du QIX", "vitQIX", "nb_QIXspdI"),
        OptionButton(375, 375, "Vitesse du Sparx", "vitSp", "nb_SparxspdI"),
        OptionButton(375, 450, "Zone à capturer", "aCapt", "nb_zone_a_capturerI"),
        OptionButton(375, 525, "Taille du QIX", "QIXSize", "nb_tailleQIX"),
        OptionButton(375, 600, "Taille du Joueur", "PlayerSize", "nb_tailleJoueur")
    ]
    return buttons


def create_options_input_buttons_increment() -> List[OptionButton]:
    """Create increment option input buttons."""
    buttons = [
        OptionButton(675, 300, "Vitesse du QIX", "vitQIX+", "nb_QIXspd+"),
        OptionButton(675, 375, "Vitesse du Sparx", "vitSp+", "nb_Sparxspd+"),
        OptionButton(675, 545, "Incrémentation par", "niv+", "nb_+"),
        OptionButton(675, 620, "Zone à capturer", "aCapt+", "nb_zone_a_capturer+")
    ]
    return buttons


def options_menu(options: dict) -> str:
    """Display options configuration menu."""
    
    # Draw static UI elements
    create_options_menu_ui()

    # Create option buttons
    left_buttons = create_options_input_buttons()
    right_buttons = create_options_input_buttons_right()
    increment_buttons = create_options_input_buttons_increment()
    all_option_buttons = left_buttons + right_buttons + increment_buttons
    
    # Draw all option fields
    for button in all_option_buttons:
        value = options[button.option]
        if button.option == "aCapt" or button.option == "aCapt+":  # Zone percentage
            value = f"{value} %"
        button.draw_full(value)

    # Create and draw menu button
    menu_button = MenuButton(WIDTH // 2 - 200, HEIGHT - 100, 400, 50,
                     "Paramètres", "Parametres")
    menu_button.draw()

    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        
        # Check menu button interaction
        if menu_button.is_clicked(x_souris, y_souris):
            menu_button.highlight()
            if tev == "ClicGauche":
                return "Parametres"
        
        # Check option button interactions
        for button in all_option_buttons:
            if button.is_clicked(x_souris, y_souris):
                button.highlight_input()
                if tev == "ClicGauche":
                    efface(button.tag)
                    entree = read_input(True)
                    if entree != "":
                        # Handle special validation for different fields
                        if button.option in ["vies", "nivInit"]:  # Lives and level - integers only
                            if entree > "0" and "." not in entree:
                                options[button.option] = int(entree)
                        elif button.option == "aCapt":  # Zone capture percentage
                            val = float(entree)
                            if 0 < val < 100:
                                options[button.option] = val
                        else:  # General numeric input
                            if "." in entree:
                                options[button.option] = float(entree)
                            else:
                                options[button.option] = int(entree)
                    
                    # Redraw the field with new value
                    value = options[button.option]
                    if button.option == "aCapt" or button.option == "aCapt+":
                        value = f"{value} %"
                    texte(button.x + button.width//2, button.y + button.height//2, 
                         str(value), COLORS["text"], "center", taille=15, tag=button.tag)
        
        mise_a_jour()
        if tev == "Quitte":
            break
        elif tev == "Touche":
            if touche(ev) == "Escape":
                return "Parametres"
    
    return "Parametres"