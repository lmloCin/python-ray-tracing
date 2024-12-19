from obj_reader import ObjReader
from point import Point
# Divirtam-se :)

def main():
    w = Point(5, 0, 0)
    h = Point(0, 0, 0)
    c = w.point_sum(w)
    j = Point(-2, -2, -2).point_subtraction(c)

    print(h.point_distance(w))
    print(j.__str__())

    #obj = ObjReader('inputs/icosahedron.obj')
    #obj.print_faces()

if __name__ == "__main__":
    main()
