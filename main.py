import pygame
from pygame.locals import *
import time
import random
import ctypes

#Creating global variables
SIZE = 40
SNAKE_SPEED = .1
WHITE = (255,255,255)

# Getting screen size
user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()
system_w, system_h = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
w = system_w // 40
h = system_h // 40
w = (w-12)*40
h = (h-3)*40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple/apple.png").convert_alpha()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,(w/40)-2)*SIZE
        self.y = random.randint(1,(h/40)-2)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        # Adding snake heads
        self.head_left = pygame.image.load("snake/left.png").convert_alpha()
        self.head_left = pygame.transform.smoothscale(self.head_left, (43, 39))
        
        self.head_right = pygame.image.load("snake/right.png").convert_alpha()
        self.head_right = pygame.transform.smoothscale(self.head_right, (43, 39))
        
        self.head_up = pygame.image.load("snake/up.png").convert_alpha()
        self.head_up = pygame.transform.smoothscale(self.head_up, (43, 39))
        
        self.head_down = pygame.image.load("snake/down.png").convert_alpha()
        self.head_down = pygame.transform.smoothscale(self.head_down, (43, 39))
        #
        
        #self.image = pygame.image.load("resources/block.jpg").convert()
        self.body_image = pygame.image.load("snake/body-round.png").convert_alpha()
        self.body_image = pygame.transform.smoothscale(self.body_image, (40, 38))
        self.direction = 'right'

        self.length = 4
        self.x = [400]*self.length
        self.y = [200]*self.length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        # Creating snake head
        if self.direction == 'left':
            self.parent_screen.blit(self.head_left, (self.x[0], self.y[0]))
        elif self.direction == 'right':
            self.parent_screen.blit(self.head_right, (self.x[0], self.y[0]))
        elif self.direction == 'up':
            self.parent_screen.blit(self.head_up, (self.x[0], self.y[0]))
        elif self.direction == 'down':
            self.parent_screen.blit(self.head_down, (self.x[0], self.y[0]))


        # Creating snake body
        for i in range(1, self.length):
            self.parent_screen.blit(self.body_image, (self.x[i], self.y[i]))
        

        # updating the window
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        #Getting screen size
        #user32 = windll.user32
        #user32.SetProcessDPIAware()
        #system_w, system_h = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

        pygame.mixer.init()
        self.play_background_music()

        #self.surface = pygame.display.set_mode((1000, 760))
        self.surface = pygame.display.set_mode((w, h))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        #pygame.mixer.music.load('resources/bg_music_1.mp3') #for music 1
        pygame.mixer.music.load('resources/bg_music_2.mp3') #for music 2
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("Resources/crash.mp3")
        elif sound_name == 'eat':
            sound = pygame.mixer.Sound("Resources/eat.wav")
        elif sound_name == "gameover":
            sound = pygame.mixer.Sound("Resources/gameover.wav")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("Resources/background.jpg").convert_alpha()
        bg = pygame.transform.smoothscale(bg, (w, h))
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        #self.apple.draw()
        self.display_score()

        font = pygame.font.SysFont('arial',15)
        pause_msg = font.render("Press Space to Pause and Enter to Continue",True, WHITE)
        self.surface.blit(pause_msg,(750,40))
        #pygame.display.flip()
        
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("eat")
            self.snake.increase_length()
            self.apple.move()
            self.apple.draw()
        else:
            self.apple.draw()

        # checking if apple appears in snake's body or not
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                #self.snake.increase_length()
                self.apple.move()
                self.apple.draw()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        # checking if snake is colliding with boundries
        if not (0 <= self.snake.x[0] <= w-40 and 0 <= self.snake.y[0] <= h-40):
            self.play_sound('crash')
            raise "Hit the boundry"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length-4}",True, WHITE)
        self.surface.blit(score,(850,10))


    def show_game_over(self):
        # Storing High score
        score_file = open("score.txt", "r+")
        high_score = int(score_file.read())
        if high_score < self.snake.length-4:
            score_file.seek(0) 
            score_file.truncate()
            score_file.write(str(self.snake.length-4))
            high_score = self.snake.length-4
        score_file.close()
        #print(high_score)

        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length-4}. High score: {high_score}", True, WHITE)
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, WHITE)
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        self.play_sound("gameover")
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  #escape
                        running = False

                    if event.key == K_RETURN:  #enter
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_SPACE:  #space
                        pause = True
                        pygame.mixer.music.pause()

                    if not pause:
                        if event.key == K_LEFT:  #left arrow
                            if self.snake.direction != "right":
                                self.snake.move_left()

                        if event.key == K_RIGHT:  #right arrow
                            if self.snake.direction != "left":
                                self.snake.move_right()

                        if event.key == K_UP:  #up arrow
                            if self.snake.direction != "down":
                                self.snake.move_up()

                        if event.key == K_DOWN:   #down arrow
                            if self.snake.direction != "up":
                                self.snake.move_down()

                elif event.type == QUIT:  #cross button of window
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(SNAKE_SPEED)

        pygame.quit() #uninitialize all pygame modules
        quit()

if __name__ == '__main__':
    game = Game()
    game.run()
