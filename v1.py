import pygame
from pygame.locals import *

#Creating global variables
TITLE = 'Snake game by Soumajit'

def draw_block():
    print(block_x, block_y)
    surface.fill((0, 0, 0)) #setting background color
    surface.blit(block, (block_x, block_y)) # print that block at 100, 100 position
    pygame.display.flip() #Update the full display Surface to the screen
    

if __name__ == "__main__":

    #initialize all imported pygame modules
    pygame.init()

    #Initialize a window or screen for display
    surface = pygame.display.set_mode((800, 720))

    #set the window title
    pygame.display.set_caption(TITLE)

    surface.fill((0, 0, 0)) #setting background color
    block = pygame.image.load("Resources/block.jpg").convert() #loading snake image
    block_x = 0
    block_y = 0
    surface.blit(block, (block_x, block_y)) # print that block at 100, 100 position

    #Update the full display Surface to the screen
    pygame.display.flip()

    #To start our event loop we initialize this variable as True so that it can run for infinite times until we press the close button
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #if any key pressed from keyboard
                if event.key == K_ESCAPE: #if pressed escape key
                    running = False
                if event.key == K_LEFT: #if pressed left arrow
                    block_x -= 40
                    draw_block()
                if event.key == K_RIGHT: #if pressed right arrow
                    block_x += 40
                    draw_block()
                if event.key == K_UP: #if pressed up arrow
                    block_y -= 40
                    draw_block()
                if event.key == K_DOWN: #if pressed down arrow
                    block_y += 40
                    draw_block()

            if event.type == QUIT:
                running = False


    pygame.quit()
    quit()
