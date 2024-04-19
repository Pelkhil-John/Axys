import pygame
import math
import json
import os


import constants as c
import utilities
import npc
import map
import player as plr



game_map: map.Map
player: plr.Player
window: pygame.surface.Surface
clock: pygame.time.Clock

pygame.init()


    

def draw():
    """ Used to handle graphics to the screen. Drawn once per tick
    
    :param player (pygame.sprit.Sprite):
    """
    window.fill("red")
    window.blit(game_map.get_surface(), (player.ref_x-c.MAP_WIDTH/2, player.ref_y-c.MAP_HEIGHT/2))
    pygame.draw.rect(window, "blue", player.rect)    
    pygame.display.update()


def update_position(vel_x, vel_y):
    #TODO: handle this using the groups provided by pygame
    global player
    if player.rect.x + vel_x < c.WIDTH/10:
        player.ref_x -= vel_x
    elif player.rect.x + vel_x > c.WIDTH * 9/10:
        player.ref_x -= vel_x
    else:
        player.rect.x += vel_x
    if player.rect.y + vel_y < c.HEIGHT/10:
        player.ref_y -= vel_y
    elif player.rect.y + vel_y > c.HEIGHT * 9/10:
        player.ref_y -= vel_y
    else:
        player.rect.y += vel_y

def save():
    """ save the current game data

    TODO: impliment multiple saves
    """
    print("Saving Data:")
    utilities.save_to(utilities.get_player_data_dict, player.save, "player_save")
    utilities.save_to(utilities.get_map_data_dict, game_map.save, "map_save")
    c.npc.update("save", utilities.get_npc_data_dict)
    # utilities.save_to({"npc_save": npc.AbstractNPC.npc_save_list}, utilities.bounce, "npc_save")
    utilities.save_to(npc.AbstractNPC.get_npc_save_list, dict, "npc_save")



def load_saves():
    print("Save Loaded")
    global player, game_map
    #make player object with the needed rect pass

    #TODO: put these in the util file to match the functionality of save
    player = plr.Player(None)
    with open("saves/player_save.json", "r") as player_save:
        player.load(json.load(player_save))
        player_save.close()
    game_map = map.Map()
    with open("saves/map_save.json", "r") as map_save:
        game_map.load(json.load(map_save))
        map_save.close()
    # for file in os.listdir("saves"):
    #     if file != "player_save.json" and file != "map_save.json" and not os.path.isfile(file):
    #         with open(f"saves/{file}", "r") as npc_save:
    #             #change this so the loaded npc is not always a Combatant
    #             npc_obj = npc.Combatant(None)
    #             npc_obj.load(json.load(npc_save))
    #             c.npc.append(npc_obj)
    #             npc_save.close()

def new_save():
    global game_map, player
    print("Load New Save")
    player = plr.Player(pygame.Rect(c.WIDTH/2 - c.PLAYER_WIDTH/2, c.HEIGHT/2 - c.PLAYER_HEIGHT/2, c.PLAYER_WIDTH, c.PLAYER_HEIGHT))
    game_map = map.Map()
    game_map.setup_new_map()


def check_for_save() -> bool :
    for file in os.listdir():
        if os.path.isdir(file) and file == "saves":
            #TODO: check for actual old saves, not just for the folder
            return True
    return False


def title_screen_loop():
    global window

    title_font = pygame.font.SysFont("Garamond", 80)
    new_game_button_color = "gray"
    new_game_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/3 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
    new_game_button_text = utilities.get_text_surface("New Game")
    is_save = check_for_save()
    load_save_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/3*2 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
    load_save_button_text = utilities.get_text_surface("Load Save")
    if is_save:
        load_save_button_color = "gray"
    else:
        load_save_button_color = "gray16"
    while True:
        clock.tick(60)
        mouse_pos= pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F11]:
            window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        if is_save:
            if load_save_button_rect.collidepoint(*mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    load_saves()
                    break
                load_save_button_color = "gray69"
            else:
                load_save_button_color = "gray"
        if new_game_button_rect.collidepoint(*mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                new_save()
                break
            new_game_button_color = "gray69"
        else:
            new_game_button_color = "gray"
        window.fill("black")
        window.blit(utilities.get_text_surface("Coding Club Example", title_font), (c.WIDTH/2 - 300, c.HEIGHT/10))
        pygame.draw.rect(window, new_game_button_color, new_game_button_rect)
        window.blit(new_game_button_text, (new_game_button_rect.x + 10, new_game_button_rect.y + 10))
        pygame.draw.rect(window, load_save_button_color, load_save_button_rect)
        window.blit(load_save_button_text, (load_save_button_rect.x + 10, load_save_button_rect.y + 10))
        pygame.display.update()
    


def main():
    """ main function, 
    this is where we control things and call all of the stuff we want to happen in the game
    
    """
    
    title_screen_loop() 
    running = True
    while running:
        #Sets the Max c.FPS for the game to run at
        clock.tick(c.FPS)
        
        keys = pygame.key.get_pressed()
        events = pygame.event.get(eventtype=[pygame.QUIT, pygame.KEYUP])
        vel_x, vel_y = 0, 0




        # Checks which keys are pressed sets the movement accordingly
        if keys[pygame.K_a]:
            vel_x -= c.MAX_VEL
        if keys[pygame.K_d]:
            vel_x += c.MAX_VEL
        if keys[pygame.K_s]:
            vel_y += c.MAX_VEL
        if keys[pygame.K_w]:
            vel_y -= c.MAX_VEL
        
        # Normalize the speed so the player doesn't move faster when going diagonal
        if math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)) > c.MAX_VEL:
            vel_x, vel_y = vel_x/math.sqrt(2), vel_y/math.sqrt(2)
        update_position(vel_x, vel_y)
        draw()


        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    print("pause")
                    while pause:
                        if pygame.event.get(pygame.QUIT):
                            #TODO: add if player is loaded to prevent unnecisary saves (maybe never mind)
                            save()
                            pygame.quit()
                            exit(0)
                        #PAUSE MENU, WITH CLOSE FUNCTION
                        for event in pygame.event.get(pygame.KEYUP):
                            if event.key == pygame.K_ESCAPE:
                                pause = False
                    print("unpause")
            if event.type == pygame.QUIT:
                save()
                running = False

    pygame.quit()


def startup():
    #check load formatting: TODO
    global window, clock
    c.setup()
    os.chdir(c.PTWD)

    window = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption(c.NAME)
    print("Finish Startup")
    pass


if __name__ == "__main__":
    startup()
    main()

