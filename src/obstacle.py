# src/obstacle.py

import random
import pygame

from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    OBSTACLE_MIN_SIZE,
    OBSTACLE_MAX_SIZE,
    OBSTACLE_START_SPEED,
    RED,
)


class Obstacle:
    def __init__(self):
        self.max_trail_length = 14
        self.reset(start_above_screen=True)

    def reset(self, start_above_screen=False):
        self.size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
        self.x = random.randint(0, SCREEN_WIDTH - self.size)

        if start_above_screen:
            self.y = random.randint(-SCREEN_HEIGHT, -self.size)
        else:
            self.y = random.randint(-220, -self.size)

        self.speed = OBSTACLE_START_SPEED + random.uniform(0, 2.4)
        self.trail = []

    def update(self, extra_speed=0):
        self.trail.append((self.x, self.y))

        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        self.y += self.speed + extra_speed

        if self.y > SCREEN_HEIGHT + self.size:
            self.reset(start_above_screen=False)

    def draw(self, screen):
        # Motion trail
        trail_count = len(self.trail)

        for index, position in enumerate(self.trail):
            if trail_count == 0:
                continue

            fade = (index + 1) / trail_count
            trail_size = max(4, int(self.size * fade))
            color_red = int(35 + 95 * fade)

            trail_rect = pygame.Rect(
                int(position[0] + (self.size - trail_size) / 2),
                int(position[1] + (self.size - trail_size) / 2),
                trail_size,
                trail_size,
            )

            pygame.draw.rect(
                screen,
                (color_red, 4, 10),
                trail_rect,
                border_radius=4,
            )

        # Vertical falling streak
        streak_x = int(self.x + self.size // 2)
        pygame.draw.line(
            screen,
            (90, 6, 14),
            (streak_x, int(self.y - 70)),
            (streak_x, int(self.y + self.size // 2)),
            2,
        )

        pygame.draw.line(
            screen,
            (45, 3, 8),
            (streak_x, int(self.y - 130)),
            (streak_x, int(self.y - 40)),
            1,
        )

        rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)

        # Glow
        glow_rect = pygame.Rect(
            int(self.x - 7),
            int(self.y - 7),
            self.size + 14,
            self.size + 14,
        )

        pygame.draw.rect(screen, (70, 4, 10), glow_rect, border_radius=7)
        pygame.draw.rect(screen, (125, 8, 18), rect.inflate(5, 5), border_radius=6)
        pygame.draw.rect(screen, RED, rect, border_radius=4)

        # Inner outline
        inner_rect = pygame.Rect(
            int(self.x + 6),
            int(self.y + 6),
            max(4, self.size - 12),
            max(4, self.size - 12),
        )

        pygame.draw.rect(
            screen,
            (255, 95, 95),
            inner_rect,
            width=1,
            border_radius=3,
        )

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)