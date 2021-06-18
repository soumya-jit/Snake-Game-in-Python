import pygame
from pygame.locals import *
import ctypes#.windll import user32


pygame.init()
pygame.display.set_caption("Snake Game")


#Getting screen size
user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()
system_w, system_h = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

print(system_w, system_h)

#if system_w > 1000 and system_h > 760:
#surface = pygame.display.set_mode((1000, 760))
#elif system_w <= 1000 and system_h <= 760:
w = system_w // 40
h = system_h // 40
surface = pygame.display.set_mode(((w-12)*40, (h-3)*40))


print((w-12)*40, (h-3)*40)




















'''
pygame.init()

surface = pygame.display.set_mode((800, 720))

pygame.display.set_caption("Game by Soumajit")

surface.fill((0, 0, 0)) #setting background color
block = pygame.image.load("resources/block.jpg").convert() #loading snake image
block_x = 0
block_y = 0
surface.blit(block, (block_x, block_y)) # print that block at 100, 100 position
pygame.display.flip() #Update the full display Surface so that the block becomes visible

running = True

while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False


pygame.quit()
quit()
'''



