class Vector:
    """
    Representa um vetor em um espaço tridimensional.

    Atributos:
        x (float): Componente do vetor na direção X.
        y (float): Componente do vetor na direção Y.
        z (float): Componente do vetor na direção Z.
    """
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def vector_sum(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def vector_subtraction(self, v2):
        return Vector(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def vector_x_scalar(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def vector_dot_product(self, v2):
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def vector_product(self, v2):
        return Vector((self.y * v2.z) - (self.z * v2.y), (v2.x * self.z) - (self.x * v2.z), (self.x * v2.y) - (self.y * v2.x))

    def vector_return_list(self):
        return [self.x, self.y, self.z]

    def vector_normalize(self):
        v = Vector(0, 0, 0)
        delx = self.x - v.x
        dely = self.y - v.y
        delz = self.z - v.z
        delta = (delx ** 2 + dely ** 2 + delz ** 2)**(1/2)
        return Vector(self.x/delta, self.y/delta, self.z/delta)

