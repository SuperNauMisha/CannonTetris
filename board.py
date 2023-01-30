import pygame
import copy
import random


class Board:
    def __init__(self, width, height):
        self.spawn = 4, 0
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 100
        self.top = 10
        self.cell_size = 30
        self.score = 0
        self.game_over = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        pass
        # x, y = cell_coords
        # if self.board[y][x] == 1 or self.board[y][x] == 2:
        #     self.board[y][x] = 0

    def start_generation(self, shapes):
        self.generate_figure(shapes[random.randint(0, len(shapes) - 1)])

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

    def red_count(self):
        counter = 0
        for i in self.board:
            for j in i:
                if j == 2 or j == 3:
                    counter += 1
        return counter

    def next_move(self):
        green_count = 0
        oldboard = copy.deepcopy(self.board)
        for y in range(self.height - 1, -1, -1):
            for x in range(0, self.width):
                if oldboard[y][x] == 2 or oldboard[y][x] == 3:
                    if y == self.height - 1:
                        green_count += 1
                    elif oldboard[y + 1][x] == 1:
                        green_count += 1

        for y in range(self.height - 1, -1, -1):
            for x in range(0, self.width):
                if oldboard[y][x] == 2 or oldboard[y][x] == 3:
                    if y == self.height - 1:
                        self.board[y][x] = 1
                        self.checkGameOver()
                        green_count += 1
                    elif oldboard[y + 1][x] == 1:
                        self.board[y][x] = 1
                        self.checkGameOver()
                        green_count += 1
                    if green_count > 0:
                        self.board[y][x] = 1
                        self.checkGameOver()
                    elif oldboard[y + 1][x] != 1 and oldboard[y][x] == 2:
                        self.board[y + 1][x] = 2
                        self.board[y][x] = 0
                    elif oldboard[y + 1][x] != 1 and oldboard[y][x] == 3:
                        self.board[y + 1][x] = 3
                        self.board[y][x] = 0

    def move_shape(self, direction):
        right = False
        left = False
        for y in range(0, self.height):
            if self.board[y][0] == 2 or self.board[y][0] == 3:
                left = True
            if self.board[y][self.width - 1] == 2 or self.board[y][self.width - 1] == 3:
                right = True

        for y in range(self.height):
            for x in range(self.width):
                if not left:
                    if (self.board[y][x] == 2 or self.board[y][x] == 3) and self.board[y][x - 1] == 1:
                        left = True
                if not right:
                    if (self.board[y][x] == 2 or self.board[y][x] == 3) and self.board[y][x + 1] == 1:
                        right = True

        oldboard = copy.deepcopy(self.board)
        for y in range(0, self.height):
            if dir == -1:
                if not left:
                    for x in range(0, self.width):
                        if oldboard[y][x] == 2:
                            self.board[y][x + direction] = 2
                            self.board[y][x] = 0
                        elif oldboard[y][x] == 3:
                            self.board[y][x + direction] = 3
                            self.board[y][x] = 0
            else:
                if not right:
                    for x in range(self.width - 1, -1, -1):
                        if oldboard[y][x] == 2:
                            self.board[y][x + direction] = 2
                            self.board[y][x] = 0
                        elif oldboard[y][x] == 3:
                            self.board[y][x + direction] = 3
                            self.board[y][x] = 0

    def rotate_shape(self, direction):
        oldboard = copy.deepcopy(self.board)
        canrot = True
        rotx, roty = -1, -1
        zerolist = [[0] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 2:
                    zerolist[y][x] = self.board[y][x]
                else:
                    zerolist[y][x] = 0

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 3:
                    rotx, roty = x, y
        if rotx >= 0 and roty >= 0:
            for y in range(self.height):
                for x in range(self.width):
                    if oldboard[y][x] == 2:
                        dx = x - rotx
                        dy = y - roty
                        if direction == -1:
                            if abs(dx) > 0 and abs(dy) > 0:
                                if dx < 0 and dy < 0:
                                    dy = -dy
                                elif dx < 0 and dy > 0:
                                    dx = -dx
                                elif dx > 0 and dy < 0:
                                    dx = -dx
                                elif dx > 0 and dy > 0:
                                    dy = -dy
                            else:
                                if dy == 0 and abs(dx) > 0:
                                    dy = -dx
                                    dx = 0
                                elif dx == 0 and abs(dy) > 0:
                                    dx = dy
                                    dy = 0
                        elif direction == 1:
                            if abs(dx) > 0 and abs(dy) > 0:
                                if dx < 0 and dy < 0:
                                    dx = -dx
                                elif dx < 0 and dy > 0:
                                    dy = -dy
                                elif dx > 0 and dy < 0:
                                    dy = -dy
                                elif dx > 0 and dy > 0:
                                    dx = -dx
                            else:
                                if dy == 0:
                                    dy = dx
                                    dx = 0
                                elif dx == 0:
                                    dx = -dy
                                    dy = 0
                        if not (roty + dy < 0 or roty + dy >= self.height or rotx + dx < 0\
                                or rotx + dx >= self.width or oldboard[roty + dy][rotx + dx] == 1):
                            zerolist[roty + dy][rotx + dx] = 2
                        else:
                            canrot = False
            if canrot:
                self.board = copy.deepcopy(zerolist)

    def generate_figure(self, figure):
        start_x, start_y = self.spawn
        counterx = 0
        countery = 0
        self.allcount = 0
        for i in figure:
            for j in i:
                if j == "#":
                    self.allcount += 1
                    self.board[start_y + countery][start_x + counterx] = 2
                elif j == "*":
                    self.allcount += 1
                    self.board[start_y + countery][start_x + counterx] = 3
                counterx += 1
            counterx = 0
            countery += 1

    def checkGameOver(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.board[y][x] == 1:
                    if y < 2:
                        self.game_over = True

    def restart(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.score = 0
        self.game_over = False

    def printScore(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.score), True, (100, 255, 100))
        text_x = self.left + 10
        text_y = self.top + self.height * self.cell_size + 20
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)

    def checkRow(self):
        for y in range(0, self.height):
            dely = y
            all_ = True
            for x in range(0, self.width):
                if self.board[y][x] != 1:
                    all_ = False
            if all_:
                self.score += 1000
                for x in range(0, self.width):
                    self.board[y][x] = 0
                for y in range(dely, -1, -1):
                    for x in range(0, self.width):
                        if self.board[y][x] == 1:
                            self.board[y][x] = 0
                            self.board[y + 1][x] = 1

    def render(self, screen):
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(self.left + x * self.cell_size, self.top + y * self.cell_size,
                                   self.cell_size, self.cell_size)
                if self.board[y][x] == 2:
                    pygame.draw.rect(screen, pygame.Color('red'), rect)
                elif self.board[y][x] == 3:
                    pygame.draw.rect(screen, pygame.Color('blue'), rect)
                elif self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color('green'), rect)
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), rect, 1)
