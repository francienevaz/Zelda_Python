import pygame
import sys
from settings import *
from level import Level
from menu import GameMenu  # Atualizado para usar o novo nome

class GameEngine:
    """Classe principal que gerencia o fluxo do jogo e estados da aplicação"""
    
    def __init__(self):
        # Inicialização do Pygame e configuração da janela
        pygame.init()
        pygame.display.set_caption('Zelda - Python')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game_clock = pygame.time.Clock()
        
        # Sistema de estados do jogo
        self.game_states = {
            'main_menu': self._handle_menu_state,
            'gameplay': self._handle_gameplay_state,
            'game_over': self._handle_game_over_state,
            'exit': self._handle_exit_state
        }
        self.current_state = 'main_menu'
        
        # Componentes do jogo
        self.game_menu = GameMenu()  # Usando a classe refatorada
        self.game_level = None

    def _handle_menu_state(self):
        """Gerencia o estado do menu principal"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = 'exit'
            
            user_choice = self.game_menu.process_input(event)
            if user_choice == "Start Game":
                self._initialize_game_session()
            elif user_choice == "Quit":
                self.current_state = 'exit'
        
        self.game_menu.render_menu()
        pygame.display.update()

    def _initialize_game_session(self):
        """Prepara uma nova sessão de jogo"""
        self.game_level = Level()
        self.current_state = 'gameplay'

    def _handle_game_over_state(self):
        """Gerencia a tela de game over"""
        # Renderiza mensagem principal
        title_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 3)
        game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        
        # Renderiza instruções
        instruction_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        instruction_text = instruction_font.render("Press any key to restart", True, TEXT_COLOR)
        instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 70))
        
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(instruction_text, instruction_rect)
        pygame.display.update()
        
        # Processa input do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = 'exit'
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self._initialize_game_session()

    def _handle_gameplay_state(self):
        """Gerencia o estado principal de jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = 'exit'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_state = 'main_menu'
        
        # Executa a lógica do nível e verifica estado
        level_status = self.game_level.run()
        if level_status == "game_over":
            self.current_state = 'game_over'
        
        pygame.display.update()
        self.game_clock.tick(FPS)

    def _handle_exit_state(self):
        """Finaliza a aplicação corretamente"""
        pygame.quit()
        sys.exit()

    def run_game_loop(self):
        """Loop principal de execução do jogo"""
        while True:
            self.game_states[self.current_state]()

if __name__ == '__main__':
    zelda_game = GameEngine()
    zelda_game.run_game_loop()