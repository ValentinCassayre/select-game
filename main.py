"""
Prototype game by Valentin Cassayre
"""

import pygame
pygame.init()

# open a window
pygame.display.set_caption("Select!")
screen = pygame.display.set_mode((1080, 720))

# background
background = pygame.image.load('assets/Board.jpg')


running = True

# loop while game is open
while running:
    # put the background
    screen.blit(background, (0, 0))

    # update screen for background
    pygame.display.flip()



    # player close windows
    for event in pygame.event.get():
        # event closing
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Closing select!")
