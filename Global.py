import tkinter as tk

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

global show
show = True

global show_percertion
show_percertion = True

root = tk.Tk() 
canvas = tk.Canvas(root, bg=BACKGROUND, height=HEIGHT, width=WIDTH)