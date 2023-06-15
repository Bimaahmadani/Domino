from pygame.sprite import Group as Layer
from objects import Domino, Player, Button
from pygame.locals import *
import numpy as np
import pygame
import random
import time
import sys

#Window configuration
pygame.init()
WIDTH, HEIGHT = 1400, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Dominó!')

ICON = pygame.image.load("assets/Domino (icon).png").convert_alpha()
pygame.display.set_icon(ICON)

PLAYERS_NUM = 2
if PLAYERS_NUM < 2:
    PLAYERS_NUM = 2
elif PLAYERS_NUM > 4:
    PLAYERS_NUM = 4

BACKGROUND = pygame.image.load(f"assets/Table({PLAYERS_NUM}).png").convert_alpha()
PLAYER__ = pygame.image.load(f"assets/Dominos (Interface)/jugador#.png").convert_alpha()

SLEEP_TIME = .2
PLAYER__pos = (26, 606)
PLAYER_NUM_pos = (240, 599)

WINDOW.blit(BACKGROUND, (0, 0))
WINDOW.blit(PLAYER__, PLAYER__pos)

OBJECTS = []
LAYERS = {0: Layer()}

PLAYERS = [Player(num) for num in range(PLAYERS_NUM)]
#PLAYERS[1].change_auto()
FPS = 160


