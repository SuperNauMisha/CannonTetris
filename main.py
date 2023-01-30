import pygame
import copy
import os
import sys
import sqlite3
import random
import board
import time
import draw_board


all_sprites = pygame.sprite.Group()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_shapes(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            shape = [line.strip() for line in mapFile]
        return shape


class GameOver(pygame.sprite.Sprite):
    image = load_image("gameover.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = GameOver.image
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


connection = sqlite3.connect("data/Shapes.db")
cur = connection.cursor()
paths = []
for path in cur.execute("""SELECT path FROM Paths""").fetchall():
    paths.append(path[0])
shapes = []
for path in paths:
    shapes.append(load_shapes(path))
print(shapes[0])
pygame.init()
pygame.display.set_caption('Тетрис 2.0')
size = 700, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
TIMER = pygame.USEREVENT + 1
BIGTIMER = pygame.USEREVENT + 2
v = 400
go = GameOver()
board = board.Board(10, 20)
drawboard = draw_board.DrawBoard(board.left + board.cell_size * board.width + 50)
oldBoard = copy.deepcopy(board.board)
running = True
start = False
v = 400
min_speed = 50
now_speed = v
counter = 0
draw = False
while running:
    if not board.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
                    drawboard.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    if draw:
                        draw = False
                        board.generate_figure(drawboard.return_figure())
                        print(drawboard.return_figure())
                        pygame.time.set_timer(TIMER, v)
                        pygame.time.set_timer(BIGTIMER, 200)
                    else:
                        start = not start
                        if not start:
                            pygame.time.set_timer(TIMER, 0)
                            pygame.time.set_timer(BIGTIMER, 0)

                        else:
                            pygame.time.set_timer(TIMER, v)
                            pygame.time.set_timer(BIGTIMER, 200)
                if start:
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
                board.score += 1
                if now_speed > min_speed:
                    v -= 1
                    now_speed -= 1
                else:
                    now_speed = min_speed
        if not draw:
            if board.red_count() == 0:
                counter += 1
                if counter == 10:
                    counter = 0
                    draw = True
                    pygame.time.set_timer(TIMER, 0)
                    pygame.time.set_timer(BIGTIMER, 0)
                else:
                    board.start_generation(shapes)

        board.checkRow()
        screen.fill((0, 0, 0))
        drawboard.render(screen)
        board.printScore(screen)
        board.render(screen)

    else:
        for i in range(30):
            all_sprites.draw(screen)
            clock.tick(10)
            pygame.display.flip()
        v = 400
        now_speed = v
        counter = 0
        pygame.time.set_timer(TIMER, 0)
        pygame.time.set_timer(BIGTIMER, 0)
        start = True
        board.restart()
        oldBoard = copy.deepcopy(board.board)

    pygame.display.flip()
