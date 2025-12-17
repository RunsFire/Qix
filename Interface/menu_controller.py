from typing import Set, Dict, Union
from Interface.main_menu import main_menu
from Interface.settings_menu import settings_menu
from Interface.variants_menu import variants_menu
from Interface.key_menu import key_menu
from Interface.options_menu import options_menu
from Interface.const import WIDTH, HEIGHT
from fltk import efface_tout


def menu_controller(variants: Set[str], options: Dict[str, Union[float, int]], keys: Dict[str, str]) -> bool:
    """Main controller of the menus.

    Args:
        variants: Set of game variant settings.
        options: Dictionary of general game options.
        keys: Dictionary of key bindings.
    Returns:
        choice: The final menu choice made by the user.
    """
    choice = main_menu()
    while choice != None :
        efface_tout()
        if choice == "Principal" :
            choice = main_menu()
        elif choice == "Variantes" :
            choice = variants_menu(WIDTH, HEIGHT, variants)
        elif choice == "Parametres" :
            while choice != None and choice != "Principal" :
                efface_tout()
                if choice == "Parametres" :
                    choice = settings_menu(WIDTH, HEIGHT)
                elif choice == "Options" :
                    choice = options_menu(WIDTH, HEIGHT, options)
                elif choice == "Touches" :
                    choice = key_menu(WIDTH, HEIGHT, keys)
        elif choice == "Commencer" :
            efface_tout()
            break
    
    return choice is not None