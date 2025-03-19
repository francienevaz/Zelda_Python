import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

class Level:
    def __init__(self):
        # Obtém a superfície de exibição
        self.display_surface = pygame.display.get_surface()

        # Configuração dos grupos de sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # Configuração do mapa
        self.create_map()

    def create_map(self):
        """
        Cria o mapa do jogo com base em layouts CSV e gráficos carregados.
        """
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('./graphics/grass'),
            'object': import_folder('./graphics/objects'),
        }

        # Itera sobre os layouts e cria os tiles correspondentes
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        self.create_tile(style, (x, y), graphics, col)

        # Cria o jogador em uma posição fixa
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites)

    def create_tile(self, style, pos, graphics, col):
        """
        Cria um tile com base no estilo, posição, gráficos e valor da célula.
        """
        x, y = pos
        if style == 'boundary':
            Tile((x, y), [self.obstacles_sprites], 'invisible')
        elif style == 'grass':
            random_grass_image = choice(graphics['grass'])
            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'grass', random_grass_image)
        elif style == 'object':
            surf = graphics['object'][int(col)]
            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', surf)

    def run(self):
        """
        Executa a lógica principal do nível, incluindo atualização e desenho dos sprites.
        """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        """
        Grupo de sprites com ordenação por profundidade (Y-sorting) e câmera centrada no jogador.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Configuração do chão
        self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """
        Desenha os sprites com ordenação por profundidade e offset da câmera.
        """
        # Calcula o offset da câmera com base na posição do jogador
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Desenha o chão
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # Desenha os sprites ordenados por profundidade (Y-sorting)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)