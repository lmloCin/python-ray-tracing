from point import Point
from vector import Vector
from objects import Plane, Sphere, Mesh
from cam import Cam
from affine_transformations import translate, rotate_x, rotate_y, rotate_z
from lightSource import Light
from obj_reader import ObjReader
# Divirtam-se :)


def main():
    camera_ponto = Point(100, 200, -100)
    alvo_ponto = Point(0, 0, 0)
    up_vector = Vector(0, 1, 0)
    u_new = rotate_x([up_vector.x, up_vector.y, up_vector.z ], 90)
    u_new = Vector(u_new[0], u_new[1], u_new[2])
    
    center = Point(0, 0, 0)
    n_center = translate([center.x, center.y, center.z], 50, 40, 0)
    n_center = Point(n_center[0], n_center[1], n_center[2])

    n_center2 = translate([center.x,center.y, center.z], -50, -40, 0)
    n_center2 = Point(n_center2[0], n_center2[1], n_center2[2])
    
    luz_posicao = Point(1000, 200, 200)  # Posição da luz acima da câmera
    luzFonte_posicao = Point(1000, 200, 200)
    luzAmbiente = Light(luz_posicao, [1.0, 1.0, 1.0], [0.3,0.3,0.3], [0.6, 0.6, 0.6])  # Luz branca
    Fonte1 = Light(luzFonte_posicao, [0 ,0, 0], [0.3,0.3, 0.3], [0.6, 0.6, 0.6])
    Fonte2 = Light(Point(300, 200, -200), [0, 0, 0], [0.3, 0.3, 0.3], [150, 150, 150])
    FontesDeLuz = [Fonte1]
    # luz = Light(luz_posicao, [0,0.0,0.8], [0,0.0,0.3], [0,0.0,0.6])  # Luz vermelha

    camera = Cam(camera_ponto, alvo_ponto, u_new, 1, 500, 500)
    new_camera = Cam(camera_ponto, alvo_ponto, u_new, 1, 500, 500)
    plano = Plane(Point(0, 100, 0), Vector(1, 1, 1), [0, 0, 255], kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, krCoefficient = 0.5, ktCoefficient = 0, irCoefficient = 1.52, nCoefficient= 500)
    esfera =  Sphere(center, radius=50, color=[0, 255, 0],kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, krCoefficient = 0.5, ktCoefficient = 0.5, irCoefficient = 1.52, nCoefficient= 500)
    esfera2 =  Sphere(n_center, radius=50, color=[255, 150, 100],kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, krCoefficient = 0.3, ktCoefficient = 0.8, irCoefficient = 1.2, nCoefficient= 500)
    esfera3 =  Sphere(n_center2, radius=50, color=[0, 100, 255],kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, krCoefficient = 0.3, ktCoefficient = 0.8, irCoefficient = 1.2, nCoefficient= 500)

    # #Visualizando interseção da malha de triangulos
    p0 = Vector(100, 0, 0)
    p1 = Vector(0, 100, 0)
    p2 = Vector(-100, 0, 0)
    p3 = Vector(0, -100, 0)
    p4 = Vector(0, 0, 100)

    # # Cálculo das normais
    n1 = (p1.vector_subtraction(p0)).vector_product(p4.vector_subtraction(p0)).vector_normalize()
    n2 = (p2.vector_subtraction(p1)).vector_product(p4.vector_subtraction(p1)).vector_normalize()
    n3 = (p3.vector_subtraction(p2)).vector_product(p4.vector_subtraction(p2)).vector_normalize()
    n4 = (p0.vector_subtraction(p3)).vector_product(p4.vector_subtraction(p3)).vector_normalize()
    
    # Criando a malha com os vetores e normais
    malha = Mesh(
        5, #num de triangulos
        5, #num de vertices
        [p0, p1, p2, p3, p4], #lista de vertices
        [(0,1,4), (1,2,4), (2,3,4), (0,3,4), (2,3,4)], #triplas dos triangulos
        [n1, n2, n3, n4, n1], #normais dos triangulos
        [],
        [[100, 0, 200], [255, 0, 0], [0, 255, 0], [0, 0, 255], [120, 255, 200]],kdCoefficient= 0.9, ksCoefficient= 0.9, kaCoefficient= 0.3, krCoefficient = 0.8, ktCoefficient = 0.4, irCoefficient = 1.2, nCoefficient= 500
    )
   

    objects = [malha, esfera]
    camera.raycasting(objects, luzAmbiente, FontesDeLuz)
    # new_camera.raycasting(objects, luz)

if __name__ == "__main__":
    main()
