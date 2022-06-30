import pygame

class Bolt:
    image = pygame.image.load("bolt.png")

    def __init__(self, point: tuple, v: int = -10) -> None:
        self.x = point[0]
        self.y = point[1]
        self.v = v
        self.hit = False

    def in_bounds(self) -> bool:
        return self.y + Bolt.image.get_height() >= 0

    def draw(self, window: pygame.Surface) -> None:
        self.y += self.v
        if not self.hit:
            window.blit(Bolt.image, (self.x, self.y))
