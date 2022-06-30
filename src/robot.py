import pygame
from settings import *
from datetime import datetime, timedelta
import bolt

class Robot:
    image = pygame.image.load("robot.png")
    max_ammo = 10
    max_health = 3

    def __init__(self) -> None:
        self.width = Robot.image.get_width()
        self.height = Robot.image.get_height()
        self.x = WINDOW_WIDTH // 2 - (self.width // 2)
        self.y = WINDOW_HEIGHT // 2 + self.height
        self.velocity = 4
        self.left_direction = (-self.velocity, 0)
        self.right_direction = (self.velocity, 0)
        self.top_direction = (0, -self.velocity)
        self.bottom_direction = (0, self.velocity)
        self.no_direction = (0, 0)
        self.direction = self.no_direction
        self.left_limit = 0
        self.right_limit = WINDOW_WIDTH - self.width
        self.bottom_limit = WINDOW_HEIGHT - self.height
        self.top_limit = 20
        self.ammo = Robot.max_ammo = 10
        self.last_shot = datetime.now()
        self.health = Robot.max_health
        self.points = 0

    def draw(self, window):
        self.x += self.direction[0] if self.in_bounds() else 0
        self.y += self.direction[1] if self.in_bounds() else 0
        window.blit(Robot.image, (self.x, self.y))

    def in_bounds(self) -> bool:
        if self.direction == self.right_direction and self.x >= self.right_limit:
            return False
        if self.direction == self.left_direction and self.x <= self.left_limit:
            return False
        if self.direction == self.top_direction and self.y <= self.top_limit:
            return False
        if self.direction == self.bottom_direction and self.y >= self.bottom_limit:
            return False
        return True

    def direction_right(self, startMove: bool) -> None:
        self.direction = self.right_direction if startMove and self.x <= self.right_limit else self.no_direction

    def direction_left(self, startMove: bool) -> None:
        self.direction = self.left_direction if startMove and self.x >= self.left_limit else self.no_direction

    def direction_up(self, startMove: bool) -> None:
        self.direction = self.top_direction if startMove and self.y > self.top_limit else self.no_direction

    def direction_down(self, startMove: bool) -> None:
        self.direction = self.bottom_direction if startMove and self.y < self.bottom_limit else self.no_direction

    def shoot(self) -> bolt.Bolt:
        n = datetime.now()
        diff = n - self.last_shot
        if self.ammo < 1 or diff < timedelta(seconds=.5):
            return None
        self.ammo -= 1
        self.last_shot = n
        gun_point = (self.x + (self.width // 3), self.y)
        return bolt.Bolt(gun_point)