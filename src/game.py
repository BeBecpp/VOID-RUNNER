# src/game.py

import sys
import pygame

from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_TITLE,
    BLACK,
    WHITE,
    LIGHT_GRAY,
    GRAY,
    RED,
    DARK_GRAY,
    DIFFICULTY_SETTINGS,
    OBSTACLE_SPEED_INCREMENT,
    SMALL_FONT_SIZE,
)

from src.player import Player
from src.obstacle import Obstacle
from src.gem import Gem
from src.storage import load_highscore, save_highscore
from src.ui import draw_text, draw_hud, draw_difficulty_badge, draw_progress_bar

from src.screens import (
    HomeScreen,
    HowToPlayScreen,
    SettingsScreen,
    PauseScreen,
    GameOverScreen,
)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "HOME"

        self.player = Player()
        self.obstacles = []
        self.gem = Gem()

        self.score = 0
        self.survival_score = 0
        self.gem_score = 0
        self.gems_collected = 0

        self.best_score = load_highscore()
        self.game_time = 0

        self.home_screen = HomeScreen()
        self.how_to_play_screen = HowToPlayScreen()
        self.settings_screen = SettingsScreen()
        self.pause_screen = PauseScreen()
        self.game_over_screen = GameOverScreen()

        self.pause_button_rect = pygame.Rect(SCREEN_WIDTH - 72, 24, 46, 46)

        self.reset_game()

    def get_current_difficulty(self):
        difficulty = self.settings_screen.difficulties[self.settings_screen.difficulty_index]

        if difficulty == "NORMAL":
            difficulty = "MEDIUM"

        return difficulty

    def get_difficulty_config(self):
        difficulty = self.get_current_difficulty()
        return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["MEDIUM"])

    def reset_game(self):
        self.player.reset()

        self.score = 0
        self.survival_score = 0
        self.gem_score = 0
        self.gems_collected = 0
        self.game_time = 0

        config = self.get_difficulty_config()
        obstacle_count = config["obstacle_count"]

        self.obstacles = [Obstacle() for _ in range(obstacle_count)]
        self.gem.reset(start_above_screen=True)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            mouse_pos = pygame.mouse.get_pos()

            self.handle_events()
            self.update(mouse_pos, dt)
            self.draw()

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()

            if self.state == "HOME":
                action = self.home_screen.handle_event(event)
                self.handle_home_action(action)

            elif self.state == "PLAYING":
                self.handle_playing_event(event)

            elif self.state == "HOW_TO_PLAY":
                action = self.how_to_play_screen.handle_event(event)
                self.handle_simple_screen_action(action)

            elif self.state == "SETTINGS":
                action = self.settings_screen.handle_event(event)
                self.handle_settings_action(action)

            elif self.state == "PAUSED":
                action = self.pause_screen.handle_event(event)
                self.handle_pause_action(action)

            elif self.state == "GAME_OVER":
                action = self.game_over_screen.handle_event(event)
                self.handle_game_over_action(action)

    def handle_home_action(self, action):
        if action == "PLAY":
            self.reset_game()
            self.state = "PLAYING"

        elif action == "HOW_TO_PLAY":
            self.state = "HOW_TO_PLAY"

        elif action == "SETTINGS":
            self.state = "SETTINGS"

        elif action == "EXIT":
            self.exit_game()

    def handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                self.state = "PAUSED"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.pause_button_rect.collidepoint(event.pos):
                self.state = "PAUSED"

    def handle_simple_screen_action(self, action):
        if action == "BACK":
            self.state = "HOME"

    def handle_settings_action(self, action):
        if action == "BACK":
            self.state = "HOME"

        elif action == "CHANGE_DIFFICULTY":
            pass

    def handle_pause_action(self, action):
        if action == "RESUME":
            self.state = "PLAYING"

        elif action == "RESTART":
            self.reset_game()
            self.state = "PLAYING"

        elif action == "HOME":
            self.state = "HOME"

        elif action == "EXIT":
            self.exit_game()

    def handle_game_over_action(self, action):
        if action == "RETRY":
            self.reset_game()
            self.state = "PLAYING"

        elif action == "HOME":
            self.state = "HOME"

        elif action == "EXIT":
            self.exit_game()

    def update(self, mouse_pos, dt):
        if self.state == "HOME":
            self.home_screen.update(mouse_pos)

        elif self.state == "PLAYING":
            self.update_gameplay(dt)

        elif self.state == "HOW_TO_PLAY":
            self.how_to_play_screen.update(mouse_pos)

        elif self.state == "SETTINGS":
            self.settings_screen.update(mouse_pos)

        elif self.state == "PAUSED":
            self.pause_screen.update(mouse_pos)

        elif self.state == "GAME_OVER":
            self.game_over_screen.update(mouse_pos)

    def update_gameplay(self, dt):
        config = self.get_difficulty_config()

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        self.game_time += dt

        self.survival_score += dt * config["survival_score_rate"]

        self.score = int(self.gem_score + self.survival_score)

        extra_speed = self.score * OBSTACLE_SPEED_INCREMENT
        extra_speed += config["speed_bonus"]
        extra_speed = max(0, extra_speed)

        self.gem.update(dt, extra_speed=extra_speed)

        if self.gem.is_collected_by(self.player):
            self.gems_collected += 1
            self.gem_score += config["gem_value"]
            self.gem.reset(start_above_screen=False)

        self.score = int(self.gem_score + self.survival_score)

        for obstacle in self.obstacles:
            obstacle.update(extra_speed=extra_speed)

            if self.check_collision(self.player, obstacle):
                self.game_over()
                break

    def game_over(self):
        if self.score > self.best_score:
            self.best_score = self.score
            save_highscore(self.best_score)

        self.state = "GAME_OVER"

    def check_collision(self, player, obstacle):
        player_x, player_y = player.get_position()
        player_radius = player.get_radius()
        rect = obstacle.get_rect()

        closest_x = max(rect.left, min(player_x, rect.right))
        closest_y = max(rect.top, min(player_y, rect.bottom))

        distance_x = player_x - closest_x
        distance_y = player_y - closest_y

        distance_squared = distance_x * distance_x + distance_y * distance_y

        return distance_squared < player_radius * player_radius

    def draw(self):
        if self.state == "HOME":
            self.home_screen.draw(self.screen)

        elif self.state == "PLAYING":
            self.draw_gameplay()

        elif self.state == "HOW_TO_PLAY":
            self.how_to_play_screen.draw(self.screen)

        elif self.state == "SETTINGS":
            self.settings_screen.draw(self.screen)

        elif self.state == "PAUSED":
            self.draw_gameplay()
            self.pause_screen.draw(self.screen)

        elif self.state == "GAME_OVER":
            self.game_over_screen.draw(self.screen, self.score, self.best_score)

    def draw_gameplay(self):
        self.draw_gameplay_background()

        self.gem.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.player.draw(self.screen)

        draw_hud(self.screen, self.score, self.best_score)
        self.draw_gem_counter()
        self.draw_pause_button()
        self.draw_bottom_status()

    def draw_gameplay_background(self):
        self.screen.fill(BLACK)

        time = pygame.time.get_ticks() * 0.001

        for i in range(18):
            x = (i * 83 + int(time * 25)) % SCREEN_WIDTH
            y1 = int((i * 47 + time * 80) % SCREEN_HEIGHT)
            y2 = y1 + 60

            pygame.draw.line(
                self.screen,
                (20, 20, 28),
                (x, y1),
                (x, min(y2, SCREEN_HEIGHT)),
                1,
            )

        pygame.draw.line(
            self.screen,
            (30, 30, 38),
            (120, SCREEN_HEIGHT - 72),
            (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 72),
            1,
        )

        for i in range(22):
            x = int((i * 157 + time * 18) % SCREEN_WIDTH)
            y = int((i * 97 + time * 32) % SCREEN_HEIGHT)

            pygame.draw.circle(
                self.screen,
                (55, 7, 12),
                (x, y),
                1,
            )

    def draw_gem_counter(self):
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 90, 28, 180, 58)

        pygame.draw.rect(self.screen, (14, 14, 20), rect, border_radius=14)
        pygame.draw.rect(self.screen, (80, 190, 255), rect, width=2, border_radius=14)

        gem_x = rect.x + 35
        gem_y = rect.y + 29

        points = [
            (gem_x, gem_y - 10),
            (gem_x + 10, gem_y),
            (gem_x, gem_y + 10),
            (gem_x - 10, gem_y),
        ]

        pygame.draw.polygon(self.screen, (80, 190, 255), points)
        pygame.draw.polygon(self.screen, WHITE, points, width=1)

        draw_text(
            self.screen,
            f"x {self.gems_collected}",
            26,
            rect.x + 62,
            rect.y + 16,
            WHITE,
            center=False,
            bold=True,
        )

    def draw_pause_button(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.pause_button_rect.collidepoint(mouse_pos)

        fill_color = (25, 10, 14) if hovered else DARK_GRAY
        border_color = RED if hovered else GRAY

        pygame.draw.rect(self.screen, fill_color, self.pause_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, self.pause_button_rect, width=2, border_radius=10)

        bar_width = 5
        bar_height = 20
        center_x = self.pause_button_rect.centerx
        center_y = self.pause_button_rect.centery

        pygame.draw.rect(
            self.screen,
            WHITE,
            pygame.Rect(center_x - 9, center_y - bar_height // 2, bar_width, bar_height),
            border_radius=2,
        )

        pygame.draw.rect(
            self.screen,
            WHITE,
            pygame.Rect(center_x + 4, center_y - bar_height // 2, bar_width, bar_height),
            border_radius=2,
        )

    def draw_bottom_status(self):
        difficulty = self.get_current_difficulty()
        config = self.get_difficulty_config()

        draw_difficulty_badge(
            self.screen,
            difficulty,
            SCREEN_WIDTH // 2 - 105,
            SCREEN_HEIGHT - 58,
        )

        progress = min(1, (self.score % 100) / 100)

        draw_progress_bar(
            self.screen,
            x=SCREEN_WIDTH // 2 - 150,
            y=SCREEN_HEIGHT - 90,
            width=300,
            progress=progress,
            label=f"GEM VALUE: +{config['gem_value']}",
        )

    def exit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()