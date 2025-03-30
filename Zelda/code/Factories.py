from entity import Entity
from player import Player
from enemy import Enemy
from tile import Tile
from settings import weapon_data, magic_data, monster_data
import random

class EntityFactory:
    """Factory responsável pela criação centralizada de todas as entidades do jogo"""

    @staticmethod
    def create_entity(entity_type, position, sprite_groups, *args, **kwargs):
        """
        Método principal para criação de entidades

        Args:
            entity_type (str): Tipo da entidade ('player', 'enemy', etc.)
            position (tuple): Posição (x, y) inicial
            sprite_groups (list): Lista de grupos de sprites

        Returns:
            Entity: Uma instância da entidade solicitada

        Raises:
            ValueError: Se o tipo de entidade não for reconhecido
        """
        creation_methods = {
            'player': EntityFactory._create_player_entity,
            'enemy': EntityFactory._create_enemy_entity,
            'boundary': EntityFactory._create_boundary_tile,
            'grass': EntityFactory._create_grass_tile,
            'object': EntityFactory._create_object_tile
        }

        if entity_type not in creation_methods:
            raise ValueError(f"Tipo de entidade desconhecido: {entity_type}")

        # Filtra kwargs específicos para cada tipo de entidade
        method = creation_methods[entity_type]
        method_params = method.__code__.co_varnames[:method.__code__.co_argcount]

        filtered_kwargs = {
            k: v for k, v in kwargs.items()
            if k in method_params and k not in ['position', 'sprite_groups']
        }

        return method(position, sprite_groups, *args, **filtered_kwargs)

    @staticmethod
    def _create_player_entity(position, sprite_groups, collision_sprites,
                              attack_creation_callback, weapon_destruction_callback,
                              magic_creation_callback):
        """
        Cria uma instância do jogador.

        Args:
            position (tuple): Posição inicial do jogador (x, y)
            sprite_groups (list): Lista de grupos de sprites
            collision_sprites (pygame.sprite.Group): Grupo de sprites com colisão
            attack_creation_callback (function): Callback para criação de ataques
            weapon_destruction_callback (function): Callback para remoção de armas
            magic_creation_callback (function): Callback para criação de magias

        Returns:
            Player: Uma instância do jogador
        """
        return Player(
            position=position,
            sprite_groups=sprite_groups,
            collision_sprites=collision_sprites,
            attack_creation_callback=attack_creation_callback,
            weapon_destruction_callback=weapon_destruction_callback,
            magic_creation_callback=magic_creation_callback
        )

    @staticmethod
    def _create_enemy_entity(position, sprite_groups, collision_sprites,
                             damage_player_callback, trigger_death_particles,
                             enemy_type=None):
        """
        Cria uma instância de inimigo.

        Args:
            position (tuple): Posição inicial do inimigo (x, y)
            sprite_groups (list): Lista de grupos de sprites
            collision_sprites (pygame.sprite.Group): Grupo de sprites com colisão
            damage_player_callback (function): Callback para aplicar dano ao jogador
            trigger_death_particles (function): Callback para ativar partículas de morte
            enemy_type (str, opcional): Nome do tipo de inimigo (caso não informado, será aleatório)

        Returns:
            Enemy: Uma instância de inimigo
        """
        if not enemy_type:
            enemy_type = random.choice(list(monster_data.keys()))

        return Enemy(
            enemy_type=enemy_type,
            position=position,
            sprite_groups=sprite_groups,
            collision_sprites=collision_sprites,
            damage_player_callback=damage_player_callback,
            trigger_death_particles=trigger_death_particles,
        )

    @staticmethod
    def _create_boundary_tile(position, sprite_groups, *args, **kwargs):
        """
        Cria um tile de boundary (invisível, apenas colisão).

        Args:
            position (tuple): Posição inicial do tile (x, y)
            sprite_groups (list): Lista de grupos de sprites

        Returns:
            Tile: Um tile de boundary
        """
        return Tile(
            position=position,
            groups=[sprite_groups[1]],  # Usa apenas o grupo de colisão
            sprite_type='invisible'
        )

    @staticmethod
    def _create_grass_tile(position, sprite_groups, surface=None, *args, **kwargs):
        """
        Cria um tile de grama (cortável).

        Args:
            position (tuple): Posição inicial do tile (x, y)
            sprite_groups (list): Lista de grupos de sprites
            surface (pygame.Surface, opcional): Superfície da grama

        Returns:
            Tile: Um tile de grama
        """
        return Tile(
            position=position,
            groups=sprite_groups,  # Usa todos os grupos fornecidos
            sprite_type='grass',
            surface=surface
        )

    @staticmethod
    def _create_object_tile(position, sprite_groups, surface=None, *args, **kwargs):
        """
        Cria um tile de objeto (decorativo/com colisão).

        Args:
            position (tuple): Posição inicial do tile (x, y)
            sprite_groups (list): Lista de grupos de sprites
            surface (pygame.Surface, opcional): Superfície do objeto

        Returns:
            Tile: Um tile de objeto decorativo ou de colisão
        """
        return Tile(
            position=position,
            groups=[sprite_groups[0], sprite_groups[1]],  # Visível + colisão
            sprite_type='object',
            surface=surface
        )
