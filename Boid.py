import random as Randy
import math
from Global import *
from Vector import Vector

class Boid:
    def __init__(self, x, y):
        self.perception = PERCEPTION        # "Zasięg wzroku" Boida 
        self.position = Vector(x,y)         # Pozycja startowa Boida
        self.velocity = Vector((Randy.random()-0.5)*2, (Randy.random()-0.5)*2)  # Początkowa prędkośc Boida
        # self.velocity = Vector(0,0)
        self.velocity.magnitude(MAX_SPEED)  # Skalowanie wektora prędkości do maksymalnej

        # Stworzenie graficznej reprezentacji Boida
        self.oval = canvas.create_oval(x - BOIDS_SIZE, y - BOIDS_SIZE, x + BOIDS_SIZE, y + BOIDS_SIZE, fill=BOIDS)
    
    # Metoda aktualizująca pozycje i prędkość Boida
    def update(self,quad, quad_obstacles):
        # Przesunięcie pozycji Boida o wektor prędkości
        self.position.add(self.velocity)

        # Aktualizacja prędkość
        self.steer2(quad, quad_obstacles)

        # Przesunięcie graficznej reprezentacji Boida
        canvas.coords(self.oval, self.position.x - BOIDS_SIZE, self.position.y - BOIDS_SIZE, self.position.x + BOIDS_SIZE, self.position.y + BOIDS_SIZE)

    # Metoda wyliczająca wektor uniknięcia przeszkód w "zasięgu wzroku" Boida
    def evasion(self, quad_obstacles):
        # Wyszukanie przeszkód w "zasięgu wzroku" Boida 
        obstacles = quad_obstacles.find_obstacles(self.position.x - PERCEPTION, 
                                    self.position.x + PERCEPTION, 
                                    self.position.y - PERCEPTION, 
                                    self.position.y + PERCEPTION)
        
        avg = Vector(0,0)   # Uśredniony wektor uniku
        temp = Vector(0,0)  # Wektor pomocniczy

        # Dla każdej Przeszkody wykonywany jest: 
        for obstacle in obstacles:
            # wyliczenie odległości Przeszkody od Boida
            temp.cpy(self.position)
            temp.x -= obstacle.x
            temp.y -= obstacle.y

            m = math.sqrt( math.pow(temp.x,2) + math.pow(temp.y,2) )

            # Przeskalowanie wektora, im bliżej jest przeszkoda tym silniejszy jest wektor 
            if m > 0:
                temp.div(m)
            
            # Dodajemy obliczony wektor do wektora średniej
            avg.add(temp)

        # Jeżeli Przeszkody znajdują się w "zasięgu wzroku" Boida, to wyliczna jest ich średnia
        l = len(obstacles)
        if l > 0:
            avg.div(l)

        return avg

    # Metoda wyliczająca wektor odpychający Boida od krawędzi
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

    # Metoda aktualizująca prędkość Boida
    def steer2(self, quad, quad_obstacles):
        # Wyszukanie Boidów w "zasięgu wzroku" danego Boida
        boids = quad.find_in_square(self.position.x - self.perception, 
                                    self.position.x + self.perception, 
                                    self.position.y - self.perception, 
                                    self.position.y + self.perception)

        avg_vel = Vector(0,0)   # Wektor uśrednionego kieruku ruchu
        avg_pos = Vector(0,0)   # Wektor uśrednionej pozycji Boidów 
        avg_sep = Vector(0,0)   # Wektor uśrednionego ... trzymania sie na dystans???
        temp = Vector(0,0)      # Wektor pomocniczy

        # Dla każdego Boida w "zasięgu wzroku"
        for boid in boids:
            if self == boid:
                continue

            # Wyznaczana jest odległość między rozpatrywanym Boidem 
            # a Boidem dla którego jest przeprowadzana aktualizaca
            temp.cpy(self.position)
            temp.sub(boid.position)
            
            m = math.sqrt( math.pow(temp.x,2) + math.pow(temp.y,2) )

            # Jeżeli rozpatrywany Boid jest bliżej niż dystans Separacji
            # to dodawany jest wektor Separacji
            if m < SEPARATION:
                temp.div(m)
                avg_sep.add(temp)

            # Wyznaczana jest odległość między rozpatrywanym Boidem 
            # a Boidem dla którego jest przeprowadzana aktualizaca
            temp.cpy(boid.position)
            temp.sub(self.position)
            temp.div(m/2)

            # Sumowany jest wektor prędkości
            avg_vel.add(boid.velocity)

            # Sumowany jest wektor ... pozycji Boidów
            avg_pos.add(temp)     

        # Jeżeli znaleziono Boidy w zasięgu wzroku, to wyliczana jest średnia
        l = len(boids) - 1
        if l > 0:
            avg_vel.div(l)
            avg_pos.div(l)
            avg_sep.div(l)

            # Dynamiczne ustawianie "pola widzenia" Boida
            self.perception = self.perception + MAX_IN_VIEW - l
            if self.perception >= PERCEPTION:   # Ograniczanie wartości do maksymalnej
                self.perception = PERCEPTION
        else:
            # Jeżeli nie ma Boidów w zasięgu wzroku, 
            # to "pola widzenia" Boida jest ustawiane na maksymalną 
            self.perception = PERCEPTION

        # Wektor uśrednionego kieruku ruchu jest skalowany i dodawany do prędkości
        avg_vel.magnitude(0.02)
        self.velocity.add(avg_vel)

        # Wektor uśrednionej pozycji Boidów jest skalowany i dodawany do prędkości
        avg_pos.magnitude(0.01)
        self.velocity.add(avg_pos)

        # Wektor separacji Boidów jest skalowany i dodawany do prędkości
        avg_sep.magnitude(0.07)
        self.velocity.add(avg_sep)

        # Wektor uniknięcia przeszkody jest skalowany i dodawany do prędkości
        avg_eve = self.evasion(quad_obstacles)
        avg_eve.magnitude(0.08)
        self.velocity.add(avg_eve)

        # Wektor uniknięcia krawędzi ekranu jest skalowany i dodawany do prędkości
        bound = self.boudry()
        bound.magnitude(0.007)
        self.velocity.add(bound)

        # Wektor prędkości jest ograniczany do limitu
        self.velocity.limit(MAX_SPEED)