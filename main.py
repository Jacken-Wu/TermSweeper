import curses
import time
from src.cursor import Cursor
from src.map import Map


class Mode:
    EASY = 40
    NORMAL = 41
    HARD = 42
    QUIT = 43


mode_info = {
    Mode.EASY: {
        "height": 9,
        "width": 9,
        "mines": 10
    },
    Mode.NORMAL: {
        "height": 16,
        "width": 16,
        "mines": 40
    },
    Mode.HARD: {
        "height": 16,
        "width": 30,
        "mines": 99
    }
}


def start_window(stdscr):
    stdscr.clear()
    height_max, width_max = stdscr.getmaxyx()
    y = (height_max - 9) // 2
    x = (width_max - 30) // 2
    stdscr.addstr(y, x, "TermSweeper".center(30))
    stdscr.addstr(y + 1, x, "┌" + "─" * 28 + "┐")
    stdscr.addstr(y + 2, x, "|" + "easy".center(28) + "|")
    stdscr.addstr(y + 3, x, "|" + "normal".center(28) + "|")
    stdscr.addstr(y + 4, x, "|" + "hard".center(28) + "|")
    stdscr.addstr(y + 5, x, "|" + "quit".center(28) + "|")
    stdscr.addstr(y + 6, x, "└" + "─" * 28 + "┘")
    stdscr.addstr(y + 7, x, "↑↓←→ to move".center(30))
    stdscr.addstr(y + 8, x, "z to open, x to flag".center(30))
    stdscr.addstr(y + 8, x, "q to quit".center(30))
    stdscr.refresh()
    mouse_index = 0
    while True:
        stdscr.addstr(y + 2, x + 1, " ")
        stdscr.addstr(y + 3, x + 1, " ")
        stdscr.addstr(y + 4, x + 1, " ")
        stdscr.addstr(y + 5, x + 1, " ")
        stdscr.addstr(y + 2 + mouse_index, x + 1, "*")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('q'):
            return Mode.QUIT
        elif key == curses.KEY_UP:
            mouse_index = max(mouse_index - 1, 0)
        elif key == curses.KEY_DOWN:
            mouse_index = min(mouse_index + 1, 3)
        elif key in [10, 13, 32, ord('z')]:
            if mouse_index == 0:
                return Mode.EASY
            elif mouse_index == 1:
                return Mode.NORMAL
            elif mouse_index == 2:
                return Mode.HARD
            elif mouse_index == 3:
                return Mode.QUIT


