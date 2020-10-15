import sys
import pygame
import constants as const
from game.plane import MyPlane, SmallEnemyPlane
from store.result import GameResult


class AirWar:
    status = const.READY

    my_plane = None

    frame = 0

    small_enemies = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    result = GameResult()

    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 480, 852

        self.screen = pygame.display.set_mode(self.size)

        self.bg = pygame.image.load(const.BG_IMG)
        self.bg_end = pygame.image.load(const.BG_IMG_END)
        pygame.display.set_caption('Air War')

        pygame.mixer_music.load(const.BG_MUSIC)
        pygame.mixer_music.play(-1)
        pygame.mixer_music.set_volume(0.2)

        self.title_iamge = pygame.image.load(const.IMAGE_GAME_TITLE)
        self.title_iamge_rect = self.title_iamge.get_rect()
        self.t_width, self.t_height = self.title_iamge.get_size()
        self.title_iamge_rect.topleft = ((self.width - self.t_width) // 2, self.height // 2 - self.t_height)

        self.start_btn = pygame.image.load(const.IMAGE_GAME_START_BTN)
        self.start_btn_rect = self.start_btn.get_rect()
        self.sbtn_width, self.sbtn_height = self.start_btn.get_size()
        self.start_btn_rect.topleft = ((self.width - self.sbtn_width) // 2, self.height // 2 + self.sbtn_height)

        self.score_font = pygame.font.SysFont('华文隶书', 32)

        self.my_plane = MyPlane(self.screen, speed=4)

        self.clock = pygame.time.Clock()

    def bind_event(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type is pygame.MOUSEBUTTONDOWN:
                if self.status is const.READY:
                    self.status = const.RUNNING
                elif self.status is const.END:
                    self.status = const.READY
                    self.add_small_enemies(const.SMALL_ENEMY_NUM)
            elif event.type is pygame.KEYDOWN:
                if self.status is const.RUNNING:
                    if event.key is pygame.K_w or event.key is pygame.K_UP:
                        self.my_plane.move_up()
                        self.my_plane.key_down = event.key
                    elif event.key is pygame.K_s or event.key is pygame.K_DOWN:
                        self.my_plane.move_down()
                        self.my_plane.key_down = event.key
                    elif event.key is pygame.K_a or event.key is pygame.K_LEFT:
                        self.my_plane.move_left()
                        self.my_plane.key_down = event.key
                    elif event.key is pygame.K_d or event.key is pygame.K_RIGHT:
                        self.my_plane.move_right()
                        self.my_plane.key_down = event.key
                    elif event.key is pygame.K_j:
                        self.my_plane.shoot()
            elif event.type is pygame.KEYUP:
                if self.status is const.RUNNING or self.status is const.END:
                    self.my_plane.key_down = None

    def add_small_enemies(self, num):
        for i in range(num):
            plane = SmallEnemyPlane(self.screen, 4)
            plane.add(self.small_enemies, self.enemies)

    def run_game(self):
        self.clock.tick(60)

        while True:
            self.frame += 1
            if self.frame >= 60:
                self.frame = 0

            self.bind_event()


            if self.status is const.READY:
                self.screen.blit(self.bg, self.bg.get_rect())
                self.screen.blit(self.title_iamge, self.title_iamge_rect)
                self.screen.blit(self.start_btn, self.start_btn_rect)
            elif self.status is const.RUNNING:
                self.screen.blit(self.bg, self.bg.get_rect())
                self.my_plane.blit()
                self.my_plane.update(self)
                self.my_plane.bullets.update(self)
                self.small_enemies.update()

                score_text = self.score_font.render(
                    '得分: {0}'.format(self.result.score),
                    False,
                    const.TEXT_SOCRE_COLOR
                )
                self.screen.blit(score_text, score_text.get_rect())
            elif self.status is const.END:
                self.screen.blit(self.bg_end, self.bg_end.get_rect())

                score_text = self.score_font.render(
                    '{0}'.format(self.result.score),
                    False,
                    const.TEXT_SOCRE_COLOR
                )
                score_text_rect = score_text.get_rect()
                text_w, text_h = score_text.get_size()

                score_text_rect.topleft = (
                    (self.width - text_w) // 2,
                    self.height // 2
                )
                self.screen.blit(score_text, score_text_rect)

                score_history = self.score_font.render(
                    '{0}'.format(self.result.get_max_score()),
                    False,
                    const.TEXT_SOCRE_COLOR
                )
                self.screen.blit(score_history, (150, 40))

            pygame.display.flip()