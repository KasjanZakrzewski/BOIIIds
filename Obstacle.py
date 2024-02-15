from Global import canvas, OBSTACLE_SIZE, OBSTACLE

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.oval = canvas.create_oval(x - OBSTACLE_SIZE, y - OBSTACLE_SIZE, x + OBSTACLE_SIZE, y + OBSTACLE_SIZE, fill=OBSTACLE)