from collections import deque

import pygame

GRAVITY_CONSTANT = 10
SHADOWS = 30


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b


class Ball:
    def __init__(self, x, y, mass, radius, colour, velocity=(0, 0)):
        self.position = (x, y)
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.acceleration = (0, 0)
        self.colour: pygame.Color = colour
        self.previous_postions = deque(maxlen=SHADOWS)

    def render(self, screen: pygame.Surface):
        for i, position in enumerate(self.previous_postions):
            i = SHADOWS - i
            pygame.draw.circle(
                screen,
                self.colour.lerp(pygame.Color(0, 0, 0, 0), i / SHADOWS),
                (position[0], position[1]),
                lerp(self.radius, 0, i / SHADOWS),
            )

    def compute_forces(self, balls):
        total_force = (0, 0)
        for ball in balls:
            if self == ball:
                continue

            distance = (
                (self.position[0] - ball.position[0]) ** 2
                + (self.position[1] - ball.position[1]) ** 2
            ) ** (1 / 2)

            gravity_force = (
                GRAVITY_CONSTANT * self.mass * ball.mass * (1 / (distance**2 + 1))
            )

            direction = (
                (ball.position[0] - self.position[0]) / distance,
                (ball.position[1] - self.position[1]) / distance,
            )

            if distance <= self.radius + ball.radius:
                total_force = (
                    total_force[0] + (gravity_force * 0.05 * direction[0]),
                    total_force[1] + (gravity_force * 0.05 * direction[1]),
                )

                continue

            total_force = (
                total_force[0] + (gravity_force * direction[0]),
                total_force[1] + (gravity_force * direction[1]),
            )

        return total_force

    def update(self, delta, force):
        self.acceleration = (force[0] / self.mass, force[1] / self.mass)

        new_velocity = (
            self.velocity[0] + delta * self.acceleration[0],
            self.velocity[1] + delta * self.acceleration[1],
        )

        self.velocity = new_velocity

        new_position = (
            self.position[0] + delta * self.velocity[0],
            self.position[1] + delta * self.velocity[1],
        )

        self.position = new_position
        self.previous_postions.append(new_position)
