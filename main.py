from pygame.sprite import Group as Layer
from objects import Domino, Player
from pygame.locals import *
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

PLAYERS_NUM = 2
BACKGROUND = pygame.image.load(f"assets/Table({PLAYERS_NUM}).png").convert()
WINDOW.blit(BACKGROUND, (0, 0))

OBJECTS = [Domino([3, 5], x=100, y=100)]
LAYERS = {0: Layer()}

FPS = 60

PLAYERS = [Player() for _ in range(PLAYERS_NUM)]

class Table:
    def __init__(self):
        self.dominoes = []

    def dominoes_distribution(self):
        for i in range(7):
            for j in range(i, 7):
                self.dominoes.append(Domino((i, j)))

        for player in PLAYERS:
            for _ in range(7):
                player.add_domino(self.draw_random())

    def start_game(self):
        self.dominoes_distribution()
    
    def draw_random(self):
        return self.dominoes.pop(random.randint(0, len(self.dominoes)))
    
    def __repr__(self):
        return str(self.dominoes)


def awake():
    for object in OBJECTS:
        if object.layer not in LAYERS:
            LAYERS[object.layer] = Layer()

        LAYERS[object.layer].add(object)  

    table = Table()
    table.start_game()
    
    for player in PLAYERS:
        print(player)


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