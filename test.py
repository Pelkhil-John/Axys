import json
import pygame
import turret
import projectile

def encode(obj):
    if isinstance(obj, pygame.color.Color):
        return (obj.r, obj.g, obj.b, obj.a)
    raise TypeError(f'Object of type {obj.__class__.__name__} '
                    f'is not JSON serializable')

class Abstractclass():

    var: int
    tup: tuple
    color: pygame.color.Color

    def __init__(self) -> None:
        self.var = 1
        self.tup = (0,0)
        self.color = pygame.color.Color("green")
        pass
    
    def save(self):
        print("absclass save")

    def trial(self):
        self.save()

class Dude(Abstractclass):
    def __init__(self) -> None:
        super().__init__()

    def save(self):
        print("dude save")
        return super().save()
    

def main():
    dudeham = Dude()
    dudeham.trial()
    print(json.dumps(dudeham.__dict__, default=encode))

    turt = turret.Gunner((500,500))
    turt.make_surface()

    bul = projectile.Bullet(location=(0,0), size=(50,50))
    bul.location = (500, 50)

    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1000,1000))
    window.fill("black")
    pygame.display.update()

    while True:
        clock.tick(5)
        window.fill("black")
        turt.rotate(5)
        # bul.rotate(5)
        surf = turt.get_surface()
        window.blit(surf, (50,50))
        # window.blit(bul.surf, (500,50))
        pygame.display.update()

        if pygame.event.get(pygame.QUIT):
            pygame.quit()
            exit(0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            print("pressed a")

        if keys[pygame.K_b]:
            print("game pause")
            while True:
                if pygame.event.get(pygame.QUIT):
                    pygame.quit()
                    exit(0)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_n]:
                    print("unpause")
                    break


if __name__ == "__main__":
    main()