class Table:
    def __init__(self):
        self.spacing = 95
        self.dominoes = np.array([], dtype=object)
        self.table_dominoes = np.array([], dtype=object)

        self.left_iterator = 0
        self.right_iterator = 0
        self.left_positions = []
        self.right_positions = []

        self.extra_dominoes = None
        self.left_arrow = Button("arrow.png")
        self.right_arrow = Button("arrow.png")
        self.left_arrow_orientation = True

    def dominoes_distribution(self):
        for i in range(7):
            for j in range(i, 7):
                self.dominoes = np.append(self.dominoes, Domino((i, j)))

        print(self.dominoes)
        for player in PLAYERS:
            for _ in range(7):
                player.add_domino(self.draw_random())
    
    def draw_random(self):
        domino = np.random.choice(self.dominoes)
        self.dominoes = np.delete(self.dominoes, np.where(self.dominoes == domino))
        return domino
    
    def draw_player_number(self, player_number):
        global player_to_play
        player_to_play = pygame.image.load(f"assets/Dominos (Interface)/{player_number + 1}p.png").convert_alpha()
        WINDOW.blit(player_to_play, PLAYER_NUM_pos)
        update_layers()

    def draw_player_dominoes(self, player_idx):
        self.erase_player_dominoes()
        x_padding = 68
        y_padding = 160

        x, y = 64, 717
        aux = 1

        for domino in PLAYERS[player_idx].dominoes:
            domino.add_position(x, y)
            
            if domino not in OBJECTS:
                OBJECTS.append(domino)

            if aux == 7:
                x, y = 64, 717
                y -= y_padding
                aux = 0

                y_padding += self.spacing
            
            else:
                x += x_padding

            aux += 1 

    def erase_player_dominoes(self):
        for player_idx in range(0, PLAYERS_NUM):
            for domino in PLAYERS[player_idx].dominoes:
                domino.add_position(9999, 9999)

    def draw_extra_dominoes(self):
        self.extra_dominoes = Domino([7, 7], x=548, y=717)
        OBJECTS.insert(0, self.extra_dominoes)

    def hide_extra_dominoes(self):
        self.extra_dominoes.add_position(9999, 9999)

    def is_empty(self):
        return len(self.table_dominoes) == 0
    
    def create_right_positions(self):
        right_x, right_y = 795, 360

        self.right_positions.append([right_x, right_y])
        for _ in range(5):
            right_x, right_y = right_x + self.spacing, right_y
            self.right_positions.append([right_x, right_y])
        
        for _ in range(4):
            right_x, right_y = right_x, right_y + self.spacing
            self.right_positions.append([right_x, right_y])

        for _ in range(6):
            right_x, right_y = right_x - self.spacing, right_y
            self.right_positions.append([right_x, right_y])

        for _ in range(3):
            right_x, right_y = right_x, right_y - self.spacing
            self.right_positions.append([right_x, right_y])

        for _ in range(6):
            right_x, right_y = right_x + self.spacing, right_y
            self.right_positions.append([right_x, right_y])

        self.right_positions = np.array(self.right_positions)

    def create_left_positions(self):
        left_x, left_y = 605,360

        self.left_positions.append([left_x, left_y])
        for _ in range(5):
            left_x, left_y = left_x - self.spacing, left_y
            self.left_positions.append([left_x, left_y])
            
        for _ in range(3):
            left_x, left_y = left_x, left_y - self.spacing
            self.left_positions.append([left_x, left_y])

        for _ in range(10):
            left_x, left_y = left_x + self.spacing, left_y
            self.left_positions.append([left_x, left_y])

        for _ in range(3):
            left_x, left_y = left_x, left_y + self.spacing
            self.left_positions.append([left_x, left_y])
            
        for _ in range(10):
            left_x, left_y = left_x - self.spacing, left_y
            self.left_positions.append([left_x, left_y])

        self.left_positions = np.array(self.left_positions)

    def can_be_put(self, domino):
        if self.is_empty():
            self.side = "none"
            return True
        
        self.side = ""
        left = self.table_dominoes[0].vals[0]
        right = self.table_dominoes[-1].vals[-1]

        if left in domino.vals: self.side = "left"
        if right in domino.vals: self.side = "right"
        if right in domino.vals and left in domino.vals:
            self.side = "both"

        return left in domino.vals or right in domino.vals
    
    def add_domino_to_table(self, domino):
        if self.side != "both":
            if domino.acotao:
                domino.view_vertical()
            else:
                domino.view_horizontal()

            if self.side == "none":
                self.table_dominoes = np.insert(self.table_dominoes, 0, domino)
                domino.add_position(700, 360)

            if self.side == "left" and domino.vals[1] != self.table_dominoes[0].vals[0] or self.side == "right" and domino.vals[0] != self.table_dominoes[-1].vals[-1]:
                domino.change_orientation_vals()     

            if self.side == "left":
                self.left_placement(domino)

            if self.side == "right":
                self.right_placement(domino)
        
        else:
            self.choose_side(domino)

    def add_domino_to_fake_table(self, fake_table, domino, side):
        if side == "left" and domino.vals[1] != fake_table[0].vals[0] or side == "right" and domino.vals[0] != fake_table[-1].vals[-1]:
            domino.change_orientation_vals()

        if side == "both":
            table1 = np.insert(fake_table, 0, domino)
            table2 = np.append(fake_table, domino)
            return table1, table2

        else:
            if side == "none":
                fake_table = np.insert(fake_table, 0, domino)

            if side == "left":
                fake_table = np.insert(fake_table, 0, domino)

            if side == "right":
                fake_table = np.append(fake_table, domino)

            return fake_table, None

    def choose_side(self, domino):
        self.activate_arrows()
        update_layers()
        choose = True

        while choose:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if self.right_arrow.click_me():
                        self.side = "right"
                        choose = False
                        break

                    if self.left_arrow.click_me():
                        self.side = "left"
                        choose = False
                        break

        self.add_domino_to_table(domino)
        self.deactivate_arrows()

    def left_placement(self, domino):
        if self.left_iterator >= 6 and self.left_iterator <= 8:
            domino.change_orientation_sprite()
            domino.view_horizontal()

        elif self.left_iterator >= 8:
            domino.change_orientation_sprite()

        self.table_dominoes = np.insert(self.table_dominoes, 0, domino)
        x, y = self.left_positions[self.left_iterator][0], self.left_positions[self.left_iterator][1]
        domino.add_position(x, y)

        self.left_iterator += 1

    def right_placement(self, domino):
        if self.right_iterator >= 6 and self.right_iterator <= 8:
            domino.change_orientation_sprite()
            domino.view_horizontal()

        elif self.right_iterator >= 8 and self.right_iterator <= 15:
            domino.change_orientation_sprite()

        elif self.right_iterator >= 15 and self.right_iterator <= 17:
            domino.view_horizontal()

        elif self.right_iterator >= 17:
            domino.change_orientation_sprite()

        self.table_dominoes = np.append(self.table_dominoes, domino)
        x, y = self.right_positions[self.right_iterator][0], self.right_positions[self.right_iterator][1]
        domino.add_position(x, y)

        self.right_iterator += 1

    def players_dominoes(self):
        x, y = 1309, 30
        num_x, num_y = 1260, 12
        for player in range(0, PLAYERS_NUM):
            dominoes_amount = len(PLAYERS[player].dominoes)

            if dominoes_amount >= 7:
                dominoes_amount = 7

            num_dominoes = pygame.image.load(f"assets/Dominos (Interface)/{dominoes_amount}.png").convert_alpha()
            player_num = pygame.image.load(f"assets/Dominos (Interface)/{player + 1}p.png").convert_alpha()

            WINDOW.blit(num_dominoes, (x, y))
            WINDOW.blit(player_num, (num_x, num_y))

            x, y = x, y + 65
            num_x, num_y = num_x, num_y + 64

    def activate_arrows(self):
        if self.left_arrow_orientation:
            self.left_arrow.change_orientation_sprite()
            self.left_arrow_orientation = False

        self.right_arrow.add_position(576, 636)
        self.left_arrow.add_position(476, 636)

        if self.left_arrow not in OBJECTS and self.right_arrow not in OBJECTS:
            OBJECTS.insert(1, self.left_arrow)
            OBJECTS.insert(2, self.right_arrow)

        self.right_arrow.update()
        self.left_arrow.update()

    def deactivate_arrows(self):
        self.right_arrow.deactivate()
        self.left_arrow.deactivate()

    def create_buttons(self):
        global PASS
        global REPEAT
        global FULLSCREEN
        global EXIT

        PASS = Button("PASS_button.png")
        REPEAT = Button("REPEAT_button.png")
        FULLSCREEN = Button("FULLSCREEN_button.png")
        EXIT = Button("EXIT_button.png")

        x, y = 598, 678
        buttons = [PASS, REPEAT, FULLSCREEN, EXIT]

        for button in buttons:
            button.add_position(x, y)
            y += 26

        for button in buttons:
            if button not in OBJECTS:
                OBJECTS.append(button)

        for button in buttons:
            button.update()

    def player_plays(self, player_idx):
        played = False

        while played != True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    for domino in PLAYERS[player_idx].dominoes:
                        if domino.click_me():
                            if self.can_be_put(domino):
                                self.add_domino_to_table(domino)
                                PLAYERS[player_idx].dominoes = np.delete(PLAYERS[player_idx].dominoes, np.where(PLAYERS[player_idx].dominoes == domino))
                                played = True

                            else:
                                print("!!")

                    try:
                        if self.extra_dominoes.click_me():
                            try:
                                PLAYERS[player_idx].add_domino(self.draw_random())
                                break

                            except:
                                self.hide_extra_dominoes()
                    
                    except:
                        pass

                    if PASS.click_me():
                        played = True

                    if REPEAT.click_me():
                        played = -1
                        return played

                    if FULLSCREEN.click_me():
                        pass

                    if EXIT.click_me():
                        pygame.quit()
                        sys.exit()

            self.draw_player_dominoes(player_idx)
            update_layers()

        time.sleep(SLEEP_TIME)
        return played

    def childrens(self, computer_idx):
        playable_dominoes = self.check_computer_dominoes(computer_idx)
        childrens = np.array([])

        for domino, side in playable_dominoes:
            child_state = self.table_dominoes.copy()
            child1, child2 = self.add_domino_to_fake_table(child_state, domino, side)
            
            childrens = np.append(childrens, child1)
            if child2 != None:
                childrens = np.append(childrens, child2)

        return childrens
    
    def check_computer_dominoes(self, computer_idx):
        playable_dominoes = np.array([])
        for domino in PLAYERS[computer_idx].dominoes:
            left = table.table_dominoes[0].vals[0]
            right = table.table_dominoes[-1].vals[-1]

            if left in domino.vals:
                playable_dominoes = np.append(playable_dominoes, np.array([domino, "left"]))

            if right in domino.vals:
                playable_dominoes = np.append(playable_dominoes, np.array([domino, "right"]))

            if right in domino.vals and left in domino.vals:
                playable_dominoes = np.append(playable_dominoes, np.array([domino, "both"]))

        return playable_dominoes

    def computer_plays(self, computer_idx):
        childrens = self.childrens(computer_idx)
        print(childrens)
        return True

    def repeat_game(self):
        OBJECTS = []
        LAYERS = {0: Layer()}

        for player in PLAYERS:
            player.remove_all()

        self.dominoes = np.array([])
        self.table_dominoes = np.array([])
        self.left_iterator = 0
        self.right_iterator = 0

        return OBJECTS, LAYERS

    def start_game(self):
        self.dominoes_distribution()
        self.create_right_positions()
        self.create_left_positions()
        self.create_buttons()

        if PLAYERS_NUM < 4:
            self.draw_extra_dominoes()
    
    def __repr__(self):
        return str(self.table_dominoes)


