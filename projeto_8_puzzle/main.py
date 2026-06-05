# -*- coding: utf-8 -*-
"""ETAPAS 1, 2, 3, 4 E 5: estrutura, estados, movimentos, heurísticas e busca A*."""

import sys

from agente_astar import resolver_astar
from estado import (
    ESTADO_OBJETIVO,
    eh_objetivo,
    eh_solucionavel,
    formatar_estado,
    gerar_sucessores,
    localizar_vazio,
    possui_nove_posicoes,
    possui_valores_validos,
    validar_estado,
)
from heuristicas import distancia_manhattan, distancia_manhattan_nao_admissivel

TITULO = "AGENTE A* — QUEBRA-CABEÇA DE 8 PEÇAS"
LARGURA = 40

ESTADO_INICIAL = (1, 2, 3, 4, 0, 6, 7, 5, 8)
ESTADO_IMPOSSIVEL = (1, 2, 3, 4, 5, 6, 8, 7, 0)


def exibir_sucessores(estado):
    """Mostra no terminal os estados sucessores gerados a partir do estado informado."""
    sucessores = gerar_sucessores(estado)

    print("Sucessores do estado inicial:")
    for descricao, novo_estado in sucessores:
        print()
        print(f"{descricao}:")
        print(formatar_estado(novo_estado))


def exibir_heuristicas(estado, objetivo):
    """Mostra no terminal os valores das heurísticas para o estado informado."""
    print("Heurísticas do estado inicial:")
    print(f"- Distância de Manhattan: {distancia_manhattan(estado, objetivo)}")
    print(
        f"- Distância de Manhattan não admissível: "
        f"{distancia_manhattan_nao_admissivel(estado, objetivo)}"
    )


def exibir_resultado_busca(resultado):
    """Mostra no terminal o resumo da execução do algoritmo A*."""
    print("Resultado da busca A*:")
    print(f"- Encontrou solução? {resultado['encontrou_solucao']}")
    print(f"- Mensagem: {resultado['mensagem']}")
    print(f"- Custo total: {resultado['custo_total']}")
    print(f"- Estados expandidos: {resultado['estados_expandidos']}")

    if not resultado["encontrou_solucao"]:
        return

    print()
    print("Caminho solução:")
    for indice, passo in enumerate(resultado["caminho"]):
        descricao_acao = passo["acao"] or "Estado inicial"
        print()
        print(f"Passo {indice}: {descricao_acao}")
        print(formatar_estado(passo["estado"]))
        print(f"g={passo['g']}, h={passo['h']}, f={passo['f']}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Cabeçalho da aplicação.
    separador = "=" * LARGURA

    print(separador)
    print(TITULO)
    print(separador)
    print()
    print("Estado inicial:")
    print(formatar_estado(ESTADO_INICIAL))
    print()
    print("Estado objetivo:")
    print(formatar_estado(ESTADO_OBJETIVO))
    print()
    print("Testes manuais:")
    # Verificações das etapas 2, 3, 4 e 5.
    print(f"- Estado inicial válido? {validar_estado(ESTADO_INICIAL)}")
    print(f"- Possui nove posições? {possui_nove_posicoes(ESTADO_INICIAL)}")
    print(f"- Possui valores de 0 a 8 sem repetição? {possui_valores_validos(ESTADO_INICIAL)}")
    print(f"- Posição do espaço vazio: {localizar_vazio(ESTADO_INICIAL)}")
    print(f"- Estado inicial já é objetivo? {eh_objetivo(ESTADO_INICIAL)}")
    print(f"- Estado objetivo já é objetivo? {eh_objetivo(ESTADO_OBJETIVO)}")
    print(f"- Estado inicial é solucionável? {eh_solucionavel(ESTADO_INICIAL)}")
    print(f"- Estado impossível é solucionável? {eh_solucionavel(ESTADO_IMPOSSIVEL)}")
    print(f"- Quantidade de sucessores válidos: {len(gerar_sucessores(ESTADO_INICIAL))}")
    print()
    exibir_sucessores(ESTADO_INICIAL)
    print()
    exibir_heuristicas(ESTADO_INICIAL, ESTADO_OBJETIVO)
    print()

    resultado = resolver_astar(
        estado_inicial=ESTADO_INICIAL,
        estado_objetivo=ESTADO_OBJETIVO,
        funcao_heuristica=distancia_manhattan,
        registrar_historico=True,
    )
    exibir_resultado_busca(resultado)


if __name__ == "__main__":
    main()
