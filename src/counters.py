from datetime import datetime, timedelta
import settings 
import pygame
import robot
import bolt
import settings
import game

class Counters:

    heart_image = pygame.image.load("heart.png")

    def __init__(self) -> None:
        self.big_font = pygame.font.SysFont("arial", 42)
        self.small_font = pygame.font.SysFont("arial", 24)
        self.ammo_rect_xy = (10, 10)
        self.health_rect_xy = (settings.WINDOW_WIDTH - ((robot.Robot.max_health +1)* Counters.heart_image.get_width()), 10)
        self.ammo_rect = pygame.Rect((self.ammo_rect_xy, ((robot.Robot.max_ammo + 1)* bolt.Bolt.image.get_width(),
                                        bolt.Bolt.image.get_height() + 4)))
        self.health_rect = pygame.Rect((
            self.health_rect_xy ,
            (robot.Robot.max_health * Counters.heart_image.get_width()+ 6, Counters.heart_image.get_height() + 3)
        ))

    def draw(self, window: pygame.Surface, game: game.Game) -> None:
        self.draw_health(window, game.robot)
        self.draw_ammo(window, game.robot)
        self.draw_points(window, game)
        self.draw_time(window, game)

    def draw_points(self, window: pygame.Surface, game: game.Game) -> None:
        text = self.small_font.render(f"LVL: {game.level} PTS: {game.robot.points}", True, settings.VIOLET)
        (x,y) = ((settings.WINDOW_WIDTH // 2) - text.get_width() // 2, 4)
        window.blit(text, (x,y))

    def draw_time(self, window: pygame.Surface, game: game.Game) ->None:
        pass

    def game_over(self, window: pygame.Surface, game: game.Game):
        window_center_w = settings.WINDOW_WIDTH // 2 
        window_center_h = settings.WINDOW_HEIGHT // 2
        text1 = self.big_font.render(f"GAME OVER!", True, settings.VIOLET)
        (x,y) = (window_center_w  - (text1.get_width()) // 2, window_center_h)
        window.blit(text1, (x,y))
        height = text1.get_height()
        text = self.small_font.render(f"You destroyed {game.robot.points} asteroids", True, settings.VIOLET)
        (x,y) = (window_center_w  - (text.get_width()) // 2, window_center_h  + height)
        window.blit(text, (x,y))
        height += text.get_height()
        text = self.small_font.render(f"You got to level {game.level}", True, settings.VIOLET)
        (x,y) = (window_center_w  - (text.get_width()) // 2, window_center_h  + height)
        window.blit(text, (x,y))
        height += text.get_height()
        duration = str(game.game_end_time - game.game_start_time).split('.')[0]
        text = self.small_font.render(f"You lasted for {str(duration)}", True, settings.VIOLET)
        (x,y) = (window_center_w - (text.get_width() // 2), window_center_h  + height)
        window.blit(text, (x,y))
        height += text.get_height()
        text = self.small_font.render(f"Press S to restart, Q to quit", True, settings.VIOLET)
        (x,y) = (window_center_w - (text.get_width() // 2), window_center_h  + text1.get_height() + height)
        window.blit(text, (x,y))

    def draw_ammo(self, window: pygame.Surface, robot: robot.Robot) -> None:
        pygame.draw.rect(window, settings.VIOLET, self.ammo_rect, 2)
        (x,y) = (self.ammo_rect_xy[0] +2, self.ammo_rect_xy[1] +2)
        for i in range(robot.ammo):
            window.blit(bolt.Bolt.image, (x, y))
            (x,y) = (x + bolt.Bolt.image.get_width() + 2, y)

    def draw_health(self, window: pygame.Surface, robot: robot.Robot) -> None:
        pygame.draw.rect(window, settings.VIOLET, self.health_rect, 2)
        (x,y) = (self.health_rect_xy[0] +2, self.health_rect_xy[1] +2)
        for i in range(robot.health):
            window.blit(Counters.heart_image, (x, y))
            (x,y) = (x + Counters.heart_image.get_width() + 2, y)

    def show_help(self, window: pygame.Surface):
        text1 = self.big_font.render(f"Welcome to MOOC game!", True, settings.VIOLET)
        height = text1.get_height()
        (x,y) = ((settings.WINDOW_WIDTH // 2) - text1.get_width() // 2, settings.WINDOW_HEIGHT // 2)
        window.blit(text1, (x,y))
        text = self.small_font.render(f"Press S to start, arrow keys to move, space to fire.", True, settings.VIOLET)
        (x,y) = ((settings.WINDOW_WIDTH // 2) - text.get_width() // 2, (settings.WINDOW_HEIGHT // 2) + height)
        window.blit(text, (x,y))
        height += text.get_height()
        text = self.small_font.render(f"Q to quit at any time.", True, settings.VIOLET)
        (x,y) = ((settings.WINDOW_WIDTH // 2) - text.get_width() // 2, (settings.WINDOW_HEIGHT // 2) + height)
        window.blit(text, (x,y))