def game_window(stdscr, height: int = 9, width: int = 9, mine_num: int = 10):
    def update_window(stdscr, final_time: float, position_x: int, position_y: int):
        stdscr.addstr(y, x, str(int(current_time - start_time)).rjust(width * 2 + 2))
        stdscr.addstr(y, x, str(game_map.mine_num - game_map.flag_num))
        for i in range(height):
            for j in range(width):
                if 0 <= game_map.get_block(i, j) <= 9:
                    stdscr.addstr(y + 2 + i, x + 1 + (j * 2), unopened_block)
                elif 20 <= game_map.get_block(i, j) <= 29:
                    stdscr.addstr(y + 2 + i, x + 1 + (j * 2), flag_block)
                elif game_map.get_block(i, j) == Map.BOMB_BLOCK:
                    stdscr.addstr(y + 2 + i, x + 1 + (j * 2), bomb_block)
                elif game_map.get_block(i, j) == 10:
                    stdscr.addstr(y + 2 + i, x + 1 + (j * 2), opened_block)
                elif 10 < game_map.get_block(i, j) < 19:
                    stdscr.addstr(y + 2 + i, x + 1 + (j * 2), f" {game_map.get_block(i, j) - 10}")
        stdscr.addstr(y + 2 + position_y, x + 1 + (position_x * 2), "→")
        stdscr.refresh()

    stdscr.clear()
    height_max, width_max = stdscr.getmaxyx()
    y = (height_max - height - 4) // 2
    x = (width_max - (width * 2) - 3) // 2
    cursor = Cursor(0, 0, width, height)
    game_map = Map(width, height, mine_num)
    unopened_block = " □"
    opened_block = "  "
    flag_block = " ■"
    bomb_block = " ☢"

    start_time = time.time()
    current_time = start_time

    stdscr.addstr(y, x, str(int(current_time - start_time)).rjust(width * 2 + 2))
    stdscr.addstr(y, x, str(game_map.mine_num - game_map.flag_num))
    stdscr.addstr(y + 1, x, "┌" + "─" * (width * 2) + "┐")
    for i in range(height):
        stdscr.addstr(y + 2 + i, x, "│" + unopened_block * width + "│")
    stdscr.addstr(y + 2 + height, x, "└" + "─" * (width * 2) + "┘")
    stdscr.addstr(y + 3 + height, x, "↑↓←→, z, x, q".center(width * 2 + 2))
    stdscr.refresh()

    while True:
        if game_map.get_status() == Map.RUNNING:
            current_time = time.time()
        position_x, position_y = cursor.get_position()
        update_window(stdscr, current_time - start_time, position_x, position_y)

        key = stdscr.getch()
        if key == curses.KEY_UP:
            cursor.move_up()
        elif key == curses.KEY_DOWN:
            cursor.move_down()
        elif key == curses.KEY_LEFT:
            cursor.move_left()
        elif key == curses.KEY_RIGHT:
            cursor.move_right()
        elif key == ord('z'):
            if game_map.get_status() == Map.NOT_STARTED:
                game_map.set_status(Map.RUNNING)
                game_map.generate_mines(position_y, position_x)
                game_map.generate_num_blocks()
                game_map.open_block(position_y, position_x)
                start_time = time.time()
            elif game_map.get_status() == Map.RUNNING:
                if 0 <= game_map.get_block(position_y, position_x) <= 9:
                    game_map.open_block(position_y, position_x)
                elif 10 <= game_map.get_block(position_y, position_x) < 19:
                    game_map.double_click_block(position_y, position_x)
        elif key == ord('x'):
            if game_map.get_status() == Map.NOT_STARTED:
                game_map.set_status(Map.RUNNING)
                game_map.generate_mines(position_y, position_x)
                game_map.generate_num_blocks()
                game_map.open_block(position_y, position_x)
                start_time = time.time()
            elif game_map.get_status() == Map.RUNNING:
                game_map.flag_block(position_y, position_x)
        elif key == ord('q'):
            return None

        # 游戏状态判断
        if game_map.get_status() == Map.WIN:
            end_time = time.time()
            update_window(stdscr, current_time - start_time, position_x, position_y)
            end_window(stdscr, end_time - start_time, True)
            return None
        elif game_map.get_status() == Map.LOSE:
            end_time = time.time()
            update_window(stdscr, current_time - start_time, position_x, position_y)
            end_window(stdscr, end_time - start_time, False)
            return None


def end_window(stdscr, final_time: float, is_win: bool = True):
    height_max, width_max = stdscr.getmaxyx()
    y = (height_max - 6) // 2
    x = (width_max - 30) // 2

    stdscr.addstr(y, x, "┌" + "─" * 28 + "┐")
    stdscr.addstr(y + 1, x, "│" + " " * 28 + "│")
    if is_win:
        stdscr.addstr(y + 2, x, "│" + "You win!".center(28) + "│")
    else:
        stdscr.addstr(y + 2, x, "│" + "You are bombed!".center(28) + "│")
    stdscr.addstr(y + 3, x, "│" + "Time: {:.2f}s".format(final_time).center(28) + "│")
    stdscr.addstr(y + 4, x, "│" + " " * 28 + "│")
    stdscr.addstr(y + 5, x, "└" + "─" * 28 + "┘")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key != -1:
            return None


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)  # 非阻塞模式
    curses.curs_set(0)  # 隐藏光标

    mode = start_window(stdscr)
    if mode == Mode.QUIT:
        return None

    height = mode_info[mode]['height']
    width = mode_info[mode]['width']
    mine_num = mode_info[mode]['mines']
    game_window(stdscr, height, width, mine_num)

curses.wrapper(main)
