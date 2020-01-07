import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
FPS_CLOCK = pygame.time.Clock()




def main():
    sys_font = pygame.font.SysFont(None, 36)
    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        counter += 1

        SURFACE.fill((0, 0, 0))
        count_image = sys_font.render(
            "count is {}".format(counter), True, (255, 255, 255)
        )
        SURFACE.blit(count_image, (50, 50))
        pygame.display.update()
        FPS_CLOCK.tick(10)


if __name__ == '__main__':
    main()
