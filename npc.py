import pygame
import json
import constants as c
import utilities


class AbstractNPC(pygame.sprite.Sprite):
    """
    Abstract class for any non-player characters
    used to give consistancy of how sprites should be handled in this game
    """
    rect: pygame.rect.Rect
    color: pygame.Color
    on_screen: bool
    health: int
    mana: int
    defence: int
    power: int
    class_type: str
    
    def __init__(self, rect, *groups):
        super().__init__(*groups)
        self.rect = rect
        self.on_screen = self.check_on_screen()
        self.add(c.npc)

    def change_group(self, old_group, new_group):
        """ used to do both remove and add groups in one method

        :param old_group: group whicht the NPC belongs to and needs to be removed from
        :param new_group: group to be added
        """
        self.remove(old_group)
        self.add(new_group)
    
    def move(self, velx, vely):
        """
        Takes in intended motion for each NPC and updates its postion
        NO CHECKING DONE AT THIS LEVEL

        :param velx: motion in the x direction
        :param vely: motion in the y direction
        """
        self.x += velx
        self.y += vely
    
    def save(self, save_dict) -> dict:
        # TODO: this save process needs to be standardized
        for variable in save_dict:
            save_dict[variable] = self.get(variable)
        return save_dict
    
    def get(self, variable):
        """TO BE OVERRIDEN IN EACH NPC CLASS
        
        """
        return eval(variable, globals(), self.__dict__)
        

    # check if the edges of the rectangle representing this NPC is on the screen, stored in a bool for all NPCs
    def check_on_screen(self):
        
        self.on_screen = not(self.rect.right < 0 
                             or self.rect.left > c.WIDTH 
                             or self.rect.bottom < 0 
                             or self.rect.top > c.HEIGHT)
        
    def load(self, save_dict):
        """
        
        TODO: add tryblocks to prevent save corruption
        """
        self.rect = utilities.rect_loader(save_dict["rect"])
        self.color = utilities.color_loader(save_dict["color"])
        self.on_screen = save_dict["on_screen"]
        self.health = save_dict["health"]
        self.mana = save_dict["mana"]
        self.defence = save_dict["defence"]
        self.power = save_dict["power"]
        self.class_type = save_dict["class_type"]

        
    def get(self, variable):
        # pygame.Rect, string cast does not play nice with json so this fixes it
        # TODO: figure out how to do this with proper overrides ANS: copy the load functionallity
        print(variable)
        if (variable == "rect"):
            return [self.rect.left, self.rect.top, self.rect.width, self.rect.height]
        if (variable == "color"):
            return [self.color.r, self.color.g, self.color.b]
        return eval(variable, globals(), self.__dict__)


class Combatant(AbstractNPC):
    """
    """
    def __init__(self, rect=None, x=c.WIDTH/2, y=c.HEIGHT/2, width=c.NPC_WIDTH, height=c.NPC_HEIGHT, *groups):
        if rect:
            super().__init__(rect, *groups)
        else:
            super().__init__(pygame.Rect(x, y, width, height), *groups)

    def load(self, save_dict):
        super().load(save_dict)
        #put extra loads here per class
    

class Civilian(AbstractNPC):
    """
    """
    def __init__(self, rect=None,  x=c.WIDTH/2, y=c.HEIGHT/2, width=c.NPC_WIDTH, height=c.NPC_HEIGHT, *groups):
        if rect:
            super().__init__(rect, *groups)
        else:
            super().__init__(pygame.Rect(x, y, width, height), *groups)
    

    def load(self, save_dict):
        super().load(save_dict)
        #put extra loads here
    


# class Soldier(pygame.sprite.Sprite):

#     def __init__(self, x, y, width, height, color):
#         super.__init__()
#         self.rect = pygame.Rect(x,y,width,height)
#         self.color = color
#         self.x_ind_vel = 0
#         self.y_ind_vel = 0
#         self.direction = 0
#         self.health = 1
#         self.mask = None

