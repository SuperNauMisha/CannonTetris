import pygame
import copy
import sqlite3
import random
import board


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
board = board.Board(10, 20)
oldBoard = copy.deepcopy(board.board)
running = True
start = False
v = 400
min_speed = 30
now_speed = v
while running:
    if not board.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    board.get_click(event.pos)
                elif event.button == 4:
                    v += 50
                elif event.button == 5:
                    v -= 50
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
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

        if board.red_count() == 0:
            board.start_generation(shapes)
        board.checkRow()
        screen.fill((0, 0, 0))
        board.printScore(screen)
        board.render(screen)
    else:
        v = 400
        now_speed = v
        board.restart()
        oldBoard = copy.deepcopy(board.board)
        pygame.time.set_timer(TIMER, 0)
        pygame.time.set_timer(BIGTIMER, 0)
        start = False
    pygame.display.flip()
