# src/player.py

import pygame

from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_RADIUS,
    PLAYER_SPEED,
    WHITE,
)


class Player:
    def __init__(self):
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.max_trail_length = 18
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 90
        self.trail = []

    def update(self, keys):
        self.trail.append((self.x, self.y))

        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        dx = 0
        dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        # Diagonal movement balance
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.x += dx * self.speed
        self.y += dy * self.speed

        self.keep_inside_screen()

    def keep_inside_screen(self):
        if self.x - self.radius < 0:
            self.x = self.radius

        if self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius

        if self.y - self.radius < 0:
            self.y = self.radius

        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius

    def draw(self, screen):
        # Trail
        trail_count = len(self.trail)

        for index, position in enumerate(self.trail):
            if trail_count == 0:
                continue

            fade = (index + 1) / trail_count
            trail_radius = max(2, int(self.radius * fade * 0.9))
            color_value = int(35 + 120 * fade)

            pygame.draw.circle(
                screen,
                (color_value, color_value, color_value + 10),
                (int(position[0]), int(position[1])),
                trail_radius,
            )

        # Outer glow
        pygame.draw.circle(
            screen,
            (45, 45, 55),
            (int(self.x), int(self.y)),
            self.radius + 14,
        )

        pygame.draw.circle(
            screen,
            (95, 95, 110),
            (int(self.x), int(self.y)),
            self.radius + 8,
        )

        pygame.draw.circle(
            screen,
            (170, 170, 185),
            (int(self.x), int(self.y)),
            self.radius + 4,
        )

        # Main player
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.radius,
        )

        # Small shine
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.x - 3), int(self.y - 3)),
            3,
        )

    def get_position(self):
        return self.x, self.y

    def get_radius(self):
        return self.radius