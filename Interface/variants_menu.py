from typing import List, Tuple
from Interface.buttons import MenuButton
from fltk import rectangle, touche, donne_ev, type_ev, abscisse_souris, ordonnee_souris, mise_a_jour, efface


def create_variant_buttons() -> List[MenuButton]:
    """Create all variant selection buttons using MenuButton class."""
    buttons = [
        MenuButton(100, 250, 100, 100, "Score", "Score", is_square=True),
        MenuButton(235, 250, 100, 100, "Vitesse", "Vitesse", is_square=True), 
        MenuButton(370, 250, 100, 100, "  Deux\nJoueurs", "Joueurs", is_square=True),
        MenuButton(100, 400, 100, 100, "Obstacles", "Obstacles", is_square=True),
        MenuButton(235, 400, 100, 100, "Bonus", "Bonus", is_square=True),
        MenuButton(100, 550, 100, 100, " Sparx\nInternes", "Sparx", is_square=True),
        MenuButton(235, 550, 100, 100, "Niveaux", "Niveaux", is_square=True)
    ]
    return buttons


def variants_menu(width: int, height: int, lst_variantes: List[str]) -> Tuple[str, List[str]]:
    """Display variants selection menu."""
    rectangle(0, 0, width, height, "black", "black", 1, "bg")
    
    # Create variant buttons and set their selection state
    variant_buttons = create_variant_buttons()
    for button in variant_buttons:
        button.set_selected(button.action in lst_variantes)
        button.draw()

    # Create and draw menu button
    menu_button = MenuButton(width // 2 - 200, height - 150, 400, 50,
                     "Menu Principal", "Principal")
    menu_button.draw()

    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        
        # Check menu button
        if menu_button.is_clicked(x_souris, y_souris):
            menu_button.highlight()
            if tev == "ClicGauche":
                return "Principal", lst_variantes
        
        # Check variant buttons
        for button in variant_buttons:
            if button.is_clicked(x_souris, y_souris):
                button.highlight()
                if tev == "ClicGauche":
                    if button.action in lst_variantes:
                        lst_variantes.remove(button.action)
                        button.set_selected(False)
                    else:
                        lst_variantes.append(button.action)
                        button.set_selected(True)
                    # Redraw the button with updated selection state
                    button.draw()
        
        mise_a_jour()
        
        if tev == "Quitte":
            break
        elif tev == "Touche" and touche(ev) == "Escape":
            return "Principal", lst_variantes
    
    return "Principal", lst_variantes