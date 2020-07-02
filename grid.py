import pygame
import math


# This is the class for each pixel on the grid
class grid():

    def __init__(self, wid, hei, midH, midV):
        self.surf = pygame.Surface((wid, hei))
        self.rect = self.surf.get_rect(center=(midH, midV))
        self.color = (0, 0, 0)
        self.midH = midH
        self.midV = midV

    # Just the distance formula
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Sets the color of pixel to a color, if paint is on and want to set lower color than current color, will not
    # set the color
    def set_color(self, val, paint=True):
        if paint and self.color[0] < val:
            self.color = (val, val, val)
        if not paint:
            self.color = (val, val, val)

    # Updates the status of the pixel, depending on how far it is away from the cursor location
    def update(self, paint):
        self.surf.fill(color=self.color)
        mouse_pos = pygame.mouse.get_pos()
        dist = self.distance(mouse_pos[0], mouse_pos[1], self.midH, self.midV)
        if paint:
            if dist < 15:
                self.set_color(255)
            elif dist < 50:
                self.set_color((50 - dist) / 50 * 255)
        else:
            if dist < 150:
                self.set_color(0, False)
