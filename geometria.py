# define duas classes: Ponto e Circulo
# estou assumindo que as operações serão feitas em um plano 2D

import math

class Ponto:
    """Ponto 2D com coordenadas x e y."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia(self, outro_ponto):
        """Calcula a distância entre o ponto corrente e um outro ponto."""
        dx = self.x - outro_ponto.x
        dy = self.y - outro_ponto.y
        return math.sqrt(dx**2 + dy**2)

class Circulo:
    """Círculo com um centro (Ponto) e um raio."""
    def __init__(self, centro: Ponto, raio: float):
        self.centro = centro
        self.raio = raio

    def contem(self, ponto: Ponto, tolerancia=1e-6) -> bool:
        """
        Diz se o ponto está dentro ou em cima do círculo. 
        Mede a distância até o centro e compara com o raio (com uma tolerância para evitar erro de cálculo). 
        Se estiver perto o suficiente, retorna True; senão, False.
        """
        return self.centro.distancia(ponto) <= self.raio + tolerancia