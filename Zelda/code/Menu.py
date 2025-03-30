import pygame
from settings import *

class GameMenu:
    """Classe que gerencia o menu principal do jogo com navegação e seleção de opções"""
    
    def __init__(self):
        # Configuração básica
        self.display_surface = pygame.display.get_surface()
        self.menu_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 2)  # Fonte maior para o menu
        
        # Configuração das opções
        self.menu_options = ["Start Game", "Quit"]  # Opções disponíveis
        self.selected_index = 0  # Índice da opção selecionada
        self.option_rectangles = []  # Armazena os retângulos de colisão
        
        # Cores e estilos
        self.normal_text_color = TEXT_COLOR
        self.highlight_text_color = UI_BORDER_COLOR_ACTIVE
        
        # Configuração do fundo
        self.background_overlay = pygame.Surface((WIDTH, HEIGHT))
        self.background_overlay.fill((0, 0, 0))
        self.background_overlay.set_alpha(200)  # Semi-transparente
        
        # Elementos visuais (logo)
        self.game_logo = pygame.image.load('../graphics/player/down/down_0.png').convert_alpha()
        self.logo_position = self.game_logo.get_rect(center=(WIDTH//2, HEIGHT//4))

    def render_menu(self):
        """Renderiza todos os elementos do menu na tela"""
        
        # Desenha o fundo semi-transparente
        self.display_surface.blit(self.background_overlay, (0, 0))
        
        # Desenha o logo do jogo
        self.display_surface.blit(self.game_logo, self.logo_position)
        
        # Prepara para armazenar os retângulos das opções
        self.option_rectangles = []
        
        # Renderiza cada opção do menu
        for index, option_text in enumerate(self.menu_options):
            # Seleciona a cor baseado na opção atual
            text_color = self.highlight_text_color if index == self.selected_index else self.normal_text_color
            
            # Cria a superfície de texto
            text_surface = self.menu_font.render(option_text, False, text_color)
            text_rectangle = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + index * 70))
            
            # Destaca a opção selecionada
            if index == self.selected_index:
                highlight_rect = text_rectangle.inflate(20, 10)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, highlight_rect, 3)
            
            # Desenha o texto e armazena o retângulo
            self.display_surface.blit(text_surface, text_rectangle)
            self.option_rectangles.append(text_rectangle)

    def process_input(self, event):
        """Processa eventos de entrada para navegação no menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                # Navega para baixo (circular)
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_UP:
                # Navega para cima (circular)
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                # Retorna a opção selecionada quando Enter é pressionado
                return self.menu_options[self.selected_index]
        return None