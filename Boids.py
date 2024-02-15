import tkinter as tk
import random as Randy

from Global import *
from Obstacle import Obstacle
from Quad_Points import Quad_Points
from Quad_Obstacles import Quad_Obstacles
from Boid import Boid

# Zmienne warunkujące wyświetlanie 
show = True             # Quad Tree
show_percertion = True  # "Zasięgu wzroku" jednego z Boidów

# Funkcja pojedyńczego kroku symulacji
def step(boids, quad, quad_obstacles, perception): 
    # Spr i poprawa pozycji Boidów, które wypadły poza obszar symulacji
    outside(boids)  

    # Tworzenie nowego i usuwnanie istniejącego QuadTree 
    if quad != None:
        del quad
    quad = Quad_Points(0, WIDTH, 0, HEIGHT, 4, show)

    # Dodawanie Boidów do QuadTree
    for boid in boids:
        quad.add_point(boid, show)

    # Aktualizacja pozycji i prędkości Biodów
    for boid in boids:
        boid.update(quad, quad_obstacles)

    # Wyświetlenie "zasięgu wzroku" jednego z Boidów
    if perception != None:
        canvas.delete(perception)

    if show_percertion:
        perception = canvas.create_rectangle(boid.position.x - boid.perception, 
                                boid.position.y - boid.perception, 
                                boid.position.x + boid.perception, 
                                boid.position.y + boid.perception, 
                                outline="#B5A8FF", width=1)

    # Wywołanie następnego kroku symulacji po 15ms
    root.after(15, step, boids, quad, quad_obstacles, perception)

# Funkcja Spr i poprawy pozycji Boidów, które wypadły poza obszar symulacji
def outside(boids):
    # Dla każdego z Boidów spr jest, czy:
    for boid in boids:
        if boid.position.x > WIDTH:     # Wypadł poza prawą krawędź ekranu
            boid.position.x -= WIDTH 

        if boid.position.x < 0:         # Wypadł poza lewą krawędź ekranu
            boid.position.x += WIDTH

        if boid.position.y > HEIGHT:    # Wypadł poza dolną krawędź ekranu
            boid.position.y -= HEIGHT 

        if boid.position.y < 0:         # Wypadł poza górną krawędź ekranu
            boid.position.y += HEIGHT

# Funkcja wyłączająca wyświetlanie QuadTree 
def show_off():
    global show
    show = False

# Funkcja włączająca wyświetlanie QuadTree 
def show_on():
    global show
    show = True

# Funkcja wyłączająca wyświetlanie "zasięgu wzroku" Boida 
def show_p_off():
    global show_percertion
    show_percertion = False

# Funkcja włączająca wyświetlanie "zasięgu wzroku" Boida  
def show_p_on():
    global show_percertion
    show_percertion = True

# Tworzymy menu
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

# Dodanie canvas do okna aplikacji
canvas.pack()

# Generowane są Boidy o losowym położeniu
boids = []
for i in range(200):
    boids.append(Boid(Randy.randint(0,WIDTH-1), Randy.randint(0,HEIGHT-1)))

# Generowane są Przeszkody o losowym położeniu
obstacles = []
for i in range(50):
    obstacles.append(Obstacle(Randy.randint(0,WIDTH-1), Randy.randint(0,HEIGHT-1)))

# Stworzenie QuadTree dla przeszkód, następnie dodanie do niego przeszkód
quad_obstacles = Quad_Obstacles(0, WIDTH, 0, HEIGHT, 4)
for obstacle in obstacles: 
    quad_obstacles.add_obstacles(obstacle)

# Uruchomienie symulacji
step(boids, None, quad_obstacles, None)
root.mainloop()