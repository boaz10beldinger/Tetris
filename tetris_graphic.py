import random
import numpy as np

print("//////////////")
N = 10
M = 20
SCORE_PER_ROW  = 100
COMBO = 2


def add_shape(pos, screen, shape):
    pos_x = pos[0]
    pos_y = pos[1]

    if pos_x + len(shape[0]) > N or pos_y + len(shape) > M or pos_x < 0 or pos_y < 0:
        print('fuck')
        return False

    i = pos_x
    while i - pos_x < len(shape[0]):
        j = pos_y
        while j - pos_y < len(shape):
            if shape[j - pos_y][i - pos_x] != 0:
                screen[j][i] = shape[j - pos_y][i - pos_x]
            j += 1
        i += 1


def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

    # rotated = []
    # for x in range(len(list(shape))):
    #     part = []
    #     for y in range(len(list(shape[0]))):
    #         part.append(shape[x][y])
    #     rotated.append(part)
    # return rotated


def check_depths(shape, pos, screen):
    ''' pos - where does the shape starts from '''
    pos_x = pos[0]
    pos_y = pos[1]

    if pos_x + len(shape[0]) > N or pos_y + len(shape) > M:
        print( pos_x, pos_y, len(shape[0]), len(shape))
        return None

    max_depths = [-1 for i in range(len(shape[0]))]
    for curr_i in range(pos_x, pos_x + len(shape[0])):
        check = True
        for curr_j in range(pos_y, M - len(shape) + 1):
            for check_j in range(curr_j, curr_j + len(shape)):
                if shape[check_j - curr_j][curr_i - pos_x] != 0 and screen[check_j][curr_i] != 0:
                    check = False
            if not check:
                print("check")
                break
            max_depths[curr_i - pos_x] += 1
    print(max_depths)
    return max_depths


def move_down(shape, pos, screen):
    depths = check_depths(shape, pos, screen)
    print(depths)
    if depths is None:
        return False
    min_d = min(depths)
    add_shape([pos[0], pos[1] + min_d], screen, shape)
    return True


def main_loop(screen, shapes):
    score = 0
    next_shapes = [shapes[random.randrange(7)] for i in range(3)]
    print(next_shapes)
    print_screen(screen)
    column = int(input("column wanted: "))
    rotation_num = int(input("how many times would you like to rotate?: "))
    upcoming_shape = next_shapes.pop(0)
    if rotation_num > 0:
        for i in range(rotation_num):
            upcoming_shape = rotate(upcoming_shape)
    if not (0 <= column < N and column + len(upcoming_shape) < N):
        print("oops")
        return 0
    while move_down(upcoming_shape,  [column, 0], screen):
        rows_exploded = check_for_rows_and_explode(screen)
        score += SCORE_PER_ROW * COMBO ** rows_exploded
        next_shapes.append(shapes[random.randrange(7)])
        print(next_shapes)
        print_screen(screen)
        column = int(input("column wanted: "))
        rotation_num = int(input("how many times would you like to rotate?: "))
        upcoming_shape = next_shapes.pop(0)
        if rotation_num > 0:
            for i in range(rotation_num):
                upcoming_shape = rotate(upcoming_shape)
        if not (0 <= column < N and column + len(upcoming_shape) < N):
            print("oops")
            break
    print("you lost, your score is: " + str(score))
    return score


def print_screen(screen):
    for i in range(len(screen)):
        print(screen[i])


def check_for_rows_and_explode(screen):
    count =0
    rows_exploded = 0
    for i in range(len(screen)):
        for j in range(len(screen[0])):
            if screen[i][j] != 0:
                count += 1
        if count == N:
            screen.pop(i)
            np.insert(screen, [0] * 10, 0)
            rows_exploded += 1
        count = 0
    return rows_exploded


if __name__ == "__main__":

    s = [[0 for i in range(N)] for j in range(M)]
    tetriminos = [[[1, 1, 1], [0, 1, 0]],
                  [[2, 2, 2, 2]],
                  [[3, 3], [3, 3]],
                  [[0, 4, 4], [4, 4, 0]],
                  [[5, 5, 0], [0, 5, 5]],
                  [[6, 6, 6], [0, 0, 6]],
                  [[7, 7, 7], [7, 0, 0]]]

    main_loop(s, tetriminos)
