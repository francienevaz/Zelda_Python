import pygame
import os

class Weapon(pygame.sprite.Sprite):
    """Classe que representa a arma equipada pelo jogador"""
    
    def __init__(self, player, groups):
        """
        Inicializa a arma do jogador
        
        Args:
            player: Instância do jogador que está usando a arma
            groups: Grupos de sprites aos quais a arma pertence
        """
        super().__init__(groups)
        self.sprite_type = 'weapon'  # Define o tipo de sprite para colisões
        
        # Obtém a direção atual do jogador (sem o estado de ataque/idle)
        direction = player.status.split('_')[0]
        
        # Carrega o gráfico da arma baseado na direção
        self._load_weapon_graphic(player.weapon, direction)
        
        # Posiciona a arma corretamente de acordo com a direção
        self._position_weapon(player.rect, direction)

    def _load_weapon_graphic(self, weapon_type, direction):
        """Carrega a imagem da arma baseada no tipo e direção"""
        # Constrói o caminho absoluto para o arquivo de imagem
        weapon_path = os.path.abspath(
            f'../graphics/weapons/{weapon_type}/{direction}.png'
        )
        
        try:
            self.image = pygame.image.load(weapon_path).convert_alpha()
        except FileNotFoundError:
            print(f"Erro: Arquivo de arma não encontrado em {weapon_path}")
            # Carrega uma imagem de fallback se o arquivo não existir
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 30, 30))

    def _position_weapon(self, player_rect, direction):
        """Posiciona a arma relativa ao jogador baseado na direção"""
        offset = pygame.math.Vector2(0, 0)  # Vetor para ajustes finos de posição
        
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player_rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player_rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player_rect.midbottom + pygame.math.Vector2(-10, 0))
        else:  # Para cima ou qualquer outra direção não especificada
            self.rect = self.image.get_rect(midbottom=player_rect.midtop + pygame.math.Vector2(-10, 0))