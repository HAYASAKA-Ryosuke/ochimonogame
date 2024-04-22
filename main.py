import sys
import random
import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, QUIT
from engine import Ball, collision, wall_collision

pygame.init()

clock = pygame.time.Clock()

CLOCK = 200
SCREEN_SIZE_WIDTH = 500
SCREEN_SIZE_HEIGHT = 600
GAME_AREA_START_X = 0
GAME_AREA_END_X = 300
GAME_AREA_START_Y = 130
GAME_AREA_END_Y = SCREEN_SIZE_HEIGHT
screen = pygame.display.set_mode((SCREEN_SIZE_WIDTH, SCREEN_SIZE_HEIGHT))
pygame.display.set_caption('Falling Balls')
background = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 128, 0), (0, 0, 128), (128, 0, 0), (128, 128, 128)]
radiuses = [i for i in range(20, 100 + 10, 10)]

objects = {}
object_count = 0
score = 0


def generate_object(position: tuple, color=None, radius=None) -> dict:
    index = random.randint(0, 4)
    if color is None:
        color = colors[index]
    if radius is None:
        radius = radiuses[index]
    position_y_margin = 20
    return Ball(GAME_AREA_END_Y, position[0], position[1] - radius - position_y_margin, radius, color, 0, 0)


selected_object = generate_object((250, GAME_AREA_START_Y), colors[0], radiuses[0])
next_object = generate_object((250, 0))


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

        wall_collision_detection = wall_collision(objects[object_id], GAME_AREA_START_X, GAME_AREA_END_X)
        if wall_collision_detection['is_updated']:
            if wall_collision_detection['left']:
                objects[object_id].velocity_x = abs(objects[object_id].velocity_x)
                objects[object_id].x = GAME_AREA_START_X + 0.2 + objects[object_id].radius
            if wall_collision_detection['right']:
                objects[object_id].velocity_x = -abs(objects[object_id].velocity_x)
                objects[object_id].x = GAME_AREA_END_X - 0.2 - objects[object_id].radius

        wall_collision_detection = wall_collision(objects[target_object_id], GAME_AREA_START_X, GAME_AREA_END_X)
        if wall_collision_detection['is_updated']:
            if wall_collision_detection['left']:
                objects[target_object_id].velocity_x = abs(objects[target_object_id].velocity_x)
                objects[target_object_id].x = GAME_AREA_START_X + 0.2 + objects[target_object_id].radius
            if wall_collision_detection['right']:
                objects[target_object_id].velocity_x = -abs(objects[target_object_id].velocity_x)
                objects[target_object_id].x = GAME_AREA_END_X - 0.2 - objects[target_object_id].radius

        if updated_positions['is_updated']:
            result.append(object_id)
    return result


def draw_game_area(x, y, width, height):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)


def draw_next_ball_area(x, y, width, height):
    pygame.draw.rect(screen, (128, 128, 128), (x, y, width, height))


def draw_score(x, y, score):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (x, y))


font = pygame.font.Font(None, 36)


def draw_next_ball(start_x, start_y, end_x, end_y, ball):
    pygame.draw.circle(screen, ball.color, (start_x + (end_x // 2), start_y + (end_y // 2)), ball.radius)


def draw_ui():
    screen.fill(background)
    # ゲームエリアの描画
    draw_game_area(GAME_AREA_START_X, GAME_AREA_START_Y, GAME_AREA_END_X, GAME_AREA_END_Y)

    # 次のボールの描画
    next_ball_area_width, next_ball_area_height = 120, 120
    next_ball_area_x = GAME_AREA_END_X + 30
    next_ball_area_y = GAME_AREA_START_Y
    draw_next_ball_area(next_ball_area_x, next_ball_area_y, next_ball_area_width, next_ball_area_height)
    draw_next_ball(next_ball_area_x, next_ball_area_y, next_ball_area_width, next_ball_area_height, next_object)

    # スコアの表示
    score_x = next_ball_area_x
    score_y = next_ball_area_y + next_ball_area_height + 10
    draw_score(score_x, score_y, score)


def update_score(index):
    global score
    match index:
        case 0:
            score += 1
        case 1:
            score += 3
        case 2:
            score += 6
        case 3:
            score += 10
        case 4:
            score += 15
        case 5:
            score += 21
        case 6:
            score += 28
        case 7:
            score += 36
        case 8:
            score += 45
        case 9:
            score += 55


def show_game_over():
    font = pygame.font.Font(None, 72)
    game_over_text = font.render('Game Over', True, (255, 255, 255))
    screen.blit(game_over_text, (100, 200))


running = True
is_game_over = False

while running:
    draw_ui()
    selected_object.draw(screen)
    remove_object_keys = []
    if is_game_over:
        show_game_over()
    for object_id in objects:
        if objects[object_id].y - objects[object_id].radius < GAME_AREA_START_Y and objects[object_id].is_game_area_collision and objects[object_id].velocity_y < 0.2:
            show_game_over()
            is_game_over = True
        if objects[object_id].y + objects[object_id].radius > GAME_AREA_START_Y:
            objects[object_id].is_game_area_collision = True
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
        objects[object_count] = generate_object((obj.x, obj.y + next_object_radius), next_object_color, next_object_radius)
        objects[object_count].is_game_area_collision = True
        object_count += 1
        if not is_game_over:
            update_score(index)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            x, y = event.pos
            if x < selected_object.radius:
                x = selected_object.radius
            if x > GAME_AREA_END_X - selected_object.radius:
                x = GAME_AREA_END_X - selected_object.radius
            selected_object.x = x
            selected_object.y = GAME_AREA_START_Y - selected_object.radius - 20
        if event.type == MOUSEBUTTONDOWN:
            objects[object_count] = selected_object
            object_count += 1
            selected_object = next_object
            next_object = generate_object((x, GAME_AREA_START_Y))
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(CLOCK)
