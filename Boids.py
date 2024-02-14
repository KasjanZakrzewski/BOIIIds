import tkinter as tk
import random as Randy
import math

# Colors 
BACKGROUND = "#000000"
BOIDS = "#A8FFED"
OBSTACLE = "#FF0000"

# Paramiters
WIDTH = 1600
HEIGHT = 800
BOIDS_SIZE = 5
OBSTACLE_SIZE = 10

BOUND = 25
MAX_IN_VIEW = 7
MAX_SPEED = 2
PERCEPTION = 50
SEPARATION = PERCEPTION/2

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.oval = canvas.create_oval(x - OBSTACLE_SIZE, y - OBSTACLE_SIZE, x + OBSTACLE_SIZE, y + OBSTACLE_SIZE, fill=OBSTACLE)

class Quad:
    def __init__(self, x1, x2, y1, y2, max):
        self.chidren = []
        self.points = []
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.max = max

        self.rectangle = canvas.create_rectangle(x1, y1, x2, y2, outline="#FFFFFF", width=1)
        canvas.lower(self.rectangle)

    def __del__(self):
        if len(self.chidren) != 0:
            for child in self.chidren:
                del child
        canvas.delete(self.rectangle)


    def split(self):
        quad = Quad(self.x1, (self.x1+self.x2)/2, self.y1, (self.y1+self.y2)/2, self.max)
        self.chidren.append(quad)

        quad = Quad((self.x1+self.x2)/2, self.x2, self.y1, (self.y1+self.y2)/2, self.max)
        self.chidren.append(quad)

        quad = Quad(self.x1, (self.x1+self.x2)/2, (self.y1+self.y2)/2, self.y2, self.max)
        self.chidren.append(quad)

        quad = Quad((self.x1+self.x2)/2, self.x2, (self.y1+self.y2)/2, self.y2, self.max)
        self.chidren.append(quad)

    def add_point(self, point):
        # spr czy mieści sie
        if (self.x1 <= point.position.x < self.x2) and (self.y1 <= point.position.y < self.y2):
            if len(self.points) == self.max:
                if len(self.chidren) == 0:
                    self.split()
                for child in self.chidren:
                    child.add_point(point)
            else:
                self.points.append(point)
    
    def intersect(self, x1, x2, y1, y2):
        return not (self.x2 < x1 or 
                    self.x1 > x2 or 
                    self.y1 > y2 or 
                    self.y2 < y1)

    def find_in_square(self, x1, x2, y1, y2):
        result = [] 
        if self.intersect(x1, x2, y1, y2):
            for point in self.points:
                if (x1 <= point.position.x < x2) and (y1 <= point.position.y < y2):
                    result.append(point)

            for child in self.chidren:
                result += child.find_in_square(x1, x2, y1, y2)      

        return result
    
    def find_obstacles(self, x1, x2, y1, y2):
        result = [] 
        if self.intersect(x1, x2, y1, y2):
            for point in self.points:
                if (x1 <= point.x < x2) and (y1 <= point.y < y2):
                    result.append(point)

            for child in self.chidren:
                result += child.find_obstacles(x1, x2, y1, y2)      

        return result
    
    def add_obstacles(self, obstacle):
        # spr czy mieści sie
        if (self.x1 <= obstacle.x < self.x2) and (self.y1 <= obstacle.y < self.y2):
            if len(self.points) == self.max:
                if len(self.chidren) == 0:
                    self.split()
                for child in self.chidren:
                    child.add_obstacles(obstacle)
            else:
                self.points.append(obstacle)
    

class Vector:
    def __init__(self, x=None, y=None):
        if x is None and y is None:
            self.x = (Randy.random()-0.5)
            self.y = (Randy.random()-0.5)
        else:
            self.x = x
            self.y = y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def cpy(self, vector):
        self.x = vector.x
        self.y = vector.y

    def div(self, div):
        self.x = self.x/div
        self.y = self.y/div

    def normalize(self):
        m = math.sqrt(math.pow(self.x,2) + math.pow(self.y,2) )
        if m != 0:
            self.x = self.x/m
            self.y = self.y/m

    def magnitude(self, f):
        self.x = self.x * f
        self.y = self.y * f

    def limit(self, f):
        m = math.sqrt(math.pow(self.x,2) + math.pow(self.y,2) )
        if m > f:
            self.x = self.x * f/m
            self.y = self.y * f/m

