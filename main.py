import pygame
import sys
import random

pygame.init()

screen_height = 600
screen_width = 600
block_size = 20
grid_height = 30
grid_width = 30

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

light_green = (0, 170, 140)
dark_green = (0, 140, 120)
food_color = (250, 200, 0)
snake_color = (34, 34, 34)

up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)


class SNAKE:
    def __init__(self):
        self.positions = [((screen_width/2), (screen_height/2))]
        self.length = 1
        self.direction = random.choice([up, down, left, right])
        self.color = snake_color
        self.score = 0

    def draw(self):
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (block_size, block_size))
            pygame.draw.rect(screen, self.color, rect)

    def move(self):
        current = self.positions[0]
        x, y = self.direction
        new = ((current[0] + (x * block_size)), (current[1] + (y * block_size)))

        if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not new in self.positions[2:]:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        else:
            self.reset()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)

    def turn(self, direction):
        if (direction[0] * - 1, direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction


class FOOD:
    def __init__(self):
        self.position = (0, 0)
        self.color = food_color
        self.random_position()

    def random_position(self):
        self.position = (random.randint(0, grid_width-1)*block_size, random.randint(0, grid_height-1)*block_size)

    def draw(self):
        rect = pygame.Rect((self.position[0], self.position[1]), (block_size, block_size))
        pygame.draw.rect(screen, self.color, rect)


def draw_grid():
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_height)):
            if (x + y) % 2 == 0:
                light = pygame.Rect((x * block_size, y * block_size), (block_size, block_size))
                pygame.draw.rect(screen, light_green, light)
            else:
                dark = pygame.Rect((x * block_size, y * block_size), (block_size, block_size))
                pygame.draw.rect(screen, dark_green, dark)


food = FOOD()
snake = SNAKE()

while True:
    clock.tick(15)
    snake.handle_keys()
    snake.move()
    draw_grid()
    if snake.positions[0] == food.position:
        snake.length += 1
        snake.score += 1
        food.random_position()
    score_text = font.render("Score: {0}".format(snake.score), True, (0, 0, 0))
    food.draw()
    snake.draw()
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

