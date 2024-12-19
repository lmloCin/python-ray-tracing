from vector import Vector
from point import Point


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


class Plane:
    def __init__(self, p: Point, nvector, color):
        self.p = p  # Ponto pertencente ao plano
        self.nvector = nvector  # vetor normal ao plano
        self.color = color    # Lista normalizada RGB


