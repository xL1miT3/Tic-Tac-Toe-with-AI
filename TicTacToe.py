import time
import random
import pygame
# Bilder
X = pygame.image.load("X.png")
O = pygame.image.load("O.png")

class Tic_Tac_Toe:
    def __init__(self):
        self.board_x = 0
        self.board_o = 0
        self.player = "X"
        self.computer = "O"
        self.winning_combinations = [
            0b111000000, 0b000111000, 0b000000111,  # Horizontale Linien
            0b100100100, 0b010010010, 0b001001001,  # Vertikale Linien
            0b100010001, 0b001010100  # Diagonale Linien
        ]
        self.zahler = 0
        self.start_time = time.time()
        self.leeres_board = 0

    def player_move(self, pos):
        self.make_move(pos, self.player)

    def computer_move(self):
        if self.board_x != 0 or self.board_o != 0:
            bestScore = -1000
            bestMove = 0
            for position in range(1, 10):
                if self.valid_move(position, self.board_x, self.board_o):
                    self.board_o = self.board_o | (1 << position - 1)
                    score = self.minimax(self.board_x, self.board_o, False)
                    self.board_o = self.board_o & ~(1 << position - 1)
                    if score > bestScore:
                        bestMove = position
                        bestScore = score

            self.make_move(bestMove, self.computer)
        else:
            self.make_move(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), self.computer)

    def make_move(self, position, x_or_o):
        if x_or_o == "X":
            self.board_x |= (1 << (position - 1))
        elif x_or_o == "O":
            self.board_o |= (1 << (position - 1))

    def valid_move(self, position, board_x, board_o):
        return (board_x & (1 << (position - 1)) == 0) and (board_o & (1 << (position - 1)) == 0) and (
                    position >= 1) and (position <= 9)

    def has_won(self):
        if self.check_win(self.board_x):
            self.end_time = time.time()
            return True
        if self.check_win(self.board_o):
            self.end_time = time.time()
            return True
        return False

    def check_win(self, board):
        for position in self.winning_combinations:
            if (board & position) == position:
                return True
        return False

    def check_draw(self, board_x, board_o):
        if (board_x | board_o) == 0b111111111:
            return True

    def minimax(self, board_x, board_o, isMaximizing):
        self.zahler += 1
        if self.check_win(board_x):
            return -1
        elif self.check_win(board_o):
            return 1
        elif self.check_draw(board_x, board_o):
            return 0

        if isMaximizing:
            bestScore = -800
            for position in range(1, 10):
                if self.valid_move(position, board_x, board_o):
                    board_o = board_o | (1 << position - 1)
                    score = self.minimax(board_x, board_o, False)
                    board_o = board_o & ~(1 << position - 1)
                    bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = 800
            for position in range(1, 10):
                if self.valid_move(position, board_x, board_o):
                    board_x = board_x | (1 << position - 1)
                    score = self.minimax(board_x, board_o, True)
                    board_x = board_x & ~(1 << position - 1)
                    bestScore = min(score, bestScore)
            return bestScore

