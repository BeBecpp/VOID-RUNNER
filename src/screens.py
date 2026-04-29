# src/screens.py

import pygame

from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLACK,
    DARK_GRAY,
    WHITE,
    LIGHT_GRAY,
    GRAY,
    RED,
    TITLE_FONT_SIZE,
    MENU_FONT_SIZE,
    SMALL_FONT_SIZE,
)
from src.ui import Button, draw_text, draw_title, draw_panel


def draw_background(screen):
    screen.fill(BLACK)

    # Minimal animated falling red blocks in background
    time = pygame.time.get_ticks() * 0.001

    for i in range(9):
        x = 100 + i * 135
        y = int((time * 45 + i * 95) % (SCREEN_HEIGHT + 120)) - 120
        size = 10 + (i % 3) * 6

        pygame.draw.rect(
            screen,
            (55, 8, 14),
            pygame.Rect(x, y, size, size),
            border_radius=2,
        )

        pygame.draw.line(
            screen,
            (40, 5, 10),
            (x + size // 2, y - 45),
            (x + size // 2, y),
            1,
        )

    # Center decorative line
    pygame.draw.line(
        screen,
        (25, 25, 32),
        (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 30),
        (SCREEN_WIDTH // 2 + 180, SCREEN_HEIGHT // 2 + 30),
        1,
    )


class HomeScreen:
    def __init__(self):
        button_width = 320
        button_height = 56
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = 350
        gap = 72

        self.buttons = {
            "play": Button(button_x, start_y, button_width, button_height, "PLAY"),
            "how_to_play": Button(button_x, start_y + gap, button_width, button_height, "HOW TO PLAY", 24),
            "settings": Button(button_x, start_y + gap * 2, button_width, button_height, "SETTINGS", 24),
            "exit": Button(button_x, start_y + gap * 3, button_width, button_height, "EXIT", 24),
        }

    def update(self, mouse_pos):
        for button in self.buttons.values():
            button.update(mouse_pos)

    def handle_event(self, event):
        if self.buttons["play"].is_clicked(event):
            return "PLAY"

        if self.buttons["how_to_play"].is_clicked(event):
            return "HOW_TO_PLAY"

        if self.buttons["settings"].is_clicked(event):
            return "SETTINGS"

        if self.buttons["exit"].is_clicked(event):
            return "EXIT"

        return None

    def draw(self, screen):
        draw_background(screen)

        draw_title(screen, "VOID RUNNER", SCREEN_WIDTH // 2, 160)

        draw_text(
            screen,
            "Move the dot. Avoid the red blocks. Survive.",
            SMALL_FONT_SIZE,
            SCREEN_WIDTH // 2,
            235,
            LIGHT_GRAY,
        )

        # Small player preview
        pygame.draw.circle(screen, (80, 80, 90), (SCREEN_WIDTH // 2, 292), 18)
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, 292), 9)

        for button in self.buttons.values():
            button.draw(screen)

        draw_text(
            screen,
            "Desktop Edition",
            SMALL_FONT_SIZE,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 35,
            GRAY,
        )


class HowToPlayScreen:
    def __init__(self):
        self.back_button = Button(SCREEN_WIDTH // 2 - 130, 620, 260, 52, "BACK", 24)

    def update(self, mouse_pos):
        self.back_button.update(mouse_pos)

    def handle_event(self, event):
        if self.back_button.is_clicked(event):
            return "BACK"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "BACK"

        return None

    def draw_instruction_panel(self, screen, x, y, number, title, lines):
        rect = pygame.Rect(x, y, 255, 260)
        draw_panel(screen, rect, border_color=GRAY, fill_color=DARK_GRAY)

        draw_text(screen, number, SMALL_FONT_SIZE, x + 22, y + 18, RED, center=False, bold=True)
        draw_text(screen, title, 30, x + 127, y + 65, WHITE, bold=True)

        pygame.draw.line(screen, RED, (x + 75, y + 95), (x + 180, y + 95), 2)

        line_y = y + 130
        for line in lines:
            draw_text(screen, line, 19, x + 127, line_y, LIGHT_GRAY)
            line_y += 30

    def draw(self, screen):
        draw_background(screen)

        draw_title(screen, "HOW TO PLAY", SCREEN_WIDTH // 2, 105)

        panel_y = 210
        gap = 285
        start_x = 80

        self.draw_instruction_panel(
            screen,
            start_x,
            panel_y,
            "01",
            "MOVE",
            [
                "Use WASD",
                "or arrow keys",
                "to move.",
            ],
        )

        self.draw_instruction_panel(
            screen,
            start_x + gap,
            panel_y,
            "02",
            "AVOID",
            [
                "Avoid falling",
                "red blocks.",
                "One hit ends it.",
            ],
        )

        self.draw_instruction_panel(
            screen,
            start_x + gap * 2,
            panel_y,
            "03",
            "SURVIVE",
            [
                "Stay alive",
                "as long as",
                "possible.",
            ],
        )

        self.draw_instruction_panel(
            screen,
            start_x + gap * 3,
            panel_y,
            "04",
            "SCORE",
            [
                "Score grows",
                "over time.",
                "Beat the best.",
            ],
        )

        self.back_button.draw(screen)


class SettingsScreen:
    def __init__(self):
        self.sound_on = True
        self.fullscreen_on = False
        self.difficulties = ["EASY", "NORMAL", "HARD"]
        self.difficulty_index = 1

        button_width = 360
        button_height = 56
        button_x = SCREEN_WIDTH // 2 - button_width // 2

        self.sound_button = Button(button_x, 280, button_width, button_height, "SOUND: ON", 24)
        self.fullscreen_button = Button(button_x, 355, button_width, button_height, "FULLSCREEN: OFF", 24)
        self.difficulty_button = Button(button_x, 430, button_width, button_height, "DIFFICULTY: NORMAL", 24)
        self.back_button = Button(button_x, 535, button_width, button_height, "BACK", 24)

        self.buttons = [
            self.sound_button,
            self.fullscreen_button,
            self.difficulty_button,
            self.back_button,
        ]

    def update_button_texts(self):
        self.sound_button.text = "SOUND: ON" if self.sound_on else "SOUND: OFF"
        self.fullscreen_button.text = "FULLSCREEN: ON" if self.fullscreen_on else "FULLSCREEN: OFF"
        self.difficulty_button.text = f"DIFFICULTY: {self.difficulties[self.difficulty_index]}"

    def update(self, mouse_pos):
        self.update_button_texts()

        for button in self.buttons:
            button.update(mouse_pos)

    def handle_event(self, event):
        if self.sound_button.is_clicked(event):
            self.sound_on = not self.sound_on
            return "TOGGLE_SOUND"

        if self.fullscreen_button.is_clicked(event):
            self.fullscreen_on = not self.fullscreen_on
            return "TOGGLE_FULLSCREEN"

        if self.difficulty_button.is_clicked(event):
            self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulties)
            return "CHANGE_DIFFICULTY"

        if self.back_button.is_clicked(event):
            return "BACK"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "BACK"

        return None

    def draw(self, screen):
        draw_background(screen)

        draw_title(screen, "SETTINGS", SCREEN_WIDTH // 2, 135)

        draw_text(
            screen,
            "Basic options for the game.",
            SMALL_FONT_SIZE,
            SCREEN_WIDTH // 2,
            205,
            LIGHT_GRAY,
        )

        for button in self.buttons:
            button.draw(screen)


class PauseScreen:
    def __init__(self):
        button_width = 320
        button_height = 56
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = 275
        gap = 72

        self.buttons = {
            "resume": Button(button_x, start_y, button_width, button_height, "RESUME", 24),
            "restart": Button(button_x, start_y + gap, button_width, button_height, "RESTART", 24),
            "home": Button(button_x, start_y + gap * 2, button_width, button_height, "HOME", 24),
            "exit": Button(button_x, start_y + gap * 3, button_width, button_height, "EXIT", 24),
        }

    def update(self, mouse_pos):
        for button in self.buttons.values():
            button.update(mouse_pos)

    def handle_event(self, event):
        if self.buttons["resume"].is_clicked(event):
            return "RESUME"

        if self.buttons["restart"].is_clicked(event):
            return "RESTART"

        if self.buttons["home"].is_clicked(event):
            return "HOME"

        if self.buttons["exit"].is_clicked(event):
            return "EXIT"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "RESUME"

        return None

    def draw(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        draw_title(screen, "PAUSED", SCREEN_WIDTH // 2, 160)

        for button in self.buttons.values():
            button.draw(screen)


class GameOverScreen:
    def __init__(self):
        button_width = 320
        button_height = 56
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = 420
        gap = 72

        self.buttons = {
            "retry": Button(button_x, start_y, button_width, button_height, "RETRY", 24),
            "home": Button(button_x, start_y + gap, button_width, button_height, "HOME", 24),
            "exit": Button(button_x, start_y + gap * 2, button_width, button_height, "EXIT", 24),
        }

    def update(self, mouse_pos):
        for button in self.buttons.values():
            button.update(mouse_pos)

    def handle_event(self, event):
        if self.buttons["retry"].is_clicked(event):
            return "RETRY"

        if self.buttons["home"].is_clicked(event):
            return "HOME"

        if self.buttons["exit"].is_clicked(event):
            return "EXIT"

        return None

    def draw(self, screen, score, best_score):
        draw_background(screen)

        draw_title(screen, "GAME OVER", SCREEN_WIDTH // 2, 130)

        score_panel = pygame.Rect(SCREEN_WIDTH // 2 - 280, 230, 240, 110)
        best_panel = pygame.Rect(SCREEN_WIDTH // 2 + 40, 230, 240, 110)

        draw_panel(screen, score_panel, border_color=RED, fill_color=DARK_GRAY)
        draw_panel(screen, best_panel, border_color=RED, fill_color=DARK_GRAY)

        draw_text(screen, "SCORE", SMALL_FONT_SIZE, score_panel.centerx, score_panel.y + 30, RED, bold=True)
        draw_text(screen, int(score), 42, score_panel.centerx, score_panel.y + 72, WHITE, bold=True)

        draw_text(screen, "BEST", SMALL_FONT_SIZE, best_panel.centerx, best_panel.y + 30, RED, bold=True)
        draw_text(screen, int(best_score), 42, best_panel.centerx, best_panel.y + 72, WHITE, bold=True)

        for button in self.buttons.values():
            button.draw(screen)