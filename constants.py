import pygame
import os

class Identity(pygame.sprite.Sprite):
    """ This Sprite should belong to ONE group and one group only 

    Purpose is to store the data for the group as accessable from any member of the group
    """

    group_name: str

    def __init__(self, group_name, *group):
        super().__init__(*group)
        self.group_name = group_name


#Actual Consatants
NAME = "Axys"
PTWD = "/"
WIDTH, HEIGHT = 1000,1000
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH/5, HEIGHT/10
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 20
NPC_WIDTH, NPC_HEIGHT = 10, 10
MAP_WIDTH, MAP_HEIGHT = 200, 200
TILE_WIDTH, TILE_HEIGHT = 10, 10
MAX_VEL = 5
FPS = 60

npc = pygame.sprite.Group()

npc.add(Identity("npc", npc))


def get(variable):
    return eval(variable, globals())


def find_proper_wd(file_name):
    #FIXME THIS AINT WORKIN
    path = ""
    for file in os.listdir(file_name):
        if file == NAME:
            return os.path.join(file_name, file)
        if path == "" and os.path.isdir(os.path.join(file_name, file)):
            path = find_proper_wd(os.path.join(file_name, file))
    return path

def update_size(window_size: tuple):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = window_size

def setup():
    global PTWD
    #setting up constants
    if os.path.dirname(os.getcwd()) != NAME:
        PTWD = find_proper_wd(os.path.dirname(os.getcwd()))
        # PTWD = find_proper_wd(os.getcwd())

    if "saves" not in os.listdir():
        os.mkdir("saves")
    pass