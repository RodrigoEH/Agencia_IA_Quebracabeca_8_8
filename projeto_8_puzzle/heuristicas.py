"""ETAPA 4: funções heurísticas para o quebra-cabeça de 8 peças."""

from estado import validar_estado


def distancia_manhattan(estado, objetivo):
    """Calcula a soma das distâncias de Manhattan, ignorando a peça vazia."""
    if not validar_estado(estado):
        raise ValueError("Estado inválido: não foi possível calcular a distância de Manhattan.")

    if not validar_estado(objetivo):
        raise ValueError("Objetivo inválido: não foi possível calcular a distância de Manhattan.")

    posicoes_objetivo = {}
    for indice, valor in enumerate(objetivo):
        if valor != 0:
            posicoes_objetivo[valor] = (indice // 3, indice % 3)

    distancia_total = 0

    for indice, valor in enumerate(estado):
        if valor == 0:
            continue

        linha_atual = indice // 3
        coluna_atual = indice % 3
        linha_objetivo, coluna_objetivo = posicoes_objetivo[valor]

        distancia_total += abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)

    return distancia_total


def distancia_manhattan_nao_admissivel(estado, objetivo):
    """Calcula uma heurística não admissível com peso 2 sobre Manhattan."""
    return 2 * distancia_manhattan(estado, objetivo)
