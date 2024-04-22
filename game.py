import pygame
import math
import json
import os

import constants as c
import utilities
import npc
import map as mp
import player as plr

map: mp.Map
player: plr.Player
window: pygame.surface.Surface
clock: pygame.time.Clock

pygame.init()


def draw():
    """ Used to handle graphics to the screen. Drawn once per tick
    
    """
    window.fill("black")
    window.blit(map.get_surface(), (player.ref_x-(c.MAP_WIDTH*c.TILE_WIDTH- c.WIDTH)/2, player.ref_y-(c.MAP_HEIGHT*c.TILE_HEIGHT-c.HEIGHT)/2))
    pygame.draw.rect(window, "blue", player.rect)    
    pygame.display.update()


def update_position():
    #TODO: handle this using the groups provided by pygame
    global player
    player.map_rect.x += vel_x
    player.map_rect.y += vel_y
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
    utilities.save_to(utilities.get_map_data_dict, map.save, "map_save")
    c.npc.update("save", utilities.get_npc_data_dict)
    # utilities.save_to({"npc_save": npc.AbstractNPC.npc_save_list}, utilities.bounce, "npc_save")
    utilities.save_to(npc.AbstractNPC.get_npc_save_list, dict, "npc_save")


def load_saves():
    print("Save Loaded")
    global player, map
    #make player object with the needed rect pass

    #TODO: put these in the util file to match the functionality of save
    player = plr.Player(None)
    with open("saves/player_save.json", "r") as player_save:
        player.load(json.load(player_save))
        player_save.close()
    map = mp.Map()
    with open("saves/map_save.json", "r") as map_save:
        map.load(json.load(map_save))
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
    global map, player
    print("Load New Save")
    player = plr.Player(pygame.Rect(c.WIDTH/2 - c.PLAYER_WIDTH/2, c.HEIGHT/2 - c.PLAYER_HEIGHT/2, c.PLAYER_WIDTH, c.PLAYER_HEIGHT))
    map = mp.Map()
    map.setup_new_map()


def check_for_save() -> bool :
    for file in os.listdir():
        if os.path.isdir(file) and file == "saves":
            #TODO: check for actual old saves, not just for the folder
            return True
    return False


def title_screen_loop():
    """ Used to separate out the process for displaing the welcom/title screen
    
    currently the only place where the window size can be changed to fullscreen
    """
    global window

    title_font = pygame.font.SysFont("Garamond", 80)
    is_save = check_for_save()

    new_game_button_color = "gray"
    new_game_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/3 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
    new_game_button_text = utilities.get_text_surface("New Game")


    load_save_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/3*2 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
    load_save_button_text = utilities.get_text_surface("Load Save")
    if is_save:
        load_save_button_color = "gray"
    else:
        load_save_button_color = "gray16"

    while True:
        clock.tick(60)
        mouse_pos= pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F11]:
            window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            c.update_size(window.get_size())
            new_game_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/3 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
            load_save_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/3*2 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
        if is_save:
            if load_save_button_rect.collidepoint(*mouse_pos):
                if mouse_pressed[0]:
                    load_saves()
                    break
                load_save_button_color = "gray25"
            else:
                load_save_button_color = "gray"
        if new_game_button_rect.collidepoint(*mouse_pos):
            if mouse_pressed[0]:
                new_save()
                break
            new_game_button_color = "gray25"
        else:
            new_game_button_color = "gray"
        window.fill("black")
        window.blit(utilities.get_text_surface("Coding Club Example", title_font), (c.WIDTH/2 - 300, c.HEIGHT/10))
        pygame.draw.rect(window, new_game_button_color, new_game_button_rect)
        window.blit(new_game_button_text, (new_game_button_rect.x + 10, new_game_button_rect.y + 10))
        pygame.draw.rect(window, load_save_button_color, load_save_button_rect)
        window.blit(load_save_button_text, (load_save_button_rect.x + 10, load_save_button_rect.y + 10))
        pygame.display.update()
    

def pause_screen_loop():
    """ Pause screen for in game use. Currently the only way to save the game

    pauses all actions of characters and npcs while open
    """

    pause_background_rect = pygame.rect.Rect(c.WIDTH/6, 0, c.WIDTH/3*2, c.HEIGHT)
    pause_background_rect_surface = utilities.get_alpha_rect_surface(pause_background_rect, (50,50,50,30), radius=10)

    title_font = pygame.font.SysFont("Garamond", 80)
    pause_title = utilities.get_text_surface("Pause", title_font)
    pause_title_location = (c.WIDTH/2 - 100, c.HEIGHT/10)
    
    new_game_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/4 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
    new_game_button_text = utilities.get_text_surface("New Game")

    load_save_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/4*2 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
    load_save_button_text = utilities.get_text_surface("Load Save")

    exit_button_rect = pygame.rect.Rect(c.WIDTH/2 - c.BUTTON_WIDTH/2, c.HEIGHT/4*3 - c.BUTTON_HEIGHT/2, c.BUTTON_WIDTH, c.BUTTON_HEIGHT)
    exit_button_text = utilities.get_text_surface("Exit/Save")

    paused = True
    while paused:
        # keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        new_game_button_color = "gray"
        load_save_button_color = "grey"
        exit_button_color = "grey"

        if new_game_button_rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                new_save()
                return
            new_game_button_color = "grey25"
        elif load_save_button_rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                load_saves()
                return
            load_save_button_color = "grey25"
        elif exit_button_rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                save()
                pygame.quit()
                exit(0)
            exit_button_color = "grey25"

        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                exit(0)             #Really shouldn't be handled this way

        # pygame.draw.rect(window, (0,0,0,200), pause_background_rect, border_radius=5)
        window.blit(pause_background_rect_surface, pause_background_rect.topleft)
        window.blit(pause_title, pause_title_location)
        pygame.draw.rect(window, new_game_button_color, new_game_button_rect, border_radius=10)
        window.blit(new_game_button_text, (new_game_button_rect.x + 10, new_game_button_rect.y + 10))
        pygame.draw.rect(window, load_save_button_color, load_save_button_rect, border_radius=10)
        window.blit(load_save_button_text, (load_save_button_rect.x + 10, load_save_button_rect.y + 10))
        pygame.draw.rect(window, exit_button_color, exit_button_rect, border_radius=10)
        window.blit(exit_button_text, (exit_button_rect.x + 10, exit_button_rect.y + 10))
        pygame.display.update()


def check_map_tile_collision():
    global vel_x, vel_y
    local_index = player.get_location_index(vel_x,vel_y)
    player.map_rect.x += vel_x
    player.map_rect.y += vel_y
    for i in range(max(0, local_index[0]-5), min(c.MAP_WIDTH, local_index[0]+6)):
        for j in range(max(0, local_index[1]-5), min(c.MAP_HEIGHT, local_index[1]+6)):
            tile = map.tiles[i][j]
            if player.map_rect.colliderect(tile.rect):
                #TODO: find a way to do this by only setting the necissary value to zero
                if not tile.walkable:
                    player.map_rect.x -= vel_x
                    player.map_rect.y -= vel_y 
                    vel_x, vel_y = 0, 0
    player.map_rect.x -= vel_x
    player.map_rect.y -= vel_y 


def main():
    """ main function, 
    this is where we control things and call all of the stuff we want to happen in the game
    
    """
    global vel_x, vel_y


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
            vel_x, vel_y = int(vel_x/math.sqrt(2)), int(vel_y/math.sqrt(2))

        check_map_tile_collision()
        update_position()
        draw()

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pause_screen_loop()
            if event.type == pygame.QUIT:
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

