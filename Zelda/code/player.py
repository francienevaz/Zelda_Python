import pygame
from settings import *
from animation import Animation
from movement import Movement
from input_handler import InputHandler

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Inicializa os módulos
        self.animation = Animation(self)
        self.movement = Movement(self, obstacles_sprites)
        self.input_handler = InputHandler(self)

        # Atributos do jogador
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Direção do movimento (Vector2)
        self.direction = pygame.math.Vector2()  # Inicializa o atributo direction

        # Status do jogador (para animações)
        self.status = 'down'  # Inicializa o atributo status

    def update(self):
        """
        Atualiza o estado do jogador a cada frame.
        """
        self.input_handler.handle_input()
        self.movement.update_cooldowns()
        self.animation.update_status()
        self.animation.animate()
        self.movement.move(self.speed)