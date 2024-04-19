import pygame
import math

import constants as c
from constants import Identity
import utilities
import nation



class Biome:
    """
    
    """

    drawn = False

    # REMINDER: Update the save funciton with any new data 
    owner_name: str
    color: pygame.color.Color
    center: tuple
    walkable: bool
    tile_list: list             #Stores indexes of the members
    biome_name: str
    
    def __init__(self, center=(0,0), owner_name=None, color="grey", biome_name=""):
        self.color = color
        self.center = center
        self.biome_name = biome_name
        self.tile_list = []
        self.owner_name = owner_name


    def find_owner(self) -> str:
        """
        """
        # TODO Testing
        if isinstance(self.owner, pygame.sprite.Group):
            for sprite in self.owner:
                if isinstance(sprite, Identity):
                    return sprite.group_name
        return ""        
    

    def get_save_data(self, save_dict) -> dict:
        
        save_dict["owner_name"]    = self.owner_name
        save_dict["color"]         = utilities.color_to_list(self.color)
        save_dict["center"]        = [self.center[0],self.center[1]]
        save_dict["tile_list"]     = self.tile_list
        save_dict["biome_name"]    = self.biome_name
        
        return save_dict
    
    def add_tile(self, i:int, j:int):
        #TODO: Docstring
        if [i,j] in self.tile_list:
            print(f"Tried to add tile at {i}, {j} to biome: {self.biome_name}, which already contains it")
        else:
            self.tile_list.append([i,j])

    def remove_tile(self, i:int, j:int) -> bool:
        #TODO: Docstring
        try:
            self.tile_list.remove([i,j])
        except:
            print(f"Tried to remove tile at {i}, {j} not from the biome: {self.biome_name}")
            return False
        
    def load(self, save_dict):
        #TODO finsih implimennting
        self.owner_name = save_dict["owner_name"]
        self.biome_name = save_dict["biome_name"]
        self.center = tuple(save_dict["center"])
        self.color = utilities.color_loader(save_dict["color"])
        self.tile_list = save_dict["tile_list"]
        
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
        super().__init__(biome_name="mountain")
        pass

    def make_range(self, start:tuple, end:tuple):
        # get slope
        if start[0] == end[0]:
            #catch a possible infinite slope issue
            for i in range(start[1], end[1]+1):
                self.tile_height_list[-1].append((start[0],i))
        else:
            slope = (end[1]-start[1])/(end[0]-start[0])
            for i in range(start[0], end[0]+1):
                self.tile_height_list[-1].append((i, int(i*slope) + start[1]))
        #TODO: figure out how to make this mountains blend into foothills

    def get(self, variable:str):
        if variable == "endpoints":
            #TODO finish
            return "TODO"
        if variable == "tile_height_list":
            #TODO finish
            return "TODO"
        return eval(globals(), self.__dict__)

    def get_save_data(self) -> dict:
        save_dict = {}
        save_dict["endpoints"] = self.get("endpoints")
        save_dict["tile_height_list"] = self.get("tile_height_list")
        return super().get_save_data(save_dict)
    
    def load(self, save_dict):
        self.endpoints = save_dict["endpoints"]
        self.tile_height_list = save_dict["tile_height_list"]
        super().load(save_dict)

class Principality(Biome):
    """
    """

    wall_list: list
    wall_radius: int

    def __init__(self, owner_name:str, center=None, color="grey", biome_name=""):
        nation.nations_dict[owner_name].owned_biomes.append(self)
        super().__init__(center, owner_name, color, biome_name)

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
    
    def get(self, variable:str):
        if variable == "wall_list":
            #TODO finish
            return "TODO"
        if variable == "wall_radius":
            #TODO finish
            return "TODO"
        return eval(globals(), self.__dict__)

    def get_save_data(self) -> dict:
        save_dict = {}
        save_dict["wall_list"] = self.get("wall_list")
        save_dict["wall_radius"] = self.get("wall_radius")
        return super().get_save_data(save_dict)
    
    def load(self, save_dict):
        self.wall_list = save_dict["wall_list"]
        self.wall_radius = save_dict["wall_radius"]
        super().load(save_dict)