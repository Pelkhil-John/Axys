import math
import pygame.font
import pygame.color
import pygame.rect
import json
from constants import Identity

pygame.font.init()

my_font = pygame.font.SysFont("Times New Roman", 30)


def get_text_surface(text, font=my_font, color="white"):
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
        return font.render('Font Error', False, "white")
    
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
        "map_rect": None,
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

def get_alpha_rect_surface(rect: pygame.rect.Rect, color, radius = -1) -> pygame.Surface:
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(surface, color, surface.get_rect(), border_radius=radius)
    return surface

def get_direction(center:tuple, target:tuple) -> int:
    if target[0] - center[0] == 0:
        target = (target[0] + 1, target[1]) 
    if target[0] - center[0] > 0:
        angle = math.degrees(math.atan((center[1]-target[1])/(target[0]-center[0])))
    else: 
        angle = 180 + math.degrees(math.atan((target[1]-center[1])/(center[0]-target[0])))
    return int(angle % 360)

def get_distance(center:tuple, target:tuple):
    return math.sqrt((center[0]-target[0])**2 + (center[1]-target[1])**2)