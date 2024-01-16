from re import L
import pygame
import random as rd
from constants import Config as cfg


class Snake:
    def __init__(self, parts_number):
        self.parts_number = parts_number
        self.parts = []
        self.direction = 0
        self.create_initial_body()

    def create_initial_body(self):
        for i in range(self.parts_number):
            if i == 0:
                self.parts.append(
                    Part(
                        cfg.general_size,
                        cfg.color_dict[1],
                        cfg.start_X,
                        cfg.start_Y,
                        None,
                    )
                )
            else:
                self.parts.append(
                    Part(
                        cfg.general_size,
                        cfg.color_dict[1],
                        cfg.start_X - i * cfg.general_size,
                        cfg.start_Y,
                        i - 1,
                    )
                )

    def move(self, point):
        hit = False
        game_over = False
        if self.direction == 0:
            self.parts[0].pos_Y -= cfg.general_size
            game_over = self.check_collision()
            hit = self.check_hit(point)
            self.follow()
        elif self.direction == 1:
            self.parts[0].pos_Y += cfg.general_size
            game_over = self.check_collision()
            hit = self.check_hit(point)
            self.follow()
        elif self.direction == 2:
            self.parts[0].pos_X -= cfg.general_size
            self.check_collision()
            game_over = self.check_collision()
            hit = self.check_hit(point)
            self.follow()
        elif self.direction == 3:
            self.parts[0].pos_X += cfg.general_size
            self.check_collision()
            game_over = self.check_collision()
            hit = self.check_hit(point)
            self.follow()

        return hit, game_over

    def change_direction(self, key):
        if key[pygame.K_w]:
            self.direction = 0
        if key[pygame.K_s]:
            self.direction = 1
        if key[pygame.K_a]:
            self.direction = 2
        if key[pygame.K_d]:
            self.direction = 3

    def follow(self):
        pointer1_X = self.parts[0].pos_X
        pointer1_Y = self.parts[0].pos_Y
        pointer2_X = self.parts[0].pos_X
        pointer2_Y = self.parts[0].pos_Y
        for idx, part in enumerate(self.parts):
            if idx == 0:
                continue
            if idx % 2 == 0:
                pointer1_X = part.pos_X
                pointer1_Y = part.pos_Y
                part.pos_X = pointer2_X
                part.pos_Y = pointer2_Y
            else:
                pointer2_X = part.pos_X
                pointer2_Y = part.pos_Y
                part.pos_X = pointer1_X
                part.pos_Y = pointer1_Y

    def check_collision(self):
        pointer1_X = self.parts[0].pos_X
        pointer1_Y = self.parts[0].pos_Y
        for idx, part in enumerate(self.parts):
            if idx == 0:
                continue
            if pointer1_X == part.pos_X and pointer1_Y == part.pos_Y:
                return True
        if pointer1_X >= cfg.game_width or pointer1_X <= 0:
            return True
        if pointer1_Y >= cfg.game_height or pointer1_Y <= 0:
            return True

    def check_hit(self, point):
        head_rad = self.parts[0].size
        point_rad = point.size
        head_vec2 = pygame.Vector2((self.parts[0].pos_X, self.parts[0].pos_Y + 10))
        point_vec2 = pygame.Vector2((point.pos_X, point.pos_Y))
        distance = head_vec2.distance_to(point_vec2)
        if distance < head_rad + point_rad:
            return True

    def generate_part(self):
        self.parts.append(
            Part(
                cfg.general_size,
                cfg.color_dict[1],
                cfg.start_X - len(self.parts) * cfg.general_size,
                cfg.start_Y,
                len(self.parts) - 1,
            )
        )

    def display(self):
        for part in self.parts:
            part.display()


class Part:
    def __init__(self, size, color, pos_X, pos_Y, follow):
        self.size = size
        self.color = color
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.follow = follow

    def display(self):
        pygame.draw.rect(
            screen, self.color, (self.pos_X, self.pos_Y, self.size * 2, self.size * 2)
        )


class Point:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.pos_X = rd.randint(0, cfg.game_width)
        self.pos_Y = rd.randint(0, cfg.game_height)

    def display(self):
        pygame.draw.circle(screen, self.color, (self.pos_X, self.pos_Y), self.size)


def main_interface(key):
    screen.fill(cfg.color_dict[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    if key[pygame.K_q]:
        pygame.quit()

    return True


def main():
    running = True
    newPoint = Point(cfg.general_size, cfg.color_dict[2])
    snake = Snake(
        4,
    )
    while running:
        curr_key = pygame.key.get_pressed()
        running = main_interface(curr_key)
        newPoint.display()
        snake.change_direction(curr_key)
        hit, game_over = snake.move(newPoint)
        if hit:
            newPoint = Point(cfg.general_size, cfg.color_dict[2])
            cfg.score += 1
            snake.generate_part()
        if game_over:
            print(f"Your score is {cfg.score}")
            running = False
        snake.display()
        pygame.display.flip()
        clock.tick(60) / 1000


pygame.init()
point_list = []
screen = pygame.display.set_mode((cfg.game_width, cfg.game_height), vsync=1)
clock = pygame.time.Clock()
main()
