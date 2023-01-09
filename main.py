import pygame
import copy
import sqlite3


class Board:
    def __init__(self, width, height):
        self.spawn = 4, 1
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
        self.generate_figure(shapes[2])
        # if cell_coords:
        #     x, y = cell_coords
        #     if self.board[y][x] == 0:
        #         self.board[y][x] = 1
        #     else:
        #         self.board[y][x] = 0

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


    def next_move(self, oldBoard):
        print("TIMER")
        for x in range(0, self.width):
            for y in range(0, self.height):
                pass


    def generate_figure(self, figure):
        print(figure)
        start_x, start_y = self.spawn
        counterx = 0
        countery = 0
        for i in figure:
            print(i)
            for j in i:
                print(2)
                if j == "#":
                    self.board[start_y + countery][start_x + counterx] = 2
                counterx += 1
            counterx = 0
            countery += 1



    def render(self, screen):
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(self.left + x * self.cell_size, self.top + y * self.cell_size,
                                   self.cell_size, self.cell_size)
                if self.board[y][x] == 2:
                    pygame.draw.rect(screen, pygame.Color('red'), rect)
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), rect, 1)

def load_shapes(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            shape = [line.strip() for line in mapFile]
            print(shape)
        return shape

connection = sqlite3.connect("data/Shapes.db")
cur = connection.cursor()
paths = []
for path in cur.execute("""SELECT path FROM Paths""").fetchall():
    paths.append(path[0])
print(paths)
shapes = []
for path in paths:
    shapes.append(load_shapes(path))

pygame.init()
pygame.display.set_caption('Тетрис')
size = 500, 700
screen = pygame.display.set_mode(size)
TIMER = pygame.USEREVENT + 1
v = 400
board = Board(10, 20)
running = True
start = False
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
                pygame.time.set_timer(TIMER, v)
            elif event.button == 5:
                v -= 50
                pygame.time.set_timer(TIMER, v)
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                start = not start
                if not start:
                    pygame.time.set_timer(TIMER, 0)
                else:
                    pygame.time.set_timer(TIMER, v)
        if event.type == TIMER:
            oldBoard = copy.deepcopy(board.board)
            board.next_move(oldBoard)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
