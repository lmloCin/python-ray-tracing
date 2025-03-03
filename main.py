from point import Point
from vector import Vector
from objects import Plane, Sphere, Mesh
from cam import Cam
# Divirtam-se :)


def main():
    # obj = ObjReader('inputs/icosahedron.obj')
    # obj.print_faces()
    
    camera_ponto = Point(-100, 200, 500)
    alvo_ponto = Point(0, 0, 0)
    up_vector = Vector(0, 1, 0)
    
    camera = Cam(camera_ponto, alvo_ponto, up_vector, 1, 500, 500)
    # plano = Plane(Point(0, 0, 0), Vector(0, 1, 0), [100, 55, 0])
    # esfera =  Sphere(center=Point(0, 0, -45), radius=50, color=[255, 0, 0])
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
        [[255, 255, 255], [255, 0, 0], [0, 255, 0], [0, 0, 255]]
    )

    objects = [malha]
    camera.raycasting(objects)

if __name__ == "__main__":
    main()
