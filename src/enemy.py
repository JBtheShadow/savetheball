import pygame
from abc import abstractmethod
from random import random, randint
from enum import Enum
from math import sqrt
from globals import *

class Enemy:
    class Mode(Enum):
        CHASE = 1
        ROAM = 2

    def faded_color(self, color):
        r, g, b = color
        return r // 2 + 13, g // 2 + 13, b // 2 + 13

    def distance(self, x1, y1, x2=None, y2=None):
        if x2 is not None and y2 is not None:
            dx, dy = x2 - x1, y2 - y1
        else:
            dx, dy = x1, y1
        return sqrt(dx ** 2 + dy ** 2)

    def rand_color_offset(self, color_value):
        return max(0, min(color_value + randint(0, 80) - 40, 255))

    def rand_start_pos(self):
        return {
            1: (random() * WIDTH, -self.radius * 4.0),
            2: (WIDTH + self.radius * 4.0, random() * HEIGHT),
            3: (random() * WIDTH, HEIGHT + self.radius * 4.0),
            4: (-self.radius * 4.0, random() * HEIGHT)
        }[randint(1, 4)]

    def rand_target_pos(self):
        return random() * WIDTH, random() * HEIGHT

    def diamond_circle_collision(self, other_x, other_y, other_radius):
        edge_x = self.x + (-1 if other_x < self.x else 1) * self.radius
        edge_y = self.y + (-1 if other_y < self.y else 1) * self.radius
        short_radius = self.radius / sqrt(2)

        d1 = self.distance(edge_x, self.y, other_x, other_y)
        d2 = self.distance(self.x, edge_y, other_x, other_y)

        return (d1 <= other_radius or d2 <= other_radius or 
                d1 + d2 <= 2 * short_radius * (1 + short_radius / other_radius))
    
    def circle_circle_collision(self, other_x, other_y, other_radius):
        d = self.distance(self.x, self.y, other_x, other_y)
        return d <= other_radius + self.radius

    def target_delta(self, other_x, other_y):
        if self.mode == self.Mode.CHASE:
            return other_x - self.x, other_y - self.y
        else:
            return self.target_x - self.x, self.target_y - self.y

    def toggle_mode(self):
        if self.mode == self.Mode.ROAM:
            self.mode = self.Mode.CHASE
            self.target_x = None
            self.target_y = None
        else:
            self.mode = self.Mode.ROAM
            self.target_x, self.target_y = self.rand_target_pos()

    def draw_diamond(self, win, color):
        points = (
            (self.x,               self.y - self.radius),
            (self.x + self.radius, self.y              ),
            (self.x,               self.y + self.radius),
            (self.x - self.radius, self.y              )
        )
        pygame.draw.polygon(win, color, points)

    def draw_spike(self, win, color):
        self.draw_diamond(win, color)
        radius = self.radius / sqrt(2)
        points = (
            (self.x - radius, self.y - radius),
            (self.x + radius, self.y - radius),
            (self.x + radius, self.y + radius),
            (self.x - radius, self.y + radius)
        )
        pygame.draw.polygon(win, color, points)

    def draw_circle(self, win, color):
        pygame.draw.circle(win, color, (self.x, self.y), self.radius)

    def __init__(self, level = 1):
        self.level = level
        self.radius = 20
        self.x, self.y = self.rand_start_pos()
        self.mode = self.Mode.ROAM
        self.target_x, self.target_y = self.rand_target_pos()

    @abstractmethod
    def check_touched(self, other_x, other_y, other_radius):
        pass

    @abstractmethod
    def draw(self, win):
        pass
    
    def move(self, other_x, other_y, dt):
        dx, dy = self.target_delta(other_x, other_y)
        dp = self.distance(dx, dy)
        step = 1 + (self.level - 1) * 0.1
        if dp > 0:
            self.x += (step if step < dp else dp) * dx/dp
            self.y += (step if step < dp else dp) * dy/dp
        elif self.mode == self.Mode.ROAM:
            self.target_x, self.target_y = self.rand_target_pos()

class Chaser(Enemy):
    def __init__(self, level=1):
        super().__init__(level)
        self.chaseColor = (255, self.rand_color_offset(50), self.rand_color_offset(25))
        self.toggle_mode()

    def check_touched(self, other_x, other_y, other_radius):
        return self.diamond_circle_collision(other_x, other_y, other_radius)

    def draw(self, win):
        self.draw_diamond(win, self.chaseColor)
        pygame.draw.rect(WIN, self.faded_color(self.chaseColor), (self.x - 8, self.y - 8, 16, 16), border_radius = 5)

class Roamer(Enemy):
    def __init__(self, level=1):
        super().__init__(level)
        self.radius = 10
        self.roamColor = (self.rand_color_offset(128), self.rand_color_offset(128), self.rand_color_offset(128))
    
    def check_touched(self, other_x, other_y, other_radius):
        return self.circle_circle_collision(other_x, other_y, other_radius)

    def draw(self, win):
        self.draw_circle(win, self.roamColor)
        pygame.draw.circle(WIN, self.faded_color(self.roamColor), (self.x, self.y), self.radius / 2.5)

class Switcher(Enemy):
    def __init__(self, level=1):
        super().__init__(level)
        self.radius = 15
        self.roamColor = (self.rand_color_offset(128), self.rand_color_offset(100), 255)
        self.chaseColor = (self.rand_color_offset(50), self.rand_color_offset(25), 255)
        self.mode_timer = 0

    def check_touched(self, other_x, other_y, other_radius):
        return self.diamond_circle_collision(other_x, other_y, other_radius)

    def move(self, other_x, other_y, dt):
        super().move(other_x, other_y, dt)
        self.mode_timer += dt
        if self.mode_timer > 15:
            self.mode_timer = 0
            self.toggle_mode()

    def draw(self, win):
        color = self.chaseColor if self.mode == self.Mode.CHASE else self.roamColor
        self.draw_diamond(win, color)
        pygame.draw.rect(WIN, self.faded_color(color), (self.x - self.radius + 5, self.y - 3, 2 * self.radius - 10, 6), border_radius = 5)

class Bully(Enemy):
    def __init__(self, level=1):
        super().__init__(level)
        self.radius = 15
        self.roamColor = (255, self.rand_color_offset(150), self.rand_color_offset(50))
        self.chaseColor = (255, self.rand_color_offset(100), self.rand_color_offset(75))

    def check_touched(self, other_x, other_y, other_radius):
        return self.circle_circle_collision(other_x, other_y, other_radius)

    def move(self, other_x, other_y, dt):
        super().move(other_x, other_y, dt)
        d = self.distance(self.x, self.y, other_x, other_y)
        if self.mode == self.Mode.CHASE and d > 150 or self.mode == self.Mode.ROAM and d <= 150:
            self.toggle_mode()

    def draw(self, win):
        color = self.chaseColor if self.mode == self.Mode.CHASE else self.roamColor
        self.draw_spike(win, color)
        pygame.draw.circle(WIN, self.faded_color(color), (self.x, self.y), 7)