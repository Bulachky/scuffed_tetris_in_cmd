import numpy as np


class Grid:
    def __init__(self, index_lst, rows=20, columns=10):
        self.rows = rows
        self.columns = columns
        self.initial_grid = np.array([['-'] * self.columns] * self.rows)
        self.set_shape(index_lst)

    def __str__(self):
        return '\n'.join([' '.join(row_) for row_ in self.initial_grid])

    def set_shape(self, index_list):
        for index in index_list:
            self.initial_grid[index // self.columns][index % self.columns] = '0'


class Tetris:
    piece_storage = {"I": np.array([[4, 14, 24, 34], [3, 4, 5, 6]] * 2),
                     "S": np.array([[5, 4, 14, 13], [4, 14, 15, 25]] * 2),
                     "Z": np.array([[4, 5, 15, 16], [5, 15, 14, 24]] * 2),
                     "L": np.array([[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]),
                     "J": np.array([[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]),
                     "O": np.array([[4, 14, 15, 5]] * 4),
                     "T": np.array([[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]])}
    index_storage = []
    limit_to_indexes = []

    def __init__(self, n, m, piece):
        self.n = n  # number of rows
        self.m = m  # number of columns
        self.current_piece = piece  # the piece we're playing with right now
        self.current_position = 0  # the position of the piece in the rotation positions (from 0 to 3)
        self.positions = self.adjust_board()  # the array containing the rotation positions of the piece adjusted to the current dimension of the board

    def adjust_board(self):
        return [[(index % 10) - (10 - self.m) // 2 + index // 10 * self.m for index in pos] for pos in
                Tetris.piece_storage[self.current_piece]]

    def load_piece(self):
        for index in self.positions[self.current_position]:
            Tetris.index_storage.append(index)
        return str(Grid(Tetris.index_storage, self.n, self.m))

    def go_down(self):
        if any(d + self.m > self.m * self.n for d in self.positions[self.current_position]) or any(d + self.m in Tetris.limit_to_indexes for d in self.positions[self.current_position]):
            for index in self.positions[self.current_position]:
                if index not in Tetris.limit_to_indexes:
                    Tetris.limit_to_indexes.append(index)
        for i, pos in enumerate(self.positions):
            if all(d + self.m < self.m * self.n for d in pos) and all(d + self.m not in Tetris.limit_to_indexes for d in pos):
                self.positions[i] = [index + self.m if index + self.m < self.m * self.n else index for index in pos]
        for _ in range(4):
            Tetris.index_storage.pop()
        for index in self.positions[self.current_position]:
            Tetris.index_storage.append(index)
        grid_str = str(Grid(Tetris.index_storage, self.n, self.m))
        if self.game_over():
            grid_str += '\n\nGame Over!'
        return grid_str

    def rotate_piece(self):
        if all(d + self.m < self.m * self.n for d in self.positions[self.current_position]):
            self.current_position += 1 if self.current_position != 3 else - self.current_position
        return self.go_down()

    def move_piece_left(self):
        for i, pos in enumerate(self.positions):
            if not any(n % self.m == 0 for n in pos) and all(d + self.m < self.m * self.n for d in pos):
                for j, index in enumerate(pos):
                    self.positions[i][j] = index - 1
        return self.go_down()

    def move_piece_right(self):
        for i, pos in enumerate(self.positions):
            if all((n + 1) % self.m != 0 for n in pos) and all(d + self.m < self.m * self.n for d in pos):
                for j, index in enumerate(pos):
                    self.positions[i][j] = index + 1
        return self.go_down()

    def break_(self):
        for n in range(self.n):
            count = 0
            remove_list = []
            for i, index in enumerate(Tetris.index_storage):
                if index // self.m == n:
                    count += 1
                    remove_list.append(index)
            if count == self.m:
                for d in remove_list:
                    Tetris.index_storage.remove(d)
                    Tetris.limit_to_indexes.remove(d)
                for i, index in enumerate(Tetris.index_storage):
                    if index // self.m < n:
                        Tetris.index_storage[i] += self.m
                for i, index in enumerate(Tetris.limit_to_indexes):
                    if index // self.m < n:
                        Tetris.limit_to_indexes[i] += self.m
        return str(Grid(Tetris.index_storage, self.n, self.m))

    def game_over(self):
        result = False
        for n in range(self.m):
            count = 0
            for index in Tetris.limit_to_indexes:
                if index % self.m == n:
                    count += 1
            if count == self.n:
                result = True
        return result


def main():
    column, row = map(int, input().split())
    print(str(Grid([], row, column)) + '\n')
    input()
    shape = input()
    game = Tetris(row, column, shape)
    print(game.load_piece(), end="\n\n")
    while True:
        command = input()
        grid_to_print = ''
        if command == 'piece':
            shape = input()
            game = Tetris(row, column, shape)
            grid_to_print = game.load_piece()
        elif command == 'rotate':
            grid_to_print = game.rotate_piece()  # end='\n\n'
        elif command == 'right':
            grid_to_print = game.move_piece_right()  # end='\n\n'
        elif command == 'left':
            grid_to_print = game.move_piece_left()  # end='\n\n'
        elif command == 'down' or command == '':
            grid_to_print = game.go_down()  # end='\n\n'
        elif command == 'break':
            grid_to_print = game.break_()
        elif command == 'exit':
            break
        print(grid_to_print)
        if 'Game Over!' in grid_to_print:
            break
        print()


if __name__ == '__main__':
    main()
