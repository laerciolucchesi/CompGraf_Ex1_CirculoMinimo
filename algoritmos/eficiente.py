# Implementação do algoritmo que fornce o raio mínimo
# Vou chamá-lo de eficiente

import random
import math
from geometria import Ponto, Circulo

_EPS = 1e-12  # tolerância numérica para pertencimento ao círculo

def _dist2(a: Ponto, b: Ponto) -> float:
    """Calcula a distância quadrada entre dois pontos."""
    dx, dy = a.x - b.x, a.y - b.y
    return dx * dx + dy * dy

def _is_in_circle(p: Ponto, c: Circulo) -> bool:
    """Verifica se um ponto está dentro de um círculo."""
    return _dist2(p, c.centro) <= (c.raio * c.raio) + 1e-9

def _circle_two_points(a: Ponto, b: Ponto) -> Circulo:
    """Cria o círculo mínimo com dois pontos na borda."""
    cx = (a.x + b.x) / 2.0
    cy = (a.y + b.y) / 2.0
    r = math.hypot(a.x - b.x, a.y - b.y) / 2.0
    return Circulo(Ponto(cx, cy), r)

def _circle_three_points(a: Ponto, b: Ponto, c: Ponto) -> Circulo:
    """
    Circumcírculo de três pontos não colineares.
    Retorna None se forem (quase) colineares.
    """
    # Transformação para variáveis auxiliares
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y

    d = 2.0 * ((ax - cx) * (by - cy) - (ay - cy) * (bx - cx))
    if abs(d) < _EPS:
        # Pontos colineares - retorna círculo com diâmetro máximo
        dist_ab = math.hypot(ax - bx, ay - by)
        dist_ac = math.hypot(ax - cx, ay - cy)
        dist_bc = math.hypot(bx - cx, by - cy)
        
        if dist_ab >= dist_ac and dist_ab >= dist_bc:
            return _circle_two_points(a, b)
        elif dist_ac >= dist_ab and dist_ac >= dist_bc:
            return _circle_two_points(a, c)
        else:
            return _circle_two_points(b, c)

    ax2ay2 = ax * ax + ay * ay
    bx2by2 = bx * bx + by * by
    cx2cy2 = cx * cx + cy * cy

    ux = ((ax2ay2 - cx2cy2) * (by - cy) - (ay - cy) * (bx2by2 - cx2cy2)) / d
    uy = ((ax - cx) * (bx2by2 - cx2cy2) - (ax2ay2 - cx2cy2) * (bx - cx)) / d

    r = math.hypot(ux - ax, uy - ay)
    return Circulo(Ponto(ux, uy), r)

def _make_circle_one_point(points: list[Ponto], p: Ponto) -> Circulo:
    """
    Menor círculo contendo "points" com p na fronteira (suporte).
    """
    c = Circulo(p, 0.0)
    for i, q in enumerate(points):
        if not _is_in_circle(q, c):
            if c.raio == 0.0:
                c = _circle_two_points(p, q)
            else:
                c = _make_circle_two_points(points[: i + 1], p, q)
    return c

def _make_circle_two_points(points: list[Ponto], p: Ponto, q: Ponto) -> Circulo:
    """
    Menor círculo contendo "points" com p e q na fronteira.
    Trata os dois semiciclos (esq/dir) e escolhe o mínimo válido.
    """
    # círculo base: diâmetro pq
    circ = _circle_two_points(p, q)

    # Candidatos do lado esquerdo e direito (do vetor pq)
    left: Circulo | None = None
    right: Circulo | None = None

    # Vetor pq
    px, py = p.x, p.y
    qx, qy = q.x, q.y
    vx, vy = qx - px, qy - py

    for r in points:
        if _is_in_circle(r, circ):
            continue

        # Construir círculo passando por p, q e r
        c = _circle_three_points(p, q, r)

        # Testar orientação para classificar como "esquerda" ou "direita"
        rx, ry = r.x, r.y
        cross = (vx * (ry - py)) - (vy * (rx - px))
        if cross > 0:
            # lado esquerdo: mantenha o menor raio válido (ou substitua se ainda não houver)
            if (left is None) or (c.raio > left.raio):
                left = c
        else:
            # lado direito
            if (right is None) or (c.raio > right.raio):
                right = c

    # Escolher o círculo mínimo válido que cobre todos os pontos.
    if left is None and right is None:
        return circ
    elif left is None:
        return right  
    elif right is None:
        return left   
    else:
        # Ambos existem; qualquer um que cubra todos os points serve — ambos devem cobrir.
        # Preferi o de menor raio.
        return left if left.raio <= right.raio else right

def calcular_circulo_eficiente(pontos: list[Ponto], seed: int | None = None) -> Circulo:
    """
    Calcula o menor círculo envolvente de um conjunto de pontos 2D.

    Parâmetros
    ----------
    pontos : lista de Ponto
    seed : int opcional - para reprodutibilidade

    Retorna
    -------
    Circulo : centro e raio do círculo mínimo.
    """
    P = list(pontos)
    if not P:
        return Circulo(Ponto(0.0, 0.0), 0.0)
    if seed is not None:
        random.Random(seed).shuffle(P)
    else:
        random.shuffle(P)

    # Inicialmente, nenhum círculo
    c: Circulo | None = None

    for i, p in enumerate(P):
        if c is None or not _is_in_circle(p, c):
            # Recalcular com p na fronteira usando apenas os pontos já vistos
            c = _make_circle_one_point(P[: i + 1], p)

    return c  
