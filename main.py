import pygame
from pygame.locals import *
import time
import random
import ctypes

#Creating global variables
SIZE = 40
SNAKE_SPEED = .1
WHITE = (255,255,255)

# Getting screen size so that it can draw a game window less that the screen resolution
user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()
system_w, system_h = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
w = system_w // 40
h = system_h // 40
w = (w-12)*40
h = (h-3)*40


# Main class to create Apple
class Apple:
    def __init__(self, parent_screen):
        '''
        Initializes all the attributes of apple object
        
        Input:
            self: the apple object itself
            parent_screen: the reference of the main window on which the apple will be drawn

        Output: Returns nothing other than initializing the attributes of the object
        '''
        self.parent_screen = parent_screen  #setting parent window 
        self.image = pygame.image.load("apple/apple.png").convert_alpha()  #loading the apple image
        self.x = 120 # setting initial x position for apple
        self.y = 120 # setting initial y position for apple

    def draw(self):
        '''
        Draws the apple image on the game window on the specified x,y coordinate
        
        Input:
            self: the apple object itself
            
        Output: returns nothing other than drawing the apple image
        '''
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        '''
        Moves apple position randomly
        
        Input:
            self: the apple object itself
        
        Output: returns nothing other than changing the x,y position
        '''
        self.x = random.randint(1,(w/40)-2)*SIZE
        self.y = random.randint(1,(h/40)-2)*SIZE


# Main class to create Snake
class Snake:
    def __init__(self, parent_screen):
        '''
        Initializes all the attributes of snake object
        
        Input:
            self: the snake object itself
            parent_screen: the reference of the main window on which the apple will be drawn

        Output: Returns nothing other than initializing the attributes of the object
        '''
        self.parent_screen = parent_screen #setting parent window
        
        # START - Loading snake heads of different angles
        self.head_left = pygame.image.load("snake/left.png").convert_alpha()
        self.head_left = pygame.transform.smoothscale(self.head_left, (43, 39))
        
        self.head_right = pygame.image.load("snake/right.png").convert_alpha()
        self.head_right = pygame.transform.smoothscale(self.head_right, (43, 39))
        
        self.head_up = pygame.image.load("snake/up.png").convert_alpha()
        self.head_up = pygame.transform.smoothscale(self.head_up, (43, 39))
        
        self.head_down = pygame.image.load("snake/down.png").convert_alpha()
        self.head_down = pygame.transform.smoothscale(self.head_down, (43, 39))
        # END - Loading snake heads of different angles

        self.body_image = pygame.image.load("snake/body-round.png").convert_alpha() # Loading the body image of the snake
        self.body_image = pygame.transform.smoothscale(self.body_image, (40, 38)) # Scaling the body image to (40,38) size
        
        self.direction = 'right' # Setting the initial direction of the snake
        self.length = 4 # Setting the initial length of the snake
        
        self.x = [400, 360, 320, 280] # Setting the initial x coordinates of the snake blocks
        self.y = [200]*self.length # Setting the initial y coordinates of the snake blocks

    def move_left(self):
        '''
        Change the direction of the snake object to left
        
        Input:
            self: the snake object itself

        Output: Returns nothing other than changing the direction
        '''
        self.direction = 'left' # Changing the direction to left

    def move_right(self):
        '''
        Change the direction of the snake object to right
        
        Input:
            self: the snake object itself

        Output: Returns nothing other than changing the direction
        '''
        self.direction = 'right' # Changing the direction to right

    def move_up(self):
        '''
        Change the direction of the snake object to upward
        
        Input:
            self: the snake object itself

        Output: Returns nothing other than changing the direction
        '''
        self.direction = 'up' # Changing the direction to upward

    def move_down(self):
        '''
        Change the direction of the snake object to downward
        
        Input:
            self: the snake object itself

        Output: Returns nothing other than changing the direction
        '''
        self.direction = 'down' # Changing the direction to downward

    def walk(self):
        '''
        Change the x,y coordinates of each block of the snake object so that it can be redrawn to make feel the user the snake is walking
        
        Input:
            self: the snake object itself

        Output: Returns nothing other than changing the x,y coordinates
        '''
        
        # START - updating x,y coordinates of each block (excluding the head) with it's previous block
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        # END - updating x,y coordinates of each block (excluding the head) with it's previous block

        # START - updating the x or y coordinate of the head block based on current direction of the snake
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        # END - updating the x or y coordinate of the head block based on current direction of the snake

        self.draw() # finally drawing the snake with updated x,y values

    def draw(self):
        '''
        Draws the snake on the game window
        
        Input:
            self: the snake object itself

        Output: Returns nothing other than drawing the snake
        '''
        # START - Drawing the snake head based on it's current direction
        if self.direction == 'left':
            self.parent_screen.blit(self.head_left, (self.x[0], self.y[0])) #drawing the specified snake head image on the specified x,y position
        elif self.direction == 'right':
            self.parent_screen.blit(self.head_right, (self.x[0], self.y[0])) #drawing the specified snake head image on the specified x,y position
        elif self.direction == 'up':
            self.parent_screen.blit(self.head_up, (self.x[0], self.y[0])) #drawing the specified snake head image on the specified x,y position
        elif self.direction == 'down':
            self.parent_screen.blit(self.head_down, (self.x[0], self.y[0])) #drawing the specified snake head image on the specified x,y position
        # END - Drawing the snake head based on it's current direction


        # START - Drawing the snake body based on the game window
        for i in range(1, self.length):
            self.parent_screen.blit(self.body_image, (self.x[i], self.y[i]))
        # END - Drawing the snake body based on the game window
        
        pygame.display.flip() # updating the game window

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


