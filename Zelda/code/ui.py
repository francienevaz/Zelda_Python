import pygame
from code.settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(UI_FONT, UI_SMALL_FONT_SIZE)

        # heart setup com redimensionamento
        self.heart_scale = 1.5  # 1.5 vezes o tamanho original
        original_heart = pygame.image.load(resource_path('graphics/ui/heart.png')).convert_alpha()
        original_half = pygame.image.load(resource_path('graphics/ui/heart_half.png')).convert_alpha()
        original_empty = pygame.image.load(resource_path('graphics/ui/heart_off.png')).convert_alpha()

        # Redimensiona todas as imagens
        new_size = (int(original_heart.get_width() * self.heart_scale), 
                    int(original_heart.get_height() * self.heart_scale))
        
        self.heart_full = pygame.transform.smoothscale(original_heart, new_size)
        self.heart_half = pygame.transform.smoothscale(original_half, new_size)
        self.heart_empty = pygame.transform.smoothscale(original_empty, new_size)
        
        self.heart_size = self.heart_full.get_size()
        self.heart_spacing = 15 

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon_surf = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon_surf)

    def show_hearts(self, current, max_amount):
        """Mostra corações para representar a vida do jogador"""
        # Calcula quantos corações mostrar (cada coração vale 20 de vida)
        heart_value = 20  # Cada coração representa 20 pontos de vida
        full_hearts = int(current // heart_value)  # Convertendo para inteiro
        half_hearts = True if current % heart_value >= heart_value/2 else False
        empty_hearts = int((max_amount // heart_value) - full_hearts - (1 if half_hearts else 0))  # Convertendo para inteiro

        # Posição inicial
        start_x = 10
        start_y = 10

        # Desenha corações cheios
        for i in range(full_hearts):
            x = start_x + i * (self.heart_size[0] + self.heart_spacing)
            self.display_surface.blit(self.heart_full, (x, start_y))

        # Desenha coração meio cheio (se necessário)
        if half_hearts:
            x = start_x + full_hearts * (self.heart_size[0] + self.heart_spacing)
            self.display_surface.blit(self.heart_half, (x, start_y))
            empty_hearts -= 1  # Ajusta para não desenhar coração vazio extra

        # Desenha corações vazios
        for i in range(empty_hearts):
            x = start_x + (full_hearts + (1 if half_hearts else 0) + i) * (self.heart_size[0] + self.heart_spacing)
            self.display_surface.blit(self.heart_empty, (x, start_y))

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def draw_arrow_keys(self, center_x, center_y, size=30, spacing=15, active_keys=None):
        """Desenha um D-pad com setas espaçadas ao redor de um ponto central"""
        if active_keys is None:
            active_keys = {
                'up': False,
                'down': False,
                'left': False,
                'right': False
            }

        # Cores
        arrow_color_active = (255, 255, 0)  # Amarelo quando pressionado
        arrow_color_inactive = (150, 150, 150)  # Cinza quando inativo

        # --- Seta para CIMA ---
        up_color = arrow_color_active if active_keys.get('up', False) else arrow_color_inactive
        pygame.draw.polygon(
            self.display_surface, up_color,
            [
                (center_x, center_y - spacing - size),  # Ponto superior
                (center_x + size//2, center_y - spacing),  # Inferior direito
                (center_x - size//2, center_y - spacing)   # Inferior esquerdo
            ]
        )

        # --- Seta para BAIXO ---
        down_color = arrow_color_active if active_keys.get('down', False) else arrow_color_inactive
        pygame.draw.polygon(
            self.display_surface, down_color,
            [
                (center_x, center_y + spacing + size),  # Ponto inferior
                (center_x + size//2, center_y + spacing),  # Superior direito
                (center_x - size//2, center_y + spacing)   # Superior esquerdo
            ]
        )

        # --- Seta para ESQUERDA ---
        left_color = arrow_color_active if active_keys.get('left', False) else arrow_color_inactive
        pygame.draw.polygon(
            self.display_surface, left_color,
            [
                (center_x - spacing - size, center_y),  # Ponto esquerdo
                (center_x - spacing, center_y - size//2),  # Superior direito
                (center_x - spacing, center_y + size//2)   # Inferior direito
            ]
        )

        # --- Seta para DIREITA ---
        right_color = arrow_color_active if active_keys.get('right', False) else arrow_color_inactive
        pygame.draw.polygon(
            self.display_surface, right_color,
            [
                (center_x + spacing + size, center_y),  # Ponto direito
                (center_x + spacing, center_y - size//2),  # Superior esquerdo
                (center_x + spacing, center_y + size//2)   # Inferior esquerdo
            ]
        )

        # --- Círculo central (opcional) ---
        pygame.draw.circle(
            self.display_surface, 
            (100, 100, 100), 
            (center_x, center_y), 
            size//3
        )

    def show_controls(self):
        """Mostra controles com fundo semi-transparente"""
        screen_width, screen_height = self.display_surface.get_size()
        
        # Configurações do painel
        controls_width = 350
        controls_height = 150
        controls_x = screen_width - controls_width - 20
        controls_y = screen_height - controls_height - 20
        
        # Garante que UI_BG_COLOR é uma tupla RGB válida
        bg_color = UI_BG_COLOR if isinstance(UI_BG_COLOR, (tuple, list)) and len(UI_BG_COLOR) == 3 else (0, 0, 0)
        
        # Cria superfície com transparência
        controls_surface = pygame.Surface((controls_width, controls_height), pygame.SRCALPHA)
        
        # Converte para RGBA (adicionando alpha)
        bg_color_rgba = (*bg_color, 180)  # 180 de 255 (~70% opaco)
        border_color_rgba = (*UI_BORDER_COLOR, 200) if isinstance(UI_BORDER_COLOR, (tuple, list)) and len(UI_BORDER_COLOR) == 3 else (255, 255, 255, 200)
        
        # Preenche o fundo
        controls_surface.fill(bg_color_rgba)
        
        # Desenha borda
        pygame.draw.rect(controls_surface, border_color_rgba, controls_surface.get_rect(), 3)
        
        # Aplica na tela principal
        self.display_surface.blit(controls_surface, (controls_x, controls_y))
        
        arrow_size = 30
        arrow_spacing = 5
        arrow_start_x = controls_x + 50
        arrow_start_y = controls_y + 50

        self.draw_arrow_keys(
            arrow_start_x, arrow_start_y, 
            size=arrow_size, 
            spacing=arrow_spacing,
            active_keys={
                'up': pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w],
                'down': pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s],
                'left': pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a],
                'right': pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]
            }
        )

        # Textos das ações
        controls_info = [
            ("Ataque", "SPACE", pygame.key.get_pressed()[pygame.K_SPACE]),
            ("Trocar Arma", "Q", pygame.key.get_pressed()[pygame.K_q]),
        ]

        text_offset_x = arrow_start_x + arrow_size + 30
        text_start_y = arrow_start_y - 15

        for i, (action, key, is_active) in enumerate(controls_info):
            # Renderiza o texto da ação (ex: "Trocar Arma:")
            action_surf = self.small_font.render(f"{action}:", False, TEXT_COLOR)
            action_y = text_start_y + i * 35  # 35px de espaçamento vertical
            self.display_surface.blit(action_surf, (text_offset_x, action_y))
            
            # Renderiza a tecla correspondente (ex: "Q")
            key_color = (255, 255, 0) if is_active else (200, 200, 200)
            key_surf = self.small_font.render(key, False, key_color)
            
            # Ajuste fino do posicionamento da tecla:
            key_x = text_offset_x + 125  # Aumentado de 100 para 120
            key_y = action_y + -1  # Deslocado 5px para baixo para alinhar com o texto
            self.display_surface.blit(key_surf, (key_x, key_y))

    def display(self, player):
        self.show_hearts(player.health, player.stats['health'])
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.show_controls()