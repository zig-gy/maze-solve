from classes import Window, Maze

def main():
    num_rows = 50
    num_cols = 25
    margin = 25
    screen_x = 1500
    screen_y = 1000
    cell_size_x = (screen_x - 2 * margin) / num_rows
    cell_size_y = (screen_y - 2 * margin) / num_cols
    
    window = Window(screen_x, screen_y)
    
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, window)
    maze.solve()
    print("fin")
    window.wait_for_close()

if __name__ == "__main__":
    main()