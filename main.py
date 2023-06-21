from objects import Domino, Player, Button
from pygame.sprite import Group as Layer
from pygame.locals import *
import numpy as np
import pygame
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
if PLAYERS_NUM < 2: PLAYERS_NUM = 2
elif PLAYERS_NUM > 4: PLAYERS_NUM = 4

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
PLAYERS[1].change_auto()
#PLAYERS[2].change_auto()
#PLAYERS[3].change_auto()
FPS = 60


class Table:
    def __init__(self):
        self.spacing = 95
        self.first_game = True
        self.dominoes = np.array([], dtype=object)
        self.table_dominoes = np.array([], dtype=object)

        self.left_iterator = 0
        self.right_iterator = 0
        self.left_positions = []
        self.right_positions = []

        self.last_player = None
        self.extra_dominoes = None
        self.left_arrow = Button("arrow1.png")
        self.right_arrow = Button("arrow1.png")
        self.left_arrow_orientation = True

    def dominoes_distribution(self):
        for i in range(7):
            for j in range(i, 7):
                self.dominoes = np.append(self.dominoes, Domino((i, j)))

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
        x_padding = 68
        y_padding = 160

        x, y = 64, 717
        aux = 1

        for domino in PLAYERS[player_idx].dominoes:
            if domino not in OBJECTS:
                OBJECTS.append(domino)

            domino.add_position(x, y)
            domino.show()

            if aux == 7:
                x, y = 64, 717
                y -= y_padding
                aux = 0

                y_padding += 100
            
            else:
                x += x_padding

            aux += 1 

    def erase_player_dominoes(self, player_idx):
        players = [index for index, player in enumerate(PLAYERS) if index != player_idx]

        for player in players:
            if PLAYERS[player].manual:
                for domino in PLAYERS[player].dominoes:
                    domino.hide()

    def draw_extra_dominoes(self):
        self.extra_dominoes = Domino([7, 7], x=548, y=717)
        OBJECTS.insert(0, self.extra_dominoes)

    def hide_extra_dominoes(self):
        self.extra_dominoes.extra_dominoes_is_empty()
        self.extra_dominoes.hide()

    def is_empty(self):
        return len(self.table_dominoes) == 0
    
    def create_right_positions(self):
        right_x, right_y = 795, 360

        self.right_positions.append([right_x, right_y])
        for _ in range(5):
            right_x += self.spacing
            self.right_positions.append([right_x, right_y])
        
        for _ in range(4):
            right_y += self.spacing
            self.right_positions.append([right_x, right_y])

        for _ in range(6):
            right_x -= self.spacing
            self.right_positions.append([right_x, right_y])

        for _ in range(2):
            right_y -= self.spacing
            self.right_positions.append([right_x, right_y])

        for _ in range(6):
            right_x -= self.spacing
            self.right_positions.append([right_x, right_y])

        right_y -= self.spacing
        self.right_positions.append([right_x, right_y])

        for _ in range(5):
            right_x += self.spacing
            self.right_positions.append([right_x, right_y])

        self.right_positions = np.array(self.right_positions)

    def create_left_positions(self):
        left_x, left_y = 605,360

        self.left_positions.append([left_x, left_y])
        for _ in range(5):
            left_x -= self.spacing
            self.left_positions.append([left_x, left_y])
            
        for _ in range(3):
            left_y -= self.spacing
            self.left_positions.append([left_x, left_y])

        for _ in range(10):
            left_x += self.spacing
            self.left_positions.append([left_x, left_y])

        for _ in range(2):
            left_y += self.spacing
            self.left_positions.append([left_x, left_y])
            
        for _ in range(8):
            left_x -= self.spacing
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
    
    def add_domino_to_table(self, domino, side=None):
        if side is not None:
            self.side = side

        if self.side != "both":
            if domino.acotao:
                domino.view_vertical()
            else:
                domino.view_horizontal()

            if self.side == "none":
                self.table_dominoes = np.insert(self.table_dominoes, 0, domino)
                domino.change_orientation_sprite()
                domino.add_position(700, 360)

            if self.side == "left" and domino.vals[1] != self.table_dominoes[0].vals[0] or self.side == "right" and domino.vals[0] != self.table_dominoes[-1].vals[-1]:
                domino.change_orientation_vals()     

            if self.side == "left":
                self.left_placement(domino)

            if self.side == "right":
                self.right_placement(domino)

            domino.domino_placed()
        
        else:
            self.choose_side(domino)

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

                    if FULLSCREEN.click_me():
                        pass

                    if EXIT.click_me():
                        pygame.quit()
                        sys.exit()

            update_layers()

        self.add_domino_to_table(domino)
        self.deactivate_arrows()

    def left_placement(self, domino):
        domino.change_orientation_sprite()
        if self.left_iterator >= 6 and self.left_iterator <= 8:
            domino.change_orientation_sprite()
            domino.view_horizontal()

        elif self.left_iterator >= 8 and self.left_iterator <= 18:
            domino.change_orientation_sprite()

        elif self.left_iterator >= 18 and self.left_iterator <= 19:
            domino.view_horizontal()
        
        elif self.left_iterator >= 19:
            domino.view_vertical()
            
        self.table_dominoes = np.insert(self.table_dominoes, 0, domino)
        x, y = self.left_positions[self.left_iterator][0], self.left_positions[self.left_iterator][1]
        domino.add_position(x, y)

        self.left_iterator += 1

    def right_placement(self, domino):
        domino.change_orientation_sprite()
        if self.right_iterator >= 6 and self.right_iterator <= 9:
            domino.change_orientation_sprite()
            domino.view_horizontal()

        elif self.right_iterator >= 9 and self.right_iterator <= 15:
            domino.change_orientation_sprite()

        elif self.right_iterator >= 15 and self.right_iterator <= 17:
            domino.view_horizontal()

        elif self.right_iterator >= 17 and self.right_iterator <= 23:
            domino.change_orientation_sprite()
        
        elif self.right_iterator >= 23 and self.right_iterator <= 24:
            domino.view_horizontal()

        elif self.right_iterator >= 24:
            domino.view_vertical()

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

            y += 65
            num_y += 64

    def activate_arrows(self):
        if self.left_arrow_orientation:
            self.left_arrow.change_orientation_sprite()
            self.left_arrow_orientation = False

        self.right_arrow.add_position(576, 636)
        self.left_arrow.add_position(476, 636)
        self.right_arrow.activate()
        self.left_arrow.activate()

        if self.left_arrow not in OBJECTS and self.right_arrow not in OBJECTS:
            OBJECTS.insert(1, self.left_arrow)
            OBJECTS.insert(2, self.right_arrow)
            self.left_arrow.arrow = True
            self.right_arrow.arrow = True

    def deactivate_arrows(self):
        self.right_arrow.deactivate()
        self.left_arrow.deactivate()

    def create_buttons(self):
        global PASS
        global REPEAT
        global FULLSCREEN
        global EXIT

        PASS = Button("PASS_button1.png")
        REPEAT = Button("REPEAT_button1.png")
        FULLSCREEN = Button("FULLSCREEN_button1.png")
        EXIT = Button("EXIT_button1.png")

        x, y = 598, 678
        buttons = [PASS, REPEAT, FULLSCREEN, EXIT]

        for button in buttons:
            button.add_position(x, y)
            y += 26

        for button in buttons:
            button.activate()
            if button not in OBJECTS:
                OBJECTS.append(button)

    def player_plays(self, player_idx):
        self.erase_player_dominoes(player_idx)
        self.draw_player_dominoes(player_idx)
        played = False

        while played != True:
            if len(self.dominoes) == 0 and self.extra_dominoes is not None:
                self.hide_extra_dominoes()

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

                    if self.extra_dominoes is not None:
                        if self.extra_dominoes.click_me():
                            PLAYERS[player_idx].add_domino(self.draw_random())
                            self.draw_player_dominoes(player_idx)

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

            update_layers()

        time.sleep(SLEEP_TIME)
        return played

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
        self.create_buttons()
        
        if self.first_game:
            self.create_right_positions()
            self.create_left_positions()
            self.first_game = False

        if PLAYERS_NUM < 4:
            self.draw_extra_dominoes()

    def return_state(self):
        return self.table_dominoes

    def __repr__(self):
        return str(self.table_dominoes)


