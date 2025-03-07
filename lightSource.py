from point import Point 

class Light:
    def __init__(self, position: Point, intensity_a, intensity_d, intensity_s):
  
        self.position = position
        self.intensity_a = intensity_a  # Intensidade da luz ambiente
        self.intensity_d = intensity_d  # Intensidade da luz difusa
        self.intensity_s = intensity_s  # Intensidade da luz especular

