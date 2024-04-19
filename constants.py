import pygame
import os

class Identity(pygame.sprite.Sprite):
    """ This Sprite should belong to ONE group and one group only 

    Purpose is to store the data for the group as accessable from any member of the group
    TODO: Docstring
    """

    group_name: str

    def __init__(self, group_name, *group):
        super().__init__(*group)
        self.group_name = group_name


#Actual Consatants
#TODO: Consider auto populating this to allow for saves between plays
NAME = "Axys"
PTWD = "/"
WIDTH, HEIGHT = 1000,1000
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH/5, HEIGHT/10
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 40
NPC_WIDTH, NPC_HEIGHT = 20, 40
MAP_WIDTH, MAP_HEIGHT = 100, 100
TILE_WIDTH, TILE_HEIGHT = 10, 10
MAX_VEL = 5
FPS = 60

npc = pygame.sprite.Group()

npc.add(Identity("npc", npc))


def get(variable):
    return eval(variable, globals())


def find_proper_wd(file_name):
    for file in os.listdir(file_name):
        print(file)
        if file == NAME:
            return os.path.join(file_name, file)
        if os.path.isdir(file):
            os.path.join(file_name, find_proper_wd(file))    
    return ""

def setup():
    global PTWD
    #setting up constants
    PTWD = find_proper_wd(os.path.dirname(os.getcwd()))

    pass