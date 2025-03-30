import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import load_map_layout, load_image_assets
from random import choice, randint
from weapon import Weapon
from ui import UserInterface as UI
from enemy import Enemy
from particles import ParticleSystem
from factories import EntityFactory  # Nome de arquivo em minúsculas (Python convention)

class Level:
    """Classe principal que gerencia o nível do jogo, incluindo criação do mapa, entidades e loop principal"""
    
    def __init__(self):
        # Configuração da superfície de exibição
        self.display_surface = pygame.display.get_surface()

        # Configuração dos grupos de sprites
        self.visible_sprites = CameraYSortGroup()  # Grupo com ordenação por eixo Y
        self.collision_sprites = pygame.sprite.Group()  # Sprites com colisão

        # Configuração de ataques
        self.active_weapon = None  # Arma atualmente equipada
        self.attack_sprites = pygame.sprite.Group()  # Sprites de ataque
        self.damageable_sprites = pygame.sprite.Group()  # Sprites que podem receber dano

        # Inicialização do mapa e entidades
        self.initialize_game_map()

        # Interface do usuário
        self.game_ui = UI()

        # Sistema de partículas
        self.particle_system = ParticleSystem()
    
    def initialize_game_map(self):
        """Carrega e constrói o mapa a partir de arquivos CSV e sprites"""
        
        # Layouts dos mapas (cada tipo em um arquivo CSV separado)
        map_layouts = {
            'boundary': load_map_layout('../map/map_FloorBlocks.csv'),  # Limites do mapa
            'grass': load_map_layout('../map/map_Grass.csv'),  # Grama cortável
            'object': load_map_layout('../map/map_Objects.csv'),  # Objetos decorativos
            'entities': load_map_layout('../map/map_Entities.csv')  # Entidades (player e inimigos)
        }

        # Carrega os gráficos necessários
        map_graphics = {
            'grass': load_image_assets('../graphics/grass'),  # Sprites de grama
            'object': load_image_assets('../graphics/objects'),  # Sprites de objetos
        }

        # Processa cada camada do mapa
        for layer_type, layer_data in map_layouts.items():
            for row_index, row in enumerate(layer_data):
                for col_index, tile_id in enumerate(row):
                    if tile_id != '-1':  # -1 representa tiles vazios
                        tile_x = col_index * TILE_SIZE
                        tile_y = row_index * TILE_SIZE

                        # Cria boundaries (invisíveis, só colisão)
                        if layer_type == 'boundary':
                            EntityFactory.create_entity(
                                'boundary', 
                                (tile_x, tile_y), 
                                [None, self.collision_sprites]  # Adiciona apenas ao grupo de colisão
                            )

                        # Cria tiles de grama (cortável)
                        elif layer_type == 'grass':
                            random_grass_sprite = choice(map_graphics['grass'])
                            EntityFactory.create_entity(
                                'grass',
                                (tile_x, tile_y),
                                [self.visible_sprites, self.collision_sprites, self.damageable_sprites],
                                surface=random_grass_sprite
                            )

                        # Cria objetos decorativos
                        elif layer_type == 'object':
                            object_sprite = map_graphics['object'][int(tile_id)]
                            EntityFactory.create_entity(
                                'object',
                                (tile_x, tile_y),
                                [self.visible_sprites, self.collision_sprites],
                                surface=object_sprite
                            )

                        # Cria entidades (player e inimigos)
                        elif layer_type == 'entities':
                            # Player (ID 394 no CSV)
                            if tile_id == '394':
                                self.player = EntityFactory.create_entity(
                                    'player',
                                    (tile_x, tile_y),
                                    [self.visible_sprites],
                                    collision_sprites=self.collision_sprites,
                                    attack_creation_callback=self.create_weapon,
                                    weapon_destruction_callback=self.destroy_weapon,
                                    magic_creation_callback=self.create_magic_spell
                                )
                            else:  # Inimigos
                                enemy_type = self._get_enemy_type_by_id(tile_id)
                                if enemy_type:
                                    EntityFactory.create_entity(
                                        'enemy',
                                        (tile_x, tile_y),
                                        [self.visible_sprites, self.damageable_sprites],
                                        collision_sprites=self.collision_sprites,
                                        damage_player_callback=self.apply_damage_to_player,
                                        trigger_death_particles=self.spawn_death_particles,
                                        enemy_type=enemy_type
                                    )

    def _get_enemy_type_by_id(self, enemy_id):
        """Mapeia IDs do CSV para tipos de inimigos"""
        enemy_types = {
            '390': 'bamboo',
            '391': 'spirit',
            '392': 'raccoon',
            '393': 'squid'
        }
        return enemy_types.get(enemy_id)

    def create_weapon(self):
        """Cria uma instância de arma para o jogador"""
        self.active_weapon = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
    
    def create_magic_spell(self, spell_type, power, mana_cost):
        """Lógica para criação de magias (a implementar)"""
        print(f"Creating {spell_type} spell with power {power} and cost {mana_cost}")

    def destroy_weapon(self):
        """Remove a arma atual do jogo"""
        if self.active_weapon:
            self.active_weapon.kill()
        self.active_weapon = None

    def handle_weapon_attacks(self):
        """Processa colisões e efeitos de ataques com armas"""
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                # Verifica colisão com sprites que podem ser danificados
                hit_sprites = pygame.sprite.spritecollide(attack_sprite, self.damageable_sprites, False)
                if hit_sprites:
                    for target in hit_sprites:
                        # Grama cortável
                        if target.sprite_type == 'grass':
                            self._destroy_grass(target)
                        # Inimigos
                        else:
                            target.receive_damage(self.player, attack_sprite.sprite_type)        

    def _destroy_grass(self, grass_tile):
        """Efeito especial para destruição de grama"""
        center_pos = grass_tile.rect.center
        offset = pygame.math.Vector2(0, 75)
        
        # Cria partículas de folhas
        for _ in range(randint(3, 6)):
            self.particle_system.create_grass_particles(
                center_pos - offset,
                [self.visible_sprites]
            )
        grass_tile.kill()

    def apply_damage_to_player(self, damage_amount, damage_type):
        """Aplica dano ao jogador e verifica morte"""
        if self.player.is_vulnerable:
            self.player.health -= damage_amount
            self.player.is_vulnerable = False
            self.player.damage_cooldown = pygame.time.get_ticks()
            
            # Efeito visual de dano
            self.particle_system.create_particles(
                damage_type,
                self.player.rect.center,
                [self.visible_sprites]
            )

            # Verifica morte do jogador
            if self.player.health <= 0:
                self._handle_player_death()

    def _handle_player_death(self):
        """Executa efeitos e lógica de morte do jogador"""
        self.particle_system.create_particles(
            'spirit', 
            self.player.rect.center, 
            [self.visible_sprites]
        )
        # Som de morte (descomentar quando implementado)
        # pygame.mixer.Sound('./audio/death.wav').play()

    def spawn_death_particles(self, position, particle_effect):
        """Ativa efeitos visuais de morte para entidades"""
        self.particle_system.create_particles(
            particle_effect,
            position,
            self.visible_sprites
        )

    def run(self):
        """Executa o loop principal do nível"""
        # Renderização
        self.visible_sprites.custom_draw(self.player)
        
        # Atualizações
        self.visible_sprites.update()
        self.visible_sprites.update_enemies(self.player)
        self.handle_weapon_attacks()
        self.game_ui.display(self.player)

        # Verifica estado do jogador
        return self._check_player_state()

    def _check_player_state(self):
        """Verifica e gerencia o estado do jogador"""
        if hasattr(self, 'player') and self.player.is_dead:
            if not hasattr(self, 'death_timer'):
                # Inicia contagem regressiva para game over
                self.death_timer = pygame.time.get_ticks()
                self.particle_system.create_particles(
                    'spirit', 
                    self.player.rect.center, 
                    [self.visible_sprites]
                )
            
            # Espera 2 segundos antes de terminar o jogo
            if pygame.time.get_ticks() - self.death_timer > 2000:
                return "game_over"
        
        return "playing"    

