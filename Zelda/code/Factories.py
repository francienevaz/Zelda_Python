from code.entity import Entity
from code.player import Player
from code.enemy import Enemy
from code.tile import Tile
from code.settings import weapon_data, monster_data
import random

class EntityFactory:
    @staticmethod
    def create_entity(entity_type, pos, groups, *args, **kwargs):
        if entity_type == "player":
            return EntityFactory.create_player(pos, groups, *args, **kwargs)
        elif entity_type == "enemy":
            return EntityFactory.create_enemy(pos, groups, *args, **kwargs)
        elif entity_type in ["boundary", "grass", "object"]:
            return EntityFactory.create_tile(entity_type, pos, groups, *args, **kwargs)
        else:
            raise ValueError(f"Tipo de entidade desconhecido: {entity_type}")

    @staticmethod
    def create_player(pos, groups, obstacles_sprites, create_attack, destroy_weapon):
        return Player(
            pos=pos,
            groups=groups,
            obstacles_sprites=obstacles_sprites,
            create_attack=create_attack,
            destroy_weapon=destroy_weapon,
        )

    @staticmethod
    def create_enemy(pos, groups, obstacles_sprites, damage_player, trigger_death_particles, monster_name=None):
        if not monster_name:
            monster_name = random.choice(list(monster_data.keys()))
        return Enemy(
            monster_name=monster_name,
            pos=pos,
            groups=groups,
            obstacles_sprites=obstacles_sprites,
            damage_player=damage_player,
            trigger_death_particles=trigger_death_particles
        )

    @staticmethod
    def create_tile(tile_type, pos, groups, surface=None):
        if tile_type == "boundary":
            # Ajuste importante: boundary deve ir apenas para obstacles_sprites
            return Tile(pos, [groups[1]], 'invisible')  # groups[1] é obstacles_sprites
        elif tile_type == "grass":
            # Grass vai para visible, obstacles e attackable
            return Tile(pos, groups, 'grass', surface)
        elif tile_type == "object":
            # Objects vão para visible e obstacles
            return Tile(pos, [groups[0], groups[1]], 'object', surface)