import pygame.time
import pytmx
import pyscroll
from constantes import *
from player import Player
from utils import get_scaled_width
pygame.init()

SWAP_EVENT = pygame.USEREVENT
HIDE_TEXT_EVENT = pygame.USEREVENT + 1


class Game:
    def __init__(self, timing_swap=20):
        self.timing_swap = timing_swap
        self.timer = 0
        self.screen = pygame.display.set_mode((1366, 768))
        self.text = None
        self.start_time = 0

        pygame.display.set_caption('Cat and mouse')
        pygame.display.set_icon(pygame.image.load(fr'{ROOT}/assets/icon.png'))
        pygame.time.set_timer(SWAP_EVENT, timing_swap * 1000)

        #  load and play the main song
        pygame.mixer.music.load(f'{ROOT}/assets/Music/main_song.wav')
        pygame.mixer.music.play(-1)

        #  load map
        tmx_data = pytmx.util_pygame.load_pygame(f'{ROOT}/assets/Background/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        #  resize the map
        map_layer.zoom = SCREEN_WIDTH_REF/1136

        #  set the police
        self.font = pygame.font.Font(f'{ROOT}/assets/Font/Helios Regular.ttf', 30)
        self.font_timer = pygame.font.Font(f'{ROOT}/assets/Font/digital-7 (mono).ttf', 30)

        #  set the panel and its position
        self.panel = pygame.image.load(f'{ROOT}/assets/Win_panel/Panel.png')
        self.rect_panel = self.panel.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))

        #  adds image in group
        self.background_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

        # set clock
        self.clock = pygame.time.Clock()

        # generate players
        self.player1 = Player(self, self.screen, 'player 1', 100, 380, 'Cat', KEYS_P1)
        self.player2 = Player(self, self.screen, 'player 2', 1280, 380, 'Mouse', KEYS_P2)

        self.player1.set_other_player(self.player2)
        self.player2.set_other_player(self.player1)

        self.score = {self.player1.name: 0,
                      self.player2.name: 0,
                      }

        self.reset()

    def reset(self):
        self.player1.reset()
        self.player2.reset()

    def run(self):
        #  main loop
        self.start_time = pygame.time.get_ticks()
        while self.loop_one():
            pass

    def loop_one(self, key_state_function=pygame.key.get_pressed):
        #  draw background
        self.background_group.draw(self.screen)

        self.display_timing(pygame.time.get_ticks()-self.start_time)

        #  management players
        self.player1.update()
        self.player1.update_move(key_state_function())
        self.player2.update_move(key_state_function())
        self.player2.update()

        #  print(pygame.time.get_ticks())

        if self.text is not None:
            text_rect = self.text.get_rect(center=(self.rect_panel.centerx, self.rect_panel.centery))
            self.screen.blit(self.panel, self.rect_panel)
            self.screen.blit(self.text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(self.score)
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
                #  print(pygame.mouse.get_pos())
                #  print(self.player1.rect)

            elif event.type == SWAP_EVENT:
                self.swap_animal_types()
            elif event.type == HIDE_TEXT_EVENT:
                self.text = None

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def swap_animal_types(self):
        tmp_type = self.player2.animal_type
        self.player2.animal_type = self.player1.animal_type
        self.player1.animal_type = tmp_type

    def display_win(self, player):
        self.text = self.font.render(f"{player.name} won!", True, pygame.Color("#000000"))
        pygame.time.set_timer(HIDE_TEXT_EVENT, 1500, 1)

    def display_timing(self, timing):
        res = self.timing_swap*1000 - (timing % (self.timing_swap*1000))

        text_result = self.font_timer.render(f"{res}", True, pygame.Color("#000000"))
        result_rect = text_result.get_rect(center=(get_scaled_width(self.screen, self.screen.get_width()/2), 20))

        self.screen.blit(text_result, result_rect)