class Board:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.window = pygame.display.set_mode((self.width, self.height))
        self.bild_pos = [[138 // 2 - 35, 138 // 2 - 35], [(self.width / 2) - 66, 138 // 2 - 35], [self.width - 165, 138 // 2 - 35],
                         [138 // 2 - 35, (self.height / 2) - 66], [(self.width / 2) - 66, (self.height / 2) - 66], [self.width - 165, (self.height / 2) - 66],
                         [138 // 2 - 35, self.height - 165], [(self.width / 2) - 66, self.height - 165], [self.width - 165, self.height - 165]
                         ]
        self.t = Tic_Tac_Toe()
        self.ist_dran = 1
        self.rendered_text = ""

    def redraw_window(self):
        self.window.fill((255, 255, 255))
        self.draw_board()

        for i in range(len(bin(self.t.board_x)) - 2):
            if self.t.board_x & (1 << i):
                self.window.blit(X, (self.bild_pos[i][0], self.bild_pos[i][1]))

        for i in range(len(bin(self.t.board_o)) - 2):
            if self.t.board_o & (1 << i):
                self.window.blit(O, (self.bild_pos[i][0], self.bild_pos[i][1]))
        if self.game_over():
            rect_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            rect_surface.fill((128, 128, 128, 200))
            self.window.blit(rect_surface, (0, 0))
            self.window.blit(self.rendered_text, (self.width / 15, self.height / 2 - 20))
            pygame.display.update()
            time.sleep(2)
            self.new_start()

        pygame.display.update()

    def draw_board(self):
        # vertical
        pygame.draw.rect(self.window, (0, 0, 0), (self.width / 3, 0, 8, self.height))
        pygame.draw.rect(self.window, (0, 0, 0), (self.width * (2/3), 0, 8, self.height))
        # horizontal
        pygame.draw.rect(self.window, (0, 0, 0), (0, self.height / 3, self.width, 8))
        pygame.draw.rect(self.window, (0, 0, 0), (0, self.height * (2 / 3), self.width, 8))

    def get_mouse_click(self, pos_x, pos_y):
        # checkt in welche der 9 felder geklickt wurde
        grid = [[self.width/3, self.height/3], [self.width * (2/3), self.height/3], [self.width, self.height/3],
                [self.width/3, self.height * (2/3)], [self.width * (2/3), self.height * (2/3)], [self.width, self.height * (2/3)],
                [self.width/3, self.height], [self.width * (2/3), self.height], [self.width, self.height]
                ]

        if pos_x <= grid[0][0] and pos_y <= grid[0][0]:
            return 1
        elif pos_x <= grid[1][0] and pos_x >= grid[0][0] and pos_x >= grid[0][1] and pos_y <= grid[1][1]:
            return 2
        elif pos_x <= grid[2][0] and pos_x >= grid[1][0] and pos_x >= grid[1][1] and pos_y <= grid[2][1]:
            return 3
        elif pos_x <= grid[0][0] and pos_y <= grid[3][1] and pos_y >= grid[0][1]:
            return 4
        elif pos_x <= grid[1][0] and pos_x >= grid[0][0] and pos_y <= grid[3][1] and pos_y >= grid[0][1]:
            return 5
        elif pos_x <= grid[2][0] and pos_x >= grid[1][0] and pos_y <= grid[3][1] and pos_y >= grid[0][1]:
            return 6
        elif pos_x <= grid[0][0] and pos_y <= grid[6][1] and pos_y >= grid[1][1]:
            return 7
        elif pos_x <= grid[1][0] and pos_x >= grid[0][0] and pos_y <= grid[7][1] and pos_y >= grid[1][1]:
            return 8
        elif pos_x <= grid[2][0] and pos_x >= grid[1][0] and pos_y <= grid[8][1] and pos_y >= grid[5][1]:
            return 9

    def game_over(self):
        font = pygame.font.SysFont("PressStart2P-Regular.ttf", 72)
        if self.t.check_win(self.t.board_o):
            self.rendered_text = font.render("O hat GEWONNEN !!!", True, (230, 0, 0))
            return True
        elif self.t.check_win(self.t.board_x):
            self.rendered_text = font.render("X hat GEWONNEN !!!", True, (230, 0, 0))
            return True
        elif self.t.check_draw(self.t.board_x, self.t.board_o):
            font = pygame.font.SysFont("PressStart2P-Regular.ttf", 62)
            self.rendered_text = font.render("Schade Unentschieden!", True, (230, 0, 0))
            return True

    def new_start(self):
        while True:
            font = pygame.font.SysFont("PressStart2P-Regular.ttf", 50)
            text_1 = font.render("Press [1] to play again!", True, (0, 0, 0))
            self.window.blit(text_1, (self.width / 4 - 30, self.height / 4 + 10))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        x_or_o = self.ist_dran
                        self.t = Tic_Tac_Toe()
                        self.t.ist_dran = 0 if x_or_o == 1 else 1
                        return False

    def game_loop(self):
        running = True
        while running:
            self.redraw_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_x, click_y = event.pos
                    feld = self.get_mouse_click(click_x, click_y)
                    if self.t.valid_move(feld, self.t.board_x, self.t.board_o) and not self.game_over() and self.ist_dran == 1:
                        self.t.player_move(self.get_mouse_click(click_x, click_y))
                        self.redraw_window()
                        self.ist_dran = 0

            if self.ist_dran == 0 and not self.game_over():
                time.sleep(1)
                self.t.computer_move()
                self.ist_dran = 1

pygame.init()
board = Board()
board.game_loop()
pygame.quit()