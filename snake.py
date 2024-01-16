import pygame
import random as rd
from constants import Config as cfg


class Point:
    global object_list

    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.pos_X = rd.randint(0, cfg.game_width)
        self.pos_Y = rd.randint(0, cfg.game_height)
        object_list.append(self)

    def display(self):
        pygame.draw.circle(screen, self.color, (self.pos_X, self.pos_Y), self.size)


def main_interface():
    screen.fill(cfg.color_dict[0])
    curr_key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    if curr_key[pygame.K_q]:
        pygame.quit()

    return True


def main():
    running = True
    for _ in range(100):
        Point(cfg.point_size, cfg.color_dict[2])
    while running:
        running = main_interface()
        for object in object_list:
            object.display()
        pygame.display.flip()
        clock.tick(60)


pygame.init()
object_list = []
screen = pygame.display.set_mode((cfg.game_width, cfg.game_height), vsync=1)
clock = pygame.time.Clock()
main()
