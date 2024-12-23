import point
from point import Point
from vector import Vector
from objects import Plane
from objects import Sphere
from cam import Cam
# Divirtam-se :)


def main():
    # obj = ObjReader('inputs/icosahedron.obj')
    # obj.print_faces()
    
    camera_ponto = Point(-100, 200, 500)
    alvo_ponto = Point(0, 0, 0)
    up_vector = Vector(0, 1, 0)
    camera = Cam(camera_ponto, alvo_ponto, up_vector, 1, 500, 500)
    plano = Plane(Point(0, 0, 0), Vector(1, 0, 0), [255, 255, 255])
    esfera =  Sphere(center=Point(0, 0, -200), radius=50, color=[100, 0, 100])
    esfera2 = Sphere(Point(0, 0, 20), radius=50, color=[255, 0, 0])
    obj = [plano, esfera, esfera2]
    camera.raycasting(obj)

if __name__ == "__main__":
    main()
