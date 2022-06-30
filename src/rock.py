import pygame
import settings
import random
import bolt
import robot
import datetime

class Rock:
    image = pygame.image.load("rock.png")
    explosion = pygame.image.load("explosion.png")

    def __init__(self, v=0) -> None:
        self.x = random.randint(0, settings.WINDOW_WIDTH - Rock.image.get_width())
        self.y = 0
        self.v = random.randint(1 + v , 5 + v)
        self.hit = False
        self.hit_time = None

    def robot_collision(self, r: robot.Robot, window: pygame.Surface):
        if self.hit:
            return
        lbound = self.x - robot.Robot.image.get_width() +8 
        rbound = self.x + Rock.image.get_width() + robot.Robot.image.get_width() -18
        ubound = self.y - robot.Robot.image.get_height()
        bbound = self.y + Rock.image.get_height() + robot.Robot.image.get_height()
        if r.x > lbound and r.x + robot.Robot.image.get_width() -10 < rbound:
            if  r.y > ubound and r.y + robot.Robot.image.get_height() < bbound:
                self.hit = True
                self.hit_time = datetime.datetime.now()
                r.health -= 1

    def bolt_hit(self, bolt: bolt.Bolt, robot: robot.Robot) -> bool:
        if self.hit:
            return
        if self.x -10 <= bolt.x <= self.x + Rock.image.get_width():
            if bolt.y - Rock.image.get_height() <= bolt.y <= self.y:
                self.hit = True
                self.hit_time = datetime.datetime.now()
                bolt.hit = True
                robot.points += 1

    def in_bounds(self) -> bool:
        return self.y  < settings.WINDOW_HEIGHT

    def draw(self, window: pygame.Surface) -> None:
        self.y += self.v
        if not self.hit:
            window.blit(Rock.image, (self.x, self.y))
        else:
            if datetime.datetime.now() - self.hit_time < datetime.timedelta(seconds=0.25):
                 window.blit(Rock.explosion, (self.x, self.y))
