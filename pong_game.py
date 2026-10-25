import tkinter as tk

class PongGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Pong Game')
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.paddle1 = self.canvas.create_rectangle(50, 250, 100, 300, fill='blue')
        self.paddle2 = self.canvas.create_rectangle(700, 250, 750, 300, fill='red')
        self.ball = self.canvas.create_oval(375, 275, 425, 325, fill='yellow')
        self.canvas.move(self.ball, 10, 10)
        self.canvas.tag_bind(self.paddle1, '<Key>', self.move_paddle1)
        self.canvas.tag_bind(self.paddle2, '<Key>', self.move_paddle2)
        self.root.mainloop()

    def move_paddle1(self, event):
        if event.keysym == 'Left':
            self.canvas.move(self.paddle1, -10, 0)
        elif event.keysym == 'Right':
            self.canvas.move(self.paddle1, 10, 0)

    def move_paddle2(self, event):
        if event.keysym == 'h':
            self.canvas.move(self.paddle2, -10, 0)
        elif event.keysym == 'l':
            self.canvas.move(self.paddle2, 10, 0)

if __name__ == '__main__':
    game = PongGame()