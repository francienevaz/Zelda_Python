import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon

class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()
    
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('./graphics/grass'),
            'object': import_folder('./graphics/objects'),
        }
    
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y),  [self.obstacles_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)
                            
                        if style == 'object':
                            surf = graphics['object'][int(col)]  
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'object', surf)
        #         if col == 'x':
        #             Tile((x, y), [self.visible_sprites,self.obstacles_sprites])
        #         elif col == 'p':
        #             self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites, self.create_attack)
 
    def create_attack(self):
        Weapon(self.player, [self.visible_sprites])
 
    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()        
        self.display_surface = pygame.display.get_surface()
        # dessa forma e possivel passar parametros para o Vector2 e mudar a posicao da tela do jogo
        # mas nao mudamos a posicao do jogo em si, apenas desenhamos todos os elementos em um lugar diferente
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

        # creating the floor
        self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery -self.half_height

        # drawing the floor 
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)  