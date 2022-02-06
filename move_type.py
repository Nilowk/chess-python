from enum import Enum


class MoveType(Enum):

    NULL = [
        []
    ]
    DIAGONAL = [
        [-1, 1],
        [-1, -1],
        [1, -1],
        [1, 1]
    ]
    LINE = [
        [0, -1],
        [-1, 0],
        [1, 0],
        [0, 1]
    ]
    ONE_WHITE = [
        [-1, 0]
    ]
    ONE_BLACK = [
        [1, 0]
    ]
    AROUND = [
        [-1, -1],
        [-1, 0],
        [-1, 1],
        [0, -1],
        [0, 1],
        [1, -1],
        [1, 0],
        [1, 1]
    ]
    KNIGHT = [
        [-2, -1],
        [-2, 1],
        [-1, 2],
        [1, 2],
        [2, -1],
        [2, 1],
        [1, -2],
        [-1, -2]
    ]