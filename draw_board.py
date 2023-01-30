import pygame
import copy
import random



class DrawBoard:
    def __init__(self, x):
        self.width = 3
        self.height = 3
        self.board = [['.'] * self.width for _ in range(self.height)]
        self.board[self.width // 2][self.height // 2] = '*'
        self.left = x
        self.top = 10
        self.cell_size = 30

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        if cell_coords:
            x, y = cell_coords
            if self.board[y][x] == '.':
                self.board[y][x] = '#'
            elif self.board[y][x] == "#":
                self.board[y][x] = "."

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x > self.left and y > self.top:
            x -= self.left
            y -= self.top
            x /= self.cell_size
            y /= self.cell_size
            x = int(x)
            y = int(y)
        else:
            return None
        if x > self.width - 1 or y > self.height - 1:
            return None
        else:
            return x, y

    def return_figure(self):
        stroka = ''
        retlist = []
        for i in self.board:
            for j in i:
                stroka += j
            retlist.append(stroka)
            stroka = ''
        return retlist

    def render(self, screen):
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(self.left + x * self.cell_size, self.top + y * self.cell_size,
                                   self.cell_size, self.cell_size)
                if self.board[y][x] == '#':
                    pygame.draw.rect(screen, pygame.Color('red'), rect)
                elif self.board[y][x] == "*":
                    pygame.draw.rect(screen, pygame.Color('blue'), rect)
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), rect, 1)