class Fake_Table():
    def __init__(self, state=None):
        if state is not None: 
            self.fake_table = state

        else: 
            self.fake_table = np.array([], dtype=object)
        
    def childrens(self, computer_idx):
        playable_dominoes = self.check_computer_dominoes(computer_idx)
        childrens = []

        for domino, side in playable_dominoes:
            child_state = list(self.fake_table.copy())
            child = self.add_domino_to_fake_table(child_state, domino, side)
            childrens.append(Fake_Table(state=child))

        return childrens
    
    def check_computer_dominoes(self, computer_idx):
        playable_dominoes = []
        for domino in PLAYERS[computer_idx].dominoes:
            if self.is_empty():
                playable_dominoes.append([domino, "none"])
                continue
        
            left = self.fake_table[0].vals[0]
            right = self.fake_table[-1].vals[-1]

            if left in domino.vals and right not in domino.vals:
                playable_dominoes.append([domino, "left"])

            if right in domino.vals and left not in domino.vals:
                playable_dominoes.append([domino, "right"])

            if right in domino.vals and left in domino.vals:
                domino_copy = domino.__copy__()
                playable_dominoes.append([domino, "right"])
                playable_dominoes.append([domino_copy, "left"])

        return playable_dominoes
    
    def add_domino_to_fake_table(self, fake_table, domino, side):
        if side == "left" and domino.vals[1] != fake_table[0].vals[0]:
            domino.change_orientation_vals()
            fake_table.insert(0, domino)

        elif side == "left":
            fake_table.insert(0, domino)

        if side == "right" and domino.vals[0] != fake_table[-1].vals[-1]:
            domino.change_orientation_vals()
            fake_table.append(domino)

        elif side == "right":
            fake_table.append(domino)

        if side == "none":
            fake_table.append(domino)
        
        return fake_table
    
    def heuristic(self, computer_idx):
        heuristic = 0

        playable_dominoes = self.check_computer_dominoes(computer_idx)
        if len(playable_dominoes) >= 1:
            heuristic += 1

        return heuristic

    def is_empty(self):
        return len(self.fake_table) == 0

    def __repr__(self):
        return str(self.fake_table)


