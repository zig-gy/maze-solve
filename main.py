from classes import Window, Maze

def main():
    window = Window(800, 600)
    
    Maze(150, 40, 10, 10, 50, 50, window, 10)
    
    window.wait_for_close()

if __name__ == "__main__":
    main()