import pygame
from pygame.draw import *
from random import randrange as rnd
from random import randint as rndi
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
Colors = [Blue, Green, Red, Brown]

class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = Colors[rndi(0, 3)]
        circle(screen, self.color, (self.x, self.y), self.r)
    
    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        if self.y < 500 or abs(self.vy) >= 10:
            self.y -= self.vy
            self.vy -= 10 / FPS
        else:
            self.vy = 0
            self.y = 500
        if self.x > 800:
            self.x = 800
            self.vx = - 0.5 * self.vx
            self.vy = 0.9 * self.vy
        if self.y >= 500:
            self.y = 500
            self.vy = - 0.8 * self.vy
            self.vx = 0.8 * self.vx
        if abs(self.vx) >= 0.1 or abs(self.vy) > 0:
            circle(screen, self.color, (int(self.x), int(self.y)), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if isinstance(obj, target):
            if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
                return True
            else:
                return False

class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x1 = self.x2 = 20
        self.y1 = self.y2 = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.pos[1]-new_ball.y) / (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.x2 = self.x1 + max(self.f2_power, 20) * math.cos(self.an)
            self.y2 = self.y1 + max(self.f2_power, 20) * math.sin(self.an)
            line(screen, Orange, (self.x1, self.y1), (int(self.x2), int(self.y2)), 7)
        else:
            self.x2 = self.x1 + 20 * math.cos(self.an)
            self.y2 = self.y1 + 20 * math.sin(self.an)
            line(screen, Black, (self.x1, self.y1), (int(self.x2), int(self.y2)), 7)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            line(screen, Orange, (self.x1, self.y1), (int(self.x2), int(self.y2)), 7)
        else:
            line(screen, Black, (self.x1, self.y1), (int(self.x2), int(self.y2)), 7)
           

class target():
    def __init__(self):
        self.points = 0
        
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(200, 450)
        r = self.r = rnd(20, 50)
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
        self.new_target()

t1 = target()
g1 = gun()
bullet = 0
balls = []
t1.new_target()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    t1.main_target()
    g1.power_up()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print('Вы набрали', t1.points, 'очков')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            g1.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            g1.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            g1.targetting(event)
            pygame.display.update()
    if balls:
        for b in balls:
            b.move()
            if b.hittest(t1):
                t1.hit()
    pygame.display.update()
    screen.fill(White)

pygame.quit()
