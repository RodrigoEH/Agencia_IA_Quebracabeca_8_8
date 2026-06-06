# -*- coding: utf-8 -*-
"""ETAPA EXTRA: geração de estados de exemplo e estados embaralhados para teste."""

from random import Random

from estado import ESTADO_OBJETIVO, gerar_sucessores

ESTADO_INICIAL_EXEMPLO = (1, 2, 3, 4, 0, 6, 7, 5, 8)


def gerar_estado_embaralhado(estado_base=ESTADO_OBJETIVO, movimentos=20, semente=None):
    """Gera um estado solucionável a partir de movimentos aleatórios válidos."""
    gerador = Random(semente)
    estado_atual = estado_base
    estado_anterior = None

    for _ in range(max(1, movimentos)):
        sucessores = gerar_sucessores(estado_atual)

        if estado_anterior is not None:
            sucessores_filtrados = [
                item for item in sucessores if item[1] != estado_anterior
            ]
            if sucessores_filtrados:
                sucessores = sucessores_filtrados

        _, proximo_estado = gerador.choice(sucessores)
        estado_anterior = estado_atual
        estado_atual = proximo_estado

    return estado_atual
