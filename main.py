import pygame
import copy
import sqlite3
import random


class Board:
    def __init__(self, width, height):
        self.spawn = 4, 0
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчаниюs
        self.left = 100
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        self.start_generation()

    def start_generation(self):
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
        print("TIMER")
        green_count = 0
        oldBoard = copy.deepcopy(board.board)
        for y in range(self.height - 1, -1, -1):
            for x in range(0, self.width):
                if oldBoard[y][x] == 2 or oldBoard[y][x] == 3:
                    if y == self.height - 1:
                        green_count += 1
                    elif oldBoard[y + 1][x] == 1:
                        green_count += 1

        for y in range(self.height - 1, -1, -1):
            for x in range(0, self.width):
                if oldBoard[y][x] == 2 or oldBoard[y][x] == 3:
                    if y == self.height - 1:
                        self.board[y][x] = 1
                        green_count += 1
                    elif oldBoard[y + 1][x] == 1:
                        self.board[y][x] = 1
                        green_count += 1
                    if green_count > 0:
                        self.board[y][x] = 1
                    elif oldBoard[y + 1][x] != 1 and oldBoard[y][x] == 2:
                        self.board[y + 1][x] = 2
                        self.board[y][x] = 0
                    elif oldBoard[y + 1][x] != 1 and oldBoard[y][x] == 3:
                        self.board[y + 1][x] = 3
                        self.board[y][x] = 0

    def move_shape(self, dir):
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


        oldBoard = copy.deepcopy(board.board)
        for y in range(0, self.height):
            if dir == -1:
                if not left:
                    for x in range(0, self.width):
                        print(x, y)
                        if oldBoard[y][x] == 2:
                            self.board[y][x + dir] = 2
                            self.board[y][x] = 0
                        elif  oldBoard[y][x] == 3:
                            self.board[y][x + dir] = 3
                            self.board[y][x] = 0
            else:
                if not right:
                    for x in range(self.width -1, -1, -1):
                        print(x, y)
                        if oldBoard[y][x] == 2:
                            self.board[y][x + dir] = 2
                            self.board[y][x] = 0
                        elif oldBoard[y][x] == 3:
                            self.board[y][x + dir] = 3
                            self.board[y][x] = 0
    def rotate_shape(self, dir):
        oldBoard = copy.deepcopy(board.board)
        canRot = True
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
                    if oldBoard[y][x] == 2:
                        dx = x - rotx
                        dy = y - roty
                        print(dir)
                        if dir == -1:
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
                        elif dir == 1:
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
                        if not (roty + dy < 0 or roty + dy >= self.height or rotx + dx < 0 \
                                or rotx + dx >= self.width or oldBoard[roty + dy][rotx + dx] == 1):
                            zerolist[roty + dy][rotx + dx] = 2
                        else:
                            canRot = False
            if canRot:
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

    def checkRow(self):

        for y in range(0, self.height):
            dely = y
            all_ = True
            for x in range(0, self.width):
                if self.board[y][x] != 1:
                    all_ = False
            if all_:
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


def load_shapes(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            shape = [line.strip() for line in mapFile]
        return shape


connection = sqlite3.connect("data/Shapes.db")
cur = connection.cursor()
paths = []
for path in cur.execute("""SELECT path FROM Paths""").fetchall():
    paths.append(path[0])
shapes = []
for path in paths:
    shapes.append(load_shapes(path))

pygame.init()
pygame.display.set_caption('Тетрис 2.0')
size = 500, 700
screen = pygame.display.set_mode(size)
TIMER = pygame.USEREVENT + 1
BIGTIMER = pygame.USEREVENT + 2
v = 400
board = Board(10, 20)
oldBoard = copy.deepcopy(board.board)
running = True
start = False
v = 400
min_speed = 10
now_speed = v
pygame.time.set_timer(BIGTIMER, 200)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                board.get_click(event.pos)
            elif event.button == 3:
                start = not start
                if not start:
                    pygame.time.set_timer(TIMER, 0)
                else:
                    pygame.time.set_timer(TIMER, v)
            elif event.button == 4:
                v += 50
            elif event.button == 5:
                v -= 50
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                start = not start
                if not start:
                    pygame.time.set_timer(TIMER, 0)
                else:
                    pygame.time.set_timer(TIMER, v)
            if event.key == 97:
                board.move_shape(-1)
            if event.key == 100:
                board.move_shape(1)
            if event.key == 113:
                board.rotate_shape(-1)
            if event.key == 101:
                board.rotate_shape(1)
            if event.key == 115:
                v = 50
        if event.type == pygame.KEYUP:
            if event.key == 115:
                v = now_speed
        if event.type == TIMER:
            pygame.time.set_timer(TIMER, v)
            oldBoard = copy.deepcopy(board.board)
            board.next_move()
        if event.type == BIGTIMER:
            if now_speed > min_speed:
                v -= 1
                now_speed -= 1

    if board.red_count() == 0:
        board.start_generation()
    board.checkRow()
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
