import pygame
from support import load_image_assets
from random import choice

class ParticleSystem:
    """Gerencia todos os efeitos de partículas do jogo, incluindo carregamento e animação"""
    
    def __init__(self):
        # Carrega todos os frames de animação de partículas
        self.particle_animations = self._load_particle_assets()
    
    def _load_particle_assets(self):
        """Carrega e organiza todos os assets de partículas em categorias"""
        return {
            # Efeitos mágicos
            'magic': {
                'flame': load_image_assets('../graphics/particles/flame/frames'),
                'aura': load_image_assets('../graphics/particles/aura'),
                'heal': load_image_assets('../graphics/particles/heal/frames')
            },
            
            # Efeitos de ataque
            'attacks': {
                'claw': load_image_assets('../graphics/particles/claw'),
                'slash': load_image_assets('../graphics/particles/slash'),
                'sparkle': load_image_assets('../graphics/particles/sparkle'),
                'leaf_attack': load_image_assets('../graphics/particles/leaf_attack'),
                'thunder': load_image_assets('../graphics/particles/thunder')
            },

            # Efeitos de morte de monstros
            'monster_death': {
                'squid': load_image_assets('../graphics/particles/smoke_orange'),
                'raccoon': load_image_assets('../graphics/particles/raccoon'),
                'spirit': load_image_assets('../graphics/particles/nova'),
                'bamboo': load_image_assets('../graphics/particles/bamboo')
            },
            
            # Efeitos ambientais
            'environment': {
                'leaf': self._prepare_leaf_animations()
            }
        }
    
    def _prepare_leaf_animations(self):
        """Prepara as variações de animação para folhas (incluindo versões espelhadas)"""
        leaf_variants = []
        for i in range(1, 7):
            base_frames = load_image_assets(f'../graphics/particles/leaf{i}')
            leaf_variants.append(base_frames)
            leaf_variants.append(self._create_flipped_frames(base_frames))
        return tuple(leaf_variants)
    
    def _create_flipped_frames(self, frames):
        """Cria versões espelhadas horizontalmente dos frames de animação"""
        return [pygame.transform.flip(frame, True, False) for frame in frames]
    
    def spawn_grass_effect(self, position, sprite_groups):
        """Cria efeito de partículas para grama cortada"""
        random_leaf_frames = choice(self.particle_animations['environment']['leaf'])
        ParticleAnimation(position, random_leaf_frames, sprite_groups)
    
    def spawn_effect(self, effect_type, position, sprite_groups):
        """
        Cria um efeito de partícula genérico
        
        Args:
            effect_type (str): Tipo de efeito (ex: 'flame', 'slash')
            position (tuple): Posição (x,y) onde o efeito aparecerá
            sprite_groups (list): Grupos de sprites para adicionar o efeito
        """
        # Procura o efeito em todas as categorias
        for category in self.particle_animations.values():
            if effect_type in category:
                ParticleAnimation(position, category[effect_type], sprite_groups)
                return
        
        raise ValueError(f"Tipo de efeito desconhecido: {effect_type}")


class ParticleAnimation(pygame.sprite.Sprite):
    """Representa uma única instância de animação de partícula"""
    
    def __init__(self, position, animation_frames, sprite_groups):
        """
        Inicializa uma animação de partícula
        
        Args:
            position (tuple): Posição (x,y) central da partícula
            animation_frames (list): Lista de frames de animação
            sprite_groups (list): Grupos de sprites para adicionar esta animação
        """
        super().__init__(sprite_groups)
        self.current_frame_index = 0
        self.animation_speed = 0.15
        self.animation_frames = animation_frames
        self.image = self.animation_frames[self.current_frame_index]
        self.rect = self.image.get_rect(center=position)
    
    def update_animation(self):
        """Atualiza o frame atual da animação e finaliza quando completa"""
        self.current_frame_index += self.animation_speed
        
        if self.current_frame_index >= len(self.animation_frames):
            self.kill()  # Remove o sprite quando a animação termina
        else:
            self.image = self.animation_frames[int(self.current_frame_index)]
    
    def update(self):
        """Método chamado a cada frame para atualizar a partícula"""
        self.update_animation()