from support import import_folder

class Animation:
    def __init__(self, player):
        self.player = player
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

    def import_player_assets(self):
        character_path = './graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def update_status(self):
        # idle status
        if self.player.direction.x == 0 and self.player.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.player.attacking:
            self.player.direction.x = 0
            self.player.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.player.image = animation[int(self.frame_index)]
        self.player.rect = self.player.image.get_rect(center=self.player.hitbox.center)