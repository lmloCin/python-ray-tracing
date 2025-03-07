from vector import Vector
from point import Point
from objects import Plane, Sphere, Mesh
import cv2 as cv
import numpy as np
from lightSource import Light



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

    def intersection(self, vetor: Vector, objects, light:Light):
        menor_t = float('inf')  # Infinito positivo para garantir que qualquer t encontrado será menor
        color = [0, 0, 0]  # Cor de fundo padrão (preto)

        for obj in objects:
            if isinstance(obj, Plane):
                plane_inter = obj.inter_plane_line(self.local, vetor)
                if plane_inter[0] and plane_inter[2] >= 0.1:
                    if plane_inter[2] < menor_t:
                        menor_t = plane_inter[2]
                        # Calcula o ponto de interseção na superfície do plano
                        intersect_point = self.local.point_sum(
                            Point(vetor.x * plane_inter[2], vetor.y * plane_inter[2], vetor.z * plane_inter[2])
                        )

                        # Calcula a componente ambiente da iluminação
                        ambiente = [
                            (light.intensity_a * obj.kaCoefficient * obj.color[0]),  # Canal R
                            (light.intensity_a * obj.kaCoefficient * obj.color[1]),  # Canal G
                            (light.intensity_a * obj.kaCoefficient * obj.color[2])   # Canal B
                        ]

                        # Calcula o vetor da luz (L) em relação ao ponto de interseção
                        l = light.position.point_subtraction(intersect_point)
                        l = Vector(l.x, l.y, l.z).vector_normalize()  # Normaliza o vetor da luz

                        # O vetor normal (N) do plano é constante e já está definido no objeto
                        n = obj.nvector  # Vetor normal do plano
                        n = n.vector_normalize()  # Garante que o vetor normal está normalizado

                        # Calcula o produto escalar entre o vetor da luz (L) e o vetor normal (N)
                        n_x_l = l.vector_dot_product(n)

                        # Calcula a componente difusa da iluminação
                        difusa = [
                            (light.intensity_d * obj.kdCoefficient * n_x_l * obj.color[0]),  # Canal R
                            (light.intensity_d * obj.kdCoefficient * n_x_l * obj.color[1]),  # Canal G
                            (light.intensity_d * obj.kdCoefficient * n_x_l * obj.color[2])   # Canal B
                        ]

                        # Calcula o vetor de reflexão (R) usando a fórmula: R = 2 * (N · L) * N - L
                        r = n.vector_x_scalar(2 * n_x_l)
                        r = r.vector_subtraction(l)
                        r = r.vector_normalize()  # Normaliza o vetor de reflexão

                        # Calcula o vetor da câmera (V) em relação ao ponto de interseção
                        v = self.local.point_subtraction(intersect_point)
                        v = Vector(v.x, v.y, v.z).vector_normalize()  # Normaliza o vetor da câmera

                        # Calcula o produto escalar entre o vetor de reflexão (R) e o vetor da câmera (V)
                        r_x_v = r.vector_dot_product(v)

                        # Calcula a componente especular da iluminação
                        especular = [
                            (light.intensity_s * obj.ksCoefficient * ((r_x_v) ** obj.nCoefficient) * obj.color[0]),  # Canal R
                            (light.intensity_s * obj.ksCoefficient * ((r_x_v) ** obj.nCoefficient) * obj.color[1]),  # Canal G
                            (light.intensity_s * obj.ksCoefficient * ((r_x_v) ** obj.nCoefficient) * obj.color[2])   # Canal B
                        ]

                        # Combina as componentes de iluminação (ambiente, difusa e especular) para obter a cor final
                        color = [
                            (ambiente[0] + difusa[0] + especular[0]),  # Canal R
                            (ambiente[1] + difusa[1] + especular[1]),  # Canal G
                            (ambiente[2] + difusa[2] + especular[2])   # Canal B
                        ]

            elif isinstance(obj, Sphere):
                sphere_inter = obj.inter_sphere_line(self.local, vetor)
                if sphere_inter[0] and sphere_inter[2] >= 0.1:
                    if sphere_inter[2] < menor_t:
                        menor_t = sphere_inter[2]
                        # Calcula o ponto de interseção na superfície da esfera
                        intersect_point = self.local.point_sum(Point(vetor.x * sphere_inter[2], vetor.y* sphere_inter[2], vetor.z* sphere_inter[2]))
                        # Calcula a componente ambiente da iluminação
                        ambiente = [(light.intensity_a * obj.kaCoefficient * obj.color[0]), (light.intensity_a * obj.kaCoefficient * obj.color[1]), (light.intensity_a * obj.kaCoefficient * obj.color[2])]
                        # Calcula o vetor da luz (L) em relação ao ponto de interseção
                        l = light.position.point_subtraction(intersect_point)
                        l = Vector(l.x, l.y, l.z).vector_normalize()
                         # Calcula o vetor normal (N) à superfície da esfera no ponto de interseção
                        n = intersect_point.point_subtraction(obj.center)
                        n = Vector(n.x, n.y, n.z).vector_normalize()
                        # Produto vetorial de n e l
                        n_x_l = l.vector_dot_product(n)
                        # Calcula a componente difusa da iluminação
                        difusa = [(light.intensity_d * obj.kdCoefficient * n_x_l * obj.color[0]),(light.intensity_d * obj.kdCoefficient * n_x_l * obj.color[1]), (light.intensity_d * obj.kdCoefficient * n_x_l * obj.color[2]) ]
                        # Calcula o vetor de reflexão (R) usando a fórmula: R = 2 * (N · L) * N - L
                        r = n.vector_x_scalar(2 * n_x_l)
                        r = r.vector_subtraction(l)
                        r = r.vector_normalize()
                         # Calcula o vetor da câmera (V) em relação ao ponto de interseção
                        v = self.local.point_subtraction(intersect_point)
                        v = Vector(v.x, v.y, v.z).vector_normalize()
                        # Produto vetorial de r e v
                        r_x_v = r.vector_dot_product(v)
                        # Calcula a componente especular da iluminação
                        especular = [(light.intensity_s * obj.ksCoefficient * ((r_x_v)**obj.nCoefficient) *obj.color[0]), (light.intensity_s * obj.ksCoefficient * ((r_x_v)**obj.nCoefficient) *obj.color[1]), (light.intensity_s * obj.ksCoefficient * ((r_x_v)**obj.nCoefficient) *obj.color[2])]
                        # Combina as componentes de iluminação (ambiente, difusa e especular) para obter a cor final
                        color = [(ambiente[0] + difusa[0] + especular[0]), (ambiente[1] + difusa[1] + especular[1]), (ambiente[2] + difusa[2] + especular[2])]                  

            elif isinstance(obj, Mesh):
                mesh_inter = obj.inter_mesh_line(self.local, vetor)
                if mesh_inter.intersecao and mesh_inter.t >= 0.01:
                    menor_t = mesh_inter.t

                    # Ponto de interseção na superfície da malha
                    intersect_point = self.local.point_sum(
                        Point(vetor.x * mesh_inter.t, vetor.y * mesh_inter.t, vetor.z * mesh_inter.t)
                    )

                    # Calcula a componente ambiente da iluminação
                    ambiente = [
                        (light.intensity_a * obj.kaCoefficient * mesh_inter.cor_normalizada[0]),  # Canal R
                        (light.intensity_a * obj.kaCoefficient * mesh_inter.cor_normalizada[1]),  # Canal G
                        (light.intensity_a * obj.kaCoefficient * mesh_inter.cor_normalizada[2])   # Canal B
                    ]

                    # Calcula o vetor da luz (L) em relação ao ponto de interseção
                    l = light.position.point_subtraction(intersect_point)
                    l = Vector(l.x, l.y, l.z).vector_normalize()  # Normaliza o vetor da luz

                    # Obtém o vetor normal (N) do triângulo intersectado
                    n = obj.normais_t[mesh_inter.idx_triangulo]  # Vetor normal do triângulo
                    n = n.vector_normalize()  # Garante que o vetor normal está normalizado

                    # Calcula o produto escalar entre o vetor da luz (L) e o vetor normal (N)
                    n_x_l = l.vector_dot_product(n)

                    # Calcula a componente difusa da iluminação
                    difusa = [
                        (light.intensity_d * obj.kdCoefficient * n_x_l * mesh_inter.cor_normalizada[0]),  # Canal R
                        (light.intensity_d * obj.kdCoefficient * n_x_l * mesh_inter.cor_normalizada[1]),  # Canal G
                        (light.intensity_d * obj.kdCoefficient * n_x_l * mesh_inter.cor_normalizada[2])   # Canal B
                    ]

                    # Calcula o vetor de reflexão (R) usando a fórmula: R = 2 * (N · L) * N - L
                    r = n.vector_x_scalar(2 * n_x_l)
                    r = r.vector_subtraction(l)
                    r = r.vector_normalize()  # Normaliza o vetor de reflexão

                    # Calcula o vetor da câmera (V) em relação ao ponto de interseção
                    v = self.local.point_subtraction(intersect_point)
                    v = Vector(v.x, v.y, v.z).vector_normalize()  # Normaliza o vetor da câmera

                    # Calcula o produto escalar entre o vetor de reflexão (R) e o vetor da câmera (V)
                    r_x_v = r.vector_dot_product(v)

                    # Calcula a componente especular da iluminação
                    especular = [
                        (light.intensity_s * obj.ksCoefficient * ((r_x_v) ** obj.nCoefficient) * mesh_inter.cor_normalizada[0]),  # Canal R
                        (light.intensity_s * obj.ksCoefficient * ((r_x_v) ** obj.nCoefficient) * mesh_inter.cor_normalizada[1]),  # Canal G
                        (light.intensity_s * obj.ksCoefficient * ((r_x_v) ** obj.nCoefficient) * mesh_inter.cor_normalizada[2])   # Canal B
                    ]

                    # Combina as componentes de iluminação (ambiente, difusa e especular) para obter a cor final
                    color = [
                        (ambiente[0] + difusa[0] + especular[0]),  # Canal R
                        (ambiente[1] + difusa[1] + especular[1]),  # Canal G
                        (ambiente[2] + difusa[2] + especular[2])   # Canal B
                    ]

        return color

    

    def raycasting(self, objects, light):

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
                    image[j, i] = self.intersection(Vector(vetor_atual[0], vetor_atual[1], vetor_atual[2]), objects, light)
            cv.imshow("Raycasting", image)
            cv.waitKey(0)
            cv.destroyAllWindows('i')
