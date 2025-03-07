from point import Point
from vector import Vector
from objects import Plane, Sphere, Mesh
from cam import Cam
from affine_transformations import translate, rotate_x, rotate_y, rotate_z
from lightSource import Light
# Divirtam-se :)


def main():
    # obj = ObjReader('inputs/icosahedron.obj')
    # obj.print_faces()
    
    camera_ponto = Point(100, 200, -100)
    alvo_ponto = Point(0, 0, 0)
    up_vector = Vector(0, 1, 0)
    u_new = rotate_y([up_vector.x, up_vector.y, up_vector.z ], 90)
    u_new = Vector(u_new[0], u_new[1], u_new[2])
    
    center = Point(0, 0, 0)
    n_center = translate([center.x, center.y, center.z], 50, 40, 0)
    n_center = Point(n_center[0], n_center[1], n_center[2])

    n_center2 = translate([center.x,center.y, center.z], -50, -40, 0)
    n_center2 = Point(n_center2[0], n_center2[1], n_center2[2])
    
    luz_posicao = Point(100, 300, 200)  # Posição da luz acima da câmera
    luz = Light(luz_posicao, 0.8, 0.3, 0.6)  # Luz branca

    camera = Cam(camera_ponto, alvo_ponto, up_vector, 1, 700, 700)
    new_camera = Cam(camera_ponto, alvo_ponto, u_new, 1, 500, 500)
    plano = Plane(Point(0, 30, 0), Vector(1, -0.3, -1), [255, 255, 255], kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, nCoefficient= 500)
    esfera =  Sphere(center, radius=50, color=[0, 150, 100],kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, nCoefficient= 500)
    esfera2 =  Sphere(n_center, radius=50, color=[255, 150, 100],kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, nCoefficient= 500)
    esfera3 =  Sphere(n_center2, radius=50, color=[0, 100, 255],kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, nCoefficient= 500)
    # obj = [plano, esfera]
    # camera.raycasting(obj)
    
    #Visualizando interseção da malha de triangulos
    p0 = Vector(100, 0, 0)
    p1 = Vector(0, 100, 0)
    p2 = Vector(-100, 0, 0)
    p3 = Vector(0, -100, 0)
    p4 = Vector(0, 0, 100)

    # Cálculo das normais
    n1 = (p1.vector_subtraction(p0)).vector_product(p4.vector_subtraction(p0)).vector_normalize()
    n2 = (p2.vector_subtraction(p1)).vector_product(p4.vector_subtraction(p1)).vector_normalize()
    n3 = (p3.vector_subtraction(p2)).vector_product(p4.vector_subtraction(p2)).vector_normalize()
    n4 = (p0.vector_subtraction(p3)).vector_product(p4.vector_subtraction(p3)).vector_normalize()
    
    # Criando a malha com os vetores e normais
    malha = Mesh(
        4, 
        5, 
        [p0, p1, p2, p3, p4], 
        [(0,1,4), (1,2,4), (2,3,4), (0,3,4)],
        [n1, n2, n3, n4],
        [],
        [[100, 0, 200], [255, 0, 0], [0, 255, 0], [0, 0, 255]],kdCoefficient= 0.9, ksCoefficient= 0.9, kaCoefficient= 0.3, nCoefficient= 500
    )

    objects = [malha, esfera, plano]
    #camera.raycasting(objects, luz)
    new_camera.raycasting(objects, luz)

if __name__ == "__main__":
    main()
