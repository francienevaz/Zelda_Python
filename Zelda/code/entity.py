import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    """Classe base para todas as entidades do jogo que possuem movimento e colisão"""
    
    def __init__(self, groups):
        """
        Inicializa a entidade básica
        
        Args:
            groups: Grupos de sprites aos quais esta entidade pertence
        """
        super().__init__(groups)
        self.frame_index = 0          # Índice do frame atual da animação
        self.animation_speed = 0.15   # Velocidade de transição entre frames
        self.direction = pygame.math.Vector2()  # Vetor de direção do movimento
        self.speed = 0                # Velocidade de movimento (será definida nas subclasses)

    def move(self, speed):
        """
        Move a entidade na direção atual, tratando colisões
        
        Args:
            speed: Velocidade de movimento (em pixels por frame)
        """
        # Normaliza o vetor de direção para movimento diagonal
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Movimento horizontal
        self.hitbox.x += self.direction.x * speed
        self._handle_collision('horizontal')

        # Movimento vertical
        self.hitbox.y += self.direction.y * speed
        self._handle_collision('vertical')

        # Atualiza a posição do retângulo de renderização
        self.rect.center = self.hitbox.center

    def _handle_collision(self, direction):
        """
        Detecta e resolve colisões na direção especificada
        
        Args:
            direction: 'horizontal' ou 'vertical' - direção do movimento a ser verificada
        """
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    self._resolve_horizontal_collision(sprite)
                else:
                    self._resolve_vertical_collision(sprite)

    def _resolve_horizontal_collision(self, obstacle):
        """Resolve colisões no eixo horizontal"""
        if self.direction.x > 0:  # Movendo para a direita
            self.hitbox.right = obstacle.hitbox.left
        elif self.direction.x < 0:  # Movendo para a esquerda
            self.hitbox.left = obstacle.hitbox.right

    def _resolve_vertical_collision(self, obstacle):
        """Resolve colisões no eixo vertical"""
        if self.direction.y > 0:  # Movendo para baixo
            self.hitbox.bottom = obstacle.hitbox.top
        elif self.direction.y < 0:  # Movendo para cima
            self.hitbox.top = obstacle.hitbox.bottom

    def wave_value(self):
        """
        Gera um valor oscilante entre 0 e 255 baseado no tempo
        Usado para efeitos de piscar quando a entidade é atingida
        
        Returns:
            int: Valor entre 0 e 255 para efeitos de transparência
        """
        time = pygame.time.get_ticks()
        return 255 if sin(time) >= 0 else 0