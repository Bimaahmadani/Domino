import pygame
import os

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, layer=0, x_scale=1, y_scale=1, orientation=0, img_path=os.path.join("assets", "empty.png")):
        super().__init__()
        self.x = x
        self.y = y
        self.layer = layer
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.orientation = orientation
        self.__load_image(img_path)
        self.change_vals = False

    def __load_image(self, path):
        self.change_vals = False

        try:
            self.image = pygame.image.load(path).convert()
        except:
            path = change_vals(path, 22, 24)
            self.image = pygame.image.load(path).convert()
            self.change_vals = True

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.x_scale, self.image.get_height()*self.y_scale))
        self.image = pygame.transform.rotate(self.image, self.orientation)
        self.image.set_colorkey( ( 0, 187, 45 ) )
        self.rect = self.image.get_rect()

        if self.change_vals:
            self.change_orientation(180)

    def update(self):
        self.rect.center = (self.x, self.y)

    def add_position(self, x, y):
        self.x = x
        self.y = y

    def change_orientation(self, new_orientation):
        self.orientation = new_orientation
        self.image = pygame.transform.rotate(self.image, self.orientation)
        self.rect = self.image.get_rect()

    def give_rect(self):
        return self.rect

    def destroy(self):
        pass


class Domino(GameObject):
    def __init__(self, vals:list, **kwargs):
        self.vals = vals

        if vals[0] == vals[1]:
            self.acotao = True
        else:
            self.acotao = False

        if vals == [7, 7]:
            self.path = "_.png"
        else:
            self.path = f"{vals[0]}-{vals[1]}.png"

        super().__init__(img_path=os.path.join("assets", "Dominos (Game)", self.path), x_scale=1, y_scale=1, orientation=0, **kwargs)

    def add_position(self, x, y):
        super().add_position(x, y)
        self.position = [x, y]

    def view_horizontal(self):
        super().change_orientation(90)

    def view_vertical(self):
        super().change_orientation(0)

    def change_orientation_sprite(self):
        super().change_orientation(180)

    def change_orientation_vals(self):
        self.vals = [self.vals[1], self.vals[0]]
        super().change_orientation(180)

    def update(self):
        super().update()

    def click_me(self):
        self.receive_rect()
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            return True
        else:
            return False
        
    def receive_rect(self):
        rect = super().give_rect()
        self.rect = rect

    def __repr__(self):
        return str(list(self.vals))


class Arrow(GameObject):
    def __init__(self):
        self.can_choose = False
        super().__init__(img_path=os.path.join("assets", "arrow_X.png", self.path), x_scale=1, y_scale=1, orientation=0)

    def change_orientation_sprite(self):
        super().change_orientation(180)

    def activate(self):
        self.can_choose = True
        super().__load_image("/assets/Dominos (Game)/arrow.png")

    def deactivate(self):
        super().__load_image("/assets/Dominos (Game)/arrow_X.png")
        self.can_choose = False

    def click_me(self):
        if self.can_choose:
            self.receive_rect()
            mouse_position = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_position):
                return True
            else:
                return False
        
    def receive_rect(self):
        rect = super().give_rect()
        self.rect = rect


class Player:
    def __init__(self, manual=True):
        self.dominoes = []
        self.manual = manual

    def add_domino(self, domino):
        self.dominoes.append(domino)

    def change_manual(self):
        if self.manual:
            self.manual = False
        else:
            self.manual = True

    def __repr__(self):
        return f"\nPlayer (Manual: {self.manual})\nDominoes: {self.dominoes}\n"


def change_vals(path, idx1, idx2):
    characters = list(path)

    characters[idx1], characters[idx2] = characters[idx2], characters[idx1]
    new_path = ''.join(characters)

    return new_path