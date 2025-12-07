# car_fast.py  ← FINAL: CLEAR CRASH + REALISTIC CARS
import pygame, math, random

WIDTH, HEIGHT = 1280, 720

class Brain:
    def __init__(self):
        self.directions = [random.uniform(-1,1) for _ in range(500)]
        self.step = 0
    def mutate(self,rate=0.07):
        for i in range(len(self.directions)):
            if random.random()<rate:
                self.directions[i] += random.uniform(-0.7,0.7)
                self.directions[i] = max(-1,min(1,self.directions[i]))
    def copy(self):
        b = Brain()
        b.directions = self.directions[:]
        return b

class Car:
    def __init__(self,x,y):
        self.x,self.y = x,y
        self.angle = 0
        self.speed = 0
        self.brain = Brain()
        self.alive = True
        self.fitness = self.dist = self.time = 0
        self.color = (random.randint(100,255),random.randint(80,220),random.randint(80,255))

    def is_on_track(self, track_points, cx, cy):
        px, py = self.x - cx, self.y - cy
        min_dist = min(math.hypot(px-x, py-y) for x,y in track_points)
        return min_dist < 130

    def update(self, track_points, cx, cy):
        if not self.alive: return
        self.time += 1
        if self.brain.step < len(self.brain.directions):
            turn = self.brain.directions[self.brain.step]
            self.angle += turn * 6
            self.brain.step += 1

        self.speed = min(self.speed + 0.35, 9.0)
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.x += dx; self.y += dy
        self.dist += self.speed

        # INSTANT CRASH IF OFF ROAD
        if not self.is_on_track(track_points, cx, cy):
            self.alive = False
            # Red flash
            pygame.draw.circle(pygame.display.get_surface(), (255,0,0,120), 
                             (int(self.x-cx), int(self.y-cy)), 80)

    def draw(self,surf,cx,cy):
        x,y = self.x-cx, self.y-cy
        if not (-400<x<WIDTH+400 and -400<y<HEIGHT+400): return

        pygame.draw.ellipse(surf,(0,0,0,130),(x-40,y+25,80,50))

        c,s = math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))
        points = [
            (x + c*42 - s*18, y + s*42 + c*18),
            (x + c*42 + s*18, y + s*42 - c*18),
            (x - c*40 + s*18, y - s*40 - c*18),
            (x - c*40 - s*18, y - s*40 + c*18),
        ]
        color = (255, 220, 60) if self.fitness > 18000 else self.color
        pygame.draw.polygon(surf, color, points)
        pygame.draw.polygon(surf, (255,255,255), points, 6)

        # Windows
        pygame.draw.polygon(surf, (20,30,60,200), [
            (x + c*28 - s*12, y + s*28 + c*12),
            (x + c*28 + s*12, y + s*28 - c*12),
            (x - c*22 + s*12, y - s*22 - c*12),
            (x - c*22 - s*12, y - s*22 + c*12),
        ])

    def calc_fitness(self):
        self.fitness = self.dist*3 + self.time*5
        if self.dist > 25000: self.fitness *= 8