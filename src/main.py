import random

import pygame

from ball import Ball

SCREEN_SIZE = (1920, 1080)
SPAWN_SIZE = (1080, 720)
SPAWN_POSITIONS = (
    int((SCREEN_SIZE[0] - SPAWN_SIZE[0]) / 2),
    int((SCREEN_SIZE[0] - SPAWN_SIZE[0]) / 2) + SPAWN_SIZE[0],
    int((SCREEN_SIZE[1] - SPAWN_SIZE[1]) / 2),
    int((SCREEN_SIZE[1] - SPAWN_SIZE[1]) / 2) + SPAWN_SIZE[1],
)

BALLS = 100

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True


masses = [random.randint(1, 1000) for _ in range(BALLS)]
radiui = [(m * 20 / 1000.0) + 5 for m in masses]


balls: list[Ball] = [
    Ball(
        random.randint(SPAWN_POSITIONS[0], SPAWN_POSITIONS[1]),
        random.randint(SPAWN_POSITIONS[2], SPAWN_POSITIONS[3]),
        masses[i],
        radiui[i],
        pygame.Color(tuple([random.randint(0, 255) for _ in range(3)])),
        (random.randint(-10, 10) / 10.0, random.randint(-10, 10)),
    )
    for i in range(BALLS)
]

while running:
    delta = clock.tick(60) / 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    forces = [ball.compute_forces(balls) for ball in balls]
    for ball, force in zip(balls, forces):
        ball.update(delta, force)
        ball.render(screen)

    pygame.display.flip()
