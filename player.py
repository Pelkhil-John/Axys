import pygame
import utilities
import constants as c

class Player(pygame.sprite.Sprite):
    """
    """

    rect: pygame.rect.Rect
    color: pygame.Color
    on_screen: bool
    health: int
    mana: int
    defence: int
    power: int
    experience: int
    level: int
    class_type: str
    #location stores the reletive position of the player within the game context as a tuple (x, y, z)
    location: tuple
    map_rect: pygame.rect.Rect
    ref_x: int
    ref_y: int

    

    def __init__(self, rect, *groups):
        self.rect = rect
        self.color = pygame.color.Color("blue")
        self.on_screen = True
        self.health = 100
        self.mana = 10
        self.defence = 0
        self.power = 1
        self.experience = 0
        self.level = 0
        self.class_type = "none"
        self.location = ((c.MAP_WIDTH*c.TILE_WIDTH)/2, -(c.MAP_HEIGHT*c.TILE_HEIGHT)/2)
        self.map_rect = pygame.rect.Rect((c.MAP_WIDTH*c.TILE_WIDTH)/2-c.PLAYER_WIDTH/2, (c.MAP_HEIGHT*c.TILE_HEIGHT)/2-c.PLAYER_HEIGHT/2, c.PLAYER_WIDTH, c.PLAYER_HEIGHT)
        self.ref_x = 0
        self.ref_y = 0

    def load(self, save_dict):
        """
        """
        #TODO: add tryblocks to prevent save corruption
        self.rect = utilities.rect_loader(save_dict["rect"])
        self.map_rect = utilities.rect_loader(save_dict["map_rect"])
        self.color = utilities.color_loader(save_dict["color"])
        self.on_screen = save_dict["on_screen"]
        self.health = save_dict["health"]
        self.mana = save_dict["mana"]
        self.defence = save_dict["defence"]
        self.power = save_dict["power"]
        self.experience = save_dict["experience"]
        self.level = save_dict["level"]
        self.ref_x = save_dict["ref_x"]
        self.ref_y = save_dict["ref_y"]


    def get_location_index(self, x_offset, y_offset):
        return (int((self.map_rect.x + x_offset) // c.TILE_WIDTH), int((self.map_rect.y + y_offset) // c.TILE_WIDTH))

        
    def get(self, variable):
        # pygame.Rect, string cast does not play nice with json so this fixes it
        if (variable == "rect"):
            return utilities.rect_to_list(self.rect)
        if (variable == "color"):
            return utilities.color_to_list(self.color)
        if (variable == "map_rect"):
            return utilities.rect_to_list(self.map_rect)
        return eval(variable, globals(), self.__dict__)

    def save(self, save_dict) -> dict:
        for variable in save_dict:
            save_dict[variable] = self.get(variable)
        return save_dict