import pygame
from code.settings import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'sword': pygame.mixer.Sound(resource_path('audio/sword.wav')),
            'heal': pygame.mixer.Sound(resource_path('audio/heal.wav')),
            'hit':pygame.mixer.Sound(resource_path('audio/hit.wav')),
            'death': pygame.mixer.Sound(resource_path('audio/death.wav')),
            
        }
        
        # Ajusta volumes
        for sound in self.sounds.values():
            sound.set_volume(VOLUME_SFX)
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()