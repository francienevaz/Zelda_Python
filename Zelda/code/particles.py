import pygame
from code.support import load_image_assets
from random import choice
from code.settings import *

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': load_image_assets(resource_path('graphics/particles/flame/frames')),
            'aura': load_image_assets(resource_path('graphics/particles/aura')),
            'heal': load_image_assets(resource_path('graphics/particles/heal/frames')),

            # attacks
            'claw': load_image_assets(resource_path('graphics/particles/claw')),
            'slash': load_image_assets(resource_path('graphics/particles/slash')),
            'sparkle': load_image_assets(resource_path('graphics/particles/sparkle')),
            'leaf_attack': load_image_assets(resource_path('graphics/particles/leaf_attack')),
            'thunder': load_image_assets(resource_path('graphics/particles/thunder')),

            # monster deaths
            'squid': load_image_assets(resource_path('graphics/particles/smoke_orange')),
            'raccoon': load_image_assets(resource_path('graphics/particles/raccoon')),
            'spirit': load_image_assets(resource_path('graphics/particles/nova')),
            'bamboo': load_image_assets(resource_path('graphics/particles/bamboo')),

            # leafs
            'leaf': (
                load_image_assets(resource_path('graphics/particles/leaf1')),
                load_image_assets(resource_path('graphics/particles/leaf2')),
                load_image_assets(resource_path('graphics/particles/leaf3')),
                load_image_assets(resource_path('graphics/particles/leaf4')),
                load_image_assets(resource_path('graphics/particles/leaf5')),
                load_image_assets(resource_path('graphics/particles/leaf6')),
                self.reflect_images(load_image_assets(resource_path('graphics/particles/leaf1'))),
                self.reflect_images(load_image_assets(resource_path('graphics/particles/leaf2'))),
                self.reflect_images(load_image_assets(resource_path('graphics/particles/leaf3'))),
                self.reflect_images(load_image_assets(resource_path('graphics/particles/leaf4'))),
                self.reflect_images(load_image_assets(resource_path('graphics/particles/leaf5'))),
                self.reflect_images(load_image_assets(resource_path('graphics/particles/leaf6')))
            )
        }

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()