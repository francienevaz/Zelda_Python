import pygame
from settings import *
from support import load_image_assets
from entity import Entity

class Player(Entity):
    """Main player class handling movement, combat, animations, and state management"""
    
    def __init__(self, position, sprite_groups, collision_sprites, 
                 attack_creation_callback, weapon_destruction_callback, 
                 magic_creation_callback):
        """
        Initialize the player character
        
        Args:
            position: Starting (x,y) position
            sprite_groups: Groups for sprite management
            collision_sprites: Sprites that block movement
            attack_creation_handler: Callback for creating attacks
            weapon_removal_handler: Callback for removing weapons
            magic_creation_handler: Callback for creating magic effects
        """
        super().__init__(sprite_groups)
        
        # Core setup
        self._setup_graphics(position)
        self._load_animations()
        self._setup_movement(collision_sprites)
        self._setup_combat_system(attack_creation_callback, 
                                  weapon_destruction_callback,
                                  magic_creation_callback)
        self._setup_stats()
        
        # State management
        self.current_status = 'down'
        self.is_dead = False

    def _setup_graphics(self, position):
        """Initialize player visuals and positioning"""
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -26)  # Tighter collision box

    def _load_animations(self):
        """
        Carrega todos os frames de animação para os diferentes estados do jogador
        
        Acessa a pasta de gráficos do player e carrega as animações para:
        - Movimento (up, down, left, right)
        - Estados idle (quando parado)
        - Ataques em cada direção
        """
        base_path = '../graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
        }
        
        for animation_state in self.animations.keys():
            try:
                animation_path = f'{base_path}{animation_state}'
                self.animations[animation_state] = load_image_assets(animation_path)
                
                if not self.animations[animation_state]:
                    print(f"Aviso: Nenhum frame encontrado para animação '{animation_state}'")
            except Exception as e:
                print(f"Erro ao carregar animação {animation_state}: {str(e)}")

    def _setup_movement(self, collision_sprites):
        """Configure movement-related properties"""
        self.collision_sprites = collision_sprites
        self.movement_speed = 0  # Will be set in _setup_stats()
        self.is_moving = False

    def _setup_combat_system(self, attack_callback, weapon_callback, magic_callback):
        """Initialize combat-related properties and callbacks"""
        self.is_attacking = False
        self.attack_cooldown = 400  # ms
        self.last_attack_time = None
        
        self.create_attack = attack_callback
        self.destroy_weapon = weapon_callback
        self.equipped_weapon_index = 0
        self.equipped_weapon = list(weapon_data.keys())[self.equipped_weapon_index]
        self.can_switch_weapon = True
        self.last_weapon_switch = None
        self.weapon_switch_cooldown = 200  # ms
        
        self.create_magic = magic_callback
        self.equipped_magic_index = 0
        self.equipped_magic = list(magic_data.keys())[self.equipped_magic_index]
        self.can_switch_magic = True
        self.last_magic_switch = None
        self.magic_switch_cooldown = 200  # ms
        
        self.is_vulnerable = True
        self.last_hit_time = None
        self.invulnerability_duration = 500  # ms

    def _setup_stats(self):
        """Initialize player attributes and stats"""
        self.base_stats = {
            'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5
        }
        self.health = self.base_stats['health'] * 0.5
        self.energy = self.base_stats['energy'] * 0.8
        self.experience = 123
        self.movement_speed = self.base_stats['speed']

    def handle_input(self):
        """Process keyboard input for player actions"""
        if not self.is_attacking and not self.is_dead:
            keys = pygame.key.get_pressed()
            self._handle_movement_input(keys)
            self._handle_combat_input(keys)
            self._handle_weapon_magic_switching(keys)

    def _handle_movement_input(self, keys):
        """Process movement-related keyboard input"""
        self.direction.y = -1 if keys[pygame.K_UP] else 1 if keys[pygame.K_DOWN] else 0
        self.direction.x = 1 if keys[pygame.K_RIGHT] else -1 if keys[pygame.K_LEFT] else 0

    def _handle_combat_input(self, keys):
        """Process combat-related keyboard input"""
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            self._initiate_attack(current_time)
        if keys[pygame.K_LCTRL]:
            self._cast_magic(current_time)

    def _initiate_attack(self, current_time):
        """Start a melee weapon attack"""
        self.is_attacking = True
        self.last_attack_time = current_time
        self.create_attack()

    def _cast_magic(self, current_time):
        """Cast a magic spell"""
        self.is_attacking = True
        self.last_attack_time = current_time
        spell_type = self.equipped_magic
        spell_power = magic_data[spell_type]['strength'] + self.base_stats['magic']
        spell_cost = magic_data[spell_type]['cost']
        self.create_magic(spell_type, spell_power, spell_cost)

    def update(self):
        """Main update method called each frame"""
        if not self.is_dead:
            self.handle_input()
            self.manage_cooldowns()
            self.update_status()
            self.update_animation()
            self.move(self.movement_speed)
            if self.health <= 0:
                return self.handle_death()
