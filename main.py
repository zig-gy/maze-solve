from classes import Window, Line, Point, Cell

def main():
    window = Window(800, 600)
    
    cell = Cell(window, Point(300,300), Point(500, 500))
    cell.has_top_wall = False
    cell.draw()
    
    cell2 = Cell(window, Point(300,100), Point(500, 300))
    cell2.has_bottom_wall = False
    cell2.draw()
    
    cell.draw_move(cell2)
    
    window.wait_for_close()

if __name__ == "__main__":
    main()