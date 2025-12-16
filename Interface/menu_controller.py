from Interface.main_menu import main_menu
from Interface.settings_menu import settings_menu
from Interface.variants_menu import variants_menu
from Interface.key_menu import key_menu
from Interface.options_menu import options_menu
from Interface.const import WIDTH, HEIGHT
from fltk import efface_tout


def menu_controller(lst_variantes, lst_options, lst_touches) :
    """Main controller of the menus.

    Args:
        lst_variantes: List of game variant settings.
        lst_options: List of general game options.
        lst_touches: List of key bindings.
    Returns:
        choice: The final menu choice made by the user.
    """
    choice = main_menu()
    while choice != None :
        efface_tout()
        if choice == "Principal" :
            choice = main_menu()
        elif choice == "Variantes" :
            choice, lst_variantes = variants_menu(WIDTH, HEIGHT, lst_variantes)
        elif choice == "Parametres" :
            while choice != None and choice != "Principal" :
                efface_tout()
                if choice == "Parametres" :
                    choice = settings_menu(WIDTH, HEIGHT)
                elif choice == "Options" :
                    choice, lst_options = options_menu(WIDTH, HEIGHT, lst_options)
                elif choice == "Touches" :
                    choice, lst_touches = key_menu(WIDTH, HEIGHT, lst_touches)
        elif choice == "Commencer" :
            efface_tout()
            break
    
    return choice is not None