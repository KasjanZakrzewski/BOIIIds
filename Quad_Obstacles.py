

class Quad_Obstacles:
    def __init__(self, x1, x2, y1, y2, max):
        self.rectangle = None
        self.chidren = []
        self.obstacles = []
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.max = max

    def __del__(self):
        if len(self.chidren) != 0:
            for child in self.chidren:
                del child

    def split(self):
        quad = Quad_Obstacles(self.x1, (self.x1+self.x2)/2, self.y1, (self.y1+self.y2)/2, self.max)
        self.chidren.append(quad)

        quad = Quad_Obstacles((self.x1+self.x2)/2, self.x2, self.y1, (self.y1+self.y2)/2, self.max)
        self.chidren.append(quad)

        quad = Quad_Obstacles(self.x1, (self.x1+self.x2)/2, (self.y1+self.y2)/2, self.y2, self.max)
        self.chidren.append(quad)

        quad = Quad_Obstacles((self.x1+self.x2)/2, self.x2, (self.y1+self.y2)/2, self.y2, self.max)
        self.chidren.append(quad)
    
    def intersect(self, x1, x2, y1, y2):
        return not (self.x2 < x1 or 
                    self.x1 > x2 or 
                    self.y1 > y2 or 
                    self.y2 < y1)
    
    def find_obstacles(self, x1, x2, y1, y2):
        result = [] 
        if self.intersect(x1, x2, y1, y2):
            for point in self.obstacles:
                if (x1 <= point.x < x2) and (y1 <= point.y < y2):
                    result.append(point)

            for child in self.chidren:
                result += child.find_obstacles(x1, x2, y1, y2)      

        return result
    
    def add_obstacles(self, obstacle):
        # spr czy mieści sie
        if (self.x1 <= obstacle.x < self.x2) and (self.y1 <= obstacle.y < self.y2):
            if len(self.obstacles) == self.max:
                if len(self.chidren) == 0:
                    self.split()
                for child in self.chidren:
                    child.add_obstacles(obstacle)
            else:
                self.obstacles.append(obstacle)