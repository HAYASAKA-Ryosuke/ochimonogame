import sys, random
import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, QUIT

pygame.init()
SCREEN_SIZE_WIDTH = 500
SCREEN_SIZE_HEIGHT = 800
GAME_AREA_START_Y = 200
GAME_AREA_END_Y = SCREEN_SIZE_HEIGHT
screen = pygame.display.set_mode((SCREEN_SIZE_WIDTH, SCREEN_SIZE_HEIGHT))
pygame.display.set_caption('Falling Balls')
background = (255, 255, 255)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 0, 255), (0, 255, 255)]
sizes = [40, 50, 60, 70, 80, 90, 100, 110]

objects = {}


def generate_object(position: tuple) -> dict:
    size = random.choice(sizes)
    return dict(color=random.choice(colors), position=(position[0], position[1] + size), size=size)


def draw_object(color: tuple, position: tuple, size: int):
    pygame.draw.circle(screen, color, position, size)


selected_object = generate_object((250, 0))


while True:
    screen.fill(background)
    pygame.draw.line(screen, (0, 0, 0), (0, GAME_AREA_START_Y), (SCREEN_SIZE_WIDTH, GAME_AREA_START_Y), 5)
    draw_object(selected_object['color'], selected_object['position'], selected_object['size'])
    for object_id in objects:
        color = objects[object_id]['color']
        position = objects[object_id]['position']
        size = objects[object_id]['size']
        draw_object(color, position, size)
        if position[1] <= GAME_AREA_END_Y - size:
            objects[object_id] = dict(color=color, position=(position[0], position[1] + 1), size=size)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            x, y = event.pos
            selected_object['position'] = (x, 0 + selected_object['size'])
        if event.type == MOUSEBUTTONDOWN:
            objects[len(objects) + 1] = selected_object
            selected_object = generate_object((x, 0))
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
