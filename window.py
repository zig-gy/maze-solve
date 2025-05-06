from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title = "Hola mundo"
        self.root.height = height
        self.root.width = width
        self.canvas = Canvas(self.root, bg="white")
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

