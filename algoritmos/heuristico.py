
# Algoritmo heurístico para encontrar um círculo que engloba todos os pontos de um conjunto.
# Não garante o círculo mínimo, mas tem complexidade O(n).
# Começa pegando os pontos mais extremos e monta um círculo usando o par mais distante como diâmetro.
# Vai ajustando o centro e o raio de um novo círculo se algum ponto ficar de fora.

from geometria import Ponto, Circulo
from itertools import combinations

def calcular_circulo_heuristico(pontos: list[Ponto]) -> Circulo:
    """
    Calcula um círculo envolvente para um conjunto de pontos.
    """
    if not pontos:
        return None
    if len(pontos) == 1:
        return Circulo(pontos[0], 0)

    # Acha os pontos extremos
    # extremos = [x_min, x_max, y_min, y_max]
    extremos = [
        min(pontos, key=lambda p: p.x),
        max(pontos, key=lambda p: p.x),
        min(pontos, key=lambda p: p.y),
        max(pontos, key=lambda p: p.y)
    ]

    # Escolhe o par mais distante entre os pontos extremos
    p_i, p_j = None, None
    max_dist_quadrada = -1
    for p1, p2 in combinations(extremos, 2):
        dist_sq = (p1.x - p2.x)**2 + (p1.y - p2.y)**2
        if dist_sq > max_dist_quadrada:
            max_dist_quadrada = dist_sq
            p_i, p_j = p1, p2

    # Calcula o círculo inicial com os pontos mais distantes definindo o diâmetro do círculo
    centro_x = (p_i.x + p_j.x) / 2
    centro_y = (p_i.y + p_j.y) / 2
    centro = Ponto(centro_x, centro_y)
    raio = p_i.distancia(p_j) / 2
    circulo = Circulo(centro, raio)

    # Para cada ponto pk da lista, se pk estiver fora do círculo, expande o círculo para incluí-lo
    for p_k in pontos:
        if not circulo.contem(p_k): # Se o ponto pk está fora do círculo
            
            # calcula a distância do centro do atual círculo ao ponto pk
            dist_pk_centro = circulo.centro.distancia(p_k)

            # expande o novo raio
            novo_raio = (circulo.raio + dist_pk_centro) / 2 

            # "move" o centro na direção do ponto externo
            fator_deslocamento = (dist_pk_centro - circulo.raio) / (2 * dist_pk_centro)
            novo_centro_x = circulo.centro.x + (p_k.x - circulo.centro.x) * fator_deslocamento
            novo_centro_y = circulo.centro.y + (p_k.y - circulo.centro.y) * fator_deslocamento

            # calcula o novo círculo que engloba todos os pontos já vistos
            circulo.centro = Ponto(novo_centro_x, novo_centro_y)
            circulo.raio = novo_raio
            
    return circulo