class GameManager():
    def __init__(self):
        self.Game_Over = False
        self.You_Win = False
        self.In_Game = False

        self.possibility_of_lock_the_game = False

    def check_game_status(self, last_turn):
        players_without_dominos = 0

        for player in PLAYERS:
            winner = self.check_for_winner(player)

            if winner:
                self.win(player)
                
            if self.possibility_of_lock_the_game:
                can_play = self.check_player_dominoes(player)
                if can_play:
                    continue
                else:
                    players_without_dominos += 1

            if players_without_dominos >= PLAYERS_NUM:
                self.game_locked(last_turn)

    def game_locked(self, last_turn):
        player1 = PLAYERS[last_turn].count_tiles()
        try:
            player2 = PLAYERS[last_turn + 1].count_tiles()
        except:
            player2 = PLAYERS[0].count_tiles()

        if player1 < player2:
            self.win(PLAYERS[last_turn])
        elif player1 > player2:
            try:
                self.win(PLAYERS[last_turn + 1])
            except:
                self.win(PLAYERS[0])
        else:
            try:
                self.win(PLAYERS[last_turn + 1])
            except:
                self.win(PLAYERS[0])

    def check_player_dominoes(self, player):
        for domino in player.dominoes:
            left = table.table_dominoes[0].vals[0]
            right = table.table_dominoes[-1].vals[-1]

            if left in domino.vals:
                return True
            if right in domino.vals:
                return True

        return False

    def check_for_winner(self, player):
        if len(player.dominoes) == 0:
            return True
        
    def lose(self):
        self.Game_Over = True

        self.You_Win = False
        self.In_Game = False

    def win(self, winner):
        print(f"Player #{winner.num + 1} wins the game")
        self.You_Win = True

        self.Game_Over = False
        self.In_Game = False

    def new_game(self):
        self.In_Game = True

        self.Game_Over = False
        self.You_Win = False


