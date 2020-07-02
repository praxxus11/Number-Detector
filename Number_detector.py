import pygame
import grid
import numpy as np
import predict

parameters = np.genfromtxt('PARABETTER.txt', delimiter=',')
factors = np.genfromtxt('norm.txt', delimiter=',')

pixels = []
for ii in range(0, 28):
    row = []
    for jj in range(0, 28):
        row.append(grid.grid(20, 20, 10 + 20 * ii, 10 + 20 * jj))
    pixels.append(row)

pygame.init()


def main_loop():
    font = pygame.font.SysFont(None, 30)

    # Paint status
    # True: means will be white circle displayed and the paintbrush will be activated
    # False: means will be red circle displayed and the paintbrush will not be activated
    paint = True
    running = True
    screen = pygame.display.set_mode((800, 560))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # This is is to change the configuration: paint or eraser
                mp = pygame.mouse.get_pos()
                if 600 < mp[0] < 750 and 20 < mp[1] < 60:
                    paint = False
                if 600 < mp[0] < 750 and 80 < mp[1] < 120:
                    paint = True
        screen.fill((0, 0, 0))
        # This is the line separating the drawing screen and the side panel
        pygame.draw.line(screen, (255, 255, 255), (560, 0), (560, 560), 10)

        # Putting each pixel on the screen
        for pix in pixels:
            for p in pix:
                screen.blit(p.surf, p.rect)

        # Determining where the drawing circle should be
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] <= 560 and mouse_pos[1] <= 560:
            if paint:
                pygame.draw.circle(screen, (255, 255, 255), mouse_pos, 30, 3)
            else:
                pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 150, 3)

        # Putting the buttons to change from paint to eraser
        pygame.draw.rect(screen, (255, 0, 0), (600, 20, 150, 40))
        pygame.draw.rect(screen, (255, 255, 255), (600, 80, 150, 40))
        screen.blit(font.render("Eraser", True, (0, 0, 0)), (600, 20))
        screen.blit(font.render("Paintbrush", True, (0, 0, 0)), (600, 80))

        # If mouse is holding down, then update each pixel's color
        # paint is passed in to see if its erasing or painting
        click = pygame.mouse.get_pressed()
        if click[0]:
            for pix in pixels:
                for p in pix:
                    p.update(paint)

        # Now retrieving to status of each pixel
        # Indexes i and j and reversed because indexing of pygame screens are weird
        current_state = np.zeros((28, 28))
        for i in range(0, 28):
            for j in range(0, 28):
                current_state[i][j] = pixels[j][i].color[0]

        # Using the current status and returns the activations of the last layer, rounds it too
        curr_num = predict.front_prop(current_state, parameters, factors)
        curr_num = np.round(curr_num * 100, 3)

        # Determine which number should be colored red and green
        max_num_ind = np.argmax(curr_num)

        # Creating a string of the percentage for each number 0-9
        for i in range(0, 10):
            stats = ""
            stats += str(i) + ": "
            stats += str(curr_num[i])
            stats += '%'
            if i == max_num_ind:
                rendered = font.render(stats, True, (0, 255, 0))
            else:
                rendered = font.render(stats, True, (255, 0, 0))
            screen.blit(rendered, (600, 150 + 40 * i))

        pygame.display.flip()


main_loop()
