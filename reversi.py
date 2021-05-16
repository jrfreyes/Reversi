

class MoveError(Exception):
    pass

class Reversi:
    colors = {'red':1, 'blue':-1}
    def __init__(self, height: int = 8, width: int = 8) -> None:
        self._height = height
        self._width = width
        self.initialize_board()

    def initialize_board(self):
        self._board = [[0]*self._width for i in range(self._height)]

        self._board[self._height//2 - 1][self._width//2 - 1] = Reversi.colors['red']
        self._board[self._height//2 - 1][self._width//2] = Reversi.colors['blue']
        self._board[self._height//2][self._width//2 - 1] = Reversi.colors['blue']
        self._board[self._height//2][self._width//2] = Reversi.colors['red']

        self._turn = 'red'
        
    
    def valid_move(self, x, y, color = None) -> bool:
        if x >= self._width or x < 0:
            raise IndexError('x is out of bounds!')
        if y >= self._height or y < 0:
            raise IndexError('y is out of bounds!')

        if color is None:
            color = self._turn

        if color not in Reversi.colors:
            raise ValueError('Invalid color! The color must be either red or blue.')
        
        if self._board[y][x]:
            return False
        dirs = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                dirs.append(self.valid_direction(x, y, i, j, color))
        
        return any(dirs)

    def valid_direction(self, x, y, dir_x, dir_y, color = None) -> bool:
        '''dir_x left if -1, right if 1
           dir_y up if -1, down if 1'''
        if color is None:
            color = self._turn

        if color not in Reversi.colors:
            raise ValueError('Invalid color! The color must be either red or blue.')
        if dir_x > 1 or dir_x < -1 or\
            dir_y > 1 or dir_y < -1:
            raise ValueError('dir_x and dir_y must be within the range of [-1,1]')
        
        if dir_x == 0 and dir_y == 0:
            return False

        found_opposite_color = False
        found_same_color = False
        color_val = Reversi.colors[color]
        x += dir_x
        y += dir_y

        while x < self._width and x >= 0 and\
            y < self._height and y >= 0:
            
            curr_square = self._board[y][x]
            if curr_square not in (color_val, 0):
                found_opposite_color = True
            else:
                if curr_square == color_val:
                    found_same_color = True
                break
            x += dir_x
            y += dir_y

        
        return found_same_color and found_opposite_color
        
    def has_valid_moves(self, color = None):
        for x in range(self._width):
            for y in range(self._height):
                if self.valid_move(x, y, color):
                    return True
        return False

    def count(self, color):
        if color not in Reversi.colors:
            raise ValueError('Invalid color! The color must be either red or blue.')
        
        return sum(row.count(Reversi.colors[color]) for row in self._board)

    def move(self, x, y, color = None):
        if color is None:
            color = self._turn
        if not self.valid_move(x, y, color):
            raise MoveError('Invalid move!')
        color_value = Reversi.colors[color]
        
        self._board[y][x] = color_value

        for dir_x in range(-1, 2):
            for dir_y in range(-1, 2):
                if self.valid_direction(x, y, dir_x, dir_y, color):
                    curr_x = x + dir_x
                    curr_y = y + dir_y
                    while self._board[curr_y][curr_x] not in (color_value, 0):
                        self._board[curr_y][curr_x] = color_value
                        curr_x += dir_x
                        curr_y += dir_y

        self.next_turn()
        if not self.has_valid_moves():
            self.next_turn()

    def next_turn(self):
        self._turn = 'blue' if self._turn == 'red' else 'red'

    def get_cell_color(self, x, y):
        cell = self._board[y][x]

        if not cell:
            return None
        return 'red' if cell == 1 else 'blue'

    def get_turn_color(self):
        return self._turn

    def all_cells_filled(self):
        return not sum(row.count(0) for row in self._board)

    def __str__(self):
        s = '\n'.join(' '.join(f'{cell: d}' for cell in row) \
                                    for row in self._board) 
        return s

