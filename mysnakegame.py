import copy
import sys
import time
import pygame
import random

class SnakeGame:
    def __init__(self):
        self.game = pygame
        self.game.init()
        self.snake_list = [[10, 10]]
        self.food_point = [random.randint(10, 490), random.randint(10, 490)]
        self.screen = self.game.display.set_mode([500, 500])
        self.title = self.game.display.set_caption("贪吃蛇小游戏")
        self.clock = self.game.time.Clock()
        # 初始化蛇的方向
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def reset_game(self):
        self.clock.tick(20)
        self.screen.fill([255, 255, 255])

    def get_game_event(self):
        # 获取游戏事件
        for event in self.game.event.get():
            # 获取键盘事件
            if event.type == self.game.KEYDOWN:
                # 向下运动
                if event.key == self.game.K_DOWN:
                    self.move_up = False
                    self.move_down = True
                    self.move_left = False
                    self.move_right = False

                # 向上运动
                if event.key == self.game.K_UP:
                    self.move_up = True
                    self.move_down = False
                    self.move_left = False
                    self.move_right = False

                # 向左运动
                if event.key == self.game.K_LEFT:
                    self.move_up = False
                    self.move_down = False
                    self.move_left = True
                    self.move_right = False

                # 向右运动
                if event.key == self.game.K_RIGHT:
                    self.move_up = False
                    self.move_down = False
                    self.move_left = False
                    self.move_right = True
            elif event.type == self.game.QUIT:
                self.game.quit()

    def snake_work(self):
        # 蛇身的运动
        snake_length = len(self.snake_list) - 1
        while snake_length > 0:
            self.snake_list[snake_length] = copy.deepcopy(self.snake_list[snake_length - 1])
            snake_length -= 1

        # 蛇头的运动
        if self.move_down:
            self.snake_list[snake_length][1] += 18
            if self.snake_list[snake_length][1] > 500:
                self.snake_list[snake_length][1] = 0
        if self.move_up:
            self.snake_list[snake_length][1] -= 18
            if self.snake_list[snake_length][1] < 0:
                self.snake_list[snake_length][1] = 500
        if self.move_right:
            self.snake_list[snake_length][0] += 18
            if self.snake_list[snake_length][0] > 500:
                self.snake_list[snake_length][0] = 0
        if self.move_left:
            self.snake_list[snake_length][0] -= 18
            if self.snake_list[snake_length][0] < 0:
                self.snake_list[snake_length][0] = 500

    def game_display(self):
        # 食物出现的位置画圆
        food_rect = pygame.draw.circle(self.screen, [255, 0, 0], self.food_point, 10)

        # 循环画出蛇的位置
        snake_rect = []
        for snake_pos in self.snake_list:
            snake_rect.append(pygame.draw.circle(self.screen, [0, 0, 0], snake_pos, 8))     # 蛇的大小与移动的步长要协调
            # 蛇吃到食物变长
            if food_rect.collidepoint(snake_pos):
                self.snake_list.append(self.food_point)
                # 重新生成食物
                self.food_point = [random.randint(10, 490), random.randint(10, 490)]
                break

        time.sleep(0.1)
        # 获取游戏中的蛇头
        snake_head_rect = snake_rect[0]
        count = len(snake_rect)

        # 蛇头咬到蛇的任何位置，游戏结束
        while count > 1:
            if snake_head_rect.colliderect(snake_rect[count - 1]):
                print("游戏结束")
                self.game.quit()
            count -= 1

    def play(self):
        while True:
            try:
                self.reset_game()
                self.get_game_event()
                self.snake_work()
                self.game_display()
                self.game.display.update()
            except:
                sys.exit()

