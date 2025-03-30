import pygame, sys
from settings import *
from level import Level
from Menu import Menu

class Game:
    def __init__(self):
        # Configuração inicial
        pygame.init()
        pygame.display.set_caption('Zelda - Python')
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.level = None
        
        # Estados do jogo
        self.states = {
            'menu': self.menu_state,
            'game': self.game_state,
            'game_over': self.game_over_state,
            'quit': self.quit_state
        }
        self.current_state = 'menu'
        
        # Instâncias
        self.menu = Menu()
        self.level = None

    def menu_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = 'quit'
            
            result = self.menu.handle_event(event)
            if result == "Start Game":
                self.level = Level()  # Cria uma nova instância do jogo
                self.current_state = 'game'
            elif result == "Quit":
                self.current_state = 'quit'
        
        self.menu.draw()
        pygame.display.update()

    def start_new_game(self):
        self.level = Level()
        self.current_state = 'game'

    def game_over_state(self):
        # Mostra mensagem de game over
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 3)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGTH//2))
        
        # Mensagem de instrução
        small_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        instruction = small_font.render("Press any key to return to menu", True, TEXT_COLOR)
        instruction_rect = instruction.get_rect(center=(WIDTH//2, HEIGTH//2 + 70))
        
        self.screen.blit(text, text_rect)
        self.screen.blit(instruction, instruction_rect)
        pygame.display.update()
        
        # Espera por input do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = 'quit'
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.start_new_game()  # Reinicia o jogo
    
    def game_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.current_state = 'menu'  # Volta ao menu com ESC
        
        # Executa o nível e verifica se o jogador morreu
        result = self.level.run()
        if result == "game_over":
            self.current_state = 'game_over'            
        
        pygame.display.update()
        self.clock.tick(FPS)

    def quit_state(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.states[self.current_state]()

if __name__ == '__main__':
    game = Game()
    game.run()
