import pygame
from settings import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'sword': pygame.mixer.Sound('../audio/sword.wav'),
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'hit':pygame.mixer.Sound('../audio/hit.wav'),
            'death': pygame.mixer.Sound('../audio/death.wav')
            
        }
        
        # Ajusta volumes
        for sound in self.sounds.values():
            sound.set_volume(VOLUME_SFX)
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()