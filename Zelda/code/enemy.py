import pygame
from settings import *
from entity import Entity
from support import load_image_assets

class Enemy(Entity):
    """Classe base para todos os inimigos do jogo, herdando de Entity"""
    
    def __init__(self, enemy_type, position, sprite_groups, collision_sprites, 
                 damage_player_callback, trigger_death_particles):
        """
        Inicializa um inimigo com características específicas
        
        Args:
            enemy_type (str): Tipo do inimigo (deve existir em monster_data)
            position (tuple): Posição inicial (x, y)
            sprite_groups (list): Grupos de sprites para renderização
            collision_sprites (pygame.sprite.Group): Sprites com colisão
            damage_handler (function): Callback para causar dano ao jogador
            death_effect_handler (function): Callback para efeitos de morte
        """
        super().__init__(sprite_groups)
        self.sprite_type = 'enemy'
        
        # Configuração visual
        self._load_enemy_assets(enemy_type)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        
        # Configuração física
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)  # Ajuste para colisão mais precisa
        self.collision_sprites = collision_sprites
        
        # Atributos baseados nos dados do monstro
        self._setup_enemy_stats(enemy_type)
        
        # Sistema de combate
        self._setup_combat_system(damage_player_callback, trigger_death_particles)
        
        # Temporizadores
        self.attack_cooldown = 400  # ms entre ataques
        self.invincibility_duration = 300  # ms de invencibilidade pós-dano    

    def _load_enemy_assets(self, enemy_type):
        """Carrega as animações para o tipo específico de inimigo"""
        self.animations = {
            'idle': [], 
            'move': [], 
            'attack': []
        }
        
        # Caminho base para os assets do inimigo
        assets_base_path = f'../graphics/monsters/{enemy_type}/'
        
        # Carrega cada animação usando a nova função
        for animation_state in self.animations.keys():
            try:
                animation_path = f"{assets_base_path}{animation_state}"
                self.animations[animation_state] = load_image_assets(animation_path)
            except Exception as e:
                print(f"Erro ao carregar animação {animation_state} para {enemy_type}: {e}")

    def animate(self):
        """Atualiza a animação do inimigo baseado no status atual"""
        animation = self.animations[self.status]
        
        # Avança o frame index
        self.frame_index += self.animation_speed
        
        # Reseta a animação se chegar ao final
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        # Atualiza a imagem e posição
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Efeito de piscar quando atingido
        if not self.is_vulnerable:  # Antigo: not self.vulnerable
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def _setup_enemy_stats(self, enemy_type):
        """Configura os atributos baseados nos dados do monstro"""
        stats = monster_data[enemy_type]
        
        self.enemy_type = enemy_type
        self.health = stats['health']
        self.experience_value = stats['exp']
        self.movement_speed = stats['speed']
        self.attack_power = stats['damage']
        self.knockback_resistance = stats['resistance']
        self.attack_range = stats['attack_radius']
        self.aggro_range = stats['notice_radius']
        self.attack_style = stats['attack_type']

    def _setup_combat_system(self, damage_player_callback, trigger_death_particles):
        """Configura callbacks e estado de combate"""
        self.can_attack = True
        self.last_attack_time = None
        self.damage_player_callback = damage_player_callback
        self.trigger_death_particles = trigger_death_particles
        
        self.is_vulnerable = True
        self.last_hit_time = None

    def calculate_player_vector(self, player):
        """Calcula distância e direção até o jogador"""
        enemy_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()
        
        direction = (player_pos - enemy_pos).normalize() if distance > 0 else pygame.math.Vector2()
        return distance, direction

    def update_behavior(self, player):
        """Atualiza o estado do inimigo baseado na distância do jogador"""
        distance_to_player, _ = self.calculate_player_vector(player)
        
        if distance_to_player <= self.attack_range and self.can_attack:
            self._handle_attack_state()
        elif distance_to_player <= self.aggro_range:
            self.status = 'move'
        else:
            self.status = 'idle'

    def _handle_attack_state(self):
        """Lida com a transição para estado de ataque"""
        if self.status != 'attack':
            self.frame_index = 0  # Reseta animação
        self.status = 'attack'

    def execute_actions(self, player):
        """Executa ações baseadas no estado atual"""
        if self.status == 'attack':
            self._perform_attack()
        elif self.status == 'move':
            self._chase_player(player)
        else:
            self.direction = pygame.math.Vector2()  # Estado idle

    def _perform_attack(self):
        """Executa lógica de ataque"""
        self.last_attack_time = pygame.time.get_ticks()
        self.damage_player_callback(self.attack_power, self.attack_style)

    def _chase_player(self, player):
        """Move-se na direção do jogador"""
        self.direction = self.calculate_player_vector(player)[1]

    def handle_damage(self, player, damage_type):
        """Processa dano recebido do jogador"""
        if self.is_vulnerable:
            self._apply_knockback(player)
            
            if damage_type == 'weapon':
                self.health -= player.calculate_total_damage()
            
            self.last_hit_time = pygame.time.get_ticks()
            self.is_vulnerable = False

    def _apply_knockback(self, player):
        """Aplica efeito de recuo quando atingido"""
        self.direction = self.calculate_player_vector(player)[1]
        
        if self.knockback_resistance > 0:
            self.direction *= -self.knockback_resistance

    def check_health(self):
        """Verifica se o inimigo morreu"""
        if self.health <= 0:
            self._trigger_death_effects()
            self.kill()

    def _trigger_death_effects(self):
        """Executa efeitos visuais/sonoros de morte"""
        self.trigger_death_particles(self.rect.center, self.enemy_type)

    def update_cooldowns(self):
        """Atualiza temporizadores de cooldown"""
        current_time = pygame.time.get_ticks()
        
        if not self.can_attack:
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.is_vulnerable:
            if current_time - self.last_hit_time >= self.invincibility_duration:
                self.is_vulnerable = True

    def update(self):
        """Atualização principal do inimigo (chamada a cada frame)"""
        self._apply_knockback_effect()
        self.move(self.movement_speed)
        self.animate()
        self.update_cooldowns()
        self.check_health()

    def _apply_knockback_effect(self):
        """Aplica efeito de recuo se necessário"""
        if not self.is_vulnerable:
            self.direction *= -self.knockback_resistance
