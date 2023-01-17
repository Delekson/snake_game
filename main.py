import pygame
from random import randint
from math import atan2,degrees
from collections import deque

size = 25
width = 800
height = 800
bg = pygame.image.load('resources/background.jpg')

class Apple:
    def __init__(self):
        """
        Initialising the apple object at a pseudo-random location
        """
        self.app_block = pygame.image.load('resources/apple.jpg')

        self.app_x = randint(0,(round(width/size)-1))*size
        self.app_y = randint(0,(round(height/size)-1))*size

    def draw_app(self, screen):
        """
        Draws the apple at coordinates app_x and app_y
        """
        screen.blit(self.app_block, (self.app_x, self.app_y))

    def move_app(self, screen):
        """
        Creates a set of pseudo-random  coordinates for the next apple
        """
        self.app_x = randint(0,(round(width/size)-1))*size
        self.app_y = randint(0,(round(height/size)-1))*size

class Snake:
    def __init__(self, length): 
        """
        Initialising a snake object
        """
        self.head = pygame.image.load("resources/snake_head.jpg")
        self.block = pygame.image.load("resources/block.jpg")
        self.direction_lu = {
                            "up": (0,1),
                            "down": (0,-1),
                            "left": (-1,0),
                            "right": (1,0)
                            }

        self.length = length
        self.direction = self.direction_lu["down"]
        self.x = deque([size])
        self.y = deque([size])

    def draw(self, screen):
        screen.blit(bg, (0,0))
        for i in range(self.length):
            if i == 0:
                screen.blit(self.head, (self.x[i], self.y[i]))
            else:
                screen.blit(self.block, (self.x[i], self.y[i]))
        
    def increase_length(self, screen):
        self.length += 1
        self.x.append(0)
        self.y.append(0)

    def change_direction(self, direction, screen):
        self.direction = self.direction_lu[direction]
    
    def rotation(self, new_direction):
        self.dot = (self.direction[0] * self.direction_lu[new_direction][0]) + (self.direction[1] * self.direction_lu[new_direction][1])
        self.det = (self.direction[0] * self.direction_lu[new_direction][1]) - (self.direction[1] * self.direction_lu[new_direction][0])

        return degrees(atan2(self.det, self.dot))

    def walk(self, screen):
        if self.direction == self.direction_lu["up"]: 
            self.y.appendleft(self.y[0] + (-size))
            self.x.appendleft(self.x[0])
        elif self.direction == self.direction_lu["down"]: 
            self.y.appendleft(self.y[0] + (size))
            self.x.appendleft(self.x[0])
        elif self.direction == self.direction_lu["left"]:
            self.y.appendleft(self.y[0]) 
            self.x.appendleft(self.x[0] + (-size))
        else:
            self.y.appendleft(self.y[0]) 
            self.x.appendleft(self.x[0] + (size))

        self.y.pop()
        self.x.pop()
        self.draw(screen)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game")
        pygame.mixer.init()
        #Making it a class member so it can be access later on in the program/other class functions
        self.screen = pygame.display.set_mode((width, height))

        self.snake = Snake(1)
        self.snake.draw(self.screen)

        self.apple = Apple()
        self.apple.draw_app(self.screen)

    def is_collision(self, apple_x, snake_x, apple_y, snake_y):
        """
        Check if there is a collision between an apple and the snake's head
        """
        test_1 = self.snake.direction[0] - self.snake.direction[1]

        if test_1 < 0:
            apple_x -= 25*self.snake.direction[0]
            apple_y += 25*self.snake.direction[1]
        else:
            snake_x += 25*self.snake.direction[0]
            snake_y -= 25*self.snake.direction[1]

        return (apple_y == snake_y) & (apple_x == snake_x)
 
    def is_snake_col(self, x1, y1, x_body, y_body):
        other_x = x_body.copy()
        other_y = y_body.copy()

        other_x.popleft()
        other_y.popleft()

        for i in range(len(other_x)):
            return self.is_collision(other_x[i], x1, other_y[i], y1)
            #return (x1 == other_x[i] & y1 == other_y[i])

    def render_background(self):
        self.screen.blit(bg, (0, 0))

    def play(self): 
        if self.is_collision(self.apple.app_x, self.snake.x[0], self.apple.app_y, self.snake.y[0]):
            self.apple.move_app(self.screen)
            self.apple.draw_app(self.screen)
            self.snake.increase_length(self.screen)

        if self.is_snake_col(self.snake.x[0], self.snake.y[0], self.snake.x, self.snake.y):
            raise 'Game over'

        self.snake.walk(self.screen)
        self.apple.draw_app(self.screen)
        self.display_score()
        pygame.display.flip()
        pygame.time.wait(120)

    def display_score(self):
        font = pygame.font.SysFont('Courier New', 30, bold = pygame.font.Font.bold)
        score = font.render('Score: ' + str(self.snake.length-1), True, (255, 255, 255),(0,153,0))
        self.screen.blit(score, (0, 0))

    def game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render('Game Over! You scored {} points!'.format(self.snake.length), True, (255, 255, 255))
        self.screen.blit(line1, (200, 200))
        line2 = font.render('Press Enter to play again!', True, (255, 255, 255))
        self.screen.blit(line2, (250, 250))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(1)
        self.apple = Apple()

    def run(self):
        running = True
        pause = False
        while running:
            clock = pygame.time.Clock()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if (key in self.snake.direction_lu)&(pause is False):
                        if self.snake.direction != self.snake.direction_lu[key]:
                            self.cw_rotation = self.snake.rotation(key)
                            self.snake.head = pygame.transform.rotate(self.snake.head, self.cw_rotation)

                        self.snake.change_direction(key, self.screen)

                    if (event.key == pygame.K_RETURN)&(pause is True):
                        pause = False

            try:
                if not pause:
                    self.play()
            except Exception:
                self.game_over()
                pause = True
                self.reset()
            clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()

    