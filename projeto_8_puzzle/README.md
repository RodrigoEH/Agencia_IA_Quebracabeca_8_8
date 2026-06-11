# Projeto 8 Puzzle com Agente A*

## Nome do projeto
Agente A* para o Quebra-Cabeça de 8 Peças

## Integrantes
Enzo Féola Tiburcio
Jenniffer Karolayne de Sousa Pereira
João Victor Barreto Vaz
Luana Victoria Sousa Beck
Rodrigo Eiji Hirata

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

## Como utilizar o sistema
### Uso pelo terminal
1. Execute o arquivo principal:

```bash
python projeto_8_puzzle/main.py
```

2. Escolha se deseja usar um estado inicial embaralhado ou o exemplo fixo.
3. Escolha se deseja exibir o histórico detalhado das expansões.
4. Observe no terminal:
   - o estado inicial;
   - o estado objetivo;
   - a heurística utilizada;
   - o caminho final da solução;
   - o custo total;
   - a quantidade de estados expandidos.

### Uso pela interface gráfica
1. Abra a interface:

```bash
python projeto_8_puzzle/interface.py
```

2. Selecione a heurística desejada.
3. Clique em `Iniciar` para executar a busca.
4. Use:
   - `Próximo passo` para avançar manualmente;
   - `Passo anterior` para voltar;
   - `Executar automático` para animar;
   - `Pausar` para parar a animação;
   - `Reiniciar` para limpar a execução atual;
   - `Embaralhar` para gerar um novo tabuleiro inicial;
   - `Comparar heurísticas` para ver os resultados lado a lado.
5. Use os modos:
   - `Ver caminho final` para acompanhar apenas a solução correta;
   - `Ver análise da busca` para observar os estados internos explorados pelo A*.
6. Em telas menores, a interface reorganiza os painéis e os botões automaticamente.
7. Se a altura da tela não for suficiente, use a roda do mouse para rolar a janela e visualizar todo o conteúdo.

## Explicação da interface gráfica
`Open List resumida`: mostra os próximos estados que ainda podem ser explorados pelo algoritmo A*.

`Closed List resumida`: mostra os estados que já foram expandidos e analisados pela busca.

`Área comparativa`: exibe, lado a lado, os resultados das duas heurísticas para facilitar a comparação.

`Caminho final`: apresenta a sequência de estados da solução encontrada, do estado inicial até o objetivo.

`Layout responsivo`: reorganiza os painéis e redistribui os botões de controle em resoluções menores, evitando cortes na visualização.

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
