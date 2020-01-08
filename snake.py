""" snake_bite.py - Copyright 2016 Kenichiro Tanaka """

import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, Rect

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPS_CLOCK = pygame.time.Clock()

FOODS = []
SNAKE = []
(W, H) = (20, 20)


def add_food():
    # 먹이를 임의의 장소에 배치
    while True:
        pos = (random.randint(0, W-1), random.randint(0, H-1))
        if pos in FOODS or pos in SNAKE:
            continue
        FOODS.append(pos)
        break


# 먹이 옮기기
def move_food(pos):
    i = FOODS.index(pos)
    del FOODS[i]
    add_food()


# 화면 그리기
def paint(message):
    SURFACE.fill((0, 0, 0))
    for food in FOODS:
        pygame.draw.ellipse(SURFACE, (0, 255, 0),
                            Rect(food[0]*30, food[1]*30, 30, 30))
    for body in SNAKE:
        pygame.draw.rect(SURFACE, (0, 255, 255), Rect(body[0]*30, body[1]*30, 30, 30))

    for index in range(20):
        pygame.draw.line(SURFACE, (64, 64, 64), (index*30, 0),
                         (index*30, 600))
        pygame.draw.line(SURFACE, (64, 64, 64), (0, index*30), (600, index*30))

    if not (message is None):
        SURFACE.blit(message, (150, 300))
    pygame.display.update()


def main():
    # main routine
    my_font = pygame.font.SysFont(None, 80)
    key = K_DOWN
    message = None
    game_over = False
    SNAKE.append((int(W/2), int(H/2)))
    head = None
    for _ in range(10):
        add_food()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key


        if not game_over:
            if key == K_LEFT:
                head = (SNAKE[0][0] - 1, SNAKE[0][1])
            elif key == K_RIGHT:
                head = (SNAKE[0][0] + 1, SNAKE[0][1])
            elif key == K_UP:
                head = (SNAKE[0][0], SNAKE[0][1] - 1)
            elif key == K_DOWN:
                head = (SNAKE[0][0], SNAKE[0][1] + 1)

        if head in SNAKE or head[0] < 0 or head[0] >= W or \
                head[1] < 0 or head[1] >= H:
            message = my_font.render("GAME OVER!", True, (255, 255, 0))
            game_over = True

        SNAKE.insert(0, head)
        if head in FOODS:
            move_food(head)
        else:
            SNAKE.pop()

        paint(message)
        FPS_CLOCK.tick(5)


if __name__ == '__main__':
    main()
