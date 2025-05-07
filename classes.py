import time

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
        if self.has_left_wall:
            wall = Line(top_left, bot_left)
            self._win.draw_line(wall, "black")
        if self.has_right_wall:
            wall = Line(top_right, bot_right)
            self._win.draw_line(wall, "black")
        if self.has_top_wall:
            wall = Line(top_left, top_right)
            self._win.draw_line(wall, "black")

    def draw_move(self, to_cell, undo=False):
        center_self = self.get_center_point()
        center_to = to_cell.get_center_point()
        color = "gray" if undo else "red"
        
        self._win.draw_line(Line(center_self, center_to), color)

class Maze():
    _cells = []
    
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
    
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
        cell = self._cells[i][j]
        cell.draw()
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.1)