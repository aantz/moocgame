import pygame
import random
import settings
import robot

class Helper:
    ammo = pygame.image.load("chest.png")
    health = pygame.image.load("heart.png")

    def __init__(self) -> None:
        self.y = 0
        self.v = random.randint(2,5)
        self.hit = False
        self.type = random.choice(["ammo", "ammo", "ammo", "health"])
        if self.type == "ammo":
            self.x = random.randint(0, settings.WINDOW_WIDTH - Helper.ammo.get_width())
        else:
            self.x = random.randint(0, settings.WINDOW_WIDTH - Helper.health.get_width())

    def in_bounds(self) -> bool:
        return self.y < settings.WINDOW_HEIGHT

    def draw(self, window: pygame.Surface) -> None:
        self.y += self.v
        if not self.hit:
            if self.type == "ammo":
                window.blit(Helper.ammo, (self.x, self.y))
            else:
                window.blit(Helper.health, (self.x, self.y))

    def robot_collision(self, r: robot.Robot, window: pygame.Surface):
        if self.hit:
            return
        if self.type == "ammo":
            w = Helper.ammo.get_width()
            h = Helper.ammo.get_height()
        else:
            w = Helper.ammo.get_width()
            h = Helper.ammo.get_height()
        lbound = self.x - robot.Robot.image.get_width() #+8 
        rbound = self.x + w + robot.Robot.image.get_width() #-18
        ubound = self.y - robot.Robot.image.get_height()
        bbound = self.y + h + robot.Robot.image.get_height()
        if r.x > lbound and r.x + robot.Robot.image.get_width() -10 < rbound:
            if  r.y > ubound and r.y + robot.Robot.image.get_height() < bbound:
                self.hit = True
                if self.type == "ammo":
                    r.ammo = min(r.ammo + 5, 10)
                else:
                    r.health = min(r.health + 5, 3)