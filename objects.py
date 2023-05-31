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


    def __load_image(self, path):
        try:
            self.image = pygame.image.load(path).convert()
        except:
            path = change_vals(path, 22, 24)
            self.image = pygame.image.load(path).convert()

        self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.x_scale, self.image.get_height()*self.y_scale))
        self.image = pygame.transform.rotate(self.image, self.orientation)
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.center = (self.x, self.y)


    def destroy(self):
        pass


class Domino(GameObject):
    def __init__(self, vals:list, **kwargs):
        self.vals = vals
        self.path = f"{vals[0]}-{vals[1]}.png"
        super().__init__(img_path=os.path.join("assets", "Dominos (Game)", self.path), x_scale=1, y_scale=1, orientation=0, **kwargs)

    def __repr__(self):
        return str(list(self.vals))


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