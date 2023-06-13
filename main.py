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
        self.spacing = 95
        self.dominoes = []
        self.table_dominoes = []
        self.left_positions = []
        self.right_positions = []
        self.left_iterator = 0
        self.right_iterator = 0

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
    
    def create_right_positions(self):
        right_x, right_y = 795, 360
        self.right_positions.append([right_x, right_y])
        for _ in range(5):
            right_x, right_y = right_x + self.spacing, right_y
            self.right_positions.append([right_x, right_y])
        
        right_x, right_y = right_x, right_y + self.spacing
        self.right_positions.append([right_x, right_y])
        for _ in range(3):
            right_x, right_y = right_x, right_y + self.spacing
            self.right_positions.append([right_x, right_y])

        right_x, right_y = right_x - self.spacing, right_y
        self.right_positions.append([right_x, right_y])
        for _ in range(5):
            right_x, right_y = right_x - self.spacing, right_y
            self.right_positions.append([right_x, right_y])

    def create_left_positions(self):
        left_x, left_y = 605,360
        self.left_positions.append([left_x, left_y])
        for _ in range(5):
            left_x, left_y = left_x - self.spacing, left_y
            self.left_positions.append([left_x, left_y])
            
        left_x, left_y = left_x, left_y - self.spacing
        self.left_positions.append([left_x, left_y])
        for _ in range(2):
            left_x, left_y = left_x, left_y - self.spacing
            self.left_positions.append([left_x, left_y])

        left_x, left_y = left_x + self.spacing, left_y
        self.left_positions.append([left_x, left_y])
        for _ in range(5):
            left_x, left_y = left_x + self.spacing, left_y
            self.left_positions.append([left_x, left_y])

    def can_be_put(self, domino):
        if self.is_empty():
            self.side = "none"
            return True
        
        self.side = ""
        left = self.table_dominoes[0].vals[0]
        right = self.table_dominoes[-1].vals[-1]

        if left in domino.vals: self.side = "left"
        if right in domino.vals: self.side = "right"
        #if right in domino.vals and left in domino.vals:
        #    self.side = "both"

        return left in domino.vals or right in domino.vals
    
    def add_domino_to_table(self, domino):
        if domino.acotao:
            domino.view_vertical()
        else:
            domino.view_horizontal()

        if self.side == "none":
            self.table_dominoes.insert(0, domino)
            domino.add_position(700, 360)

        if self.side == "left" and domino.vals[1] != self.table_dominoes[0].vals[0] or self.side == "right" and domino.vals[0] != self.table_dominoes[-1].vals[-1]:
            domino.change_orientation_vals()     

        if self.side != "both":
            if self.side == "left":
                if self.left_iterator >= 6 and self.left_iterator <= 8:
                    domino.change_orientation_sprite()
                    domino.view_horizontal()

                elif self.left_iterator >= 8:
                    domino.change_orientation_sprite()

                self.table_dominoes.insert(0, domino)
                x, y = self.left_positions[self.left_iterator][0], self.left_positions[self.left_iterator][1]
                domino.add_position(x, y)

                self.left_iterator += 1

            if self.side == "right":
                if self.right_iterator >= 6 and self.right_iterator <= 8:
                    domino.change_orientation_sprite()
                    domino.view_horizontal()

                elif self.right_iterator >= 8:
                    domino.change_orientation_sprite()

                self.table_dominoes.append(domino)
                x, y = self.right_positions[self.right_iterator][0], self.right_positions[self.right_iterator][1]
                domino.add_position(x, y)

                self.right_iterator += 1

        else:
            self.choose_side(domino)
            pass
    
    def choose_side(self, domino):
        pass

    def players_dominoes(self):
        x, y = 1300, 30
        for player_idx in range(1, PLAYERS_NUM):
            num_dominoes = pygame.image.load(f"assets/Dominos (Interface)/{len(PLAYERS[player_idx].dominoes)}.png").convert()
            num_dominoes.set_colorkey( ( 0, 187, 45 ) )
            WINDOW.blit(num_dominoes, (x, y))
            x, y = x, y + 65

    def start_game(self):
        self.dominoes_distribution()
        self.draw_player_dominoes()
        self.create_right_positions()
        self.create_left_positions()

        if PLAYERS_NUM < 4:
            self.draw_extra_dominoes()
    
    def __repr__(self):
        return str(self.table_dominoes)


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

    while True:
        #print(f"Player #{TURN+1} turn")
        #print(OBJECTS)
        print(table, PLAYERS[0])
        clock.tick(FPS)      

        if TURN == 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:

                    for domino in PLAYERS[0].dominoes:
                        if domino.click_me():
                            if table.can_be_put(domino):
                                table.add_domino_to_table(domino)
                                PLAYERS[0].dominoes.remove(domino)

                                played = True

                            else:
                                print("!!")
                                
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

        WINDOW.blit(BACKGROUND, (0, 0))
        table.draw_player_dominoes()
        table.players_dominoes()
        
        update_layers()
        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main()