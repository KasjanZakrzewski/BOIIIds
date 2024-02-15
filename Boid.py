import random as Randy
import math
from Global import *
from Vector import Vector

class Boid:
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