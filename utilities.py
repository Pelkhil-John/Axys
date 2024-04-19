import pygame.font
import pygame.color
import pygame.rect
import json
from constants import Identity

WHITE = (255,255,255)

pygame.font.init()

my_font = pygame.font.SysFont("Times New Roman", 30)


def get_text_surface(text, font=my_font, color=WHITE):
    """ used to get the text surface to display on the screen
        you will need to then call blit on the surface to display it using a location in the form of a tuple like this:

        window.blit(text_surface, (x, y))
        pygame.display.update()

    :param text: str
    :param font: pygame.font.Font
    :param color: pygame.Color
    """
    try:
        text = str(text)
        return font.render(text, False, color)
    except:
        print(f'Font Error: fix yo fonts. Trying to print: {text}')
        return font.render('Font Error', False, WHITE)
    
def normalize(list, max):
    #TODO: this stuff
    return 1

def get_npc_data_dict():
    return {
        "rect": None,
        "color": None,
        "on_screen": False,
        "health": 0,
        "mana": 0,
        "defence": 0,
        "power": 0,
        "npc_index":0,
        "class_type": None
    }

def get_player_data_dict():
    return {
        "rect": None,
        "color": None,
        "on_screen": False,
        "health": 0,
        "mana": 0,
        "defence": 0,
        "power": 0,
        "class_type": None,
        "experience": 0,
        "level": 0,
        "ref_x": 0,
        "ref_y": 0
    }

def get_map_data_dict():
    return {
        "biomes": {},
        "tiles": []
    }

def save_to(dict_func, save_func, file_path):
    save_dict = save_func(dict_func())
    save_file = open("saves/" + file_path + ".json", "w")
    json.dump(save_dict, save_file, indent=4)
    save_file.close()

def rect_loader(rect_save):
    """ for loading the converted/ overridden string cast for rect.
    
    :param rect_save: list(left(float),top(float),width(float),height(float))
    """
    return pygame.rect.Rect(rect_save[0], rect_save[1], rect_save[2], rect_save[3])

def color_loader(color_save) -> pygame.color.Color:
    """ for loading the converted/overriden string cast for color
    
    :param color_save: list(r(int), g(int), b(int))
    """
    if isinstance(color_save, str):
            return pygame.color.Color(color_save)
    return pygame.color.Color(color_save[0], color_save[1], color_save[2])

def color_to_list(color):
    #TODO Docstring
    if isinstance(color, pygame.color.Color):
        return [color.r, color.g, color.b, color.a]
    elif isinstance(color, str):
        return color
    return "cyan"

def rect_to_list(rect):
    #TODO: Docstring
    if isinstance(rect, pygame.rect.Rect):
        return [rect.left, rect.top, rect.w, rect.h]
    return [0,0,0,0]