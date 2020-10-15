import random

import pygame
import constants as const
from game.bullet import Bullet


class Plane(pygame.sprite.Sprite):
    plane_images = []
    destroy_images = []
    destroy_sound_src = []
    active = True
    # 子弹精灵组
    bullets = pygame.sprite.Group()

    def __init__(self, screen, speed=10):
        super().__init__()
        self.screen = screen

        self.img_list = []
        self.destroy_img_list = []
        self.destory_sound = None
        self.load_src()

        self.speed = speed
        self.rect = self.img_list[0].get_rect()

        self.plane_w, self.plane_h = self.img_list[0].get_size()
        self.screen_w, self.screen_h = self.screen.get_size()
        self.rect.left = (self.screen_w - self.plane_w) // 2
        self.rect.top = self.screen_h - 2 * self.plane_h

    def load_src(self):
        for img in self.plane_images:
            self.img_list.append(pygame.image.load(img))

        for img in self.destroy_images:
            self.destroy_img_list.append(pygame.image.load(img))

        if self.destroy_sound_src:
            self.destory_sound = pygame.mixer.Sound(self.destroy_sound_src)

    @property
    def image(self):
        return self.img_list[0]

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        self.rect.top -= self.speed

    def move_down(self):
        self.rect.top += self.speed

    def move_left(self):
        self.rect.left -= self.speed

    def move_right(self):
        self.rect.left += self.speed

    def broken_down(self):
        if self.destory_sound:
            self.destory_sound.play()
        for img in self.destroy_img_list:
            self.screen.blit(img, self.rect)
        self.active = False

    def shoot(self):
        bullet = Bullet(self.screen, self, 15)
        self.bullets.add(bullet)


class MyPlane(Plane):
    plane_images = const.MY_PLANE_IMG_LIST
    destroy_images = const.MY_PALEN_DESTROY_IMG_LIST
    down_sound_src = None
    key_down = None

    def update(self, war):
        self.move(self.key_down)

        if (war.frame // 3) & 1:
            self.screen.blit(self.img_list[0], self.rect)
        else:
            self.screen.blit(self.img_list[1], self.rect)

        result = pygame.sprite.spritecollide(self, war.enemies, False)
        if result:
            war.status = const.END

            war.enemies.empty()
            war.small_enemies.empty()

            self.broken_down()

    def move(self, key):
        if key == pygame.K_w or key == pygame.K_UP:
            self.move_up()
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.move_down()
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.move_left()
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.move_right()

    def move_up(self):
        if self.rect.top >= 0:
            super().move_up()

    def move_down(self):
        if self.rect.top <= self.screen_h - self.plane_h:
            super().move_down()

    def move_left(self):
        if self.rect.left >= 0:
            super().move_left()

    def move_right(self):
        if self.rect.left <= self.screen_w - self.plane_w:
            super().move_right()

class SmallEnemyPlane(Plane):
    plane_images = const.SMALL_ENEMY_PLANE_IMG_LIST
    destroy_images = const.SMALL_ENEMY_DESTROY_IMG_LIST
    destroy_sound_src = const.SMALL_ENEMY_PLANE_DESTROY_SOUND

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        self.init_pos()

    def init_pos(self):
        self.rect.left = random.randint(0, self.screen_w - self.plane_w)
        self.rect.top = random.randint(-5 * self.plane_h, - self.plane_h)

    def update(self, *args):
        super().move_down()

        self.blit()
        if self.rect.top >= self.screen_h:
            self.active = False
            # 重用
            self.reset()

    def reset(self):
        self.active = True
        self.init_pos()

    def broken_down(self):
        super().broken_down()
        self.reset()


