import pygame
import random

import utilities
import constants as c
import biomes
import nation


#TODO: map change update handling
#TODO: Biome coloring and non npc related Biomes


class Biome_tiles():
    """ This class stores all of the different biome and land control data from all of the different groups.
    """

    rect: pygame.rect.Rect
    color: pygame.color.Color
    name: str
    biome_type: str
    drawn: bool
    walkable: bool
    #TODO change this to a tuple please!
    index_i:int 
    index_j:int

    def __init__(self, index_i, index_j, rect=None, color="dark green", name=None, biome_type="plain") -> None:
        self.rect = rect
        #TODO: make this based off of the biome type
        self.color = color
        self.name = name
        self.biome_type = biome_type
        self.drawn = False
        self.walkable = True
        self.index_i = index_i
        self.index_j = index_j
    
    def load(self, save_dict):
        self.index_i = save_dict["index_i"]
        self.index_j = save_dict["index_j"]
        self.rect = utilities.rect_loader(save_dict["rect"])
        self.color = utilities.color_loader(save_dict["color"])
        self.name = save_dict["name"]
        self.walkable = save_dict["walkable"]
        self.biome_type = save_dict["biome_type"]

    def get_save_data(self) -> dict:
        return{
            "index_i": self.index_i,
            "index_j": self.index_j,
            "rect": utilities.rect_to_list(self.rect),
            "color": utilities.color_to_list(self.color),
            "name": self.name,
            "biome_type": self.biome_type,
            "walkable": self.walkable
        }


class Map:
    """ This class stores all of the different biome and land control data from all of the different groups.

    The different terains are stored as rectangles with a color and a name. 
    
    """
    biome_dict: dict
    tiles: list
    drawn: bool
    surface: pygame.surface.Surface

    def __init__(self) -> None:
        """
        """
        self.surface = None
        self.tiles = [[None for n in range(0,c.MAP_WIDTH)]for m in range(0,c.MAP_HEIGHT)]
        self.biome_dict = {}
        self.drawn = False

    def setup_new_map(self):
        self.set_up_tiles()
        self.set_up_biomes()
        self.make_fortresses()
        self.make_boundary()

    def set_up_tiles(self):
        for i in range(0,c.MAP_WIDTH):
            for j in range(0,c.MAP_HEIGHT):
                self.tiles[i][j] = Biome_tiles(i, j, pygame.rect.Rect(i*c.TILE_WIDTH, j*c.TILE_HEIGHT, c.TILE_WIDTH, c.TILE_HEIGHT))
                # TODO:Impliment render distance

    def set_up_biomes(self):
        for group in nation.nations_dict:
            self.biome_dict[group] = biomes.Principality(group, (random.randint(0,c.MAP_WIDTH)*c.TILE_WIDTH, random.randint(0,c.MAP_HEIGHT)*c.TILE_HEIGHT), 
                                                         color=group)

    def make_fortresses(self):
        for group in self.biome_dict:
            wall_list = self.biome_dict[group].make_wall(random.randint(c.TILE_WIDTH*4,c.TILE_WIDTH*10))
            for tup in wall_list[0]:
                # changes color of wall tiles
                self.tiles[tup[0]][tup[1]].biome_type = "wall"
                self.tiles[tup[0]][tup[1]].color = "black"
            for tup in wall_list[1]:
                #changes color of interior of wall tiles
                self.tiles[tup[0]][tup[1]].biome_type = "owned"
                self.tiles[tup[0]][tup[1]].color = self.biome_dict[group].color
                self.biome_dict[group].add_tile(tup[0], tup[1])

    def make_boundary(self):
        """ Make the map borders recommend using mountains to accomplish this
        """
        boarder = biomes.Mountain()
        boarder.make_range((0,0), (c.MAP_WIDTH-1,0))
        boarder.make_range((0,0), (0,c.MAP_HEIGHT-1))
        boarder.make_range((0,c.MAP_HEIGHT-1), (c.MAP_WIDTH-1, c.MAP_HEIGHT-1))
        boarder.make_range((c.MAP_WIDTH-1,0), (c.MAP_WIDTH-1, c.MAP_HEIGHT-1))
        self.biome_dict["boarder_mountains"] = boarder
        for tup in boarder.tile_height_list[-1]:
            self.tiles[tup[0]][tup[1]].biome_type = "mountain_peak"
            self.tiles[tup[0]][tup[1]].color = boarder.IMPASS_COLOR
            self.tiles[tup[0]][tup[1]].walkable = False
        for tup in boarder.tile_height_list[3]:
            self.tiles[tup[0]][tup[1]].biome_type = "mountain"
            self.tiles[tup[0]][tup[1]].color = "grey50"
            self.tiles[tup[0]][tup[1]].walkable = False
        for tup in boarder.tile_height_list[2]:
            self.tiles[tup[0]][tup[1]].biome_type = "hill"
            self.tiles[tup[0]][tup[1]].color = "grey80"
        for tup in boarder.tile_height_list[1]:
            self.tiles[tup[0]][tup[1]].biome_type = "foot_hill"
            self.tiles[tup[0]][tup[1]].color = "grey100"
        for tup in boarder.tile_height_list[0]:
            self.tiles[tup[0]][tup[1]].biome_type = "foot_hill"
            self.tiles[tup[0]][tup[1]].color = "green"

    def load(self, save_dict):
        for biome_name in save_dict["biomes"]:
            self.biome_dict[biome_name] = biomes.Biome()
            self.biome_dict[biome_name].load(save_dict["biomes"][biome_name])    
            pass
        self.tiles = []
        index = 0
        for tile_collum in save_dict["tiles"]:
            self.tiles.append([])
            for tile_dict in tile_collum:
                self.tiles[index].append(Biome_tiles(0,0))
                self.tiles[index][-1].load(tile_dict)
            index += 1
        self.get_surface()

    def get(self, variable):
        """
        """
        if variable == "biomes":
            temp_dict = {}
            for biome in self.biome_dict:
                temp_dict[biome] = self.biome_dict[biome].get_save_data({})
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
                    self.tiles[k][l].drawn = True
        elif not self.drawn:
            #TODO find a way to do this without looping through all of the lists, maybe storing a reference to the tile that needs to be drawn
            for k in range(0, c.MAP_WIDTH):
                for l in range(0,c.MAP_HEIGHT):
                    if not self.tiles[k][l].drawn:
                        pygame.draw.rect(self.surface, self.tiles[k][l].color, self.tiles[k][l].rect)
                        self.tiles[k][l].drawn = True
        self.drawn = True
        return self.surface
    
    def save(self, save_dict:dict) -> dict:
        """TODO: docstring
        """
        for variable in save_dict:
            save_dict[variable] = self.get(variable)
        return save_dict
