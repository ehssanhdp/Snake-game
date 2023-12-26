from tkinter import *
import random

class SnakeGame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake game")
        self.window.resizable(False, False)

        self.score = 0
        self.direction = 'down'

        self.label = Label(self.window, text="Score:{}".format(self.score), font=('consolas', 40))
        self.label.pack()

        self.canvas = Canvas(self.window, bg="#000000", height=400, width=400)
        self.canvas.pack()

        self.window.update()

        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        x = int((self.screen_width/2) - (self.window_width/2))
        y = int((self.screen_height/2) - (self.window_height/2))

        self.window.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

        self.next_turn()

        self.window.mainloop()

    def next_turn(self):
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= 20
        elif self.direction == "down":
            y += 20
        elif self.direction == "left":
            x -= 20
        elif self.direction == "right":
            x += 20

        self.snake.coordinates.insert(0, (x, y))

        square = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="#00FF00")

        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text="Score:{}".format(self.score))
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(100, self.next_turn)

    def change_direction(self, new_direction):
        if new_direction == 'left':
            if self.direction != 'right':
                self.direction = new_direction
        elif new_direction == 'right':
            if self.direction != 'left':
                self.direction = new_direction
        elif new_direction == 'up':
            if self.direction != 'down':
                self.direction = new_direction
        elif new_direction == 'down':
            if self.direction != 'up':
                self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake.coordinates[0]
        if x < 0 or x >= 400:
            return True
        elif y < 0 or y >= 400:
            return True

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(
            self.canvas.winfo_width()/2,
            self.canvas.winfo_height()/2,
            font=('consolas',40),
            text="GAME OVER",
            fill="red",
            tag="gameover"
        )


class Snake:
    def __init__(self, canvas):
        self.body_size = 2
        self.coordinates = []
        self.squares = []

        for _ in range(self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + 20, y + 20, fill="#00FF00", tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, canvas):
        x = random.randint(0, (400 / 20)-1) * 20
        y = random.randint(0, (400 / 20) - 1) * 20
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + 20, y + 20, fill="#FF0000", tag="food")


SnakeGame()