# Main class which creates the game and enable the user to play it
class Game:
    def __init__(self):
        '''
        Initializes all the attributes of Game object
        
        Input:
            self: the Game object itself

        Output: Returns nothing other than initializing the attributes of the object
        '''
        pygame.init() # initializing all the submodules of pygame
        pygame.display.set_caption("Snake Game") # Setting the title of the game window

        pygame.mixer.init() # initializing the mixer module 
        self.play_background_music() # calling the funtion that plays background music

        #self.surface = pygame.display.set_mode((1000, 760))
        self.surface = pygame.display.set_mode((w, h)) # Creates the game window based on system resolution
        self.snake = Snake(self.surface) # Creating snake object
        self.snake.draw() # calling the function that draws the snake on the game window
        self.apple = Apple(self.surface) # Creating apple object
        self.apple.draw() # calling the function that draws the apple on the game window

    def play_background_music(self):
        '''
        Load and plays background music
        
        Input:
            self: the Game object itself

        Output: Returns nothing other than playing the music
        '''
        pygame.mixer.music.load('resources/bg_music_2.mp3') # loading backgroud music file
        pygame.mixer.music.set_volume(0.3);
        pygame.mixer.music.play(-1, 0) # playing the audio

    def play_sound(self, sound_name):
        '''
        Loads and plays different sound based on snake's action
        
        Input:
            self: the Game object itself
            sound_name: name of the sound specifing which sound to play

        Output: Returns nothing other than playing the sound
        '''
        if sound_name == "crash":
            sound = pygame.mixer.Sound("Resources/crash.mp3") # loads the crash sound
        elif sound_name == 'eat':
            sound = pygame.mixer.Sound("Resources/eat.wav") # loads the eating sound
        elif sound_name == "gameover":
            sound = pygame.mixer.Sound("Resources/gameover.wav") # loads the game over voice

        pygame.mixer.Sound.play(sound) # playing the loaded sound

    def reset(self):
        '''
        Re-initialize the snake and apple variables
        
        Input:
            self: the Game object itself

        Output: Returns nothing other than re-initializing the snake and apple variables
        '''
        self.snake = Snake(self.surface) # creating new snake object
        self.apple = Apple(self.surface) # creating new apple object

    def is_collision(self, x1, y1, x2, y2):
        '''
        Checks collision of two blocks based on their x and y positions
        
        Input:
            self: the Game object itself
            x1: x position of first object
            y1: y position of first object
            x2: x position of second object
            y2: y position of second object

        Output: Returns a boolean value if two blocks are colliding each other
        '''
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        '''
        Loads the background image and set that as backgroud
        
        Input:
            self: the Game object itself

        Output: Returns nothing other than setting background image
        '''
        bg = pygame.image.load("Resources/background.jpg").convert_alpha() # loads thr image
        bg = pygame.transform.smoothscale(bg, (w, h)) # scaling the image to game window's width and height
        self.surface.blit(bg, (0,0)) # draws the background image on the game window

    def play(self):
        '''
        Updates the game window and handle differnet events
        
        Input:
            self: the Game object itself

        Output: Returns nothing
        '''
        self.render_background() # calling the method that draws background image
        self.snake.walk() # change the positions of the snake
        #self.apple.draw()
        self.display_score() # calling the method that displays score

        font = pygame.font.SysFont('arial',20) # creating font object from system font
        pause_msg = font.render("Press Space to Pause and Enter to Continue",True, WHITE)
        self.surface.blit(pause_msg,(w//2-150, h-30)) # prints the msg at specified position
        #pygame.display.flip()
        
        pygame.display.flip() # updating the game window

        # checking if snake ate the apple by checking collision between them
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("eat") # play eat sound
            self.snake.increase_length() # increase the snake length
            self.apple.move() # move the apple to a random position
            self.apple.draw() # draws the apple to that position
        else:
            self.apple.draw() # snake doesn't eat the apple then draw the apple at the same position

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
        '''
        Displays the score on the top right corner
        
        Input:
            self: the Game object itself

        Output: Returns nothing
        '''
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length-4}",True, WHITE)
        self.surface.blit(score,(850,10))


    def show_game_over(self):
        '''
        Checks and store high score and displays the game over msg
        
        Input:
            self: the Game object itself

        Output: Returns nothing
        '''
        # Storing High score logic
        score_file = open("score.txt", "r+") # opening the score file
        high_score = int(score_file.read()) # reading the score from the file
        if high_score < self.snake.length-4: # checking if current score is > high score
            score_file.seek(0) # moving file pointer to index 0(starting of file)
            score_file.truncate() # delete everything from the file from start
            score_file.write(str(self.snake.length-4)) # write the new score
            high_score = self.snake.length-4 # creating a new variable called high_score
        score_file.close() # closing the file
        #print(high_score)

        self.render_background() # draws the background
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length-4}. High score: {high_score}", True, WHITE)
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, WHITE)
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.rewind() # Resets playback of the current music to the beginning
        pygame.mixer.music.pause()
        self.play_sound("gameover")
        pygame.display.flip()

    def run(self):
        '''
        Runs event loop and performs some operation based on specified events
        
        Input:
            self: the Game object itself

        Output: Returns nothing
        '''
        running = True # flag variable to run the loop upto a specified condition
        pause = False # flag variable to pause the loop when pause event occurs

        # main event loop
        while running:
            for event in pygame.event.get(): # getting all the events that occurs
                if event.type == KEYDOWN: # checking if the event is a keyboard keypress event
                    if event.key == K_ESCAPE:  # checking if the event is escape key press event
                        running = False

                    if event.key == K_RETURN:  # checking if the event is enter key press event
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_SPACE:  # checking if the event is space key press event
                        pause = True
                        pygame.mixer.music.pause()

                    if not pause: # checking if game is paused or  not
                        if event.key == K_LEFT:  # checking if left arrow key pressed
                            if self.snake.direction != "right":
                                self.snake.move_left()

                        if event.key == K_RIGHT:  # checking if right arrow key pressed
                            if self.snake.direction != "left":
                                self.snake.move_right()

                        if event.key == K_UP:  # checking if up arrow key pressed
                            if self.snake.direction != "down":
                                self.snake.move_up()

                        if event.key == K_DOWN:   # checking if down arrow key pressed
                            if self.snake.direction != "up":
                                self.snake.move_down()

                elif event.type == QUIT:  # checking if cross button of window is pressed
                    running = False
            try:

                if not pause:
                    self.play() # running the play method every time if game not paused

            except Exception as e:
                self.show_game_over() # if play() throws exception that means game over
                pause = True
                self.reset() # reset the snake and apple object

            time.sleep(SNAKE_SPEED)

        pygame.quit() #uninitialize all pygame modules
        quit()

if __name__ == '__main__':
    game = Game()
    game.run()
