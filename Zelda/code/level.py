import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from factories import EntityFactory
from support import load_map_layout, load_image_assets
from sound import SoundManager

class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # sound
        self.sound_manager = SoundManager()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
    
    def create_map(self):
        layouts = {
            'boundary': load_map_layout('../map/map_FloorBlocks.csv'),
            'grass': load_map_layout('../map/map_Grass.csv'),
            'object': load_map_layout('../map/map_Objects.csv'),
            'entities': load_map_layout('../map/map_Entities.csv')
        }

        graphics = {
            'grass': load_image_assets('../graphics/grass'),
            'object': load_image_assets('../graphics/objects'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE

                        if style == 'boundary':
                            EntityFactory.create_entity(
                                'boundary', 
                                (x, y), 
                                [None, self.obstacles_sprites]
                            )
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            EntityFactory.create_entity(
                                'grass',
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                                surface=random_grass_image
                            )
                        elif style == 'object':
                            surf = graphics['object'][int(col)]
                            EntityFactory.create_entity(
                                'object',
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites],
                                surface=surf
                            )
                        elif style == 'entities':
                            if col == '394':
                                self.player = EntityFactory.create_entity(
                                    'player',
                                    (x, y),
                                    [self.visible_sprites],
                                    obstacles_sprites=self.obstacles_sprites,
                                    create_attack=self.create_attack,
                                    destroy_weapon=self.destroy_weapon,
                                )
                            else:
                                monster_name = {
                                    '390': 'bamboo',
                                    '391': 'spirit',
                                    '392': 'raccoon',
                                    '393': 'squid'
                                }.get(col)
                                
                                if monster_name:
                                    EntityFactory.create_entity(
                                        'enemy',
                                        (x, y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        obstacles_sprites=self.obstacles_sprites,
                                        damage_player=self.damage_player,
                                        trigger_death_particles=self.trigger_death_particles,
                                        monster_name=monster_name
                                    )
    
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        self.sound_manager.play('sword') 
    
    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for _ in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
                            self.sound_manager.play('hit')        

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

            if self.player.health <= 0:
                self.animation_player.create_particles('spirit', self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

        if hasattr(self, 'player') and self.player.is_dead:
            if not hasattr(self, 'death_time'):
                self.death_time = pygame.time.get_ticks()
                self.animation_player.create_particles('spirit', self.player.rect.center, [self.visible_sprites])
            
            if pygame.time.get_ticks() - self.death_time > 2000:
                return "game_over"
        
        return "playing"
    
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
