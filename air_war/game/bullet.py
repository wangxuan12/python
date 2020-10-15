import pygame
import constants as const

class Bullet(pygame.sprite.Sprite):
    active = True

    def __init__(self, screen, plane, speed=10):
        super().__init__()
        self.screen = screen
        self.plane = plane
        self.speed = speed

        self.image = pygame.image.load(const.BULLET_IMG)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.plane.rect.centerx
        self.rect.top = self.plane.rect.top

        self.shoot_sound = pygame.mixer.Sound(const.BULLET_SHOOT_SOUND)
        self.shoot_sound.set_volume(0.3)
        self.shoot_sound.play()

    def update(self, war):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.remove(self.plane.bullets)

        self.screen.blit(self.image, self.rect)

        result = pygame.sprite.spritecollide(self, war.enemies, False)
        for dead in result:
            self.kill()

            dead.broken_down()

            war.result.score += const.SCORE_SHOOT_SMALL