class Point:
    """
    Representa um ponto em um espaço tridimensional.

    Atributos:
        x (float): Coordenada X do ponto.
        y (float): Coordenada Y do ponto.
        z (float): Coordenada Z do ponto.
    """

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def point_sum(self, p2):
        return Point(self.x + p2.x, self.y + p2.y, self.z + p2.z)

    def point_subtraction(self, p2):
        return Point(self.x - p2.x, self.y - p2.y, self.z - p2.z)

    def point_distance(self, p2):
        delx = self.x - p2.x
        dely = self.y - p2.y
        delz = self.z - p2.z
        return (delx ** 2 + dely ** 2 + delz ** 2)**(1/2)

    def point_return_list(self):
        return [self.x, self.y, self.z]
