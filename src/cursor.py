class Cursor:
    def __init__(self, x: int = 0, y: int = 0, width: int = 9, height: int = 9):
        self.x = x
        self.y = y
        self.width_max = width
        self.height_max = height

    def get_position(self):
        return self.x, self.y

    def move_up(self):
        if self.y > 0:
            self.y -= 1
        elif self.y == 0:
            pass
        else:
            self.y = 0

    def move_down(self):
        if self.y < self.height_max - 1:
            self.y += 1
        elif self.y == self.height_max - 1:
            pass
        else:
            self.y = self.height_max - 1

    def move_left(self):
        if self.x > 0:
            self.x -= 1
        elif self.x == 0:
            pass
        else:
            self.x = 0

    def move_right(self):
        if self.x < self.width_max - 1:
            self.x += 1
        elif self.x == self.width_max - 1:
            pass
        else:
            self.x = self.width_max - 1
