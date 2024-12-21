import point
from point import Point
from vector import Vector
from objects import Plane
from objects import Sphere
from cam import Cam
# Divirtam-se :)


def main():
    w = Point(5, 0, 0)
    h = Point(0, 0, 0)
    c = w.point_sum(w)
    j = Point(-2, -2, -2).point_subtraction(c)
    v1 = Vector(1, 2, 0)
    v2 = Vector(4, 5, 6)
    print(type(v2))
    print(v1.vector_sum(v2))
    print(v1.vector_subtraction(v2))
    print(v1.vector_dot_product(v2))
    print(v1.vector_x_scalar(2))
    print(v1.vector_product(v2))
    print(h.point_distance(w))
    print(j.__str__())
    pi = Plane(h, v1, [75, 203, 133])
    print(pi.inter_plane_line(w, v2))
    print(v1.vector_product(v2))
    print(w.x)
    if type(w) == point.Point:
        print('yes')
    # obj = ObjReader('inputs/icosahedron.obj')
    # obj.print_faces()


def test():
    camera_ponto = Point(-100, 200, 500)
    alvo_ponto = Point(0, 0, 0)
    up_vector = Vector(0, 1, 0)
    camera = Cam(camera_ponto, alvo_ponto, up_vector, 1, 500, 500)
    plano = Plane(Point(0, 0, 50), Vector(100, 50, 50), [0, 255, 0])
    esfera =  Sphere(center=Point(50, 50, 50), radius=30, color=[255, 0, 0])
    obj = [plano, esfera]
    if isinstance(plano, Plane):
        print('yes, it is a plane')
    if isinstance(esfera, Sphere):
        print('yes, it is a sphere')
    print(type(plano))
    camera.raycasting(obj)


if __name__ == "__main__":
    test()
