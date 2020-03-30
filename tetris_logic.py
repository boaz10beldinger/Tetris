import random
import numpy as np
# great job boaz

class Logic:
    N = 10
    M = 20
    SCORE_PER_ROW = 100
    COMBO = 2
    TETRIMINOS = {1: [[[1, 1, 1],
                       [0, 1, 0]], [[0, 1, 0],
                                    [1, 1, 1]], [[1, 0],
                                                 [1, 1],
                                                 [1, 0]], [[0, 1],
                                                           [1, 1],
                                                           [0, 1]]],
                  2: [[[2, 2, 2, 2]], [[2],
                                     [2],
                                     [2],
                                     [2]]],
                  3: [[[3, 3],
                      [3, 3]]],
                  4: [[[0, 4, 4],
                       [4, 4, 0]], [[4, 0],
                                    [4, 4],
                                    [0, 4]]],
                  5: [[[5, 5, 0],
                       [0, 5, 5]], [[0, 5],
                                    [5, 5],
                                    [5, 0]]],
                  6: [[[6, 6, 6],
                       [0, 0, 6]], [[6, 0, 0],
                                    [6, 6, 6]], [[6, 6],
                                                 [6, 0],
                                                 [6, 0]], [[0, 6],
                                                           [0, 6],
                                                           [6, 6]]],
                  7: [[[7, 7, 7],
                       [7, 0, 0]], [[0, 0, 7],
                                    [7, 7, 7]], [[7, 0],
                                                 [7, 0],
                                                 [7, 7]], [[7, 7],
                                                           [0, 7],
                                                           [6, 7]]]}

    def __init__(self):
        self.screen = [[0 for i in range(Logic.N)] for j in range(Logic.M)]
        idx = [random.randrange(7) for i in range(3)]
        upcoming_shapes=[]
        for i in range(3):
            upcoming_shapes.append(Logic.TETRIMINOS[idx[i]+1])
        self.upcoming_shapes = upcoming_shapes
        self.score = 0

    def get_upcoming_shapes(self):
        i = self.upcoming_shapes.pop(0)
        self.upcoming_shapes.append(Logic.TETRIMINOS[random.randrange(7) + 1])
        return i

    def move_down(self, shape, pos):
        depths = self.check_depths(shape, pos)
        if depths is None:
            return False
        min_d = min(depths)
        self.add_shape([pos[0], pos[1] + min_d], shape)
        return True

# changes screen according to the shape located
    def add_shape(self, pos, shape):
        pos_x = pos[0]
        pos_y = pos[1]

        if pos_x + len(shape[0]) > Logic.N or pos_y + len(shape) > Logic.M or pos_x < 0 or pos_y < 0:
            return False
        i = pos_x
        while i - pos_x < len(shape[0]):
            j = pos_y
            while j - pos_y < len(shape):
                if shape[j - pos_y][i - pos_x] != 0:
                    self.screen[j][i] = shape[j - pos_y][i - pos_x]
                j += 1
            i += 1

    def check_depths(self, shape, pos):
        ''' pos - where does the shape starts from '''
        pos_x = pos[0]
        pos_y = pos[1]

        if pos_x + len(shape[0]) > Logic.M or pos_y + len(shape) > Logic.N:
            return None

        max_depths = [-1 for i in range(len(shape[0]))]
        for curr_i in range(pos_x, pos_x + len(shape[0])):
            check = True
            for curr_j in range(pos_y, Logic.M - len(shape) + 1):
                for check_j in range(curr_j, curr_j + len(shape)):
                    if shape[check_j - curr_j][curr_i - pos_x] != 0 and self.screen[check_j][curr_i] != 0:
                        check = False
                if not check:
                    break
                max_depths[curr_i - pos_x] += 1
        if max(max_depths) <= 0:
            return None
        return max_depths

    def get_next_shape_version_and_column(self):
        return 0, 0

    def check_for_rows_and_explode(self):
        count = 0
        rows_exploded = 0
        for i in range(len(self.screen)):
            for j in range(len(self.screen[0])):
                if self.screen[i][j] != 0:
                    count += 1
            if count == Logic.N:
                self.screen.pop(i)
                np.insert(self.screen, [0] * 10, 0)
                rows_exploded += 1
            count = 0
        return rows_exploded