class BOId:
    def __init__(self, x, y):
        self.perception = PERCEPTION
        self.position = Vector(x,y)
        self.velocity = Vector((Randy.random()-0.5)*2, (Randy.random()-0.5)*2)
        # self.velocity = Vector(0,0)
        self.velocity.magnitude(MAX_SPEED)
        # self.acceleration = Vector()
        self.oval = canvas.create_oval(x - BOIDS_SIZE, y - BOIDS_SIZE, x + BOIDS_SIZE, y + BOIDS_SIZE, fill=BOIDS)
    
    def update(self,quad, quad_obstacles):
        self.position.add(self.velocity)
        self.steer2(quad, quad_obstacles)

        canvas.coords(self.oval, self.position.x - BOIDS_SIZE, self.position.y - BOIDS_SIZE, self.position.x + BOIDS_SIZE, self.position.y + BOIDS_SIZE)

    def evasion(self, quad_obstacles):
        obstacles = quad_obstacles.find_obstacles(self.position.x - PERCEPTION, 
                                    self.position.x + PERCEPTION, 
                                    self.position.y - PERCEPTION, 
                                    self.position.y + PERCEPTION)
        avg = Vector(0,0)
        temp = Vector(0,0)

        for obstacle in obstacles:
            temp.cpy(self.position)
            temp.x -= obstacle.x
            temp.y -= obstacle.y

            m = math.sqrt( math.pow(temp.x,2) + math.pow(temp.y,2) )

            if m > 0:
                temp.div(m)
            
            avg.add(temp)

        l = len(obstacles)
        if l > 0:
            avg.div(l)

        # self.velocity.add(avg)
        return avg

    def boudry(self):
        x = 0
        y = 0
        if self.position.x > WIDTH - BOUND:
            x = self.position.x - WIDTH

        if self.position.x < BOUND:
            x = self.position.x

        if self.position.y > HEIGHT - BOUND:
            y = self.position.y - HEIGHT

        if self.position.y < BOUND:
            y = self.position.y
        
        return Vector(x,y)

    def steer2(self, quad, quad_obstacles):
        boids = quad.find_in_square(self.position.x - self.perception, 
                                    self.position.x + self.perception, 
                                    self.position.y - self.perception, 
                                    self.position.y + self.perception)

        avg_vel = Vector(0,0)
        avg_pos = Vector(0,0)
        avg_sep = Vector(0,0)
        temp = Vector(0,0)

        for boid in boids:
            if self == boid:
                continue

            temp.cpy(self.position)
            temp.sub(boid.position)
            
            m = math.sqrt( math.pow(temp.x,2) + math.pow(temp.y,2) )

            if m < SEPARATION:
                temp.div(m)
                avg_sep.add(temp)

            temp.cpy(boid.position)
            temp.sub(self.position)
            temp.div(m/2)

            avg_vel.add(boid.velocity)
            avg_pos.add(temp)     

        l = len(boids) - 1
        if l > 0:
            avg_vel.div(l)
            avg_pos.div(l)
            avg_sep.div(l)

            self.perception = self.perception + MAX_IN_VIEW - l
            if self.perception >= PERCEPTION:
                self.perception = PERCEPTION
        else:
            self.perception = PERCEPTION

        avg_vel.magnitude(0.02)
        self.velocity.add(avg_vel)

        avg_pos.magnitude(0.01)
        self.velocity.add(avg_pos)

        avg_sep.magnitude(0.07)
        self.velocity.add(avg_sep)

        avg_eve = self.evasion(quad_obstacles)
        avg_eve.magnitude(0.08)
        self.velocity.add(avg_eve)

        bound = self.boudry()
        bound.magnitude(0.007)
        self.velocity.add(bound)

        self.velocity.limit(MAX_SPEED)

def step(boids, quad, quad_obstacles, perception): 
    outside(boids)
    if quad != None:
        del quad
    quad = Quad(0, WIDTH, 0, HEIGHT, 4)

    for boid in boids:
        quad.add_point(boid)

    for boid in boids:
        boid.update(quad, quad_obstacles)

    if perception != None:
        canvas.delete(perception)

    perception = canvas.create_rectangle(boid.position.x - boid.perception, 
                            boid.position.y - boid.perception, 
                            boid.position.x + boid.perception, 
                            boid.position.y + boid.perception, 
                            outline="#B5A8FF", width=1)

    root.after(15, step, boids, quad, quad_obstacles, perception)

def outside(boids):
    for boid in boids:
        if boid.position.x > WIDTH:
            boid.position.x -= WIDTH 

        if boid.position.x < 0:
            boid.position.x += WIDTH

        if boid.position.y > HEIGHT:
            boid.position.y -= HEIGHT 

        if boid.position.y < 0:
            boid.position.y += HEIGHT

root = tk.Tk() 
canvas = tk.Canvas(root, bg=BACKGROUND, height=HEIGHT, width=WIDTH) 
canvas.pack()

boids = []
for i in range(200):
    boids.append(BOId(Randy.randint(0,WIDTH-1), Randy.randint(0,HEIGHT-1)))

obstacles = []
for i in range(50):
    obstacles.append(Obstacle(Randy.randint(0,WIDTH-1), Randy.randint(0,HEIGHT-1)))

quad_obstacles = Quad(0, WIDTH, 0, HEIGHT, 4)
for obstacle in obstacles:
    quad_obstacles.add_obstacles(obstacle)

step(boids, None, quad_obstacles, None)
root.mainloop()