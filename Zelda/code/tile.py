import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        """
        Inicializa um tile.

        :param pos: Tupla (x, y) representando a posição do tile.
        :param groups: Lista de grupos de sprites aos quais o tile pertence.
        :param sprite_type: Tipo do sprite (ex: 'object', 'grass', 'boundary').
        :param surface: Superfície do tile (opcional, padrão é uma superfície vazia do tamanho do tile).
        """
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface

        # Ajusta a posição do retângulo com base no tipo de sprite
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        # Define a hitbox do tile (um pouco menor que o retângulo)
        self.hitbox = self.rect.inflate(0, -10)