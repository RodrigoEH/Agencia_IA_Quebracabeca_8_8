# Projeto 8 Puzzle com Agente A*

## Nome do projeto
Agente A* para o Quebra-Cabeça de 8 Peças

## Integrantes
Preencher com os nomes dos integrantes da equipe.

## Orientação para grupos de desenvolvedores
Este projeto está público.

Isso significa que:

- o código pode ser acessado pelos integrantes do grupo e por avaliadores;
- o projeto pode ser estudado, executado e testado livremente;
- novas melhorias podem ser feitas em equipe a partir desta base;
- recomenda-se manter os créditos do grupo autor e registrar claramente futuras alterações.

## Linguagem utilizada
Python 3

## Como executar
No terminal, entre na pasta raiz do projeto e execute:

```bash
python projeto_8_puzzle/main.py
```

Para abrir a interface gráfica:

```bash
python projeto_8_puzzle/interface.py
```

## Explicação da interface gráfica
`Open List resumida`: mostra os próximos estados que ainda podem ser explorados pelo algoritmo A*.

`Closed List resumida`: mostra os estados que já foram expandidos e analisados pela busca.

`Área comparativa`: exibe, lado a lado, os resultados das duas heurísticas para facilitar a comparação.

`Caminho final`: apresenta a sequência de estados da solução encontrada, do estado inicial até o objetivo.

## Arquivo principal
`projeto_8_puzzle/main.py`

## Problema resolvido
Resolver automaticamente o Quebra-Cabeça de 8 Peças usando o algoritmo A*.

## Heurística admissível utilizada
Distância de Manhattan.

## Heurística não admissível utilizada
Distância de Manhattan multiplicada por 2.

## Custo com heurística admissível
No estado inicial de exemplo, o custo encontrado foi `2`.

## Custo com heurística não admissível
No estado inicial de exemplo, o custo encontrado também foi `2`.

## Observação sobre a comparação
A heurística admissível não superestima o custo real. A heurística não admissível pode superestimar o custo e não garante a melhor solução. Dependendo do tabuleiro analisado, as duas heurísticas podem encontrar o mesmo caminho, como acontece no exemplo atual.

## Como executar os testes
No terminal, execute:

```bash
python -m unittest discover projeto_8_puzzle/testes
```
