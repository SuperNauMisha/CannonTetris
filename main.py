import pygame
import copy

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчаниюs
        self.left = 100
        self.top = 10
        self.cell_size = 20

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        pass
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
                if oldBoard[y][x] == 0:
                    if self.white_neighbours_count(x, y, oldBoard) == 3:
                        self.board[y][x] = 1
                if oldBoard[y][x] == 1:
                    if self.white_neighbours_count(x, y, oldBoard) == 3 or self.white_neighbours_count(x, y, oldBoard) == 2:
                        self.board[y][x] = 1
                    else:
                        self.board[y][x] = 0


    def white_neighbours_count(self, x, y, allboard):
        maxy = self.width
        maxx = self.height
        ans = 0
        if allboard[y][x - 1] == 1:
            ans += 1
        if allboard[y - 1][x - 1] == 1:
            ans += 1
        if allboard[y - 1][x] == 1:
            ans += 1
        if allboard[y][(x + 1) % maxx] == 1:
            ans += 1
        if allboard[y - 1][(x + 1) % maxx] == 1:
            ans += 1
        if allboard[(y + 1) % maxy][(x + 1) % maxx] == 1:
            ans += 1
        if allboard[(y + 1) % maxy][x] == 1:
            ans += 1
        if allboard[(y + 1) % maxy][x - 1] == 1:
            ans += 1
        return ans



    def render(self, screen):
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(self.left + x * self.cell_size, self.top + y * self.cell_size,
                                   self.cell_size, self.cell_size)
                if self.board[y][x]:
                    pygame.draw.rect(screen, pygame.Color('white'), rect)
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), rect, 1)

def load_shapes(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
            print(level_map)
        return 0

pygame.init()
pygame.display.set_caption('Жизнь')
size = 700, 700
screen = pygame.display.set_mode(size)
TIMER = pygame.USEREVENT + 1
load_shapes("File_Names.txt")
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
