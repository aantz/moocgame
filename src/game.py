import pygame
from datetime import datetime, timedelta
from random import randint
import robot
import rock
import counters
import settings
import helper

class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.robot = robot.Robot()
        self.clock = pygame.time.Clock()
        self.bolts = []
        self.n_rocks = 3
        self.rocks = [rock.Rock() for _ in range(self.n_rocks)]
        self.level = self.n_rocks -2
        self.level_started = datetime.now()
        self.counters = counters.Counters()
        self.helpers = []
        self.last_helper = datetime.now()
        self.next_helper = datetime.now() + timedelta(seconds = randint(5,20))
        self.game_started = False
        self.game_start_time = None
        self.game_over = False
        self.game_end_time = None
        pygame.display.set_caption("MOOC Game")
        self.game_loop()

    def reset(self):
        self.robot = robot.Robot()
        self.bolts = []
        self.n_rocks = 3
        self.rocks = [rock.Rock() for _ in range(self.n_rocks)]
        self.level = self.n_rocks -2
        self.level_started = datetime.now()
        self.helpers = []
        self.last_helper = datetime.now()
        self.next_helper = datetime.now() + timedelta(seconds = randint(3,10))
        self.game_started = True
        self.game_start_time = datetime.now()
        self.game_over = False
        self.game_end_time = None

    def game_loop(self) -> None:
        while True:
            self.game_over = self.robot.health < 1
            if self.game_over and self.game_end_time is None:
                self.game_end_time = datetime.now()
            if not self.game_over:
                self.set_difficulty()
            self.check_events()
            self.draw_window()

    def set_difficulty(self) -> None:
        if datetime.now() - self.level_started > timedelta(seconds=15):
            self.level_started = datetime.now()
            self.n_rocks += 1
            self.level = self.n_rocks - 2        

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot.direction_left(True)
                    continue
                if event.key == pygame.K_RIGHT:
                    self.robot.direction_right(True)
                    continue
                if event.key == pygame.K_UP:
                    self.robot.direction_up(True)
                    continue
                if event.key == pygame.K_DOWN:
                    self.robot.direction_down(True)
                    continue
                if event.key == pygame.K_SPACE:
                    bolt = self.robot.shoot()
                    if bolt:
                        self.bolts.append(bolt)
                    continue
                if event.key == pygame.K_s:
                    self.reset()
                if event.key == pygame.K_q:
                    exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot.direction_left(False)
                    continue
                if event.key == pygame.K_RIGHT:
                    self.robot.direction_right(False)
                    continue
                if event.key == pygame.K_UP:
                    self.robot.direction_up(False)
                    continue
                if event.key == pygame.K_DOWN:
                    self.robot.direction_down(False)
                    continue

    def draw_window(self) -> None:
        self.window.fill(settings.BLACK)
        if self.game_over:
            self.counters.game_over(self.window, self)
        if not self.game_started:
            self.counters.show_help(self.window)
        if not self.game_over and self.game_started:
            self.robot.draw(self.window)
            self.draw_bolts()
            self.blow_rocks()
            self.draw_rocks()
            self.collide_rocks()
            self.counters.draw(self.window, self)
            self.draw_helpers()
        pygame.display.flip()
        self.clock.tick(60)

    def draw_helpers(self):
        if datetime.now() > self.next_helper:
            self.helpers.append(helper.Helper())
            self.next_helper = datetime.now() + timedelta(seconds = randint(3,10))
        if len(self.helpers) < 1:
            return
        list(map(lambda h: h.robot_collision(self.robot, self.window), self.helpers))           
        self.helpers = [h for h in self.helpers if h.in_bounds()]
        list(map(lambda h: h.draw(self.window), self.helpers))

    def draw_bolts(self) -> None:
        self.bolts = [b for b in self.bolts if b.in_bounds()]
        list(map(lambda b: b.draw(self.window), self.bolts))

    def draw_rocks(self) -> None:
        self.rocks = [r for r in self.rocks if r.in_bounds()]
        new_rocks = [rock.Rock(self.level // 5) for _ in range(self.n_rocks - len(self.rocks))]
        self.rocks.extend(new_rocks)
        list(map(lambda r: r.draw(self.window), self.rocks))

    def blow_rocks(self) -> None:
        if len(self.bolts) < 1 or len(self.rocks) < 1:
            return
        for b in self.bolts:
            if b.hit:
                continue
            list(map(lambda r: r.bolt_hit(b, self.robot), self.rocks))

    def collide_rocks(self) -> None:
        if len(self.rocks) < 1:
            return
        list(map(lambda r: r.robot_collision(self.robot, self.window), self.rocks))           

if __name__ == "__main__":
    Game()
