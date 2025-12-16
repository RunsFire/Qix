import os
from typing import List, Tuple, Optional
from fltk import image, rectangle, texte, attend_clic_gauche, efface, ligne
from Interface.const import WIDTH, HEIGHT, COLORS, FONTS, PATH

def _draw_ui_elements(captured_zone: float, target_zone: float, lives: int, 
                     level: int, score: Optional[int]) -> None:
    """Draw the UI elements for the game screen."""
    # Capture percentage indicator
    ligne(186, 129, 206, 95, "gray", epaisseur="2")
    texte(106, 113, f"{captured_zone:.2f} %", "white", "center", 
          police=FONTS["main"], taille=30, tag="Zonecapturee")
    texte(260, 113, f"{target_zone} %", "gray", "center", 
          police=FONTS["main"], taille=30, tag="Zone_a_capturee")
    
    # Lives
    texte(670, 114, f"{lives}", "Violet", "center", 
          police=FONTS["main"], taille=25, tag="nbVies")
    image(700, 113, os.path.join(PATH, 'heart.gif'), ancrage="center", tag="im")
    
    # Level
    texte(775, 55, "Niveau :", "light gray", "center", 
          police=FONTS["main"], taille=30)
    texte(900, 55, f"{level}", "light gray", "center", 
          police=FONTS["main"], taille=30, tag="niveau")
    
    # Drawing indicator
    texte(850, 113, "Drawing", "red", "center", police="Courier", 
          taille=20, tag="dessiner")
    
    # Score (if enabled)
    if score is not None:
        texte(106, 50, "Score :", "white", "center", 
              police=FONTS["main"], taille=30)
        texte(275, 50, f"{score}", "white", "center", 
              police=FONTS["main"], taille=30, tag="score")


def start_game(captured_zone: float, target_zone: float, lives: int, 
                 level: int, score: Optional[int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Create the game launch screen with UI elements.
    
    Args:
        captured_zone: Percentage of zone already captured
        target_zone: Target percentage to capture
        lives: Number of remaining lives
        level: Current game level
        score: Current score (None if not tracking)
        
    Returns:
        Tuple of top-left and bottom-right corner coordinates
    """
    top_left = (200, 180)
    bottom_right = (800, 850)
    
    # Background
    rectangle(0, 0, WIDTH, HEIGHT, remplissage=COLORS["background"])
    
    # Game zone
    rectangle(top_left[0], top_left[1], bottom_right[0], bottom_right[1], 
             "white", tag="ZdJ")
    
    # Logo placeholder
    rectangle(320, 352, 680, 548, "white", epaisseur="5", tag="im")
    attend_clic_gauche()
    efface("im")
    
    # Start message
    texte(500, 500, "Appuyez sur click \ngauche pour jouer", "gray", "center", 
          police=FONTS["main"], taille=30, tag="interaction")
    attend_clic_gauche()
    efface('interaction')
    
    # UI Elements
    _draw_ui_elements(captured_zone, target_zone, lives, level, score)
    
    return top_left, bottom_right