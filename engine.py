import pygame
import math


def wall_collision(ball, start_width, end_width):
    # 左端か右端に衝突した場合
    return {
        'is_updated': ball.x - ball.radius <= start_width or ball.x + ball.radius >= end_width,
        'left': ball.x - ball.radius <= start_width,
        'right': ball.x + ball.radius >= end_width,
    }


def collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    restitution = 0.2  # 1に近い弾性的,0に近い非弾性
    if distance < ball1.radius + ball2.radius:
        # ボール間の距離を調整
        overlap = ball1.radius + ball2.radius - distance

        # ボールの衝突角を計算
        angle = math.atan2(dy, dx)

        # 速度分解
        velocity1 = math.sqrt(ball1.velocity_x ** 2 + ball1.velocity_y ** 2)
        velocity2 = math.sqrt(ball2.velocity_x ** 2 + ball2.velocity_y ** 2)
        theta1 = math.atan2(ball1.velocity_y, ball1.velocity_x)
        theta2 = math.atan2(ball2.velocity_y, ball2.velocity_x)

        # 衝突後の速度
        velocity1_x = velocity1 * math.cos(theta1 - angle)
        velocity1_y = velocity1 * math.sin(theta1 - angle)
        velocity2_x = velocity2 * math.cos(theta2 - angle)
        velocity2_y = velocity2 * math.sin(theta2 - angle)

        # 速度更新
        final_velocity1_x = restitution * velocity1_x
        final_velocity2_x = restitution * velocity2_x
        final_velocity1_y = velocity1_y
        final_velocity2_y = velocity2_y

        # ボールの位置を調整
        return {
            'is_updated': True,
            'ball1_x': ball1.x - overlap * math.cos(angle) / 2,
            'ball1_y': ball1.y - overlap * math.sin(angle) / 2,
            'ball1_velocity_x': math.cos(angle) * final_velocity1_x + math.cos(angle + math.pi / 2) * final_velocity1_y,
            'ball1_velocity_y': math.sin(angle) * final_velocity1_x + math.sin(angle + math.pi/2) * final_velocity1_y,
            'ball2_x': ball2.x + overlap * math.cos(angle) / 2,
            'ball2_y': ball2.y + overlap * math.sin(angle) / 2,
            'ball2_velocity_x': math.cos(angle) * final_velocity2_x + math.cos(angle + math.pi / 2) * final_velocity2_y,
            'ball2_velocity_y': math.sin(angle) * final_velocity2_x + math.sin(angle + math.pi / 2) * final_velocity2_y
        }
    return {
        'is_updated': False,
        'ball1_x': ball1.x,
        'ball1_y': ball1.y,
        'ball1_velocity_x': ball1.velocity_x,
        'ball1_velocity_y': ball1.velocity_y,
        'ball2_x': ball2.x,
        'ball2_y': ball2.y,
        'ball2_velocity_x': ball2.velocity_x,
        'ball2_velocity_y': ball2.velocity_y
    }


class Ball:
    def __init__(self, height, x, y, radius, color, velocity_x, velocity_y):
        self.height = height
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.friction = 0.2
        self.is_game_area_collision = False

    def move(self):
        # 重力と摩擦による速度の更新
        self.velocity_y += 0.8  # 重力加速度
        # 摩擦による速度減衰
        self.velocity_x *= (1 - self.friction)
        self.velocity_y *= (1 - self.friction)

        # 移動
        self.x += self.velocity_x
        self.y += self.velocity_y

        # 地面との衝突
        if self.y + self.radius >= self.height:
            self.y = self.height - self.radius
            self.velocity_y = -self.velocity_y * 0.01  # 反発係数で調整
            self.angular_velocity = -self.velocity_x / self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