def update_layers():
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(PLAYER__, PLAYER__pos)
    WINDOW.blit(player_to_play, PLAYER_NUM_pos)
    table.players_dominoes()

    for object in OBJECTS:
        if object.layer not in LAYERS:
            LAYERS[object.layer] = Layer()

        LAYERS[object.layer].add(object)

    for _, layer in LAYERS.items():
        layer.update()
        layer.draw(WINDOW)

    pygame.display.flip()
    pygame.display.update() 


def main():
    global table
    global TURN

    table = Table()
    table.start_game()
    gameManager = GameManager()
    gameManager.new_game()

    clock = pygame.time.Clock()
    TURN = 0  

    while gameManager.In_Game:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if PLAYERS[TURN].manual:
            table.draw_player_number(TURN)
            table.draw_player_dominoes(TURN)
            played = table.player_plays(TURN)

        else:
            played = table.computer_plays(TURN)

        if played == -1:
            break

        if played:
            played = False
            TURN += 1

            time.sleep(SLEEP_TIME)
            if TURN >= PLAYERS_NUM:
                TURN = 0

        if len(table.dominoes) == 0:
            gameManager.possibility_of_lock_the_game = True

        update_layers()
        gameManager.check_game_status(TURN)
        if gameManager.You_Win:
            time.sleep(SLEEP_TIME*2)
            pass

        if gameManager.Game_Over:
            time.sleep(SLEEP_TIME*2)
            pass

        update_layers()

    OBJECTS, LAYERS = table.repeat_game()
    return OBJECTS, LAYERS

if __name__ == '__main__':
    while True:
        OBJECTS, LAYERS = main()