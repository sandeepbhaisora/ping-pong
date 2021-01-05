import os, sys
import pygame
from pygame.locals import *

pygame.init()

if not pygame.font:
    print("font disabled ")
if not pygame.mixer:
    print("sound disabled")

is_over = False
myfont = pygame.font.SysFont("monospace", 40)
myfont2 = pygame.font.SysFont("orange juice", 80)

size = width, height = 1200, 800
bar_speed = 160


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = 255, 0, 0
        x_pos, y_pos = 600, 400
        self.x_speed = 5
        self.y_speed = 4
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.start = False

    def _move(self):
        if self.start:
            self.x_pos += self.x_speed
            self.y_pos += self.y_speed
            if self.x_pos > width or self.x_pos < 0:
                self.is_over = True
                self.__init__()

            if self.y_pos > height or self.y_pos < 0:
                self.y_speed = -self.y_speed

    def _draw_circle(self):
        screen = pygame.display.get_surface()
        black = 0, 0, 0
        screen.fill(black)
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), 20)


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = (0, 255, 255)
        self.left = 0
        self.top = 120
        self.width = 20
        self.height = 200

    def _draw_rect(self):
        rect = Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)

    def _move_bar(self, y):
        if self.top >= 0 and (self.top <= height - self.height):
            top = self.top + y
            if top < 0:
                top = 0
            elif (top + self.height) > height:
                top = height - self.height
            self.top = top

    def is_colliding(self, object):
        ball_x, ball_y = object.x_pos, object.y_pos
        if ball_y > self.top and ball_y < self.top + self.height:
            if ball_x > self.left and ball_x < self.left + self.width:
                object.x_speed = -object.x_speed
                object.score += 10
                object.x_speed += 1
                object.y_speed += 1
        return object


if __name__ == '__main__':
    pygame.display.set_caption("PING PONG")
    screen = pygame.display.set_mode(size)
    ball = Ball()
    ball.is_over = False
    ball.score = 0
    left_bar = Bar()
    right_bar = Bar()
    right_bar.left = width - 20
    allsprites = pygame.sprite.RenderPlain((ball, right_bar))
    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not ball.start:
                    ball.start = True
                    ball.is_over = False
                    ball.score = 0
                if event.key == pygame.K_DOWN:
                    right_bar._move_bar(y=bar_speed)
                if event.key == pygame.K_UP:
                    right_bar._move_bar(y=-bar_speed)
                if event.key == pygame.K_w:
                    left_bar._move_bar(y=-bar_speed)
                if event.key == pygame.K_s:
                    left_bar._move_bar(y=bar_speed)
        ball._draw_circle()
        left_bar._draw_rect()
        right_bar._draw_rect()
        scoretext = myfont.render("Score = " + str(ball.score), True, (0, 233, 0))
        screen.blit(scoretext, (5, 10))
        ball = left_bar.is_colliding(object=ball)
        ball = right_bar.is_colliding(object=ball)
        ball._move()
        if ball.is_over:
            scoretext = myfont2.render( r"GAME OVER ", True, (123, 23, 233))
            screen.blit(scoretext, (400, 280))
        pygame.display.flip()
