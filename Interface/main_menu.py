import os
from typing import Optional, List
from Interface.const import COLORS, QIX_LOGO_PATH, WIDTH, HEIGHT
from Interface.buttons import MenuButton
from fltk import image, rectangle, texte, touche, donne_ev, type_ev, abscisse_souris, ordonnee_souris, mise_a_jour, efface


def handle_escape_confirmation() -> bool:
    """Handle escape key confirmation dialog.
    
    Returns:
        True if user wants to quit, False otherwise
    """
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Draw confirmation dialog
    rectangle(center_x - 200, center_y - 100, center_x + 200, center_y + 100,
             "white", COLORS["background"], epaisseur=4, tag="confirmer")
    texte(center_x, center_y - 50, "Êtes-vous sûr de", COLORS["error"], 
          "center", 20, tag="confirmer")
    texte(center_x, center_y - 10, "vouloir quitter ?", COLORS["error"], 
          "center", 20, tag="confirmer")
    
    # Yes/No buttons
    rectangle(center_x - 100, center_y + 50, center_x - 40, center_y + 80,
             "white", COLORS["background"], 2, tag="confirmer")
    texte(center_x - 70, center_y + 65, "Oui", COLORS["error"], "center", 
          taille=13, tag="oui")
    
    rectangle(center_x + 40, center_y + 50, center_x + 100, center_y + 80,
             "white", COLORS["background"], 2, tag="confirmer") 
    texte(center_x + 70, center_y + 65, "Non", COLORS["highlight"], "center",
          taille=13, tag="non")
    
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        mouse_x = abscisse_souris()
        mouse_y = ordonnee_souris()
        efface('cadre')
        
        if center_y + 50 <= mouse_y <= center_y + 80:
            if center_x - 100 <= mouse_x <= center_x - 40:  # Yes button
                rectangle(center_x - 100, center_y + 50, center_x - 40, 
                         center_y + 80, COLORS["error"], epaisseur=2, tag="cadre")
                if tev == "ClicGauche":
                    return True
            elif center_x + 40 <= mouse_x <= center_x + 100:  # No button
                rectangle(center_x + 40, center_y + 50, center_x + 100, 
                         center_y + 80, COLORS["highlight"], epaisseur=2, tag="cadre")
                if tev == "ClicGauche":
                    for tag in ["confirmer", "cadre", "oui", "non"]:
                        efface(tag)
                    return False
        
        if tev == "Quitte" or (tev == "Touche" and touche(ev) == "Escape"):
            return True
            
        mise_a_jour()


def create_menu_buttons() -> List[MenuButton]:
    """Create the main menu buttons."""
    center_x = WIDTH // 2
    button_width = 400
    button_height = 50
    
    buttons = [
        MenuButton(center_x - 200, 250, button_width, button_height, 
                  "Commencer", "Commencer"),
        MenuButton(center_x - 200, 325, button_width, button_height,
                  "Variantes", "Variantes"),
        MenuButton(center_x - 200, 400, button_width, button_height,
                  "Paramètres", "Parametres"),
        MenuButton(center_x - 200, 475, button_width, button_height,
                  "Quitter", "Quitter")
    ]
    return buttons


def main_menu() -> Optional[str]:
    """Display the main menu and handle user interactions.
    
    Returns:
        Selected action or None to quit
    """
    rectangle(0, 0, WIDTH, HEIGHT, COLORS["background"], COLORS["background"], 1, "bg")
    img_height = 80
    image(WIDTH//2,125, QIX_LOGO_PATH, ancrage="center", tag="im", largeur=int(img_height * (414/188)), hauteur=img_height)
    
    buttons = create_menu_buttons()
    for button in buttons:
        button.draw()
    
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        mouse_x = abscisse_souris()
        mouse_y = ordonnee_souris()
        efface("rectangle")
        
        # Check button interactions
        for button in buttons:
            if button.is_clicked(mouse_x, mouse_y):
                button.highlight()
                if tev == "ClicGauche":
                    if button.action == "Quitter":
                        return None
                    return button.action
        
        mise_a_jour()
        
        if tev == "Quitte":
            return None
        elif tev == "Touche" and touche(ev) == 'Escape':
            if handle_escape_confirmation():
                return None