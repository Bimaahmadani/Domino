from pygame.sprite import Group as Layer
from pygame.locals import *
from objects import Domino
import pygame
import random
import sys
import os


#Window configuration
pygame.init()
WIDTH, HEIGHT = 1400, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Dominó!')

ICON = pygame.image.load("assets/Domino (icon).png").convert()
pygame.display.set_icon(ICON)

BACKGROUND = pygame.image.load("assets/Table.png").convert()
WINDOW.blit(BACKGROUND, (0, 0))

OBJECTS = [Domino([3, 5], x=100, y=100)]
LAYERS = {0: Layer()}

FPS = 60


def awake():
    for object in OBJECTS:
        if object.layer not in LAYERS:
            LAYERS[object.layer] = Layer()

        LAYERS[object.layer].add(object)    


def main():
    awake()

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for _, layer in LAYERS.items():
            layer.update()
            layer.draw(WINDOW)

        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main()