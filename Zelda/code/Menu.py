import pygame
from code.settings import *

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 2)
        
        # Opções do menu
        self.options = ["Start Game", "Quit"]
        self.selected_option = 0
        self.option_rects = []
        
        # Cores
        self.text_color = TEXT_COLOR
        self.selected_color = UI_BORDER_COLOR_ACTIVE
        
        # Background
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((0, 0, 0))
        self.background.set_alpha(200)
        
        # Logo do jogo (opcional)
        self.logo = pygame.image.load(resource_path('graphics/player/down/down_0.png')).convert_alpha()  # Crie uma imagem para o logo
        self.logo_rect = self.logo.get_rect(center=(WIDTH//2, HEIGHT//4))

    def draw(self):
        # Desenha o background semi-transparente
        self.display_surface.blit(self.background, (0, 0))
        
        # Desenha o logo (opcional)
        self.display_surface.blit(self.logo, self.logo_rect)
        
        # Desenha as opções do menu
        self.option_rects = []
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.text_color
            
            # Texto
            text_surf = self.font.render(option, False, color)
            text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 70))
            
            # Bordas para opção selecionada
            if i == self.selected_option:
                border_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, border_rect, 3)
            
            self.display_surface.blit(text_surf, text_rect)
            self.option_rects.append(text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None