class GameManager():
    def __init__(self):
        self.Game_Over = False
        self.You_Win = False
        self.In_Game = False

        self.possibility_of_lock_the_game = False
        self.winner = None

    def check_game_status(self, last_turn):
        players_without_dominos = 0
        terminal_val = None

        for player in PLAYERS:
            winner = self.check_for_winner(player)

            if winner:
                terminal_val = player
                self.win(player)
                
            if self.possibility_of_lock_the_game:
                can_play = self.check_player_dominoes(player)
                if can_play:
                    continue
                else:
                    players_without_dominos += 1

            if players_without_dominos >= PLAYERS_NUM:
                result = self.game_locked(last_turn)
                return result * np.inf

        if terminal_val == PLAYERS[last_turn]:
            return 1 * np.inf
        elif terminal_val is not None:
            return -1 * np.inf
        else:
            return terminal_val

    def game_locked(self, last_turn):
        player1 = PLAYERS[last_turn].count_tiles()
        try:
            player2 = PLAYERS[last_turn + 1].count_tiles()
        except:
            player2 = PLAYERS[0].count_tiles()

        if player1 < player2:
            self.win(PLAYERS[last_turn])
            return 1
        
        elif player1 > player2:
            try:
                self.win(PLAYERS[last_turn + 1])
                return -1
            
            except:
                self.win(PLAYERS[0])
                return -1
            
        else:
            try:
                self.win(PLAYERS[last_turn + 1])
                return -1
            
            except:
                self.win(PLAYERS[0])
                return -1  

    def check_player_dominoes(self, player):
        if len(table.table_dominoes) == 0:
            return True

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
        self.winner = winner
        self.You_Win = True

        self.Game_Over = False
        self.In_Game = False

    def new_game(self):
        self.In_Game = True

        self.Game_Over = False
        self.You_Win = False


