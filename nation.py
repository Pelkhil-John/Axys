import pygame
from constants import Identity

class Nation(pygame.sprite.Group):

    owned_biomes: list

    def __init__(self, *sprites) -> None:
        self.owned_biomes = []
        super().__init__(*sprites)

    def obj(self):
        return self 


#Create all of the main groups
red = Nation()
white = Nation()
blue = Nation()
green = Nation()
black = Nation()
yellow = Nation()


# Add Identity sprite to each of these gorups, 
# Identity sprite will store the name of the group and other important data
red.add(Identity("red", red))
white.add(Identity("white", white))
blue.add(Identity("blue", blue))
green.add(Identity("green", green))
black.add(Identity("black", black))
yellow.add(Identity("yellow", yellow))


#for easy of reference and use:
#TODO: create a class for this, it porbably shouldn't live in constants
nations_dict = {"red": red, "white": white, "blue": blue, "green": green, "black": black, "yellow": yellow}




    