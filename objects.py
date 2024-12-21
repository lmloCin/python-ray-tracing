from vector import Vector
from point import Point
from math import sqrt


def normalize_list(list_):  # Pode ser utilizada para normalizar pontos, vetores e listas contendo valores RGB
    p = Point(list_[0], list_[1], list_[2])
    p0 = Point(0, 0, 0)
    delta = p.point_distance(p0)
    return [p.x/delta, p.y/delta, p.z/delta]


class Sphere:
    def __init__(self, center: Point, radius, color):
        self.center = center  # Ponto
        self.radius = radius  # Número real
        self.color = color    # Lista normalizada RGB
    def inter_sphere_line(self, p: Point, vectorD: Vector):
        CP = Vector(p.x - self.center.x, p.y - self.center.y, p.z - self.center.z)

        a = vectorD.vector_dot_product(vectorD)
        b = 2 * vectorD.vector_dot_product(CP)
        c = CP.vector_dot_product(CP) - self.radius ** 2

        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return [False, [0, 0, 0], float('inf')]

        t1 = (-b - sqrt(delta)) / (2 * a)
        t2 = (-b + sqrt(delta)) / (2 * a)

        t = min(t1, t2)
        if t < 0:
            return [False, [0, 0, 0], float('inf')]

        x = p.x + vectorD.x * t
        y = p.y + vectorD.y * t
        z = p.z + vectorD.z * t

        return [True, [x, y, z], t]

class Plane:
    def __init__(self, p: Point, nvector, color):
        self.p = p  # Ponto pertencente ao plano
        self.nvector = nvector  # vetor normal ao plano
        self.color = color    # Lista normalizada RGB

    def inter_plane_line(self, p, vectorD):
        # projeção do vetor diretor no vetor normal
        proj = self.nvector.vector_dot_product(vectorD)
        # verifica se o plano e a reta são paralelos
        if proj == 0:
            return [False, [0, 0, 0], 1000000]
        # calcula o ponto de interseção
        param = (self.nvector.vector_dot_product(self.p) - self.nvector.vector_dot_product(p)) / proj
        x, y, z = p.x + vectorD.x * param, p.y + vectorD.y * param, p.z + vectorD.z * param
        return [True, [x, y, z], param]
