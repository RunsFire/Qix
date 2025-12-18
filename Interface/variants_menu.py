from typing import Set, List
from Interface.buttons import MenuButton
from Interface.const import QIX_LOGO_PATH, COLORS, WIDTH, HEIGHT
from fltk import image, image, rectangle, touche, donne_ev, type_ev, abscisse_souris, ordonnee_souris, mise_a_jour, efface


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


def variants_menu(variants: Set[str]) -> str:
    """Display variants selection menu."""
    rectangle(0, 0, WIDTH, HEIGHT, COLORS["background"], COLORS["background"], 1, "bg")
    img_height = 80
    image(WIDTH//2,125, QIX_LOGO_PATH, ancrage="center", tag="im", largeur=int(img_height * (414/188)), hauteur=img_height)

    # Create variant buttons and set their selection state
    variant_buttons = create_variant_buttons()
    for button in variant_buttons:
        button.set_selected(button.action in variants)
        button.draw()

    # Create and draw menu button
    menu_button = MenuButton(WIDTH // 2 - 200, HEIGHT - 150, 400, 50,
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
                return "Principal"
        
        # Check variant buttons
        for button in variant_buttons:
            if button.is_clicked(x_souris, y_souris):
                button.highlight()
                if tev == "ClicGauche":
                    if button.action in variants:
                        variants.remove(button.action)
                        button.set_selected(False)
                    else:
                        variants.add(button.action)
                        button.set_selected(True)
                    # Redraw the button with updated selection state
                    button.draw()
        
        mise_a_jour()
        
        if tev == "Quitte":
            break
        elif tev == "Touche" and touche(ev) == "Escape":
            return "Principal"
    
    return "Principal"