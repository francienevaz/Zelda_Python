import pygame

class Movement:
    def __init__(self, player, obstacles_sprites):
        self.player = player
        self.obstacles_sprites = obstacles_sprites
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.player.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.player.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.player.rect.center = self.player.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.player.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.player.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.player.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.player.hitbox.bottom = sprite.hitbox.top

    def update_cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.player.attacking:
            if current_time - self.player.attack_time >= self.player.attack_cooldown:
                self.player.attacking = False