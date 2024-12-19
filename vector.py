class Vector:
    """
    Representa um vetor em um espaço tridimensional.

    Atributos:
        x (float): Componente do vetor na direção X.
        y (float): Componente do vetor na direção Y.
        z (float): Componente do vetor na direção Z.
    """
    def __init__(self, x: float, y: float, z:float):
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
    # Implemente os métodos de vetores aqui
