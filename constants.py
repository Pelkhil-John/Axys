import pygame


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
#TODO: Considet auto populating this to allow for saves between plays
PTWD = "John_Caudill/"
WIDTH, HEIGHT = 1000,1000
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH/5, HEIGHT/10
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 40
NPC_WIDTH, NPC_HEIGHT = 20, 40
MAP_WIDTH, MAP_HEIGHT = 100, 100
TILE_WIDTH, TILE_HEIGHT = 10, 10
MAX_VEL = 5
FPS = 60

#Create all of the main groups
red = pygame.sprite.Group()
white = pygame.sprite.Group()
blue = pygame.sprite.Group()
green = pygame.sprite.Group()
black = pygame.sprite.Group()
yellow = pygame.sprite.Group()
npc = pygame.sprite.Group()

# Add Identity sprite to each of these gorups, 
# Identity sprite will store the name of the group and other important data
red.add(Identity("red", red))
white.add(Identity("white", white))
blue.add(Identity("blue", blue))
green.add(Identity("green", green))
black.add(Identity("black", black))
yellow.add(Identity("yellow", yellow))
npc.add(Identity("npc", npc))


