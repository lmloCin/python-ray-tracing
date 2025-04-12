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
    def __init__(self, center: Point, radius, color, kdCoefficient, ksCoefficient, kaCoefficient, krCoefficient, ktCoefficient, irCoefficient, nCoefficient):
        self.center = center  # Ponto
        self.radius = radius  # Número real
        self.color = color    # Lista normalizada RGB
        self.kdCoefficient = kdCoefficient # Coeficient difuso
        self.ksCoefficient = ksCoefficient # Coeficiente especular
        self.kaCoefficient = kaCoefficient # Coeficiente Ambiental
        self.krCoefficient = krCoefficient # Coeficiente de reflexão
        self.ktCoefficient = ktCoefficient # Coeficiente de refração
        self.IOR = irCoefficient # Indíce de refração
        self.nCoefficient = nCoefficient # Coeficiente de Rugosidade
        
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
    def __init__(self, p: Point, nvector, color, kdCoefficient, ksCoefficient, kaCoefficient, krCoefficient, ktCoefficient, irCoefficient, nCoefficient):
        self.p = p  # Ponto pertencente ao plano
        self.nvector = nvector  # vetor normal ao plano
        self.color = color    # Lista normalizada RGB
        self.kdCoefficient = kdCoefficient # Coeficient difuso
        self.ksCoefficient = ksCoefficient # Coeficiente especular
        self.kaCoefficient = kaCoefficient # Coeficiente Ambiental
        self.krCoefficient = krCoefficient # Coeficiente de reflexão
        self.ktCoefficient = ktCoefficient # Coeficiente de refração
        self.IOR = irCoefficient # Indíce de refração
        self.nCoefficient = nCoefficient # Coeficiente de Rugosidade

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
    def __init__(self, n_triangulos, n_vertices, lista_vertices, triplas, lista_normais, lista_normais_vertices, lista_cores_normalizadas, kdCoefficient, ksCoefficient, kaCoefficient, krCoefficient, ktCoefficient, irCoefficient, nCoefficient):
        self.n_triangulos = n_triangulos
        self.n_vertices = n_vertices
        self.lista_vertices = lista_vertices
        self.triangulos = triplas # Organizadas por índice
        self.normais_t = lista_normais
        self.normais_v = lista_normais_vertices
        self.lista_cores_normalizadas = lista_cores_normalizadas
        self.kdCoefficient = kdCoefficient # Coeficient difuso
        self.ksCoefficient = ksCoefficient # Coeficiente especular
        self.kaCoefficient = kaCoefficient # Coeficiente Ambiental
        self.krCoefficient = krCoefficient # Coeficiente de reflexão
        self.ktCoefficient = ktCoefficient # Coeficiente de refração
        self.IOR = irCoefficient # Indíce de refração
        self.nCoefficient = nCoefficient # Coeficiente de Rugosidade

    def inter_mesh_line(self, P, vdiretor):
        menor_t = self.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.lista_cores_normalizadas[0], idx_triangulo = 0)
        for idx_triangulo in range(self.n_triangulos):
            intersecao = self.intersecao_triangulo_reta(vdiretor, P, idx_triangulo)
            if intersecao.intersecao and intersecao.t <= menor_t.t:
                menor_t = intersecao
        return menor_t

    class Intersecao_Return:
        def __init__(self, intersecao, t, ponto_intersecao, cor_normalizada, idx_triangulo):
            self.intersecao = intersecao
            self.t = t
            self.ponto_intersecao = ponto_intersecao
            self.cor_normalizada = cor_normalizada
            self.idx_triangulo = idx_triangulo
    def calculo_ponto_intersecao(self, vdiretor: Vector, P: Vector, vetor_normal: Vector, ponto_plano: Vector, idx_triangulo):
        temp = vetor_normal.vector_dot_product(vdiretor)
        if temp == 0:
            return Mesh.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.lista_cores_normalizadas[0], idx_triangulo = 0 )
        
        t = (vetor_normal.vector_dot_product(ponto_plano) - vetor_normal.vector_dot_product(P)) / temp
        x = P.x + vdiretor.x * t
        y = P.y + vdiretor.y * t
        z = P.z + vdiretor.z * t
        
        return Mesh.Intersecao_Return(True, t, Vector(x, y, z), self.lista_cores_normalizadas[0], idx_triangulo)

    def intersecao_triangulo_reta(self, vdiretor: Vector, P: Vector, idx_triangulo):
        tripla_triangulo = self.triangulos[idx_triangulo]
        normal_triangulo = self.normais_t[idx_triangulo]
        cor_normalizada = self.lista_cores_normalizadas[idx_triangulo]

        #Chechando interseção com o plano em que o triangulo está
        temp = normal_triangulo.vector_dot_product(vdiretor) #produto vetorial entre normal do triangulo e vdiretor
        if temp == 0: #são paralelos?
            return Mesh.Intersecao_Return(False, 1000000, Vector(0, 0, 0), cor_normalizada, idx_triangulo = 0)

        #vértices do triangulo
        p1 = self.lista_vertices[tripla_triangulo[0]]
        p2 = self.lista_vertices[tripla_triangulo[1]]
        p3 = self.lista_vertices[tripla_triangulo[2]]

        #Identificando interseção c o triangulo
        intersecao_plano = self.calculo_ponto_intersecao(vdiretor, P, normal_triangulo, p1, idx_triangulo)

        if intersecao_plano.intersecao:
            ponto_intersecao = intersecao_plano.ponto_intersecao
            #vetores do triangulo
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
                return Mesh.Intersecao_Return(True, intersecao_plano.t, ponto_intersecao, cor_normalizada, idx_triangulo)

        return Mesh.Intersecao_Return(False, 1000000, Vector(0, 0, 0), cor_normalizada, idx_triangulo = 0)

