import pygame
import random

import utilities
import constants as c
import biomes
from constants import Identity


#TODO: add save functionallity
#TODO: map change update handling
#TODO: Biome coloring and non npc related Biomes



class Biome_tiles():
    """ This class stores all of the different biome and land control data from all of the different groups.
    """

    rect: pygame.rect.Rect
    color: pygame.color.Color
    name: str
    biome_type: str
    index_i:int 
    index_j:int

    def __init__(self, index_i, index_j, rect=None, color="dark green", name=None, biome_type="plain") -> None:
        self.rect = rect
        #TODO: make this based off of the biome type
        # self.color = pygame.color.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = color
        self.name = name
        self.biome_type = biome_type
        self.index_i = index_i
        self.index_j = index_j
    
    def load(self, save_dict):
        self.index_i = save_dict["index_i"]
        self.index_j = save_dict["index_j"]
        self.rect = utilities.rect_loader(save_dict["rect"])
        self.color = utilities.color_loader(save_dict["color"])
        self.name = save_dict["name"]
        self.biome_type = save_dict["biome_type"]

    def get_save_data(self) -> dict:
        rect_list = [self.rect.x, self.rect.y, self.rect.w, self.rect.h]
        if isinstance(self.color, tuple):
            #color could be stored in two types, either a tuple of len 3 or 4
            color_list = list(self.color)
        else: 
            # or as string, and we can't put tuples in .json files
            color_list = self.color
        return{
            "index_i": self.index_i,
            "index_j": self.index_j,
            "rect": rect_list,
            "color": color_list,
            "name": self.name,
            "biome_type": self.biome_type,
        }


class Map:
    """ This class stores all of the different biome and land control data from all of the different groups.

    The different terains are stored as rectangles with a color and a name. 
    
    """
    biome_dict: dict
    tiles: list
    surface: pygame.surface.Surface

    def __init__(self) -> None:
        """
        """
        self.surface = None
        self.tiles = [[None for n in range(0,c.MAP_WIDTH)]for m in range(0,c.MAP_HEIGHT)]
        self.set_up_tiles()
        self.biome_dict = {}
        self.set_up_biomes()
        # self.make_boundary()
        self.make_fortresses()

    def set_up_tiles(self):
        for i in range(0,c.MAP_WIDTH):
            for j in range(0,c.MAP_HEIGHT):
                self.tiles[i][j] = Biome_tiles(i, j, pygame.rect.Rect(i*c.TILE_WIDTH, j*c.TILE_HEIGHT, c.TILE_WIDTH, c.TILE_HEIGHT))
                # TODO:Impliment render distance
        #DEBUG START
        # i,j = 0,0
        # for lst in self.tiles:
        #     i += 1
        #     j = 0
        #     for tile in lst:
        #         j+= 1
        #         if isinstance(tile, None):
        #             print(f"found NoneType at {i}, {j}")
        #DEBUG END


    def set_up_biomes(self):
        # TODO: this needs to use the other types of biomes
        for group in ["red", "white", "blue", "green", "black","yellow"]:
            self.biome_dict[group] = biomes.Biome((random.randint(0,c.MAP_WIDTH)*c.TILE_WIDTH, random.randint(0,c.MAP_HEIGHT)*c.TILE_HEIGHT), color=group)

    def make_fortresses(self):
        for group in self.biome_dict:
            wall_list = self.biome_dict[group].make_wall(random.randint(c.TILE_WIDTH*4,c.TILE_WIDTH*10))
            for tup in wall_list[0]:
                # changes color of wall tiles
                self.tiles[tup[0]][tup[1]].color = "black"
            for tup in wall_list[1]:
                #changes color of interior of wall tiles
                self.tiles[tup[0]][tup[1]].color = self.biome_dict[group].color
                self.biome_dict[group].add_tile(tup[0], tup[1])



    def make_boundary():
        """ Make the map borders recommend using mountains to accomplish this
        """
        pass

###########################################################################
    def load(self, save_dict):
        for biome_name in save_dict["biomes"]:
            #TODO FINISH THIS
            pass
        for tile_collum in save_dict["tiles"]:
            index = 0
            self.tiles.append([])
            for tile_dict in tile_collum:
                self.tiles[index].append(Biome_tiles(0,0).load(tile_dict))
                index += 1
#########################################################################
    def get(self, variable):
        """
        """
        if variable == "biomes":
            temp_dict = {}
            for biome in self.biome_dict:
                temp_dict[biome] = self.biome_dict[biome].get_save_data()
            return temp_dict
        elif variable == "tiles":
            temp_list = []
            for tile_row in self.tiles:
                temp_collum = []
                for tile in tile_row:
                    temp_collum.append(tile.get_save_data())
                temp_list.append(temp_collum)
            return temp_list
        else:
            return eval(variable, globals(), self.__dict__)
    

    
    def get_surface(self)-> pygame.surface.Surface:
        """TODO: docstring
        """
        if self.surface == None:
            self.surface = pygame.surface.Surface((c.MAP_WIDTH*c.TILE_WIDTH, c.MAP_HEIGHT*c.TILE_HEIGHT))
            for k in range(0, c.MAP_WIDTH):
                for l in range(0,c.MAP_HEIGHT):
                    pygame.draw.rect(self.surface, self.tiles[k][l].color, self.tiles[k][l].rect)
        return self.surface
    
    def save(self, save_dict:dict) -> dict:
        """TODO: docstring
        """
        for variable in save_dict:
            save_dict[variable] = self.get(variable)
        return save_dict
        

    
