import pygame
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

    def __init__(self, rect:pygame.rect.Rect=None, location:tuple[int, int]=(0,0), size:tuple[int, int]=(c.TILE_WIDTH, c.TILE_HEIGHT//2), *groups) -> None:
        if rect:
            self.rect = rect
            self.location = rect.topleft()
            self.size = rect.size
        else:
            self.rect = pygame.rect.Rect(location, size)       
            self.size = size
            self.location = location      
        super().__init__(*groups)
        self.make_surf()

    def make_surf(self):
        # self.surf = pygame.surface.Surface(self.rect.size*2, pygame.SRCALPHA)
        self.bullet_surf = pygame.surface.Surface((self.rect.w*2, self.rect.h*2))
        self.surf = pygame.surface.Surface((self.rect.w*2, self.rect.h*2), pygame.SRCALPHA)
        pygame.draw.rect(self.surf, (255,20,10), ((0,0), self.size), 
                         border_top_left_radius=self.size[0]//2, border_top_right_radius=self.size[0]//2)
        self.bullet_surf_rect = self.bullet_surf.get_rect()
        self.rotate(0)

    def rotate(self, amount):
        self.direction = self.direction + amount % 360
        temp_surf = self.bullet_surf.copy()
        self.bullet_surf = pygame.transform.rotate(self.bullet_surf, self.direction)
        self.bullet_surf_rect = self.bullet_surf.get_rect()
        self.bullet_surf_rect.center = temp_surf.get_rect().center
        self.surf.fill((0,0,0,0))
        self.surf.blit(self.bullet_surf, self.bullet_surf_rect)
        

    