class Paraboloid:
    def __init__(self, vertex: Point, p_parameter, color, kdCoefficient, ksCoefficient, kaCoefficient, krCoefficient, ktCoefficient, irCoefficient, nCoefficient):
        self.vertex = vertex            # Vértice do paraboloide (ponto de referência para a forma)
        self.p_parameter = p_parameter  # Parâmetro que controla a abertura do paraboloide
        self.color = color
        self.kdCoefficient = kdCoefficient
        self.ksCoefficient = ksCoefficient
        self.kaCoefficient = kaCoefficient
        self.krCoefficient = krCoefficient
        self.ktCoefficient = ktCoefficient
        self.IOR = irCoefficient
        self.nCoefficient = nCoefficient

    def inter_paraboloid_line(self, ray_origin: Point, ray_direction: Vector):
        """
        Calcula a interseção entre uma reta e o paraboloide definido pela equação implícita:
        
            (x - v_x)^2 + (y - v_y)^2 - 4*p*(z - v_z) = 0
        
        onde v = (v_x, v_y, v_z) é o vértice do paraboloide e p é o parâmetro de abertura.
        A reta é definida por: ray_origin + t * ray_direction.
        """
        # Calcula as diferenças entre o ponto de origem da reta e o vértice do paraboloide.
        dx0 = ray_origin.x - self.vertex.x
        dy0 = ray_origin.y - self.vertex.y
        dz0 = ray_origin.z - self.vertex.z
        
        # Componentes do vetor direção da reta.
        Dx = ray_direction.x
        Dy = ray_direction.y
        Dz = ray_direction.z
        
        # Parâmetro que controla a abertura do paraboloide.
        p = self.p_parameter

        # Monta os coeficientes da equação quadrática A*t^2 + B*t + C = 0
        # Originada da substituição da reta na equação implícita do paraboloide
        A = Dx**2 + Dy**2
        B = 2*(dx0 * Dx + dy0 * Dy) - 4*p*Dz
        C = dx0**2 + dy0**2 - 4*p*dz0

        # Se A for muito pequeno, trata-se de um caso degenerado (reta quase paralela à base do paraboloide)
        if abs(A) < 1e-6:
            if abs(B) < 1e-6:
                return [False, [0, 0, 0], float('inf')]
            t = -C / B
            if t > 1e-6:
                # Calcula o ponto de interseção usando a reta
                x = ray_origin.x + Dx * t
                y = ray_origin.y + Dy * t
                z = ray_origin.z + Dz * t
                return [True, [x, y, z], t]
            else:
                return [False, [0, 0, 0], float('inf')]

        # Calcula o discriminante da equação quadrática
        delta = B**2 - 4*A*C
        if delta < 0:
            # Se delta é negativo, não há solução real: não há interseção
            return [False, [0, 0, 0], float('inf')]
        
        sqrt_delta = sqrt(delta)
        # Calcula as duas raízes t1 e t2 da equação quadrática
        t1 = (-B - sqrt_delta) / (2*A)
        t2 = (-B + sqrt_delta) / (2*A)
        
        # Escolhe o menor t positivo, que indica a interseção mais próxima (da câmera)
        t = float('inf')
        if t1 > 1e-6 and t1 < t:
            t = t1
        if t2 > 1e-6 and t2 < t:
            t = t2
        
        # Se nenhum valor de t válido foi encontrado, retorna sem interseção.
        if t == float('inf'):
            return [False, [0, 0, 0], float('inf')]
        
        # Calcula as coordenadas do ponto de interseção
        x = ray_origin.x + Dx * t
        y = ray_origin.y + Dy * t
        z = ray_origin.z + Dz * t
        return [True, [x, y, z], t]

    def get_normal(self, point_intersection: Point):
        """
        Calcula a normal da superfície do paraboloide no ponto de interseção.
        Para a função implícita do paraboloide:
        
            F(x,y,z) = (x - v_x)^2 + (y - v_y)^2 - 4*p*(z - v_z)
        
        o gradiente (∇F) fornece a normal, onde:
        
            ∇F(x,y,z) = (2*(x - v_x), 2*(y - v_y), -4*p)
        
        A normal é então normalizada para obter um vetor unitário.
        """
        x = point_intersection.x
        y = point_intersection.y
        # A componente z da normal é constante e depende do parâmetro p
        normal = Vector(2*(x - self.vertex.x), 2*(y - self.vertex.y), -4*self.p_parameter)
        return normal.vector_normalize()
