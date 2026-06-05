# -*- coding: utf-8 -*-
"""ETAPAS 1, 2 E 3: estrutura inicial, validação dos estados e movimentos possíveis."""

import sys

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
    # Verificações das etapas 2 e 3.
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


if __name__ == "__main__":
    main()
