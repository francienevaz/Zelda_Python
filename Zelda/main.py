import pygame, sys
from code.settings import *
from code.level import Level
from code.menu import Menu
from code.sound import *

class GameEngine:
    def __init__(self):
        # Configuração inicial
        pygame.init()
        pygame.display.set_caption('Zora - Python')
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = None

        # Sons
        self.sound_manager = SoundManager()
        self.game_over_sound = None
        self.load_sounds()

        # Carrega a música de fundo
        self.load_music()

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

    def load_sounds(self):
        """Carrega todos os sons necessários"""
        try:
            self.game_over_sound = pygame.mixer.Sound(resource_path('audio/game_over.wav'))
            self.game_over_sound.set_volume(VOLUME_SFX)
        except Exception as e:
            print(f"Erro ao carregar sons: {e}")

    def game_over_state(self):
        # Toca o som de game over e para a música de fundo
        pygame.mixer.music.stop()
        self.game_over_sound.play()

        # Mostra mensagem de game over
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 3)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))

        # Mensagem de instrução
        small_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        instruction = small_font.render("Press any key to return to menu", True, TEXT_COLOR)
        instruction_rect = instruction.get_rect(center=(WIDTH//2, HEIGHT//2 + 70))

        self.screen.blit(text, text_rect)
        self.screen.blit(instruction, instruction_rect)
        pygame.display.update()

        # Espera por input do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = 'quit'
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.load(resource_path('audio/main.mp3'))
                pygame.mixer.music.play(-1)
                self.current_state = 'menu'
                # self.start_new_game()  # Reinicia o jogo

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

    def load_music(self):
        """Carrega e configura a música de fundo"""
        try:
            pygame.mixer.music.load(resource_path('audio/main.mp3'))
            pygame.mixer.music.set_volume(VOLUME_MUSIC)
            pygame.mixer.music.play(-1)  # -1 faz loop infinito
        except Exception as e:
            print(f"Erro ao carregar música: {e}")

    def run(self):
        while True:
            self.states[self.current_state]()
            self.screen.fill(WATER_COLOR)

if __name__ == '__main__':
    game = GameEngine()
    game.run()