import numpy as np
import pygame
import time
import os

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, layer=0, x_scale=1, y_scale=1, orientation=0, img_path=os.path.join("assets", "empty.png")):
        super().__init__()
        self.x = x
        self.y = y
        self.layer = layer
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.position = np.array([x, y])
        self.orientation = orientation
        self.__load_image(img_path)
        self.change_vals = False

    def __load_image(self, path):
        self.change_vals = False

        try:
            self.image = pygame.image.load(path).convert_alpha()
        except:
            path = change_vals(path, 22, 24)
            self.image = pygame.image.load(path).convert_alpha()
            self.change_vals = True

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.x_scale, self.image.get_height()*self.y_scale))
        self.image = pygame.transform.rotate(self.image, self.orientation)
        self.rect = self.image.get_rect()

        if self.change_vals:
            self.change_orientation(180)

    def update_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()

    def __refresh_sprite(self):
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.x_scale, self.image.get_height()*self.y_scale))
        self.rect = self.image.get_rect()

    def update(self):
        self.__refresh_sprite()
        self.rect.center = (self.x, self.y) 

    def is_colliding(self, position):
        return self.rect.collidepoint(position)

    def add_position(self, x, y):
        self.position = np.array([x, y])
        self.x = x
        self.y = y

    def change_orientation(self, new_orientation):
        self.orientation = new_orientation
        self.image = pygame.transform.rotate(self.image, self.orientation)
        self.rect = self.image.get_rect()

    def give_rect(self):
        return self.rect
    
    def give_position(self):
        return self.x, self.y

    def destroy(self):
        pass


class Domino(GameObject):
    def __init__(self, vals:list, **kwargs):
        self.vals = np.array(vals)
        self.placed = False
        self.empty = False
        self.extra = False
        self.jump = True

        if vals[0] == vals[1]:
            self.acotao = True
        else:
            self.acotao = False

        if vals == [7, 7]:
            self.in_screen = True
            self.path = "_.png"
            self.extra = True

        else:
            self.path = f"{vals[0]}-{vals[1]}.png"
            self.in_screen = False

        super().__init__(img_path=os.path.join("assets", "Dominos (Game)", self.path), x_scale=1, y_scale=1, orientation=0, **kwargs)
        self.rect = super().give_rect()

    def add_position(self, x, y):
        super().add_position(x, y)

    def view_horizontal(self):
        super().change_orientation(90)

    def view_vertical(self):
        super().change_orientation(0)

    def change_orientation_sprite(self):
        super().change_orientation(180)

    def change_orientation_vals(self):
        self.vals = np.array([self.vals[1], self.vals[0]])
        super().change_orientation(180)

    def change_vals(self):
        self.vals = np.array([self.vals[1], self.vals[0]])

    def domino_placed(self):
        self.placed = True

    def update(self):
        if super().is_colliding(pygame.mouse.get_pos()) and self.placed == False and self.in_screen == True:
            if self.empty:
                self.placed = True
                self.jump = False

            if self.jump:
                self.on_hover()
        
        else:
            super().update()
            self.jump = True

        if self.extra and self.empty != True:
            self.x = 548
            self.y = 717

    def extra_dominoes_is_empty(self):
        self.empty = True

    def on_hover(self):
        pixels_to_move = 2
        self.y -= pixels_to_move

        new_height = self.rect.height + pixels_to_move*2
        self.rect.height = new_height
        self.rect.center = (self.x, self.y)
        self.jump = False

    def sum_vals(self):
        return int(self.vals[0]) + int(self.vals[1])

    def click_me(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            return True
        else:
            return False

    def __repr__(self):
        return str(list(self.vals))


class Button(GameObject):
    def __init__(self, path):
        self.path = path
        self.arrow = False
        self.side = ""
        self.position = None
        super().__init__(img_path=os.path.join("assets", "Dominos (Interface)", self.path), x_scale=1, y_scale=1, orientation=0)
        self.rect = super().give_rect()

    def add_position(self, x, y):
        super().add_position(x, y)
        self.position = super().give_rect()

    def change_orientation_sprite(self):
        super().change_orientation(180)

    def activate(self):
        self.add_position(9999, 9999)

    def deactivate(self):
        self.add_position(9999, 9999)

    def update(self):
        if super().is_colliding(pygame.mouse.get_pos()) and self.arrow != True:
            self.on_hover()

        super().update()

    def on_hover(self):
        pass


    def click_me(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            return True
        else:
            return False


class Player:
    def __init__(self, num, manual=True):
        self.num = num
        self.dominoes = np.array([])
        self.manual = manual

    def add_domino(self, domino):
        self.dominoes = np.append(self.dominoes, domino)

    def remove_all(self):
        self.dominoes = np.array([])

    def count_tiles(self):
        sum_of_dominoes = 0

        for domino in self.dominoes:
            sum_of_dominoes += domino.sum_vals()

        return sum_of_dominoes

    def change_manual(self):
        self.manual = True

    def change_auto(self):
        self.manual = False

    def __repr__(self):
        return f"\nPlayer #{self.num} (Manual: {self.manual})\nDominoes: {self.dominoes}\n"


def change_vals(path, idx1, idx2):
    characters = list(path)

    characters[idx1], characters[idx2] = characters[idx2], characters[idx1]
    new_path = ''.join(characters)

    return new_path