from typing import Optional
from fltk import donne_ev, type_ev, touche, ferme_fenetre, mise_a_jour, rectangle, texte, attend_clic_gauche, cercle, efface
from Interface.const import FONTS, WIDTH, HEIGHT, COLORS
import string


def draw_square(x: float, y: float, side: float, color: str = "black", 
               fill: Optional[str] = None, tag: Optional[str] = None, 
               thickness: float = 1.0) -> None:
    """Draw a square with given coordinates and side length.
    
    Args:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner  
        side: Length of the square's side
        color: Border color (default "black")
        fill: Fill color (default None for transparent)
        tag: Element tag for identification
        thickness: Border thickness
    """
    rectangle(x, y, x + side, y + side, couleur=color, 
             remplissage=fill, tag=tag, epaisseur=thickness)


def is_mouse_in_rect(mouse_x: int, mouse_y: int, x: int, y: int, 
                    width: int, height: int) -> bool:
    """Check if mouse coordinates are within a rectangle."""
    return x <= mouse_x <= x + width and y <= mouse_y <= y + height


def read_input(number: bool) -> str :
    """Read user input from keyboard.
    Args:
        number: If True, only accept numeric input (digits and period)
        Returns: The input string entered by the user.
    """
    texte = ""
    while True :
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Touche" :
            nom_touche = touche(ev)
            if nom_touche == "Escape" :
                return ""
            elif not number :
                return nom_touche
            else :
                if nom_touche in string.digits :
                    texte = texte + nom_touche
                elif nom_touche == "period" :
                    texte = texte + "."
                elif nom_touche == "Return" : 
                    if texte[-1] == "." :
                        texte = texte[:-1]
                    break
        elif tev == "Quitte" :
            ferme_fenetre()
        mise_a_jour()
    return texte


def update_action(captured_zone: float, score: Optional[int]) -> None:
    """Update UI elements after each game action.
    
    Args:
        captured_zone: Current captured zone percentage
        score: Current score (None if not tracking)
    """
    texte(106, 113, f"{captured_zone:.2f} %", "white", "center", 
          police=FONTS["main"], taille=30, tag="Zonecapturee")
    if score is not None:
        texte(275, 50, f"{score}", "white", "center", 
              police=FONTS["main"], taille=30, tag="score")


def update_round(target_zone: float, lives: int, level: int) -> None:
    """Update UI elements after each level.
    
    Args:
        target_zone: Target zone percentage to capture
        lives: Number of remaining lives
        level: Current level number
    """
    texte(260, 113, f"{target_zone} %", "gray", "center", 
          police=FONTS["main"], taille=30, tag="Zone_a_capturee")
    texte(670, 114, f"{lives}", "Violet", "center", 
          police=FONTS["ui"], taille=25, tag="nbVies")
    texte(900, 55, f"{level}", "light gray", "center", 
          police=FONTS["ui"], taille=30, tag="niveau")
    draw_status(0)


def draw_status(speed: int) -> None:
    """Update the drawing status indicator.
    
    Args:
        speed: Drawing speed (0=slow/red, 1=normal/green, 2=fast/blue)
    """
    efface("dessiner")
    color_map = {0: "red", 1: "green", 2: "blue"}
    color = color_map.get(speed, "red")
    texte(850, 113, "Drawing", color, "center", 
          police=FONTS["main"], taille=20, tag="dessiner")


def show_game_over(remaining_lives: int) -> None:
    """Display game over message with remaining lives.
    
    Args:
        remaining_lives: Number of lives remaining
    """
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Game over message
    texte(center_x, center_y, "Perdu", COLORS["error"], "center", 
          police=FONTS["main"], taille=25, tag="Perdu")
    texte(center_x, HEIGHT * 3 // 4, "Appuyez sur click gauche pour continuer", 
          "white", "center", police=FONTS["main"], taille=10, tag="Continue")
    mise_a_jour()
    attend_clic_gauche()
    efface("Perdu")
    
    # Remaining lives
    texte(center_x, center_y - 30, "Vies restantes :", COLORS["error"], 
          "center", police=FONTS["main"], taille=25, tag="Restes")
    texte(center_x, center_y, remaining_lives, COLORS["error"], "center", 
          police=FONTS["main"], taille=25, tag="nbVies")
    mise_a_jour()
    attend_clic_gauche()
    
    # Cleanup
    for tag in ["nbVies", "Restes", "Trainée", "Continue"]:
        efface(tag)
    mise_a_jour()


def show_level_complete(level: int) -> None:
    """Display level completion message.
    
    Args:
        level: Current level number
    """
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    texte(center_x, HEIGHT * 3 // 4, "Appuyez sur click gauche pour continuer", 
          "white", "center", police=FONTS["main"], taille=10, tag="Continue")
    texte(center_x, center_y - 30, "Vous avez gagné", COLORS["error"], 
          "center", police=FONTS["main"], taille=25, tag="Gagner")
    mise_a_jour()
    attend_clic_gauche()
    efface("Gagner")
    
    texte(center_x, center_y - 30, f"Niveau {level}", COLORS["error"], 
          "center", police=FONTS["main"], taille=25, tag="Niveau")
    mise_a_jour()
    attend_clic_gauche()
    
    efface("Niveau")
    efface("Continue")
    mise_a_jour()


def draw_player(x: float, y: float, radius: float) -> None:
    """Draw the player (cyan circle with border).
    
    Args:
        x: X coordinate of center
        y: Y coordinate of center
        radius: Circle radius
    """
    cercle(x, y, radius, "Aqua", epaisseur="4", tag="curseur")


def draw_sparx(x: float, y: float) -> None:
    """Draw a Sparx enemy (white border, magenta fill).
    
    Args:
        x: X coordinate of center
        y: Y coordinate of center
    """
    cercle(x, y, 5, couleur="White", remplissage="Magenta", 
           epaisseur="2", tag="Sparx")