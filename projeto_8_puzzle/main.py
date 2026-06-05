# -*- coding: utf-8 -*-

import sys

TITULO = "AGENTE A* — QUEBRA-CABEÇA DE 8 PEÇAS"
LARGURA = 40

ESTADO_INICIAL = (
    (1, 2, 3),
    (4, 0, 6),
    (7, 5, 8),
)

ESTADO_OBJETIVO = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0),
)


def formatar_estado(estado):
    return "\n".join(" ".join(str(valor) for valor in linha) for linha in estado)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

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


if __name__ == "__main__":
    main()
