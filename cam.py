from vector import Vector
from point import Point
from objects import Plane, Sphere
import cv2 as cv
import numpy as np


def normalize_list(list_):  # Pode ser utilizada para normalizar pontos, vetores e listas contendo valores RGB
    p = Point(list_[0], list_[1], list_[2])
    p0 = Point(0, 0, 0)
    delta = p.point_distance(p0)
    return [p.x/delta, p.y/delta, p.z/delta]


class Cam:
    def __init__(self, loc: Point, target: Point, upvector: Vector, dist, high, width):
        self.local = loc
        self.target = target
        self.upvector = upvector
        self.dist = dist
        self.high = high
        self.width = width

        self.vorto1 = self.target.point_subtraction(loc)  # subtraindo dois pontos M-C
        self.vorto1 = Vector(self.vorto1.x, self.vorto1.y, self.vorto1.z)  # transformando em vetor
        self.vorto1 = self.vorto1.vector_normalize()  # normalizando

        self.vorto2 = self.vorto1.vector_product(upvector)  # criando vetor ortonormal
        self.vorto2 = self.vorto2.vector_normalize()  # normalizando

        self.vorto3 = self.vorto1.vector_product(self.vorto2)  # criando vetor ortonormal
        self.vorto3 = self.vorto3.vector_x_scalar(-1)  # invertendo o vetor
        self.vorto3 = self.vorto3.vector_normalize()  # normalizando
        # criado todos os vetores ortonormais

    def intersection(self, vetor, objects):
        # lower_product = 1000000
        color = [0, 0, 0]
        for obj in objects:
            if isinstance(obj, Plane):
                plane_inter = obj.inter_plane_line(self.local, vetor)
                if plane_inter[0]:
                    if plane_inter[2] >= 0.1:
                        color = [100, 100, 0]
                        # lower_product = plane_inter[2]
        return color

    def raycasting(self, objects):

            self.vorto1 = np.array([self.vorto1.x, self.vorto1.y, self.vorto1.z])
            self.vorto2 = np.array([self.vorto2.x, self.vorto2.y, self.vorto2.z])
            self.vorto3 = np.array([self.vorto3.x, self.vorto3.y, self.vorto3.z])
            deltay = (2*0.5/(self.high - 1)*self.vorto2)  # deslocamento vertical
            deltax = (2*0.5/(self.width - 1)*self.vorto3)  # deslocamento horizontal
            center = (self.vorto1 * self.dist)  # centro da tela
            pixel_0_0 = center - (0.5 * self.vorto2) - (0.5 * self.vorto3)
            image = np.zeros((self.width, self.high, 3), dtype=np.uint8)  # Imagem a ser gerada
            for i in range(self.width):
                for j in range(self.high):
                    vetor_atual = pixel_0_0 + deltay*i + deltax*j
                    image[j, i] = self.intersection(Vector(vetor_atual[0], vetor_atual[1], vetor_atual[2]), objects)
            cv.imshow("Raycasting", image)
            cv.waitKey(0)
            cv.destroyAllWindows('i')
