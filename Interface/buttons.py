from typing import Union
from Interface.const import COLORS
from fltk import rectangle, texte
from Interface.utils import draw_square, is_mouse_in_rect

class MenuButton:
    """Represents a clickable menu button."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, action: str, is_square: bool = False) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.is_square = is_square
        self.is_selected = False
    
    def draw(self, tag: str = "bouton") -> None:
        """Draw the button."""
        if self.is_square:
            # Draw square button with selection state
            color = COLORS["highlight"] if self.is_selected else COLORS["button"]
            draw_square(self.x, self.y, self.width, color, tag=tag)
            texte(self.x + self.width//2, self.y + self.width//2, self.text,
                  COLORS["text"], "center", taille=14, tag=tag)
        else:
            # Draw rectangular button
            rectangle(self.x, self.y, self.x + self.width, self.y + self.height,
                     COLORS["button"], epaisseur=2, tag=tag)
            texte(self.x + self.width//2, self.y + self.height//2, self.text,
                  COLORS["text"], "center", taille=24, tag=tag)
    
    def is_hovered(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if the mouse is hovering over the button."""
        if self.is_square:
            return (self.x <= mouse_x <= self.x + self.width and 
                    self.y <= mouse_y <= self.y + self.width)
        else:
            return is_mouse_in_rect(mouse_x, mouse_y, self.x, self.y, 
                                   self.width, self.height)
    
    def highlight(self, tag: str = "rectangle") -> None:
        """Highlight the button."""
        if self.is_square:
            draw_square(self.x, self.y, self.width, COLORS["button_hover"], tag=tag)
        else:
            rectangle(self.x, self.y, self.x + self.width, self.y + self.height, COLORS["button_hover"], 
             epaisseur=2, tag=tag)
    
    def toggle_selection(self) -> bool:
        """Toggle selection state and return new state."""
        self.is_selected = not self.is_selected
        return self.is_selected
    
    def set_selected(self, selected: bool) -> None:
        """Set the selection state."""
        self.is_selected = selected


class InputButton(MenuButton):
    """Unified button for input fields (options and key bindings)."""
    
    def __init__(self, x: int, y: int, label: str, identifier: str, tag: str, input_type: str = "option"):
        # Input field is always 50x50 at x+200, y-1 from label
        prefix = "option" if input_type == "option" else "key"
        super().__init__(x + 200, y - 1, 50, 51, "", f"{prefix}_{identifier}", is_square=False)
        self.label = label
        self.label_x = x
        self.label_y = y
        self.identifier = identifier
        self.tag = tag
        self.input_type = input_type

        
    def draw_full(self, value: Union[str, int, float], tag: str = "bouton") -> None:
        """Draw both the label and the input field."""
        # Draw label rectangle and text
        rectangle(self.label_x, self.label_y, self.label_x + 200, self.label_y + 50, 
                 COLORS["button"], epaisseur=2, tag="cadre")
        
        # Handle label text formatting based on input type
        label_tag = self.label.lower()
        if self.input_type == "key":
            label_tag = label_tag.replace(" ", "")
        
        texte(self.label_x + 100, self.label_y + 25, self.label, 
              COLORS["text"], "center", taille=15, tag=label_tag)
        
        # Draw input field and value
        rectangle(self.x, self.y, self.x + self.width, self.y + self.height, 
                 COLORS["button"], tag=tag)
        texte(self.x + self.width//2, self.y + self.height//2, str(value), 
              COLORS["text"], "center", taille=15, tag=self.tag)
    
    def highlight_input(self) -> None:
        """Highlight just the input field."""
        rectangle(self.x, self.y, self.x + self.width, self.y + self.height, 
                 COLORS["button_hover"], tag="rectangle")