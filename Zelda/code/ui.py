import pygame
from settings import *

class UserInterface:
    """Classe responsável por renderizar todos os elementos da interface do usuário"""
    
    def __init__(self):
        """Inicializa os elementos da UI"""
        # Configuração básica
        self.display_surface = pygame.display.get_surface()
        self.ui_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Configuração das barras de status
        self._setup_status_bars()
        
        # Carrega os gráficos de armas e magias
        self._load_equipment_graphics()

    def _setup_status_bars(self):
        """Prepara os retângulos das barras de status"""
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def _load_equipment_graphics(self):
        """Carrega as imagens das armas e magias disponíveis"""
        # Armas
        self.weapon_graphics = [
            pygame.image.load(weapon['graphic']).convert_alpha() 
            for weapon in weapon_data.values()
        ]
        
        # Magias
        self.magic_graphics = [
            pygame.image.load(magic['graphic']).convert_alpha()
            for magic in magic_data.values()
        ]

    def draw_status_bar(self, current_value, max_value, bg_rect, color):
        """
        Desenha uma barra de status na tela
        
        Args:
            current_value: Valor atual a ser exibido
            max_value: Valor máximo possível
            bg_rect: Retângulo de fundo da barra
            color: Cor da barra de preenchimento
        """
        # Desenha o fundo
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        
        # Calcula a largura atual
        ratio = current_value / max_value
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        # Desenha a barra de preenchimento e borda
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def draw_experience(self, exp):
        """Exibe a quantidade de experiência do jogador"""
        exp_text = self.ui_font.render(str(int(exp)), False, TEXT_COLOR)
        
        # Posiciona no canto inferior direito
        screen_width, screen_height = self.display_surface.get_size()
        text_rect = exp_text.get_rect(bottomright=(screen_width - 20, screen_height - 20))
        
        # Desenha o fundo e o texto
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(exp_text, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def _create_equipment_box(self, x, y, is_active):
        """
        Cria uma caixa de seleção para equipamentos
        
        Args:
            x, y: Posição da caixa
            is_active: Se o item está ativo/selecionado
        """
        box_rect = pygame.Rect(x, y, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, box_rect)
        
        # Cor da borda baseada no estado
        border_color = UI_BORDER_COLOR_ACTIVE if is_active else UI_BORDER_COLOR
        pygame.draw.rect(self.display_surface, border_color, box_rect, 3)
        
        return box_rect

    def draw_weapon_slot(self, weapon_index, is_active):
        """Exibe o ícone da arma equipada"""
        box_rect = self._create_equipment_box(10, 630, is_active)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=box_rect.center)
        
        self.display_surface.blit(weapon_surf, weapon_rect)

    def draw_magic_slot(self, magic_index, is_active):
        """Exibe o ícone da magia equipada"""
        box_rect = self._create_equipment_box(80, 635, is_active)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=box_rect.center)
        
        self.display_surface.blit(magic_surf, magic_rect)

    def update(self, player):
        """
        Atualiza todos os elementos da UI baseado no estado do jogador
        
        Args:
            player: Instância do jogador para obter os status atuais
        """
        # Barras de status
        self.draw_status_bar(player.health, player.stats['health'], 
                           self.health_bar_rect, HEALTH_COLOR)
        self.draw_status_bar(player.energy, player.stats['energy'],
                           self.energy_bar_rect, ENERGY_COLOR)
        
        # Experiência
        self.draw_experience(player.exp)
        
        # Slots de equipamento
        self.draw_weapon_slot(player.weapon_index, not player.can_switch_weapon)
        self.draw_magic_slot(player.magic_index, not player.can_switch_magic)