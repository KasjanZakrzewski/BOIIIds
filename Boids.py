import tkinter as tk
import random as Randy

from Global import *
from Obstacle import Obstacle
from Quad_Points import Quad_Points
from Quad_Obstacles import Quad_Obstacles
from Boid import Boid

show = True
show_percertion = True

def step(boids, quad, quad_obstacles, perception): 
    outside(boids)
    if quad != None:
        del quad
    quad = Quad_Points(0, WIDTH, 0, HEIGHT, 4, show)

    for boid in boids:
        quad.add_point(boid, show)

    for boid in boids:
        boid.update(quad, quad_obstacles)

    if perception != None:
        canvas.delete(perception)

    if show_percertion:
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

def show_off():
    global show
    show = False

def show_on():
    global show
    show = True

def show_p_off():
    global show_percertion
    show_percertion = False

def show_p_on():
    global show_percertion
    show_percertion = True

# root = tk.Tk() 

menu = tk.Menu(root)
quad_menu = tk.Menu(menu, tearoff=0)
quad_menu.add_command(label="show off", command=show_off)
quad_menu.add_command(label="show on", command=show_on)

percertion_menu = tk.Menu(menu, tearoff=0)
percertion_menu.add_command(label="show off", command=show_p_off)
percertion_menu.add_command(label="show on", command=show_p_on)

menu.add_cascade(menu=quad_menu, label="Quad Tree")
menu.add_cascade(menu=percertion_menu, label="Percertion")
root.config(menu=menu)

# canvas = tk.Canvas(root, bg=BACKGROUND, height=HEIGHT, width=WIDTH) 
canvas.pack()

boids = []
for i in range(200):
    boids.append(Boid(Randy.randint(0,WIDTH-1), Randy.randint(0,HEIGHT-1)))

obstacles = []
for i in range(50):
    obstacles.append(Obstacle(Randy.randint(0,WIDTH-1), Randy.randint(0,HEIGHT-1)))

quad_obstacles = Quad_Obstacles(0, WIDTH, 0, HEIGHT, 4)
for obstacle in obstacles:
    quad_obstacles.add_obstacles(obstacle)

step(boids, None, quad_obstacles, None)
root.mainloop()