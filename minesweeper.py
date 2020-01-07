""" based on mine_sweeper.py - Copyright 2016 Kenichiro Tanaka """
import sys
from random import randint
from math import floor
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# 화면 크기 1000X1000
WIDTH = 910
HEIGHT = 910
# 위 여백 80 아래 20
# 왼쪽 50 오른쪽 50
P_TOP = 80
P_BOTTOM = 20
P_LEFT = 50
P_RIGHT = 50
# 9X9
BLOCK_NUM_X = 9
BLOCK_NUM_Y = 9
BOMB_NUM = 10

BOMB = -1

pygame.init()
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
FPS_CLOCK = pygame.time.Clock()


def count_bomb(board, x, y, max_x, max_y):
    direction_x = [-1, -1, -1, 0, 0, 1, 1, 1]
    direction_y = [-1, 0, 1, -1, 1, -1, 0, 1]
    count = 0
    for i in range(len(direction_x)):
        t_x = x + direction_x[i]
        t_y = y + direction_y[i]
        if t_x < 0 or t_x > max_x or t_y < 0 or t_y > max_y:
            continue
        if board[t_y][t_x] == -1:
            count += 1

    return count


def openTile(board, check_board, x_pos, y_pos):
    direction_x = [-1, 0, 0, 1]
    direction_y = [0, -1, 1, 0]
    if board[y_pos][x_pos] > 0 and check_board[y_pos][x_pos] == 0:
        check_board[y_pos][x_pos] = 1
    elif board[y_pos][x_pos] == 0 and check_board[y_pos][x_pos] == 0:
        check_board[y_pos][x_pos] = 1
        for i in range(len(direction_x)):
            new_x = x_pos + direction_x[i]
            new_y = y_pos + direction_y[i]

            if new_x < 0 or new_y < 0:
                continue
            elif new_x > 8 or new_y > 8:
                continue
            elif check_board[new_y][new_x] == 1:
                continue
            else:
                openTile(board, check_board, new_x, new_y)


def main():
    # 초기화
    check_board = [[0 for _ in range(BLOCK_NUM_X)] for _ in range(BLOCK_NUM_Y)]
    board = [[0 for _ in range(BLOCK_NUM_X)] for _ in range(BLOCK_NUM_Y)]
    flags = [[-1 for _ in range(BLOCK_NUM_X)] for _ in range(BLOCK_NUM_Y)]
    block_size_x = int((WIDTH - P_LEFT - P_RIGHT) / BLOCK_NUM_X)
    block_size_y = int((HEIGHT - P_TOP - P_BOTTOM) / BLOCK_NUM_Y)
    game_over = False
    open_count = 0
    # font
    small_font = pygame.font.SysFont(None, 70)
    # image
    flag_image = pygame.image.load('./images/flag.png')
    print(block_size_y)
    # 폭탄 배치하기
    for _ in range(BOMB_NUM):
        x_pos = randint(0, BLOCK_NUM_X-1)
        y_pos = randint(0, BLOCK_NUM_Y-1)
        board[y_pos][x_pos] = -1
    # 폭탄 수 세기
    for y in range(BLOCK_NUM_Y):
        for x in range(BLOCK_NUM_X):
            if board[y][x] != -1:
                board[y][x] = count_bomb(board, x, y, BLOCK_NUM_X-1, BLOCK_NUM_Y-1)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                x_pos = floor((event.pos[0] - P_LEFT) / block_size_x)
                y_pos = floor((event.pos[1] - P_TOP) / block_size_y)
                if x_pos < 0 or y_pos < 0:
                    continue
                elif x_pos > BLOCK_NUM_X - 1 or y_pos > BLOCK_NUM_Y - 1:
                    continue
                # 왼쪽 클릭
                if event.button == 1:
                    if board[y_pos][x_pos] == -1:
                        game_over = True
                    elif check_board[y_pos][x_pos] == 1:
                        print("already open")
                    else:
                        openTile(board, check_board, x_pos, y_pos)
                # 오른쪽 클릭
                elif event.button == 3:
                    flags[y_pos][x_pos] = flags[y_pos][x_pos] * -1

        SURFACE.fill((0, 0, 0))
        # 타일 그리기
        for y_pos in range(BLOCK_NUM_Y):
            for x_pos in range(BLOCK_NUM_X):
                # if this block was opened
                rect = (x_pos*block_size_x + P_LEFT, y_pos*block_size_y + P_TOP, block_size_x, block_size_y)
                if check_board[y_pos][x_pos] == 1:
                    tile = board[y_pos][x_pos]
                    if tile > 0:
                        num_image = small_font.render("{}".format(tile), True, (255, 255, 0))
                        SURFACE.blit(num_image, (rect[0] + int(block_size_x/3), rect[1] + int(block_size_y/3)))
                # if this block was closed
                else:
                    if flags[y_pos][x_pos] == 1:
                        SURFACE.blit(flag_image, (rect[0], rect[1]))
                    else:
                        pygame.draw.rect(SURFACE, (150, 220, 140), rect)
        # 선그리기
        for x_pos in range(0, BLOCK_NUM_X+1):
            x_now = x_pos * block_size_x
            pygame.draw.line(SURFACE, (0, 96, 200), (P_LEFT + x_now, P_TOP), (P_LEFT + x_now, HEIGHT-P_BOTTOM), 4)
        for y_pos in range(0, BLOCK_NUM_Y+1):
            y_now = y_pos * block_size_y
            pygame.draw.line(SURFACE, (0, 96, 200), (P_LEFT, P_TOP + y_now), (WIDTH-P_RIGHT, P_TOP + y_now), 4)

        # 화면 업데이트
        pygame.display.update()
        FPS_CLOCK.tick(15)


if __name__ == '__main__':
    main()
