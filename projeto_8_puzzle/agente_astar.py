"""ETAPA 5: implementação do algoritmo A* para o quebra-cabeça de 8 peças."""

from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count

from estado import eh_objetivo, eh_solucionavel, gerar_sucessores, validar_estado


@dataclass
class NoBusca:
    """Representa um nó da árvore de busca do algoritmo A*."""

    estado: tuple[int, ...]
    pai: "NoBusca | None"
    acao: str | None
    g: int
    h: int
    f: int


def reconstruir_caminho(no_objetivo):
    """Reconstrói o caminho solução a partir do nó objetivo."""
    caminho = []
    no_atual = no_objetivo

    while no_atual is not None:
        caminho.append(
            {
                "estado": no_atual.estado,
                "acao": no_atual.acao,
                "g": no_atual.g,
                "h": no_atual.h,
                "f": no_atual.f,
            }
        )
        no_atual = no_atual.pai

    caminho.reverse()
    return caminho


def criar_resultado(
    encontrou_solucao,
    caminho,
    custo_total,
    estados_expandidos,
    historico,
    mensagem=None,
):
    """Monta a estrutura de retorno padronizada da busca."""
    return {
        "encontrou_solucao": encontrou_solucao,
        "caminho": caminho,
        "custo_total": custo_total,
        "estados_expandidos": estados_expandidos,
        "historico": historico,
        "mensagem": mensagem,
    }


def resolver_astar(
    estado_inicial,
    estado_objetivo,
    funcao_heuristica,
    registrar_historico=False,
):
    """Executa a busca A* a partir do estado inicial até o estado objetivo."""
    if not validar_estado(estado_inicial):
        raise ValueError("Estado inicial inválido: não foi possível iniciar a busca A*.")

    if not validar_estado(estado_objetivo):
        raise ValueError("Estado objetivo inválido: não foi possível iniciar a busca A*.")

    if not eh_solucionavel(estado_inicial):
        return criar_resultado(
            encontrou_solucao=False,
            caminho=[],
            custo_total=None,
            estados_expandidos=0,
            historico=[],
            mensagem="O estado inicial não é solucionável.",
        )

    h_inicial = funcao_heuristica(estado_inicial, estado_objetivo)
    no_inicial = NoBusca(
        estado=estado_inicial,
        pai=None,
        acao=None,
        g=0,
        h=h_inicial,
        f=h_inicial,
    )

    contador = count()
    open_list = []
    heappush(open_list, (no_inicial.f, next(contador), no_inicial))

    closed_list = set()
    melhor_g = {estado_inicial: 0}
    historico = []
    estados_expandidos = 0

    while open_list:
        _, _, no_atual = heappop(open_list)

        # Ignora entradas antigas da fila que já foram superadas por caminhos melhores.
        if no_atual.g > melhor_g.get(no_atual.estado, float("inf")):
            continue

        if no_atual.estado in closed_list:
            continue

        estados_expandidos += 1

        if registrar_historico:
            historico.append(
                {
                    "estado": no_atual.estado,
                    "acao": no_atual.acao,
                    "g": no_atual.g,
                    "h": no_atual.h,
                    "f": no_atual.f,
                }
            )

        if eh_objetivo(no_atual.estado, estado_objetivo):
            caminho = reconstruir_caminho(no_atual)
            return criar_resultado(
                encontrou_solucao=True,
                caminho=caminho,
                custo_total=no_atual.g,
                estados_expandidos=estados_expandidos,
                historico=historico,
                mensagem="Solução encontrada com sucesso.",
            )

        closed_list.add(no_atual.estado)

        for acao, estado_sucessor in gerar_sucessores(no_atual.estado):
            novo_g = no_atual.g + 1

            if novo_g >= melhor_g.get(estado_sucessor, float("inf")):
                continue

            if estado_sucessor in closed_list:
                closed_list.remove(estado_sucessor)

            novo_h = funcao_heuristica(estado_sucessor, estado_objetivo)
            novo_no = NoBusca(
                estado=estado_sucessor,
                pai=no_atual,
                acao=acao,
                g=novo_g,
                h=novo_h,
                f=novo_g + novo_h,
            )

            melhor_g[estado_sucessor] = novo_g
            heappush(open_list, (novo_no.f, next(contador), novo_no))

    return criar_resultado(
        encontrou_solucao=False,
        caminho=[],
        custo_total=None,
        estados_expandidos=estados_expandidos,
        historico=historico,
        mensagem="Nenhuma solução foi encontrada.",
    )
