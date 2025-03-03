from vector import Vector
from point import Point
from math import sqrt
import numpy as np


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
        CP = Vector(p.x - self.center.x, p.y - self.center.y, p.z - self.center.z) # vetor do ponto inicial da reta até o centro da esfera

        #coeficientes da equação quadrática
        a = vectorD.vector_dot_product(vectorD) #produto escalar
        b = 2 * vectorD.vector_dot_product(CP)
        c = CP.vector_dot_product(CP) - self.radius ** 2

        delta = b ** 2 - 4 * a * c

        if delta < 0: #não existe interseção com a reta
            return [False, [0, 0, 0], float('inf')]

        t1 = (-b - sqrt(delta)) / (2 * a)
        t2 = (-b + sqrt(delta)) / (2 * a)

        if t1 > 0:  # Ponto mais próximo
            t = t1
        elif t2 > 0:  # Caso o raio saia de dentro da esfera
            t = t2
        else:
            return [False, [0, 0, 0], float('inf')]  # Ambos os pontos estão no lado oposto do raio
        #calcula o ponto de interseção
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
            return [False, [0, 0, 0], float('inf')]
        # calcula o ponto de interseção
        param = (self.nvector.vector_dot_product(self.p) - self.nvector.vector_dot_product(p)) / proj
        x, y, z = p.x + vectorD.x * param, p.y + vectorD.y * param, p.z + vectorD.z * param
        return [True, [x, y, z], param]

class Mesh:
    def __init__(self, n_triangulos, n_vertices, lista_vertices, triplas, lista_normais, lista_normais_vertices, lista_cores_normalizadas):
        self.n_triangulos = n_triangulos
        self.n_vertices = n_vertices
        self.tipo = "Malha"
        self.lista_vertices = lista_vertices
        self.triangulos = triplas # Organizadas por índice
        self.normais_t = lista_normais
        self.normais_v = lista_normais_vertices
        self.lista_cores_normalizadas = lista_cores_normalizadas

    def inter_mesh_line(self, P, vdiretor):
        menor_t = self.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.lista_cores_normalizadas[0])
        for idx_triangulo in range(self.n_triangulos):
            intersecao = self.intersecao_triangulo_reta(vdiretor, P, idx_triangulo)
            if intersecao.intersecao and intersecao.t <= menor_t.t:
                menor_t = intersecao
        return menor_t

    class Intersecao_Return:
        def __init__(self, intersecao, t, ponto_intersecao, cor_normalizada):
            self.intersecao = intersecao
            self.t = t
            self.ponto_intersecao = ponto_intersecao
            self.cor_normalizada = cor_normalizada
    def calculo_ponto_intersecao(self, vdiretor: Vector, P: Vector, vetor_normal: Vector, ponto_plano: Vector):
        temp = vetor_normal.vector_dot_product(vdiretor)
        if temp == 0:
            return Mesh.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.lista_cores_normalizadas[0])
        
        t = (vetor_normal.vector_dot_product(ponto_plano) - vetor_normal.vector_dot_product(P)) / temp
        x = P.x + vdiretor.x * t
        y = P.y + vdiretor.y * t
        z = P.z + vdiretor.z * t
        
        return Mesh.Intersecao_Return(True, t, Vector(x, y, z), self.lista_cores_normalizadas[0])

    def intersecao_triangulo_reta(self, vdiretor: Vector, P: Vector, idx_triangulo):
        tripla_triangulo = self.triangulos[idx_triangulo]
        normal_triangulo = self.normais_t[idx_triangulo]
        cor_normalizada = self.lista_cores_normalizadas[idx_triangulo]

        temp = normal_triangulo.vector_dot_product(vdiretor)
        if temp == 0:
            return Mesh.Intersecao_Return(False, 1000000, Vector(0, 0, 0), cor_normalizada)

        p1 = self.lista_vertices[tripla_triangulo[0]]
        p2 = self.lista_vertices[tripla_triangulo[1]]
        p3 = self.lista_vertices[tripla_triangulo[2]]

        intersecao_plano = self.calculo_ponto_intersecao(vdiretor, P, normal_triangulo, p1)

        if intersecao_plano.intersecao:
            ponto_intersecao = intersecao_plano.ponto_intersecao
            v0 = p2.vector_subtraction(p1)
            v1 = p3.vector_subtraction(p1)
            v2 = ponto_intersecao.vector_subtraction(p1)

            d00 = v0.vector_dot_product(v0)
            d01 = v0.vector_dot_product(v1)
            d11 = v1.vector_dot_product(v1)
            d20 = v2.vector_dot_product(v0)
            d21 = v2.vector_dot_product(v1)

            denom = d00 * d11 - d01 * d01

            v = (d11 * d20 - d01 * d21) / denom
            w = (d00 * d21 - d01 * d20) / denom
            u = 1.0 - v - w

            if v >= 0 and w >= 0 and u >= 0:
                return Mesh.Intersecao_Return(True, intersecao_plano.t, ponto_intersecao, cor_normalizada)

        return Mesh.Intersecao_Return(False, 1000000, Vector(0, 0, 0), cor_normalizada)