class CameraYSortGroup(pygame.sprite.Group):
    """Grupo de sprites com ordenação por eixo Y e câmera que segue o jogador"""
    
    def __init__(self):
        super().__init__()        
        self.display_surface = pygame.display.get_surface()
        
        # Configuração da câmera
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.camera_offset = pygame.math.Vector2()

        # Carrega o chão do mapa
        self.floor_texture = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_texture.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """Renderiza os sprites com ordenação Y e offset de câmera"""
        # Calcula offset para centralizar no jogador
        self.camera_offset.x = player.rect.centerx - self.half_width
        self.camera_offset.y = player.rect.centery - self.half_height

        # Renderiza o chão primeiro
        floor_render_pos = self.floor_rect.topleft - self.camera_offset
        self.display_surface.blit(self.floor_texture, floor_render_pos)

        # Renderiza sprites ordenados pela posição Y (para sobreposição correta)
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            sprite_render_pos = sprite.rect.topleft - self.camera_offset
            self.display_surface.blit(sprite.image, sprite_render_pos)

    def update_enemies(self, player):
        """Atualiza todos os inimigos do grupo"""
        enemies = [s for s in self.sprites() if getattr(s, 'sprite_type', None) == 'enemy']
        for enemy in enemies:
            enemy.update_behavior(player)