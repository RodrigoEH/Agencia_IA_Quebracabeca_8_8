"""ETAPAS 2 E 3: representação, validação e geração de sucessores do quebra-cabeça de 8 peças."""

ESTADO_OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def eh_tupla(estado):
    """Verifica se a estrutura usada é uma tupla imutável."""
    return isinstance(estado, tuple)


def possui_nove_posicoes(estado):
    """Confirma se o estado possui exatamente nove posições."""
    return eh_tupla(estado) and len(estado) == 9


def possui_valores_validos(estado):
    """Verifica se os números de 0 a 8 aparecem exatamente uma vez."""
    if not possui_nove_posicoes(estado):
        return False

    if any(type(valor) is not int for valor in estado):
        return False

    return tuple(sorted(estado)) == tuple(range(9))


def validar_estado(estado):
    """Valida a estrutura completa do estado."""
    return possui_nove_posicoes(estado) and possui_valores_validos(estado)


def formatar_estado(estado):
    """Formata o estado em três linhas e três colunas."""
    if not validar_estado(estado):
        raise ValueError("Estado inválido: use uma tupla com os números de 0 a 8, sem repetição.")

    linhas = []
    for indice in range(0, 9, 3):
        linha = estado[indice:indice + 3]
        linhas.append(" ".join(str(valor) for valor in linha))

    return "\n".join(linhas)


def localizar_vazio(estado):
    """Localiza a posição atual do espaço vazio representado por 0."""
    if not validar_estado(estado):
        raise ValueError("Estado inválido: não foi possível localizar o espaço vazio.")

    return estado.index(0)


def eh_objetivo(estado, objetivo=ESTADO_OBJETIVO):
    """Verifica se o estado atual corresponde ao objetivo."""
    if not validar_estado(estado):
        raise ValueError("Estado inválido: não foi possível comparar com o objetivo.")

    return estado == objetivo


def contar_inversoes(estado):
    """Conta as inversões do estado, ignorando o espaço vazio."""
    if not validar_estado(estado):
        raise ValueError("Estado inválido: não foi possível contar inversões.")

    numeros = [valor for valor in estado if valor != 0]
    inversoes = 0

    for indice, atual in enumerate(numeros):
        for proximo in numeros[indice + 1:]:
            if atual > proximo:
                inversoes += 1

    return inversoes


def eh_solucionavel(estado):
    """Determina se a configuração pode ser resolvida pela paridade das inversões."""
    return contar_inversoes(estado) % 2 == 0


def trocar_posicoes(estado, indice_a, indice_b):
    """Cria um novo estado trocando duas posições."""
    lista_estado = list(estado)
    lista_estado[indice_a], lista_estado[indice_b] = lista_estado[indice_b], lista_estado[indice_a]
    return tuple(lista_estado)


def gerar_sucessores(estado):
    """Gera apenas os movimentos válidos a partir do estado atual."""
    if not validar_estado(estado):
        raise ValueError("Estado inválido: não foi possível gerar sucessores.")

    indice_vazio = localizar_vazio(estado)
    linha = indice_vazio // 3
    coluna = indice_vazio % 3
    sucessores = []

    # Cada ação troca o espaço vazio com uma peça vizinha válida.
    if linha > 0:
        novo_estado = trocar_posicoes(estado, indice_vazio, indice_vazio - 3)
        sucessores.append(("Mover vazio para cima", novo_estado))

    if linha < 2:
        novo_estado = trocar_posicoes(estado, indice_vazio, indice_vazio + 3)
        sucessores.append(("Mover vazio para baixo", novo_estado))

    if coluna > 0:
        novo_estado = trocar_posicoes(estado, indice_vazio, indice_vazio - 1)
        sucessores.append(("Mover vazio para esquerda", novo_estado))

    if coluna < 2:
        novo_estado = trocar_posicoes(estado, indice_vazio, indice_vazio + 1)
        sucessores.append(("Mover vazio para direita", novo_estado))

    return sucessores
