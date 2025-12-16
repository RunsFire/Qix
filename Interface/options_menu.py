from typing import List, Tuple, Union
from Interface.buttons import MenuButton, OptionButton
from Interface.const import COLORS
from Interface.utils import read_input
from fltk import rectangle, texte, ligne, touche, donne_ev, type_ev, abscisse_souris, ordonnee_souris, mise_a_jour, efface


def create_options_menu_ui() -> None:
    """Create the static UI elements for the options menu."""
    rectangle(0, 0, 1000, 800, COLORS["background"], COLORS["background"], 1, "bg")
    
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
        OptionButton(75, 300, "Nombre d'obstacles", 0, "nombre_obstacles"),
        OptionButton(75, 375, "Nombre de bonus", 1, "nombre_pommes"),
        OptionButton(75, 450, "Nombre de vies", 2, "nombre_vies"),
        OptionButton(75, 525, "Niveau initial", 3, "nb_niveau"),
        OptionButton(75, 600, "Vitesse lente", 4, "nombre_JoueurSpd(n)"),
        OptionButton(75, 675, "Vitesse rapide", 5, "nombre_JoueurSpd(f)")
    ]
    return buttons


def create_options_input_buttons_right() -> List[OptionButton]:
    """Create all option input buttons for the right side."""
    buttons = [
        OptionButton(375, 300, "Vitesse du QIX", 6, "nb_QIXspdI"),
        OptionButton(375, 375, "Vitesse du Sparx", 7, "nb_SparxspdI"),
        OptionButton(375, 450, "Zone à capturer", 8, "nb_zone_a_capturerI"),
        OptionButton(375, 525, "Taille du QIX", 9, "nb_tailleQIX"),
        OptionButton(375, 600, "Taille du Joueur", 10, "nb_tailleJoueur")
    ]
    return buttons


def create_options_input_buttons_increment() -> List[OptionButton]:
    """Create increment option input buttons."""
    buttons = [
        OptionButton(675, 300, "Vitesse du QIX", 11, "nb_QIXspd+"),
        OptionButton(675, 375, "Vitesse du Sparx", 12, "nb_Sparxspd+"),
        OptionButton(675, 545, "Incrémentation par", 13, "nb_+"),
        OptionButton(675, 620, "Zone à capturer", 14, "nb_zone_a_capturer+")
    ]
    return buttons


def options_menu(width: int, height: int, lst_options: List[Union[str, int, float]]) -> Tuple[str, List[Union[str, int, float]]]:
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
        value = lst_options[button.option_index]
        if button.option_index == 8 or button.option_index == 14:  # Zone percentage
            value = f"{value}%" if button.option_index == 8 else f"{value} %"
        button.draw_full(value)

    # Create and draw menu button
    menu_button = MenuButton(width // 2 - 200, height - 100, 400, 50,
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
                return "Parametres", lst_options
        
        # Check option button interactions
        for button in all_option_buttons:
            if button.is_clicked(x_souris, y_souris):
                button.highlight_input()
                if tev == "ClicGauche":
                    efface(button.tag)
                    entree = read_input(True)
                    if entree != "":
                        # Handle special validation for different fields
                        if button.option_index in [2, 3]:  # Lives and level - integers only
                            if entree > "0" and "." not in entree:
                                lst_options[button.option_index] = int(entree)
                        elif button.option_index == 8:  # Zone capture percentage
                            val = float(entree)
                            if 0 < val < 100:
                                lst_options[button.option_index] = val
                        else:  # General numeric input
                            if "." in entree:
                                lst_options[button.option_index] = float(entree)
                            else:
                                lst_options[button.option_index] = int(entree)
                    
                    # Redraw the field with new value
                    value = lst_options[button.option_index]
                    if button.option_index == 8 or button.option_index == 14:
                        value = f"{value}%" if button.option_index == 8 else f"{value} %"
                    texte(button.x + button.width//2, button.y + button.height//2, 
                         str(value), COLORS["text"], "center", taille=15, tag=button.tag)
        
        mise_a_jour()
        if tev == "Quitte":
            break
        elif tev == "Touche":
            if touche(ev) == "Escape":
                return "Parametres", lst_options
    
    return "Parametres", lst_options