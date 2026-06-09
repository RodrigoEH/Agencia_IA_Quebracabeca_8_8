# -*- coding: utf-8 -*-
"""ETAPAS 6, 7 E 12: execução no terminal com solução, histórico e estado embaralhado."""

import sys

from agente_astar import resolver_astar
from estado import ESTADO_OBJETIVO, formatar_estado
from exemplos import ESTADO_INICIAL_EXEMPLO, gerar_estado_embaralhado
from heuristicas import distancia_manhattan

TITULO = "AGENTE A* — QUEBRA-CABEÇA DE 8 PEÇAS"
LARGURA = 40


def exibir_cabecalho():
    """Mostra o cabeçalho principal da aplicação."""
    separador = "=" * LARGURA
    print(separador)
    print(TITULO)
    print(separador)


def perguntar_estado_embaralhado():
    """Permite escolher entre o exemplo fixo e um estado embaralhado."""
    print()
    try:
        resposta = input("Deseja embaralhar o estado inicial para testar outro caso? (S/n): ")
    except EOFError:
        return True

    return resposta.strip().lower() not in {"n", "nao", "não"}


def perguntar_exibicao_historico():
    """Permite ativar ou desativar a exibição detalhada do histórico."""
    print()
    try:
        resposta = input("Deseja exibir o histórico detalhado das expansões? (s/N): ")
    except EOFError:
        return False

    return resposta.strip().lower() in {"s", "sim"}


def obter_estado_inicial():
    """Escolhe o estado inicial que será usado na execução atual."""
    if perguntar_estado_embaralhado():
        return gerar_estado_embaralhado(movimentos=20), "Embaralhado automaticamente"

    return ESTADO_INICIAL_EXEMPLO, "Exemplo fixo"


def exibir_estados_principais(estado_inicial, origem_estado):
    """Mostra o estado inicial utilizado e o objetivo da busca."""
    print()
    print(f"Tipo de estado inicial: {origem_estado}")
    print()
    print("Estado inicial:")
    print(formatar_estado(estado_inicial))
    print()
    print("Estado objetivo:")
    print(formatar_estado(ESTADO_OBJETIVO))


def exibir_caminho_solucao(resultado):
    """Mostra cada passo da solução com ação e custos da busca."""
    print()
    print("Heurística utilizada: Distância de Manhattan (admissível)")
    print()

    for indice, passo in enumerate(resultado["caminho"]):
        descricao = passo["acao"] or "Estado inicial"
        print(f"Passo {indice} — {descricao}")
        print(formatar_estado(passo["estado"]))
        print(f"Movimento realizado: {descricao}")
        print(f"g = {passo['g']}, h = {passo['h']}, f = {passo['f']}")
        print()

    print("Solução encontrada.")
    print(f"Custo total: {resultado['custo_total']} movimentos")
    print(f"Estados expandidos: {resultado['estados_expandidos']}")


def exibir_erro(resultado):
    """Mostra a mensagem de erro quando não existe solução."""
    print()
    print("Heurística utilizada: Distância de Manhattan (admissível)")
    print()
    print(f"Erro: {resultado['mensagem']}")
    print(f"Estados expandidos: {resultado['estados_expandidos']}")


def exibir_resumo_final(resultado):
    """Repete no fim da execução um resumo claro do resultado obtido."""
    print()
    print("=" * LARGURA)
    print("RESULTADO FINAL")
    print("=" * LARGURA)

    if resultado["encontrou_solucao"]:
        print("Situação: solução encontrada com sucesso.")
        print(f"Custo total: {resultado['custo_total']} movimentos")
        print(f"Estados expandidos: {resultado['estados_expandidos']}")
        print(f"Estado final alcançado: {resultado['caminho'][-1]['estado']}")
    else:
        print("Situação: nenhuma solução encontrada.")
        print(f"Motivo: {resultado['mensagem']}")
        print(f"Estados expandidos: {resultado['estados_expandidos']}")


def exibir_lista_estados(titulo, estados):
    """Mostra uma lista resumida de estados no terminal."""
    print(titulo)

    if not estados:
        print("(vazia)")
        return

    for indice, estado in enumerate(estados, start=1):
        print(f"Estado {indice}:")
        print(formatar_estado(estado))
        print()


def exibir_historico(resultado):
    """Mostra o histórico resumido de cada expansão do algoritmo A*."""
    if not resultado["historico"]:
        print()
        print("Histórico detalhado: não foi registrado.")
        return

    print()
    print("Histórico detalhado das expansões:")

    for item in resultado["historico"]:
        descricao_acao = item["acao"] or "Estado inicial"
        print()
        print(f"Etapa {item['numero_etapa']}")
        print("Estado atual:")
        print(formatar_estado(item["estado_atual"]))
        print(f"Ação: {descricao_acao}")
        print(f"g = {item['g']}, h = {item['h']}, f = {item['f']}")
        print(f"Quantidade total na Open List: {item['quantidade_open']}")
        print(f"Quantidade total na Closed List: {item['quantidade_closed']}")
        exibir_lista_estados("Open List resumida:", item["open_resumida"])
        exibir_lista_estados("Closed List resumida:", item["closed_resumida"])


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    exibir_cabecalho()
    estado_inicial, origem_estado = obter_estado_inicial()
    exibir_estados_principais(estado_inicial, origem_estado)
    exibir_historico_detalhado = perguntar_exibicao_historico()

    resultado = resolver_astar(
        estado_inicial=estado_inicial,
        estado_objetivo=ESTADO_OBJETIVO,
        funcao_heuristica=distancia_manhattan,
        registrar_historico=exibir_historico_detalhado,
    )

    if resultado["encontrou_solucao"]:
        exibir_caminho_solucao(resultado)
    else:
        exibir_erro(resultado)

    if exibir_historico_detalhado:
        exibir_historico(resultado)

    exibir_resumo_final(resultado)


if __name__ == "__main__":
    main()
