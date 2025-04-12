from point import Point
from vector import Vector
from objects import Sphere, Paraboloid
from cam import Cam
from affine_transformations import rotate_x
from lightSource import Light
# Divirtam-se :)


def main():
    camera_ponto = Point(200, 30, 0)
    alvo_ponto = Point(150, 20, -10)
    up_vector = Vector(0, 1, 0)
    u_new = rotate_x([up_vector.x, up_vector.y, up_vector.z ], 90)
    u_new = Vector(u_new[0], u_new[1], u_new[2])
    
    luz_posicao = Point(1000, 200, 200)
    luzAmbiente = Light(luz_posicao, [1.0, 1.0, 1.0], [0.3,0.3,0.3], [0.6, 0.6, 0.6])  # Luz branca
    Fonte1 = Light(luz_posicao, [0 ,0, 0], [0.6,0.6, 0.6], [0.6, 0.6, 0.6])
    FontesDeLuz = [Fonte1]

    camera = Cam(camera_ponto, alvo_ponto, u_new, 1, 500, 500)

    esfera =  Sphere(Point(0, 0, 0), radius=1, color=[255, 255, 255],kdCoefficient= 0.8, ksCoefficient= 0.8, kaCoefficient= 0.3, krCoefficient = 0.5, ktCoefficient = 0.5, irCoefficient = 1.0, nCoefficient= 500)
    paraboloide = Paraboloid(
        vertex = Point(-95, -75, 0),
        p_parameter = -13,
        color = [200, 200, 0],
        kdCoefficient = 0.8,
        ksCoefficient = 0.8,
        kaCoefficient = 0.3,
        krCoefficient = 0.5,
        ktCoefficient = 0.5,
        irCoefficient = 1.0,
        nCoefficient = 500
    )
   
    objects = [paraboloide, esfera]
    camera.raycasting(objects, luzAmbiente, FontesDeLuz)

if __name__ == "__main__":
    main()
