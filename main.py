from tkinter import *
from piece import Piece
from move_type import MoveType


class Grid(Tk):

    def __init__(self):
        super().__init__()
        self.minsize(640, 640)
        self.maxsize(640, 640)
        self.geometry("640x640")
        self.title("chess")
        self.lap = 0
        self.initialize_pos = {}
        self.grid = [
            [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
            [BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN],
            [VOID, VOID, VOID, VOID, VOID, VOID, VOID, VOID],
            [VOID, VOID, VOID, VOID, VOID, VOID, VOID, VOID],
            [VOID, VOID, VOID, VOID, VOID, VOID, VOID, VOID],
            [VOID, VOID, VOID, VOID, VOID, VOID, VOID, VOID],
            [WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN],
            [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK]
        ]
        self.current_case = [None, None]
        self.map_button = []

    def add_piece(self, piece, row, column):
        self.initialize_pos[piece] = [row, column]

    def initialize(self):
        for row in range(8):
            column_list = []
            for column in range(8):
                case = Button(self, command=lambda r=row, c=column: self.click(r, c))
                case.grid(row=row, column=column)
                column_list.append(case)
            self.map_button.append(column_list)
            self.grid.append([None, None, None, None, None, None, None, None])
        for piece in self.initialize_pos:
            self.grid[self.initialize_pos[piece][0]][self.initialize_pos[piece][1]] = piece
        self.load_color()
        self.load_image()
        self.mainloop()

    def load_image(self):
        for row in range(8):
            for column in range(8):
                if self.grid[row][column] is not None:
                    image = PhotoImage(file=f"./img/{self.grid[row][column].name}.png").subsample(7)
                    lbl = Label(image=image)
                    lbl.image = image
                    self.map_button[row][column].config(image=image)
                else:
                    image = PhotoImage(file="./img/void.png").subsample(7)
                    lbl = Label(image=image)
                    lbl.image = image
                    self.map_button[row][column].config(image=image)

    def load_color(self):
        c = 1
        for row in self.map_button:
            c += 1
            for case in row:
                if c % 2 == 0:
                    case.config(background="#ffffff")
                else:
                    case.config(background="#543b18")
                c += 1

    def click(self, row, column):
        piece = self.grid[row][column]
        case = self.map_button[row][column]
        movement = piece.get_movement()
        if case["bg"] != SELECTED_COLOR:
            if (piece.get_color() == "white" and self.lap % 2 == 0) or (
                    piece.get_color() == "black" and self.lap % 2 == 1) or piece.get_color() == "void":
                self.load_color()
                if self.current_case[0] != row or self.current_case[1] != column:
                    self.current_case = [row, column]
                    for m in movement:
                        r = row
                        c = column
                        if m == MoveType.LINE.value or m == MoveType.DIAGONAL.value:
                            for co in m:
                                while 0 <= r <= 7 and 0 <= c <= 7:
                                    if self.current_case[0] == r and self.current_case[1] == c:
                                        r += co[0]
                                        c += co[1]
                                        continue
                                    if str(self.grid[r][c].name).startswith(
                                            str(self.grid[self.current_case[0]][self.current_case[1]].name)[0]):
                                        break
                                    self.map_button[r][c].config(bg=SELECTED_COLOR)
                                    if self.grid[r][c].name != VOID.name:
                                        break
                                    r += co[0]
                                    c += co[1]
                                r = row
                                c = column
                        elif m != MoveType.NULL.value:
                            for co in m:
                                if 0 <= r + co[0] <= 7 and 0 <= c + co[1] <= 7:
                                    if self.grid[self.current_case[0]][self.current_case[1]] == WHITE_PAWN or \
                                            self.grid[self.current_case[0]][self.current_case[1]] == BLACK_PAWN:
                                        if self.grid[r + co[0]][c + co[1]] == VOID:
                                            self.map_button[r + co[0]][c + co[1]].config(bg=SELECTED_COLOR)
                                        if 0 <= c + co[1] + 1 <= 7:
                                            if self.grid[r + co[0]][c + co[1] + 1] != VOID:
                                                if not (str(self.grid[r + co[0]][c + co[1] + 1].name).startswith(
                                                        str(self.grid[self.current_case[0]][self.current_case[1]].name)[
                                                            0])):
                                                    self.map_button[r + co[0]][c + co[1] + 1].config(bg=SELECTED_COLOR)
                                        if 0 <= c + co[1] - 1 <= 7:
                                            if self.grid[r + co[0]][c + co[1] - 1] != VOID:
                                                if not (str(self.grid[r + co[0]][c + co[1] - 1].name).startswith(
                                                        str(self.grid[self.current_case[0]][self.current_case[1]].name)[
                                                            0])):
                                                    self.map_button[r + co[0]][c + co[1] - 1].config(bg=SELECTED_COLOR)
                                    elif not (str(self.grid[r + co[0]][c + co[1]].name).startswith(
                                            str(self.grid[self.current_case[0]][self.current_case[1]].name)[0])):
                                        self.map_button[r + co[0]][c + co[1]].config(bg=SELECTED_COLOR)
            else:
                self.current_case = [None, None]
        else:
            self.perform_movement(row, column)

    def perform_movement(self, row, column):
        current_piece = self.grid[self.current_case[0]][self.current_case[1]]
        selected_piece = self.grid[row][column]
        if selected_piece == VOID:
            self.grid[self.current_case[0]][self.current_case[1]] = selected_piece
            self.grid[row][column] = current_piece
        else:
            self.grid[self.current_case[0]][self.current_case[1]] = VOID
            self.grid[row][column] = current_piece
        self.current_case = [None, None]
        self.load_color()
        self.load_image()
        self.lap += 1


SELECTED_COLOR = "#00561b"

VOID = Piece("void", MoveType.NULL.value)

WHITE_PAWN = Piece("wp", MoveType.ONE_WHITE.value)
BLACK_PAWN = Piece("bp", MoveType.ONE_BLACK.value)

BLACK_KING = Piece("bk", MoveType.AROUND.value)
WHITE_KING = Piece("wk", MoveType.AROUND.value)

BLACK_QUEEN = Piece("bq", MoveType.DIAGONAL.value, MoveType.LINE.value)
WHITE_QUEEN = Piece("wq", MoveType.DIAGONAL.value, MoveType.LINE.value)

WHITE_BISHOP = Piece("wb", MoveType.DIAGONAL.value)
BLACK_BISHOP = Piece("bb", MoveType.DIAGONAL.value)

BLACK_KNIGHT = Piece("bkn", MoveType.KNIGHT.value)
WHITE_KNIGHT = Piece("wkn", MoveType.KNIGHT.value)

WHITE_ROOK = Piece("wr", MoveType.LINE.value)
BLACK_ROOK = Piece("br", MoveType.LINE.value)

grid = Grid()
grid.initialize()
