import pygame
import math
import constants as c

class AbstractProjectile(pygame.sprite.Sprite):

    size: tuple
    location: tuple

    rect: pygame.rect.Rect
    surf: pygame.surface.Surface
    direction: int

    def __init__(self, *groups) -> None:
        self.surf = None
        self.direction = 0
        super().__init__(*groups)


class Bullet(AbstractProjectile):

    bullet_surf: pygame.surface.Surface
    bullet_surf_rect: pygame.rect.Rect

    bullets_list:list

    memory: list

    #FIXME: location and size are being used wrong here!!!

    def __init__(self, location:tuple[int, int]=(0,0), size:tuple[int, int]=(c.TILE_WIDTH, c.TILE_HEIGHT//2), *groups) -> None:
        self.rect = None      
        self.size = size
        self.location = location
        self.memory = [None for _ in range(360)]
        self.bullets_list = []
        super().__init__(*groups)
        self.make_surf()

    def make_surf(self):
        self.bullet_surf = pygame.surface.Surface(self.size, pygame.SRCALPHA)

        self.surf = pygame.surface.Surface((max(self.size)*2, max(self.size)*2), pygame.SRCALPHA)

        pygame.draw.rect(self.bullet_surf, (255,20,10), ((0,0), self.size), 
                         border_top_left_radius=self.size[0]//2, border_top_right_radius=self.size[0]//2)
        
        self.bullet_surf_rect = self.bullet_surf.get_rect()

        for dir in range(360):
            self.rotate(1)
            self.memory[(dir+91) % 360] = self.surf


    def rotate(self, amount):
        self.direction = self.direction + amount % 360
        temp_surf = self.bullet_surf.copy()

        self.bullet_surf = pygame.transform.rotate(self.bullet_surf, self.direction)
        self.bullet_surf_rect = self.bullet_surf.get_rect()
        self.bullet_surf_rect.center = self.surf.get_rect().center

        self.surf.fill((0,0,0,0))
        self.surf.blit(self.bullet_surf, self.bullet_surf_rect)

        self.bullet_surf = temp_surf
        
    def fire(self, dir: int, vel, b_range, origin:tuple=None):
        if not origin:
            origin = self.location
        self.bullets_list.append([dir, (origin[0]+(vel*math.cos(math.radians(dir))), origin[1] - (vel*math.sin(math.radians(dir)))), 
                                  vel, 0, b_range, self.memory[dir].copy()])

    def tick(self):
        for bul in self.bullets_list:
            if bul[3] > bul[4]:
                self.bullets_list.remove(bul)
                continue
            bul[1] = (bul[1][0] + (bul[2]*math.cos(math.radians(bul[0]))), bul[1][1] - (bul[2]*math.sin(math.radians(bul[0]))))
            bul[3] += bul[2]