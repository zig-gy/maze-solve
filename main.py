from classes import Window, Line, Point, Cell

def main():
    window = Window(800, 600)
    
    line1 = Line(Point(22,22), Point(44,44))
    line2 = Line(Point(45,30), Point(500,500))
    
    window.draw_line(line1, "black")
    window.draw_line(line2, "red")
    
    cell = Cell(window, Point(300,300), Point(500, 500))
    cell.has_top_wall = False
    cell.draw()
    
    window.wait_for_close()

if __name__ == "__main__":
    main()