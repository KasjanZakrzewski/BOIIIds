from Global import canvas

class Quad_Points:
    def __init__(self, x1, x2, y1, y2, max, show):
        self.rectangle = None
        self.chidren = []
        self.points = []
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.max = max
        if show:
            self.rectangle = canvas.create_rectangle(x1, y1, x2, y2, outline="#FFFFFF", width=1)
            canvas.lower(self.rectangle)

    def __del__(self):
        if len(self.chidren) != 0:
            for child in self.chidren:
                del child
        if self.rectangle != None:
            canvas.delete(self.rectangle)

    def split(self, show):
        quad = Quad_Points(self.x1, (self.x1+self.x2)/2, self.y1, (self.y1+self.y2)/2, self.max, show)
        self.chidren.append(quad)

        quad = Quad_Points((self.x1+self.x2)/2, self.x2, self.y1, (self.y1+self.y2)/2, self.max, show)
        self.chidren.append(quad)

        quad = Quad_Points(self.x1, (self.x1+self.x2)/2, (self.y1+self.y2)/2, self.y2, self.max, show)
        self.chidren.append(quad)

        quad = Quad_Points((self.x1+self.x2)/2, self.x2, (self.y1+self.y2)/2, self.y2, self.max, show)
        self.chidren.append(quad)

    def add_point(self, point, show):
        if (self.x1 <= point.position.x < self.x2) and (self.y1 <= point.position.y < self.y2):
            if len(self.points) == self.max:
                if len(self.chidren) == 0:
                    self.split(show)
                for child in self.chidren:
                    child.add_point(point, show)
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