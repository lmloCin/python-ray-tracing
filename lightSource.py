from point import Point 

class Luz:
    def __init__(self, posicao: Point, cor=(255, 255, 255)):
        if not isinstance(posicao, Point):
            raise TypeError("A posição da luz deve ser um objeto da classe Point")
        
        self.posicao = posicao
        self.Ia = self.validar_cor(cor)

    def validar_cor(self, cor):
        """ Garante que a cor está dentro do intervalo [0, 255] para cada componente RGB """
        return tuple(max(0, min(255, c)) for c in cor)

