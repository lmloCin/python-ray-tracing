import vector
from obj_reader import ObjReader
from point import Point
from vector import Vector
# Divirtam-se :)

def main():
    w = Point(5, 0, 0)
    h = Point(0, 0, 0)
    c = w.point_sum(w)
    j = Point(-2, -2, -2).point_subtraction(c)
    v1 = Vector(-2, 0, 1)
    v2 = Vector(4, 2, 5)
    print(type(v2))
    if type(v2) == vector.Vector:
        print('yes')
    print(v1.vector_sum(v2))
    print(v1.vector_subtraction(v2))
    print(v1.vector_dot_product(v2))
    print(v1.vector_x_scalar(2))
    print(v1.vector_product(v2))
    print(h.point_distance(w))
    print(j.__str__())

    #obj = ObjReader('inputs/icosahedron.obj')
    #obj.print_faces()

if __name__ == "__main__":
    main()
