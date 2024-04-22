import sys
import random
import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, QUIT
from engine import Ball, collision, wall_collision

pygame.init()

clock = pygame.time.Clock()

CLOCK = 200
SCREEN_SIZE_WIDTH = 300
SCREEN_SIZE_HEIGHT = 800
GAME_AREA_START_Y = 200
GAME_AREA_END_Y = SCREEN_SIZE_HEIGHT
screen = pygame.display.set_mode((SCREEN_SIZE_WIDTH, SCREEN_SIZE_HEIGHT))
pygame.display.set_caption('Falling Balls')
background = (255, 255, 255)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 0, 255), (0, 255, 255)]
radiuses = [i for i in range(20, 100 + 10, 10)]

objects = {}
object_count = 0


def generate_object(position: tuple, color=None, radius=None) -> dict:
    index = random.randint(0, 3)
    if color is None:
        color = colors[index]
    if radius is None:
        radius = radiuses[index]
    return Ball(GAME_AREA_END_Y, position[0], position[1] + radius, radius, color, 0, 0)


selected_object = generate_object((250, 0), colors[0], radiuses[0])


def collision_detection(target_object_id: int):
    result = []
    for object_id in objects:
        if object_id == target_object_id:
            continue
        updated_positions = collision(objects[object_id], objects[target_object_id])
        if updated_positions['is_updated']:
            objects[object_id].x = updated_positions['ball1_x']
            objects[object_id].y = updated_positions['ball1_y']
            objects[object_id].velocity_x = updated_positions['ball1_velocity_x']
            objects[object_id].velocity_y = updated_positions['ball1_velocity_y']
            objects[target_object_id].x = updated_positions['ball2_x']
            objects[target_object_id].y = updated_positions['ball2_y']
            objects[target_object_id].velocity_x = updated_positions['ball2_velocity_x']
            objects[target_object_id].velocity_y = updated_positions['ball2_velocity_y']

        wall_collision_detection = wall_collision(objects[object_id], SCREEN_SIZE_WIDTH)
        if wall_collision_detection['is_updated']:
            if wall_collision_detection['left']:
                objects[object_id].velocity_x = abs(objects[object_id].velocity_x)
                objects[object_id].x = 0.2 + objects[object_id].radius
            if wall_collision_detection['right']:
                objects[object_id].velocity_x = -abs(objects[object_id].velocity_x)
                objects[object_id].x = SCREEN_SIZE_WIDTH - 0.2 - objects[object_id].radius

        wall_collision_detection = wall_collision(objects[target_object_id], SCREEN_SIZE_WIDTH)
        if wall_collision_detection['is_updated']:
            if wall_collision_detection['left']:
                objects[target_object_id].velocity_x = abs(objects[target_object_id].velocity_x)
                objects[target_object_id].x = 0.2 + objects[target_object_id].radius
            if wall_collision_detection['right']:
                objects[target_object_id].velocity_x = -abs(objects[target_object_id].velocity_x)
                objects[target_object_id].x = SCREEN_SIZE_WIDTH - 0.2 - objects[target_object_id].radius

        if updated_positions['is_updated']:
            result.append(object_id)
    return result


while True:
    screen.fill(background)
    pygame.draw.line(screen, (0, 0, 0), (0, GAME_AREA_START_Y), (SCREEN_SIZE_WIDTH, GAME_AREA_START_Y), 5)
    selected_object.draw(screen)
    remove_object_keys = []
    for object_id in objects:
        color = objects[object_id].color
        position = (objects[object_id].x, objects[object_id].y)
        radius = objects[object_id].radius
        collision_objects = collision_detection(object_id)
        for collision_object_id in collision_objects:
            if objects[collision_object_id].radius == radius:
                remove_object_keys.append((object_id, collision_object_id))
                continue
        objects[object_id].move()
        objects[object_id].draw(screen)

    for remove_object_key in remove_object_keys:
        if objects.get(remove_object_key[0]) is None or objects.get(remove_object_key[1]) is None:
            continue
        is_delete_object = False

        obj = objects[remove_object_key[1] if remove_object_key[0] < remove_object_key[1] else remove_object_key[0]]
        index = radiuses.index(obj.radius)
        if index == len(radiuses) - 1:
            is_delete_object = True
        else:
            next_object_radius = radiuses[index + 1]
            next_object_color = colors[index + 1]
        next_object_position = (obj.x, obj.y)
        del objects[remove_object_key[0]]
        del objects[remove_object_key[1]]
        if is_delete_object:
            continue
        # ボールを成長させる
        objects[object_count] = generate_object((obj.x, obj.y - next_object_radius), next_object_color, next_object_radius)
        object_count += 1

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            x, y = event.pos
            selected_object.x = x
            selected_object.y = selected_object.radius
        if event.type == MOUSEBUTTONDOWN:
            objects[object_count] = selected_object
            object_count += 1
            selected_object = generate_object((x, 0))
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(CLOCK)
