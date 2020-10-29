import pygame
from pygame.draw import *
from random import randrange as rnd
import math
import time
pygame.init()

screen = pygame.display.set_mode((800, 600))
rect(screen, (255, 255, 255), (0, 0, 800, 600))
#установка частоты кадров 
FPS = 30

#цвета
Blue = (0, 0, 255)
Green = (0, 128, 0)
Red = (255, 0, 0)
Brown = (165, 42, 42)
Orange = (255, 165, 0)
Black = (0, 0, 0)
White = (255, 255, 255)

class target():
    def __init__(self):
        self.points = 0
        
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = Red
        circle(screen, color, (x, y), r)

    def main_target(self):
        x = self.x 
        y = self.y 
        r = self.r
        color = self.color = Red
        circle(screen, color, (x, y), r)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

t1 = target()
t1.new_target()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    t1.main_target()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.MOUSEMOTION:
            pass
    
       
    pygame.display.update()
    screen.fill(White)

pygame.quit()
