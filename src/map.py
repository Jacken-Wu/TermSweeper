import random


class Map:
    """
    0~8 for unopened blocks, 9 for mine, 10~18 for opened blocks, 19 for bomb, 20~29 for flag.
    """
    MINE_BLOCK = 9
    BOMB_BLOCK = 19

    WIN = 30
    LOSE = 31
    RUNNING = 32
    NOT_STARTED = 33

    def __init__(self, width: int = 9, height: int = 9, mine_num: int = 10):
        self.width = width
        self.height = height
        self.mine_num = mine_num
        self.grid = [[0 for x in range(width)] for y in range(height)]
        self.game_status = Map.NOT_STARTED
        self.unopened_block_num = self.width * self.height - self.mine_num
        self.flag_num = 0

    def generate_mines(self, y_safe: int = -1, x_safe: int = -1):
        counter = 0
        while counter < self.mine_num:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if x != x_safe and y != y_safe and self.grid[y][x] == 0:
                self.grid[y][x] = Map.MINE_BLOCK
                counter += 1

    def generate_num_blocks(self):
        def count_around(y, x):
            counter = 0
            for i in range(max(0, y - 1), min(self.height, y + 2)):
                for j in range(max(0, x - 1), min(self.width, x + 2)):
                    if self.grid[i][j] == Map.MINE_BLOCK:
                        counter += 1
            return counter
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    self.grid[y][x] = count_around(y, x)

    def open_count(self):
        self.unopened_block_num -= 1
        if self.unopened_block_num <= 0:
            self.game_status = Map.WIN

    def open_single_block(self, y: int, x: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            if 0 <= self.grid[y][x] < 9:
                self.grid[y][x] += 10
                self.open_count()
            elif self.grid[y][x] == Map.MINE_BLOCK:
                self.grid[y][x] = Map.BOMB_BLOCK
                self.game_status = Map.LOSE
    
    def open_block(self, y: int, x: int):
        if self.grid[y][x] == 0:
            for i in range(max(0, y - 1), min(self.height, y + 2)):
                for j in range(max(0, x - 1), min(self.width, x + 2)):
                    self.open_single_block(y, x)
                    self.open_block(i, j)
        else:
            self.open_single_block(y, x)

    def double_click_block(self, y: int, x: int):
        # 双击操作
        if 10 < self.grid[y][x] < 19:
            flag_around = 0
            for i in range(max(0, y - 1), min(self.height, y + 2)):
                for j in range(max(0, x - 1), min(self.width, x + 2)):
                    if 20 <= self.grid[i][j] <= 29:
                        flag_around += 1
            if flag_around == self.grid[y][x] - 10:
                for i in range(max(0, y - 1), min(self.height, y + 2)):
                    for j in range(max(0, x - 1), min(self.width, x + 2)):
                        self.open_block(i, j)

    def flag_block(self, y: int, x: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            if 0 <= self.grid[y][x] <= 9:
                self.grid[y][x] += 20
                self.flag_num += 1
            elif 20 <= self.grid[y][x] <= 29:
                self.grid[y][x] -= 20
                self.flag_num -= 1

    def get_status(self):
        return self.game_status

    def set_status(self, status: int):
        self.game_status = status

    def get_block(self, y: int, x: int):
        return self.grid[y][x]
