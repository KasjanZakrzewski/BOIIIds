import random as Randy
import math

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