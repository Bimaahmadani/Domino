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

OBJECTS = []#Domino([1, 6], x=200, y=200)]
LAYERS = {0: Layer()}

PLAYERS = [Player() for _ in range(PLAYERS_NUM)]
FPS = 60


class Table:
    def __init__(self):
        self.dominoes = []
        self.table_dominoes = []

    def dominoes_distribution(self):
        for i in range(7):
            for j in range(i, 7):
                self.dominoes.append(Domino((i, j)))

        for player in PLAYERS:
            for _ in range(7):
                player.add_domino(self.draw_random())
    
    def draw_random(self):
        return self.dominoes.pop(random.randint(0, len(self.dominoes)-1))
    
    def draw_by_position(self, position):
        return self.dominoes.pop(position)
    
    def draw_player_dominoes(self):
        spacing = 64

        for domino in PLAYERS[0].dominoes:
            domino.add_position(spacing, 717)
            OBJECTS.append(domino)
            spacing += 68

    def draw_extra_dominoes(self):
        OBJECTS.insert(0, Domino([7, 7], x=548, y=717))

    def is_empty(self):
        return len(self.table_dominoes) == 0

    def can_be_put(self, domino):
        if self.is_empty():
            return True
        
        self.side = ""
        left = self.table_dominoes[0].vals[0]
        right = self.table_dominoes[-1].vals[-1]

        if left in domino.val:
            self.side = "left"

        if right in domino.val:
            self.side = "left"

        if right in domino.val and left in domino.val:
            self.side = "both"

        return left in domino.val or right in domino.val
    
    def add_domino_to_table(self, domino):
        pass


    def start_game(self):
        self.dominoes_distribution()
        self.draw_player_dominoes()

        if PLAYERS_NUM < 4:
            self.draw_extra_dominoes()
    
    def __repr__(self):
        return str(self.dominoes)


def update_layers():
    for object in OBJECTS:
        if object.layer not in LAYERS:
            LAYERS[object.layer] = Layer()

        LAYERS[object.layer].add(object)

    for _, layer in LAYERS.items():
        layer.update()
        layer.draw(WINDOW)


def main():
    table = Table()
    table.start_game()

    clock = pygame.time.Clock()
    played = False
    TURN = 0  

    print(OBJECTS[0])

    while True:
        #print(f"Player #{TURN+1} turn")
        clock.tick(FPS)
        update_layers()    

        if TURN == 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    for domino in PLAYERS[0].dominoes:
                        if domino.click_me():
                            #print(domino)
                            
                            if not table.can_be_put(domino):
                                continue

                            played = True
                                
                    if OBJECTS[0].click_me():
                        try:
                            PLAYERS[0].add_domino(table.draw_random())
                            #print(PLAYERS[0])

                        except:
                            pass

        else:
            pass

        if played:
            TURN += 1

        if TURN >= PLAYERS_NUM:
            played = False
            TURN = 0

        update_layers()
        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main()