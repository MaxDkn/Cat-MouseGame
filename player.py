from constantes import *
from utils import get_scaled_height, get_scaled_width, cut_image, load_animations


class Player(pygame.sprite.Sprite):
    sprint_position_and_size_in_sheet = {
        'Mouse': {
            'Idle': [
                (1, 23, 25, 9, 0, 0),
                (33, 22, 25, 10, 0, 0),
                (65, 21, 25, 11, 0, 0),
                (97, 22, 25, 10, 0, 0),
            ],
            'Walk': [
                (1, 23, 25, 9, 0, 0),
                (33, 21, 25, 11, 0, 0),
                (65, 21, 25, 11, 0, 0),
                (97, 23, 25, 9, 0, 0),
            ],
        },
        'Cat': {
            'Idle': [
                (6, 29, 24, 19, 0, 0),
                (54, 28, 24, 20, 0, -1),
                (102, 28, 25, 20, 0, -1),
                (151, 29, 24, 19, 1, 0),
            ],
            'Walk': [
                (5, 29, 25, 19, 0, 0),
                (51, 29, 28, 19, 0, 0),
                (96, 29, 31, 20, 0, 0),
                (146, 28, 29, 20, 0, 0),
                (193, 28, 29, 20, 0, 0),
                (242, 29, 28, 19, 0, 0),
            ],
        },
    }

    delta_speeds = {
        'Mouse': 3,
        'Cat': 2,
    }

    def __init__(self, game, screen, name, initial_x, initial_y, animal_type, keys):
        super().__init__()
        self.game = game
        self.screen = screen
        self.initial_x = get_scaled_width(self.screen, initial_x)
        self.initial_y = get_scaled_height(self.screen, initial_y)
        self.animal_type = animal_type
        self.keys = keys
        self.name = name

        # set variable
        self.update_time = pygame.time.get_ticks()
        self.speed = get_scaled_width(self.screen, 2)
        self.flip = False
        self.action = 'Idle'  # set idle animation
        self.index = 0
        self.score = 0
        self.other_player = None
        self.delta_speed = self.delta_speeds[self.animal_type]
        self.direction = pygame.math.Vector2()

        #  default image
        self.image = cut_image(1, 21, 25, 11, 0, 0, pygame.image.load(f'{ROOT}/assets/Animal/Mouse/Idle.png'))
        #  resize the image
        self.image = pygame.transform.scale(self.image, (25, 11))
        #  and removes the background of the image
        self.image.set_colorkey([0, 0, 0])

        #  set the animation list

        self.animations = load_animations(self.sprint_position_and_size_in_sheet)
        self.reset()

    def reset(self):
        #  set initial position of the rectangle
        self.rect = self.animations[self.animal_type]['Walk'][1].get_rect()
        self.rect.centerx = self.initial_x
        self.rect.centery = self.initial_y

    def win(self):
        self.score += 1
        self.game.score[self.name] += 1

    def update_animation(self):
        # update animation
        animation_cool_down = 100

        if pygame.time.get_ticks() - self.update_time > animation_cool_down:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        self.index = self.index % len(self.animations[self.animal_type][self.action])
        self.image = self.animations[self.animal_type][self.action][self.index]

    def update(self):
        self.update_animation()
        self.draw()
        self.delta_speed = self.delta_speeds[self.animal_type]
        self.speed = get_scaled_width(self.screen, self.delta_speed)

    def update_move(self, pressed):
        self.action = 'Idle'
        if pressed[self.keys[0]] and self.rect.left > 39:  # left
            self.rect.x -= self.speed
            self.action = 'Walk'
            self.flip = True
        if pressed[self.keys[1]] and self.rect.right < 1322:  # right
            self.rect.x += self.speed
            self.action = 'Walk'
            self.flip = False
        if pressed[self.keys[2]] and self.rect.y > 40:  # up
            self.rect.y -= self.speed
            self.action = 'Walk'
        if pressed[self.keys[3]] and self.rect.bottom < 728:  # down --> check collide with the floor
            self.rect.y += self.speed
            self.action = 'Walk'
        if self.animal_type == 'Cat':
            if self.check_collide():
                self.win()
                self.game.display_win(self)
                self.game.reset()

    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def check_collide(self):
        return self.rect.colliderect(self.other_player.rect)

    def set_other_player(self, player):
        self.other_player = player
