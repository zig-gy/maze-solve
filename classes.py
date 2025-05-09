import time
import random

from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("Hola mundo")
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        self.is_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root.update()
        self.root.update_idletasks()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()
        print("Window closed...")

    def close(self):
        self.is_running = False
        
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        
    def draw(self, canvas, fill_color):
        x1 = self.point1.x
        x2 = self.point2.x
        y1 = self.point1.y
        y2 = self.point2.y
        canvas.create_line(x1,y1,x2,y2, fill=fill_color, width=2)

class Cell():
    def __init__(self, win, point1, point2):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._win = win
        if point1.x > point2.x:
            self._x1 = point2.x
            self._x2 = point1.x
        else:
            self._x1 = point1.x
            self._x2 = point2.x
        if point1.y > point2.y:
            self._y1 = point2.y
            self._y2 = point1.y
        else:
            self._y1 = point1.y
            self._y2 = point2.y
    
    def get_center_point(self):
        return Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        
    def draw(self):        
        top_left = Point(self._x1, self._y1)
        top_right = Point(self._x2, self._y1)
        bot_left = Point(self._x1, self._y2)
        bot_right = Point(self._x2, self._y2)
        
        if self.has_bottom_wall:
            wall = Line(bot_left, bot_right)
            self._win.draw_line(wall, "black")
        else:
            wall = Line(bot_left, bot_right)
            self._win.draw_line(wall, "white")
        if self.has_left_wall:
            wall = Line(top_left, bot_left)
            self._win.draw_line(wall, "black")
        else:
            wall = Line(top_left, bot_left)
            self._win.draw_line(wall, "white")
        if self.has_right_wall:
            wall = Line(top_right, bot_right)
            self._win.draw_line(wall, "black")
        else:
            wall = Line(top_right, bot_right)
            self._win.draw_line(wall, "white")
        if self.has_top_wall:
            wall = Line(top_left, top_right)
            self._win.draw_line(wall, "black")
        else:
            wall = Line(top_left, top_right)
            self._win.draw_line(wall, "white")

    def draw_move(self, to_cell, undo=False):
        center_self = self.get_center_point()
        center_to = to_cell.get_center_point()
        color = "gray" if undo else "red"
        
        self._win.draw_line(Line(center_self, center_to), color)

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        current_x = self.x1
        current_y = self.y1
        for col in range(self.num_cols):
            row_cells = []
            for row in range(self.num_rows):
                top_left = Point(current_x, current_y)
                current_x += self.cell_size_x
                bot_right = Point(current_x, current_y + self.cell_size_y)
                row_cells.append(Cell(self.win, top_left, bot_right))
            self._cells.append(row_cells)
            current_y += self.cell_size_y
            current_x = self.x1

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i,j)
    
    def _draw_cell(self, i, j):
        if self.win is None:
            return None
        cell = self._cells[i][j]
        cell.draw()
        self._animate()
    
    def _animate(self):
        if self.win is None:
            return None
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._cells[-1][-1].has_right_wall = False

    def _break_walls_r(self, i, j):
        # print("loop", i, j)
        self._cells[i][j].visited = True
        while True:
            places = []
            if i > 0 and not self._cells[i-1][j].visited:
                places.append((i-1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                places.append((i, j-1))
            if i + 1 < len(self._cells) and not self._cells[i+1][j].visited:
                places.append((i+1, j))
            if j + 1 < len(self._cells[i]) and not self._cells[i][j+1].visited:
                places.append((i, j+1))
            
            if len(places) == 0:
                self._draw_cell(i, j)
                return
        
            direction = random.randrange(len(places))
            next_cell = places[direction]
            
            if next_cell[0] == i + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
            if next_cell[0] == i - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i-1][j].has_bottom_wall = False
            if next_cell[1] == j + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i][j+1].has_left_wall = False
            if next_cell[1] == j - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i][j-1].has_right_wall = False
            self._break_walls_r(next_cell[0], next_cell[1])

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False

    def solve(self):
        i, j = 0, 0
        return self._solve_r(i, j)
        
    def _solve_r(self, i, j):
        print(i, j)
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[-1][-1]:
            return True
        if i > 0 and not self._cells[i][j].has_top_wall and not self._cells[i-1][j].visited:
            current = self._cells[i][j]
            post = self._cells[i-1][j]
            current.draw_move(post)
            if self._solve_r(i-1, j):
                return True
            post.draw_move(current, True)
        if j > 0 and not self._cells[i][j].has_left_wall and not self._cells[i][j-1].visited:
            current = self._cells[i][j]
            post = self._cells[i][j-1]
            current.draw_move(post)
            if self._solve_r(i, j-1):
                return True
            post.draw_move(current, True)
        if i + 1 < len(self._cells) and not self._cells[i][j].has_bottom_wall and not self._cells[i+1][j].visited:
            current = self._cells[i][j]
            post = self._cells[i+1][j]
            current.draw_move(post)
            if self._solve_r(i+1, j):
                return True
            post.draw_move(current, True)
        if j + 1 < len(self._cells[i]) and not self._cells[i][j].has_right_wall and not self._cells[i][j+1].visited:
            current = self._cells[i][j]
            post = self._cells[i][j+1]
            current.draw_move(post)
            if self._solve_r(i, j+1):
                return True
            post.draw_move(current, True)
        return False