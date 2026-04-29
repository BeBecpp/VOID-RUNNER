# src/gem.py

import random
import math
import pygame

from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GEM_RADIUS,
    GEM_SPAWN_PADDING,
    GEM_BLUE,
    GEM_GLOW,
    WHITE,
)


class Gem:
    def __init__(self):
        self.radius = GEM_RADIUS
        self.max_trail_length = 16
        self.reset(start_above_screen=True)

    def reset(self, start_above_screen=False):
        self.x = random.randint(
            GEM_SPAWN_PADDING,
            SCREEN_WIDTH - GEM_SPAWN_PADDING,
        )

        if start_above_screen:
            self.y = random.randint(-SCREEN_HEIGHT, -self.radius)
        else:
            self.y = random.randint(-260, -self.radius)

        self.base_speed = random.uniform(2.2, 3.8)
        self.pulse_time = random.uniform(0, 10)
        self.sparkle_rotation = random.uniform(0, 10)
        self.trail = []

    def update(self, dt, extra_speed=0):
        self.trail.append((self.x, self.y))

        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        self.pulse_time += dt * 5
        self.sparkle_rotation += dt * 4

        # Gem obstacle-той хамт дээрээс унадаг
        self.y += self.base_speed + (extra_speed * 0.55)

        if self.y > SCREEN_HEIGHT + self.radius:
            self.reset(start_above_screen=False)

    def draw(self, screen):
        # Blue falling trail
        trail_count = len(self.trail)

        for index, position in enumerate(self.trail):
            if trail_count == 0:
                continue

            fade = (index + 1) / trail_count
            trail_radius = max(2, int(self.radius * fade))
            blue_value = int(65 + 150 * fade)

            pygame.draw.circle(
                screen,
                (10, 55, blue_value),
                (int(position[0]), int(position[1])),
                trail_radius,
            )

        pulse = math.sin(self.pulse_time) * 3
        glow_radius = int(self.radius + 15 + pulse)

        # Outer glow
        pygame.draw.circle(
            screen,
            GEM_GLOW,
            (int(self.x), int(self.y)),
            glow_radius,
        )

        pygame.draw.circle(
            screen,
            (25, 125, 185),
            (int(self.x), int(self.y)),
            self.radius + 10,
        )

        # Sparkle lines
        sparkle_length = int(17 + pulse)
        angle = self.sparkle_rotation

        for i in range(4):
            current_angle = angle + i * math.pi / 2

            x1 = self.x + math.cos(current_angle) * (self.radius + 3)
            y1 = self.y + math.sin(current_angle) * (self.radius + 3)

            x2 = self.x + math.cos(current_angle) * sparkle_length
            y2 = self.y + math.sin(current_angle) * sparkle_length

            pygame.draw.line(
                screen,
                WHITE,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                1,
            )

        # Diamond gem shape
        points = [
            (int(self.x), int(self.y - self.radius - 5)),
            (int(self.x + self.radius + 5), int(self.y)),
            (int(self.x), int(self.y + self.radius + 5)),
            (int(self.x - self.radius - 5), int(self.y)),
        ]

        pygame.draw.polygon(screen, GEM_BLUE, points)
        pygame.draw.polygon(screen, WHITE, points, width=1)

        # Inner shine
        inner_points = [
            (int(self.x), int(self.y - 5)),
            (int(self.x + 5), int(self.y)),
            (int(self.x), int(self.y + 5)),
            (int(self.x - 5), int(self.y)),
        ]

        pygame.draw.polygon(screen, (170, 230, 255), inner_points)

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x - 4), int(self.y - 4)),
            2,
        )

    def is_collected_by(self, player):
        player_x, player_y = player.get_position()
        player_radius = player.get_radius()

        dx = self.x - player_x
        dy = self.y - player_y

        distance_squared = dx * dx + dy * dy
        collect_distance = self.radius + player_radius + 6

        return distance_squared <= collect_distance * collect_distance