class MinimaxSolver():
    def __init__(self, max_depth=6, ts=None, max_time=None, timeit=False):
        self.max_depth = max_depth
        self.max_time = max_time
        self.timeit = timeit
        self.ts = ts

    def solve(self, state, computer_idx):
        max_child, _ = self.__maximize(state, -np.inf, np.inf, computer_idx, 0)
        return max_child

    def __maximize(self, state, alpha, beta, computer_idx, depth):
        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        terminal_val = gameManager.check_game_status(computer_idx)
        if terminal_val is not None:
            return (None, terminal_val)
        
        if depth >= self.max_depth:
            return (None, state.heuristic(computer_idx))
        
        max_child, max_utility = (None, -np.inf)
        for child in state.childrens(computer_idx):
            _, utility = self.__minimize(child, alpha, beta, computer_idx, depth + 1)

            if utility > max_utility:
                max_child, max_utility = child, utility

            if utility >= beta:
                break

            alpha = max(alpha, max_utility)
        return max_child, max_utility
    
    def __minimize(self, state, alpha, beta, computer_idx, depth):
        if self.timeit:
            if time.time() - self.ts >= self.max_time:
                return (None, -np.inf)

        terminal_val = gameManager.check_game_status(computer_idx)
        if terminal_val is not None:
            return (None, terminal_val)
        
        if depth >= self.max_depth:
            return (None, state.heuristic(computer_idx))
        
        min_child, min_utility = (None, np.inf)
        for child in state.childrens(computer_idx):
            _, utility = self.__maximize(child, alpha, beta, computer_idx, depth + 1)

            if utility < min_utility:
                min_child, min_utility = child, utility

            if utility < alpha:
                break

            beta = min(beta, min_utility)
        return min_child, min_utility


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


def add_layers(domino):
    if domino not in OBJECTS:
        domino.change_orientation_sprite()
        OBJECTS.append(domino)
        domino.in_screen = True
        domino.update()


def main():
    global gameManager
    global table
    global TURN

    table = Table()
    table.start_game()
    gameManager = GameManager()
    gameManager.new_game()

    clock = pygame.time.Clock()
    max_time = 0.5
    TURN = 0  

    while gameManager.In_Game:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if PLAYERS[TURN].manual:
            table.draw_player_number(TURN)
            played = table.player_plays(TURN)

        else:
            state = Fake_Table(state=table.table_dominoes)
            best_state = None

            ts = time.time()
            minimax_solver = MinimaxSolver(max_time=max_time, ts=ts)
            for depth in range(1, 20):
                minimax_solver.max_depth = depth
                best_state = minimax_solver.solve(state, TURN)

                if time.time() - ts >= max_time:
                    break
            
            if best_state is not None:
                domino = np.array([domino for domino in best_state.fake_table if domino not in state.fake_table])
                idx = np.where(best_state.fake_table == domino)[0]
                
                domino_idx = int(np.where(PLAYERS[TURN].dominoes == domino)[0])
                domino_to_play = PLAYERS[TURN].dominoes[domino_idx]

                if len(state.fake_table) == 0:
                    table.add_domino_to_table(domino_to_play, "none")

                elif idx <= 0 and len(state.fake_table) != 0:
                    table.add_domino_to_table(domino_to_play, "left")

                elif idx >= 1 and len(state.fake_table) != 0:
                    table.add_domino_to_table(domino_to_play, "right")

                PLAYERS[TURN].dominoes = np.delete(PLAYERS[TURN].dominoes, np.where(PLAYERS[TURN].dominoes == domino))
                add_layers(domino_to_play)
                played = True
            
            elif best_state is None and len(table.dominoes) != 0:
                PLAYERS[TURN].add_domino(table.draw_random())
                continue

            elif best_state is None and len(table.dominoes) == 0:
                played = True

        if played == -1:
            break

        update_layers()
        gameManager.check_game_status(TURN)

        if played:
            played = False
            TURN += 1

            time.sleep(SLEEP_TIME)
            if TURN >= PLAYERS_NUM:
                TURN = 0

        if len(table.dominoes) == 0:
            gameManager.possibility_of_lock_the_game = True

        if gameManager.You_Win:
            print(f"Player #{gameManager.winner.num + 1} wins the game")
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