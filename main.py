from copy import deepcopy

from termcolor import colored

COLORS = {
    'R': 'red',
    'G': 'green',
    'B': 'blue',
    'Y': 'yellow'
}

TILES = [
    ('RYBGRGYB', 'RYGBRGBY'),
    ('RBYGRYGB', 'BRGYBYRG'),
    ('GRBGRYBY', 'BRYBRGYG'),
    ('YRGYRBGB', 'YRBYRGBG'),
    ('YRBGYBGR', 'RBGYRYBG'),
    ('RBGRBYGY', 'GBYGBRYR'),
    ('BRYGBYGR', 'YRGBYBRG'),
    ('RBYBGRYG', 'RYGYBRGB'),
    ('BRGRYBGY', 'BGYGRBYR'),
]

BOARD = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
]

X = Y = 3

UP = (0, False)
RIGHT = (2, False)
DOWN = (4, True)
LEFT = (6, True)


def validate_tile(tile):
    if len(tile) != 2 or len(tile[0]) != 8 or len(tile[1]) != 8:
        raise Exception(f'WRONG TILE LENGTH: {tile}')
    for color in COLORS.keys():
        if len([t for t in tile[0] if t == color]) != 2 or len([t for t in tile[1] if t == color]) != 2:
            raise Exception(f'WRONG TILE COLORS: {tile}')


def validate_tiles():
    for tile in TILES:
        validate_tile(tile)


def get_neighbors(x, y):
    return [(x + i, y + j) for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= x + i < X and 0 <= y + j < Y]


def get_colors(tile, position):
    colors = tile[0][position[0]:position[0] + 2]
    if position[1]:
        return colors[::-1]
    return colors


def validate_neighbors(board, x1, y1, x2, y2):
    if not board[y1][x1] or not board[y2][x2]:
        return True
    tile1 = board[y1][x1]
    tile2 = board[y2][x2]
    if x1 == x2:
        if y1 > y2:
            return get_colors(tile1, UP) == get_colors(tile2, DOWN)
        else:
            return get_colors(tile1, DOWN) == get_colors(tile2, UP)
    elif y1 == y2:
        if x1 > x2:
            return get_colors(tile1, LEFT) == get_colors(tile2, RIGHT)
        else:
            return get_colors(tile1, RIGHT) == get_colors(tile2, LEFT)
    else:
        raise Exception('TILT')


def validate_board(board):
    for x in range(X):
        for y in range(Y):
            for i, j in get_neighbors(x, y):
                if not validate_neighbors(board, x, y, i, j):
                    return False
    return True


def rotate_tile(tile, n):
    return (tile[0][2 * n:] + tile[0][:2 * n], tile[1])


def flip_tile(tile):
    return (tile[1], tile[0])


def get_all_tile_rotations(tile):
    result = []
    for i in range(4):
        result.append(rotate_tile(tile, i))
    tile = flip_tile(tile)
    for i in range(4):
        result.append(rotate_tile(tile, i))
    return result


def c(point):
    return colored(point, COLORS[point])


# YRBGYGRB ==>
# +----+
# | YR |
# |B  B|
# |R  G|
# | GY |
# +----+
def print_tile(tile):
    if tile:
        print('+----+')
        print('| ' + c(tile[0][0]) + c(tile[0][1]) + ' |')
        print('|' + c(tile[0][7]) + '  ' + c(tile[0][2]) + '|')
        print('|' + c(tile[0][6]) + '  ' + c(tile[0][3]) + '|')
        print('| ' + c(tile[0][5]) + c(tile[0][4]) + ' |')
        print('+----+')
    else:
        print('+----+')
        print('|    |')
        print('|    |')
        print('|    |')
        print('|    |')
        print('+----+')


def print_board(board):
    print('----------------------------------------------')
    print('Arrange tiles:')
    print('+---+')
    print('|123|')
    print('|456|')
    print('|789|')
    print('+---+')
    i = 1
    for line in board:
        for tile in line:
            print(f'{i}=')
            i += 1
            print_tile(tile)
    print('----------------------------------------------')


def find_empty(board):
    for x in range(X):
        for y in range(Y):
            if not board[y][x]:
                return x, y
    return None


def put_onto_board(board, tile, x, y):
    result = deepcopy(board)
    result[y][x] = tile
    return result


def find_solution(board, tiles):
    if not tiles:
        print_board(board)
        return
    x, y = find_empty(board)
    for tile in tiles:
        next_tiles = deepcopy(tiles)
        next_tiles.remove(tile)
        for final_tile in get_all_tile_rotations(tile):
            next_board = put_onto_board(board, final_tile, x, y)
            if not validate_board(next_board):
                continue
            else:
                find_solution(next_board, next_tiles)
    pass


if __name__ == '__main__':
    validate_tiles()
    find_solution(BOARD, TILES)
