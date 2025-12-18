from typing import List
from Interface.const import COLORS, HEIGHT, QIX_LOGO_PATH, WIDTH
import os
from fltk import image, rectangle, touche, donne_ev, type_ev, abscisse_souris, ordonnee_souris, mise_a_jour, efface
from Interface.buttons import MenuButton


def create_settings_menu_buttons() -> List[MenuButton]:
    """Create buttons for the parametres menu."""
    center_x = WIDTH // 2
    buttons = [
        MenuButton(center_x - 200, 250, 400, 50, "Options des ennemis", "Options"),
        MenuButton(center_x - 200, 325, 400, 50, "Touches", "Touches"),
        MenuButton(center_x - 200, HEIGHT - 150, 400, 50, "Menu Principal", "Principal")
    ]
    return buttons


def settings_menu() -> str:
    """Display parameters menu."""
    rectangle(0, 0, WIDTH, HEIGHT, COLORS["background"], COLORS["background"], 1, "bg")
    img_height = 80
    image(WIDTH//2,125, QIX_LOGO_PATH, ancrage="center", tag="im", largeur=int(img_height * (414/188)), hauteur=img_height)
    # Create and draw buttons
    buttons = create_settings_menu_buttons()
    for button in buttons:
        button.draw()

    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        
        # Check button interactions
        for button in buttons:
            if button.is_clicked(x_souris, y_souris):
                button.highlight()
                if tev == "ClicGauche":
                    return button.action
        
        mise_a_jour()
        if tev == "Quitte":
            break
        elif tev == "Touche":
            if touche(ev) == "Escape":
                return "Principal"
            
    return "Principal"