# src/ui.py

import pygame

from src.settings import (
    WHITE,
    LIGHT_GRAY,
    GRAY,
    RED,
    DARK_GRAY,
    FONT_NAME,
    TITLE_FONT_SIZE,
    MENU_FONT_SIZE,
    HUD_FONT_SIZE,
    SMALL_FONT_SIZE,
)


def create_font(size, bold=False):
    return pygame.font.SysFont(FONT_NAME, size, bold=bold)


def draw_text(screen, text, size, x, y, color=WHITE, center=True, bold=False):
    font = create_font(size, bold)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    screen.blit(text_surface, text_rect)
    return text_rect


def draw_title(screen, text, x, y):
    # Title shadow / glow
    draw_text(screen, text, TITLE_FONT_SIZE, x + 3, y + 3, (45, 45, 55), bold=True)
    draw_text(screen, text, TITLE_FONT_SIZE, x, y, WHITE, bold=True)

    # Red underline decoration
    pygame.draw.line(screen, RED, (x - 90, y + 56), (x - 18, y + 56), 2)
    pygame.draw.line(screen, RED, (x + 18, y + 56), (x + 90, y + 56), 2)
    pygame.draw.circle(screen, RED, (x, y + 56), 4)


def draw_panel(screen, rect, border_color=GRAY, fill_color=DARK_GRAY):
    pygame.draw.rect(screen, fill_color, rect, border_radius=14)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=14)


def draw_stat_card(screen, label, value, x, y, width=190, height=72):
    rect = pygame.Rect(x, y, width, height)

    # Glow border
    glow_rect = rect.inflate(8, 8)
    pygame.draw.rect(screen, (55, 8, 14), glow_rect, width=1, border_radius=16)

    pygame.draw.rect(screen, (14, 14, 20), rect, border_radius=14)
    pygame.draw.rect(screen, (75, 75, 88), rect, width=1, border_radius=14)

    # Small red accent line
    pygame.draw.line(screen, RED, (x + 16, y + 15), (x + 70, y + 15), 2)

    draw_text(screen, label, 16, x + 16, y + 23, RED, center=False, bold=True)
    draw_text(screen, str(value).zfill(6), 30, x + 16, y + 40, WHITE, center=False, bold=True)


def draw_hud(screen, score, best_score):
    # Left score card
    draw_stat_card(
        screen=screen,
        label="SCORE",
        value=int(score),
        x=28,
        y=24,
        width=200,
        height=82,
    )

    # Right best score card
    draw_stat_card(
        screen=screen,
        label="BEST",
        value=int(best_score),
        x=1048,
        y=24,
        width=200,
        height=82,
    )


def draw_difficulty_badge(screen, difficulty, x, y):
    colors = {
        "EASY": (70, 180, 120),
        "NORMAL": RED,
        "HARD": (220, 50, 50),
    }

    badge_color = colors.get(difficulty, RED)

    rect = pygame.Rect(x, y, 210, 42)

    pygame.draw.rect(screen, (14, 14, 20), rect, border_radius=12)
    pygame.draw.rect(screen, badge_color, rect, width=2, border_radius=12)

    pygame.draw.circle(screen, badge_color, (x + 24, y + 21), 5)

    draw_text(
        screen,
        f"MODE: {difficulty}",
        20,
        x + 48,
        y + 11,
        WHITE,
        center=False,
        bold=True,
    )


def draw_progress_bar(screen, x, y, width, progress, label="PROGRESS"):
    progress = max(0, min(1, progress))

    bg_rect = pygame.Rect(x, y, width, 8)
    fill_rect = pygame.Rect(x, y, int(width * progress), 8)

    pygame.draw.rect(screen, (35, 35, 45), bg_rect, border_radius=4)
    pygame.draw.rect(screen, RED, fill_rect, border_radius=4)

    pygame.draw.circle(screen, RED, (x + int(width * progress), y + 4), 5)

    draw_text(
        screen,
        label,
        14,
        x,
        y - 22,
        LIGHT_GRAY,
        center=False,
        bold=True,
    )


class Button:
    def __init__(self, x, y, width, height, text, font_size=MENU_FONT_SIZE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        if self.is_hovered:
            border_color = RED
            text_color = WHITE
            fill_color = (28, 8, 14)
        else:
            border_color = (75, 75, 88)
            text_color = LIGHT_GRAY
            fill_color = DARK_GRAY

        pygame.draw.rect(screen, fill_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=12)

        if self.is_hovered:
            glow_rect = self.rect.inflate(10, 10)
            pygame.draw.rect(screen, (90, 10, 18), glow_rect, width=1, border_radius=16)

            pygame.draw.line(
                screen,
                RED,
                (self.rect.x + 18, self.rect.y + self.rect.height - 10),
                (self.rect.x + 78, self.rect.y + self.rect.height - 10),
                2,
            )

        draw_text(
            screen,
            self.text,
            self.font_size,
            self.rect.centerx,
            self.rect.centery,
            text_color,
            center=True,
            bold=True,
        )

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )