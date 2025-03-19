import pygame

class InputHandler:
    def __init__(self, player):
        self.player = player

    def handle_input(self):
        if not self.player.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.player.direction.y = -1
                self.player.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.player.direction.y = 1
                self.player.status = 'down'
            else:
                self.player.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.player.direction.x = 1
                self.player.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.player.direction.x = -1
                self.player.status = 'left'
            else:
                self.player.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.player.attacking = True
                self.player.attack_time = pygame.time.get_ticks()
                print('attack')
            # magic input
            if keys[pygame.K_LCTRL]:
                self.player.attacking = True
                self.player.attack_time = pygame.time.get_ticks()
                print('magic')