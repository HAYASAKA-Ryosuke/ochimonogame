import sys
import random
import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, QUIT
import copy

pygame.init()

clock = pygame.time.Clock()

CLOCK = 300
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
object_count = 0


def generate_object(position: tuple, color=None, size=None) -> dict:
    index = random.randint(0, 3)
    if color is None:
        color = colors[index]
    if size is None:
        size = sizes[index]
    return dict(color=color, position=(position[0], position[1] + size), size=size)


def draw_object(color: tuple, position: tuple, size: int):
    pygame.draw.circle(screen, color, position, size)


selected_object = generate_object((250, 0), colors[0], sizes[0])


def collision_detection(target_object_id: int):
    result = {}
    for object_id in objects:
        if object_id == target_object_id:
            continue
        dx = objects[target_object_id]['position'][0] - objects[object_id]['position'][0]
        dy = objects[target_object_id]['position'][1] - objects[object_id]['position'][1]
        size = objects[target_object_id]['size'] + objects[object_id]['size']
        if dx ** 2 + dy ** 2 <= size ** 2:
            result[object_id] = copy.deepcopy(objects[object_id]['size'])
    return result


while True:
    screen.fill(background)
    pygame.draw.line(screen, (0, 0, 0), (0, GAME_AREA_START_Y), (SCREEN_SIZE_WIDTH, GAME_AREA_START_Y), 5)
    draw_object(selected_object['color'], selected_object['position'], selected_object['size'])
    remove_object_keys = []
    objects_keys = list(objects.keys())
    for object_id in objects_keys:
        color = objects[object_id]['color']
        position = objects[object_id]['position']
        size = objects[object_id]['size']
        draw_object(color, position, size)
        collision_objects = collision_detection(object_id)
        is_collision = False
        for collision_object_id in collision_objects:
            if collision_objects[collision_object_id] == size:
                remove_object_keys.append((object_id, collision_object_id))
                continue
            is_collision = True
        if position[1] <= GAME_AREA_END_Y - size:
            if not is_collision:
                objects[object_id] = dict(color=color, position=(position[0], position[1] + 1), size=size)

    for remove_object_key in remove_object_keys:
        if objects.get(remove_object_key[0]) is None or objects.get(remove_object_key[1]) is None:
            continue
        is_delete_object = False

        obj = objects[remove_object_key[1] if remove_object_key[0] < remove_object_key[1] else remove_object_key[0]]
        index = sizes.index(obj['size'])
        if index == len(sizes) - 1:
            is_delete_object = True
        else:
            next_object_size = sizes[index + 1]
            next_object_color = colors[index + 1]
        next_object_position = obj['position']
        del objects[remove_object_key[0]]
        del objects[remove_object_key[1]]
        if is_delete_object:
            continue
        objects[object_count] = generate_object(next_object_position, next_object_color, next_object_size)
        object_count += 1

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            x, y = event.pos
            selected_object['position'] = (x, 0 + selected_object['size'])
        if event.type == MOUSEBUTTONDOWN:
            objects[object_count] = selected_object
            object_count += 1
            selected_object = generate_object((x, 0))
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(CLOCK)
