import pygame
import constants as c
import projectile as p

class AbstractTurret():
    
    modules: list
    location: tuple
    surface: pygame.surface.Surface
    projectile: p.AbstractProjectile 

    def __init__(self, location:tuple, surface: pygame.surface.Surface=None, projectile:p.AbstractProjectile=None):
        self.modules = []
        self.location = location
        self.surface = surface
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


class Gunner(AbstractTurret):

    facing: float
    color: pygame.color.Color
    last_surf: pygame.surface.Surface
    base: pygame.surface.Surface
    head: pygame.surface.Surface
    turned_head: pygame.surface.Surface
    turned_head_rect: pygame.rect.Rect
    

    def __init__(self, location: tuple, color="green", surface: pygame.Surface = None, projectile: p.AbstractProjectile = None):
        self.color = pygame.color.Color(color)
        self.facing = 0.0
        self.turned_head = pygame.surface.Surface((4* c.TILE_WIDTH, 4* c.TILE_HEIGHT))
        self.last_surf = pygame.surface.Surface((4* c.TILE_WIDTH, 4* c.TILE_HEIGHT))
        super().__init__(location, surface, projectile)

    def make_surface(self):
        #base
        self.base = pygame.surface.Surface((4* c.TILE_WIDTH, 4* c.TILE_HEIGHT))
        base_rect = pygame.rect.Rect(c.TILE_WIDTH, c.TILE_HEIGHT, 2* c.TILE_WIDTH, 2* c.TILE_HEIGHT)
        pygame.draw.rect(self.base, "grey48", base_rect)
        pygame.draw.circle(self.base, self.color, (2* c.TILE_WIDTH, 2* c.TILE_HEIGHT), c.TILE_WIDTH*5/7)
        #head
        self.head = pygame.surface.Surface((4* c.TILE_WIDTH, 4* c.TILE_HEIGHT), pygame.SRCALPHA)
        head_rect = pygame.rect.Rect(3* c.TILE_WIDTH/2, 0, c.TILE_WIDTH, 4*c.TILE_HEIGHT*2/3)
        pygame.draw. rect(self.head, "white", head_rect, 
                          border_top_left_radius=c.TILE_WIDTH//2, border_top_right_radius=c.TILE_WIDTH//2,
                          border_bottom_left_radius=c.TILE_WIDTH//3, border_bottom_right_radius=c.TILE_WIDTH//3)
        
    def rotate(self, amount:float):
        self.facing = self.facing + amount % 360
        temp_surf = self.head.copy()
        self.turned_head = pygame.transform.rotate(self.head, self.facing)
        self.turned_head_rect = self.turned_head.get_rect()
        self.turned_head_rect.center = (2* c.TILE_WIDTH, 2* c.TILE_HEIGHT)
        self.head = temp_surf

    def get_surface(self) -> pygame.surface.Surface:
        self.last_surf.blit(self.base, (0,0))
        self.last_surf.blit(self.turned_head, self.turned_head_rect)
        return self.last_surf


    




        
