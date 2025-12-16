from typing import List, Tuple
from Interface.const import COLORS
from Interface.buttons import MenuButton, KeyButton
from fltk import rectangle, texte, ligne, touche, donne_ev, type_ev, abscisse_souris, ordonnee_souris, mise_a_jour, efface
from Interface.utils import read_input


def create_key_buttons_player1() -> List[KeyButton]:
    """Create key binding buttons for Player 1."""
    buttons = [
        KeyButton(75, 300, "Monter", 0, "touche_monter1"),
        KeyButton(75, 375, "A gauche", 1, "touche_gauche1"),
        KeyButton(75, 450, "Descendre", 2, "touche_descendre1"),
        KeyButton(75, 525, "A droite", 3, "touche_droite1"),
        KeyButton(75, 600, "Vitesse normale", 4, "touche_spd(n)1"),
        KeyButton(75, 675, "Vitesse rapide", 5, "touche_spd(f)1")
    ]
    return buttons


def create_key_buttons_player2() -> List[KeyButton]:
    """Create key binding buttons for Player 2."""
    buttons = [
        KeyButton(375, 300, "Monter", 6, "touche_monter2"),
        KeyButton(375, 375, "A gauche", 7, "touche_gauche2"),
        KeyButton(375, 450, "Descendre", 8, "touche_descendre2"),
        KeyButton(375, 525, "A droite", 9, "touche_droite2"),
        KeyButton(375, 600, "Vitesse normale", 10, "touche_spd(n)2"),
        KeyButton(375, 675, "Vitesse rapide", 11, "touche_spd(f)2")
    ]
    return buttons


def key_menu(width: int, height: int, lst_touches: List[str]) -> Tuple[str, List[str]]:
    """Display key bindings configuration menu."""
    rectangle(0, 0, width, height, COLORS["background"], COLORS["background"], 1, "bg")
    # image(largeurFenetre//2,125, os.path.join(PATH,'QIX_logo.gif'), ancrage="center", tag="im", largeur=300, hauteur=int(188*(300/414)))

    entree = ""

    # Draw player sections  
    rectangle(65, 200, 335, 735, COLORS["accent"], epaisseur=3, tag="cadre")
    texte(200, 245, "Joueur 1", COLORS["accent"], "center", tag="titre")
    ligne(65, 290, 335, 290, COLORS["accent"], 3, "ligne")

    rectangle(365, 200, 635, 735, COLORS["accent"], epaisseur=3, tag="cadre")
    texte(500, 245, "Joueur 2", COLORS["accent"], "center", tag="titre")
    ligne(365, 290, 635, 290, COLORS["accent"], 3, "ligne")

    # Create key binding buttons
    player1_buttons = create_key_buttons_player1()
    player2_buttons = create_key_buttons_player2()
    all_key_buttons = player1_buttons + player2_buttons
    
    # Draw all key binding fields
    for button in all_key_buttons:
        key_name = lst_touches[button.key_index]
        button.draw_full(key_name)

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
                return "Parametres", lst_touches
        
        # Check key binding button interactions
        for button in all_key_buttons:
            if button.is_clicked(x_souris, y_souris):
                button.highlight_input()
                if tev == "ClicGauche":
                    efface(button.tag)
                    entree = read_input(False)  # Allow any key input
                    if entree != "" and entree not in lst_touches:
                        lst_touches[button.key_index] = entree
                    
                    # Redraw the field with new key
                    texte(button.x + button.width//2, button.y + button.height//2, 
                         lst_touches[button.key_index], COLORS["text"], 
                         "center", taille=15, tag=button.tag)
        
        mise_a_jour()
        if tev == "Quitte":
            break
        elif tev == "Touche":
            if touche(ev) == "Escape":
                return "Parametres", lst_touches
    
    return "Parametres", lst_touches