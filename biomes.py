import pygame
import math

import constants as c
from constants import Identity



class Biome:
    """
    
    """

    drawn = False

    # REMINDER: Update the save funciton with any new data 
    owner: pygame.sprite.Group
    owner_name: str
    color: pygame.color.Color
    center: tuple
    walkable: bool
    tile_list: list             #Stores indexes of the members
    #wall_radius: int
    wall_list: list
    biome_name: str
    
    def __init__(self, center=None, owner=None, color="grey", biome_name=""):
        self.color = color
        self.center = center
        self.owner = owner
        self.biome_name = biome_name
        self.tile_list = []
        if owner == None:
            self.owner_name = ""
        else:
            self.owner_name = self.find_owner()


    def find_owner(self) -> str:
        """ TODO: Testing
        """
        if isinstance(self.owner, pygame.sprite.Group):
            for sprite in self.owner:
                if isinstance(sprite, Identity):
                    return sprite.group_name
        return ""        

    def make_wall(self, radius) -> list:
        """Makes a wall around the center of a groups domain
        
        returns a list where
        wall_list[0] is a list of the wall tiles
        wall_list[1] is a list of th interiour tiles 

        :param radius: int
        """
        self.wall_list = [[],[]]
        for i in range(0,c.MAP_WIDTH):
            for j in range(0,c.MAP_HEIGHT):
                dist = int(math.sqrt((i*c.TILE_WIDTH-self.center[0])**2 + (j*c.TILE_HEIGHT-self.center[1])**2))
                #base off of wall radius
                if dist < radius + (c.TILE_HEIGHT):
                    if dist > radius - (c.TILE_WIDTH):
                        self.wall_list[0].append((i,j))
                    else:
                        self.wall_list[1].append((i,j))
        return self.wall_list
    

    def get_save_data(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "color": self.color,
            "center": [self.center[0],self.center[1]],
            "tile_list": self.tile_list,
            "wall_list": self.wall_list,
            "biome_name": self.biome_name
        }
    
    def add_tile(self, i:int, j:int):
        """TODO: Docstring
        """
        if [i,j] in self.tile_list:
            print(f"Tried to add tile at {i}, {j} to biome: {self.biome_name}, which already contains it")
        else:
            self.tile_list.append([i,j])

    def remove_tile(self, i:int, j:int) -> bool:
        """TODO: Docstring
        """
        try:
            self.tile_list.remove([i,j])
        except:
            print(f"Tried to remove tile at {i}, {j} not from the biome: {self.biome_name}")
            return False
        
class Mountain(Biome):
    """
    """

    IMPASS_COLOR = pygame.color.Color("white")
    FOOT_HILL_COLOR = pygame.color.Color("brown")

    tile_height_list: list
    endpoints: tuple

    def __init__(self) -> None:
        self.tile_height_list = [[]for i in range(0,10)]
        self.endpoints = None
        pass

    def make_range(self, start:tuple, end:tuple):
        # get slope
        if start[1] == end[1]:
            for i in range(start[0], end[0]):
                self.tile_height_list[9].append((i,start[1]))
        else:
            slope = (end[0]-start[0])/(end[1]-start[1])