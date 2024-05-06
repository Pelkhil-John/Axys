import pygame
import utilities as u
import constants as c
import projectile as p

class AbstractTurret():
    
    modules: list
    location: tuple

    surf: pygame.surface.Surface
    projectile: p.AbstractProjectile 

    def __init__(self, location:tuple, surface: pygame.surface.Surface=None, projectile:p.AbstractProjectile=None):
        self.modules = []
        self.location = location
        self.projectile = projectile
    
    def get_save_data(self) -> dict:
        return {
            "modules": self.modules,
            "location": self.location,
            "projectile_type": self.projectile.type_name()
        }
    
    def load(self, save_dict:dict):
        self.modules = save_dict["modules"]
        self.location = tuple(save_dict["location"])
        self.projectile = p.get_loader(save_dict["projectile_type"])

    ###################################-----------------------TURRET SPECIFIC---------------------------#######################################


    def fire(self): ...

    def copy(self): ...        


    ###################################----------------------MODULES-----------------------------------#######################################
    detetction_range = 10

    def detetction(self, target:pygame.rect.Rect):
        if u.get_distance(self.location, target.center) < self.detection_range:
            return True
        pass

    def auto_fire(self):
        self.fire()
    
    def auto_rotate(self):
        self.rotate(1)
        

class Gunner(AbstractTurret):


    BASE_SCALE = 2
    BASE_COLOR_RADIUS_SCALE = 4/5
    HEAD_WIDTH_SCALE = 1
    HEAD_COLOR = pygame.color.Color("gold")
    BASE_COLOR = pygame.color.Color("grey48") 

    ###################################-----------------------STATUS-----------------------------###########################################

    facing: float
    color: pygame.color.Color
    since_fire: int

    ###################################-----------------------VISUALS-----------------------------###########################################

    base: pygame.surface.Surface
    head: pygame.surface.Surface
    turned_head_surf: pygame.surface.Surface
    turned_head_rect: pygame.rect.Rect
    memory: list
    
    ##################################---------------------ATTRIBUTES------------------------------##########################################

    rotation_speed: int
    rate_of_fire: int

    ###################################-----------------------SETTUP-----------------------------###########################################


    def __init__(self, location: tuple, color="green", surface: pygame.Surface = None, projectile: p.AbstractProjectile = None):
        self.color = pygame.color.Color(color)
        self.facing = 0.0
        self.surf = pygame.surface.Surface((2* Gunner.BASE_SCALE * c.TILE_WIDTH, 2* Gunner.BASE_SCALE * c.TILE_HEIGHT), pygame.SRCALPHA)
        self.turned_head_surf = self.surf.copy()
        self.memory = [None for _ in range(360)]
        self.since_fire = 0
        self.rate_of_fire = 20
        super().__init__(location, surface, projectile)
        self.location = (self.location[0] - self.surf.get_rect().w//2 , self.location[1] - self.surf.get_rect().h//2)
        self.make_surface()

    def make_surface(self):
        #base
        self.base = self.surf.copy()
        base_rect = pygame.rect.Rect(c.TILE_WIDTH, c.TILE_HEIGHT, Gunner.BASE_SCALE * c.TILE_WIDTH, Gunner.BASE_SCALE * c.TILE_HEIGHT)
        pygame.draw.rect(self.base, Gunner.BASE_COLOR, base_rect)
        pygame.draw.circle(self.base, self.color, (Gunner.BASE_SCALE * c.TILE_WIDTH, Gunner.BASE_SCALE * c.TILE_HEIGHT), Gunner.BASE_COLOR_RADIUS_SCALE * c.TILE_WIDTH)
        #head
        self.head = self.surf.copy()
        head_rect = pygame.rect.Rect(base_rect.w * 3/4, 0, base_rect.w/2, Gunner.BASE_SCALE * base_rect.h * 2/3)
        pygame.draw.rect(self.head, Gunner.HEAD_COLOR, head_rect, 
                          border_top_left_radius=c.TILE_WIDTH//2, border_top_right_radius=c.TILE_WIDTH//2,
                          border_bottom_left_radius=c.TILE_WIDTH//3, border_bottom_right_radius=c.TILE_WIDTH//3)
        for rot in range(360):
            self.rotate(1)
    
###################################-----------------------ACTIONS-----------------------------###########################################


    def rotate(self, amount):
        self.facing = int((self.facing + amount) % 360)
        if self.memory and self.memory[(self.facing + 90)%360]:
            self.surf = self.memory[self.facing]
            return
        temp_surf = self.head.copy()
        self.turned_head_surf = pygame.transform.rotate(self.head, self.facing)
        self.turned_head_rect = self.turned_head_surf.get_rect()
        self.turned_head_rect.center = self.surf.get_rect().center
        self.head = temp_surf

        self.surf.fill((0,0,0,0))
        self.surf.blit(self.base, (0,0))
        self.surf.blit(self.turned_head_surf, self.turned_head_rect)

        self.memory[(self.facing + 90) % 360] = self.surf.copy()


    def rotate_to(self, theta):
        if self.memory[theta]:
            self.facing = theta
            self.surf = self.memory[theta]
        else:
            self.rotate(self.facing - theta)

    def fire(self):
        if self.since_fire == 0:
            #TODO: code in custom bullet speed
            self.projectile.fire(self.facing, 5, 300)
            self.since_fire = self.rate_of_fire
        
###################################-----------------------UTILS-----------------------------###########################################


    def get_surface(self) -> pygame.surface.Surface:
        self.surf.fill((0,0,0,0))
        self.surf.blit(self.base, (0,0))
        self.surf.blit(self.turned_head_surf, self.turned_head_rect)
        return self.surf
    
    def get_projectile_list(self) -> list:
        return [[item[-1], item[1]] for item in self.projectile.bullets_list]

    def tick(self):
        self.projectile.tick()
        if self.since_fire > 0:
            self.since_fire -= 1
    
    def copy(self):
        temp_turret = Gunner(self.location, self.color)
        temp_turret.memory = self.memory
        return temp_turret


    




        
