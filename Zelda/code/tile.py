import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    """Classe que representa um tile no mapa do jogo, podendo ser um objeto, terreno ou obstáculo"""
    
    def __init__(self, position, groups, sprite_type, surface=None):
        """
        Inicializa um tile no mapa
        
        Args:
            position (tuple): Posição (x,y) do tile no mundo do jogo
            groups (list): Grupos de sprites aos quais este tile pertence
            sprite_type (str): Tipo do tile ('object', 'boundary', 'grass', etc.)
            surface (pygame.Surface, optional): Superfície gráfica do tile. Se None, cria uma vazia.
        """
        super().__init__(groups)
        
        # Configuração básica do sprite
        self.sprite_type = sprite_type
        self.image = surface if surface else pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        # Posicionamento diferente para objetos que precisam de offset
        self._setup_position(position)
        
        # Hitbox ajustada para colisões mais precisas
        self.hitbox = self.rect.inflate(0, -10)

    def _setup_position(self, position):
        """
        Configura o posicionamento do tile considerando seu tipo
        
        Args:
            position (tuple): Posição (x,y) inicial do tile
        """
        if self.sprite_type == 'object':
            # Objetos são renderizados uma tile acima de sua posição lógica
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - TILE_SIZE))
        else:
            # Demais tiles usam a posição padrão
            self.rect = self.image.get_rect(topleft=position)