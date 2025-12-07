# main_fast.py  ← FINAL PERFECT VERSION (NO ERRORS)
import pygame
import math
import random
from car_fast import Car, WIDTH, HEIGHT
from track import get_track_points

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Learns to Drive - One Clear Path")
clock = pygame.time.Clock()

# Sky
for y in range(HEIGHT//2):
    ratio = y / (HEIGHT//2)
    color = (int(100 + ratio*100), int(150 + ratio*80), int(220 + ratio*35))
    pygame.draw.line(screen, color, (0,y), (WIDTH,y))

# Green grass
grass = pygame.Surface((WIDTH, HEIGHT//2))
grass.fill((34, 55, 34))

TRACK_POINTS = get_track_points()

CAMERA_X = 640 - WIDTH//2
CAMERA_Y = 360 - HEIGHT//2

POPULATION_SIZE = 50
cars = [Car(640, 360) for _ in range(POPULATION_SIZE)]
generation = 1

font = pygame.font.SysFont("arial", 30, bold=True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((34, 55, 34))
    screen.blit(grass, (0, HEIGHT//2))

    # ONE SUPER CLEAR ROAD
    offset = [(x - CAMERA_X, y - CAMERA_Y) for x,y in TRACK_POINTS]

    pygame.draw.polygon(screen, (50, 50, 60), offset)
    pygame.draw.lines(screen, (255, 255, 255), True, offset, 20)
    pygame.draw.lines(screen, (255, 255, 0), True, offset, 8)

    # Dashed white center line
    dash = 50
    gap = 40
    for i in range(len(offset)-1):
        x1,y1 = offset[i]
        x2,y2 = offset[(i+1) % len(offset)]
        dx,dy = x2-x1, y2-y1
        dist = math.hypot(dx,dy)
        if dist < 1: continue
        ux,uy = dx/dist, dy/dist
        pos = 0
        while pos < dist:
            start = (x1 + ux*pos, y1 + uy*pos)
            end = (x1 + ux*min(pos+dash,dist), y1 + uy*min(pos+dash,dist))
            pygame.draw.line(screen, (255,255,255), start, end, 8)
            pos += dash + gap

    # Update & draw cars
    alive = [c for c in cars if c.alive]
    for car in alive:
        car.update(TRACK_POINTS, CAMERA_X, CAMERA_Y)
        car.draw(screen, CAMERA_X, CAMERA_Y)

    # Evolution
    if not alive:
        for c in cars: c.calc_fitness()
        cars.sort(key=lambda c: c.fitness, reverse=True)
        print(f"Gen {generation} | Best: {int(cars[0].fitness)}")

        new_cars = []  # ← FIXED: was 'new_c'
        for i in range(POPULATION_SIZE):
            parent = cars[0] if i < 6 else random.choice(cars[:15])
            child = Car(640, 360)
            child.brain = parent.brain.copy()
            child.brain.mutate(0.07)
            new_cars.append(child)
        cars = new_cars  # ← FIXED
        generation += 1

    # HUD
    overlay = pygame.Surface((400, 180))
    overlay.set_alpha(200)
    overlay.fill((0,0,20))
    screen.blit(overlay, (20,20))

    best = cars[0]
    stats = ["AI CAR EVOLUTION", f"GEN: {generation}", f"ALIVE: {len(alive)}", f"BEST: {int(best.fitness):,}", "ONE CLEAR ROAD"]
    colors = [(0,255,255),(255,255,100),(100,255,255),(255,100,200),(150,255,150)]
    for i, (t,c) in enumerate(zip(stats,colors)):
        s = font.render(t, True, c)
        screen.blit(s, (40, 30 + i*32))

    pygame.display.flip()
    clock.tick(300)

pygame.quit()