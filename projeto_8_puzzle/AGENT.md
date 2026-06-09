
# Projeto de Inteligência Artificial — Agente A* para o Quebra-Cabeça de 8 Peças

Desenvolver um projeto em Python 3 para resolver o Quebra-Cabeça de 8 Peças utilizando o algoritmo A*.

O projeto deve ser desenvolvido gradualmente. Não implemente todas as etapas de uma vez. Em cada etapa:

1. Informe quais arquivos serão criados ou alterados.
2. Explique resumidamente o que foi implementado.
3. Apresente o código completo dos arquivos modificados.
4. Informe como executar e testar a etapa.
5. Não altere funcionalidades prontas sem necessidade.
6. Utilize codificação UTF-8 para manter corretamente os acentos em português.
7. Utilize preferencialmente apenas bibliotecas nativas do Python.
8. Mantenha a lógica do algoritmo separada da interface gráfica.
9. Utilize nomes de funções, classes e variáveis em português para facilitar a explicação do grupo.
10. Não avance para a próxima etapa até que eu solicite.

A estrutura desejada inicialmente é:

```text
projeto_8_puzzle/
│
├── main.py
├── estado.py
├── heuristicas.py
├── agente_astar.py
├── exemplos.py
├── interface.py
├── testes/
│   ├── test_estado.py
│   └── test_astar.py
└── README.md
```

O estado inicial utilizado como exemplo será:

```text
1 2 3
4 0 6
7 5 8
```

O estado objetivo será:

```text
1 2 3
4 5 6
7 8 0
```

O valor `0` representa o espaço vazio.

Cada movimento válido possui custo igual a `1`.

---

# ETAPA 1 — Criar a estrutura inicial do projeto

Crie a estrutura básica do projeto em Python.

Nesta primeira etapa:

* crie os arquivos principais;
* implemente apenas um `main.py` simples;
* adicione uma mensagem inicial;
* mostre o estado inicial e o estado objetivo no terminal;
* não implemente ainda o algoritmo A*;
* não crie ainda a interface gráfica.

O terminal deve mostrar algo semelhante a:

```text
========================================
AGENTE A* — QUEBRA-CABEÇA DE 8 PEÇAS
========================================

Estado inicial:
1 2 3
4 0 6
7 5 8

Estado objetivo:
1 2 3
4 5 6
7 8 0
```

Ao finalizar, explique como executar o programa pelo terminal.

---

# ETAPA 2 — Representar e validar os estados

Agora implemente o arquivo `estado.py`.

Utilize uma tupla imutável com nove números inteiros para representar internamente o tabuleiro:

```python
(1, 2, 3, 4, 0, 6, 7, 5, 8)
```

A representação deve ser imutável para permitir o uso do estado em conjuntos e dicionários.

Implemente funções para:

* validar se o estado possui exatamente nove posições;
* verificar se os números de `0` a `8` aparecem exatamente uma vez;
* formatar o estado visualmente em três linhas e três colunas;
* localizar a posição atual do espaço vazio;
* verificar se o estado já corresponde ao objetivo;
* verificar se uma configuração é solucionável utilizando a quantidade de inversões.

Adicione exemplos de testes manuais no arquivo `main.py`.

Não implemente ainda o A*.

---

# ETAPA 3 — Implementar os movimentos possíveis

Atualize o arquivo `estado.py`.

Implemente uma função que gere os estados sucessores a partir de um estado atual.

O espaço vazio pode executar quatro ações:

* mover para cima;
* mover para baixo;
* mover para esquerda;
* mover para direita.

Cada movimento deve trocar o valor `0` com uma peça vizinha.

A função deve retornar uma lista contendo:

```python
[
    ("Mover vazio para cima", novo_estado),
    ("Mover vazio para baixo", novo_estado)
]
```

Inclua apenas movimentos válidos.

Exemplos:

* se o espaço vazio estiver na primeira linha, não pode subir;
* se estiver na última linha, não pode descer;
* se estiver na primeira coluna, não pode ir para a esquerda;
* se estiver na última coluna, não pode ir para a direita.

Mostre pelo terminal os sucessores do estado inicial.

---

# ETAPA 4 — Criar as funções heurísticas

Implemente o arquivo `heuristicas.py`.

Crie duas funções:

```python
distancia_manhattan(estado, objetivo)
distancia_manhattan_nao_admissivel(estado, objetivo)
```

A função `distancia_manhattan()` deve:

* ignorar a peça vazia `0`;
* calcular a distância horizontal e vertical de cada peça até sua posição no objetivo;
* somar todas as distâncias;
* retornar um número inteiro.

A segunda função deve utilizar:

```python
2 * distancia_manhattan(estado, objetivo)
```

Essa será a heurística não admissível utilizada para comparação.

Adicione testes simples no terminal, mostrando o resultado das duas heurísticas para o estado inicial.

---

# ETAPA 5 — Implementar o algoritmo A*

Implemente o arquivo `agente_astar.py`.

Crie uma classe chamada `NoBusca` utilizando `dataclass`.

Cada nó deve armazenar:

```python
estado
pai
acao
g
h
f
```

Onde:

* `estado` representa a configuração atual;
* `pai` aponta para o nó anterior;
* `acao` informa o movimento realizado;
* `g` representa o custo acumulado;
* `h` representa a estimativa restante;
* `f` representa `g + h`.

Implemente o algoritmo A* utilizando:

* `heapq` para a Open List;
* `set` ou `dict` para a Closed List;
* um dicionário `melhor_g` para armazenar o melhor custo conhecido de cada estado;
* um contador incremental para desempatar nós com o mesmo valor de prioridade.

O algoritmo deve:

1. inserir o estado inicial na Open List;
2. retirar o nó com menor valor de `f`;
3. verificar se o nó retirado é o objetivo;
4. inserir o estado retirado na Closed List;
5. gerar sucessores válidos;
6. calcular `g`, `h` e `f`;
7. evitar caminhos repetidos ou mais caros;
8. repetir o processo até encontrar a solução;
9. reconstruir o caminho utilizando os nós pais.

A função principal pode possuir uma assinatura semelhante a:

```python
resolver_astar(
    estado_inicial,
    estado_objetivo,
    funcao_heuristica,
    registrar_historico=False
)
```

Ela deve retornar um objeto ou dicionário contendo:

```python
{
    "encontrou_solucao": True,
    "caminho": [...],
    "custo_total": 2,
    "estados_expandidos": 3,
    "historico": [...]
}
```

Antes de iniciar a busca, valide se o estado é solucionável.

---

# ETAPA 6 — Mostrar o resultado pelo terminal

Atualize o arquivo `main.py`.

Execute o A* inicialmente com a Distância de Manhattan admissível.

Mostre:

* estado inicial;
* estado objetivo;
* heurística utilizada;
* cada passo da solução;
* movimento realizado;
* valores de `g`, `h` e `f`;
* custo total;
* quantidade de estados expandidos;
* mensagem de erro caso não exista solução.

Exemplo simplificado:

```text
Passo 0 — Estado inicial
1 2 3
4 0 6
7 5 8

Passo 1 — Mover vazio para baixo
1 2 3
4 5 6
7 0 8

Passo 2 — Mover vazio para direita
1 2 3
4 5 6
7 8 0

Solução encontrada.
Custo total: 2 movimentos
Estados expandidos: 3
```

---

# ETAPA 7 — Registrar o histórico do algoritmo

Atualize o algoritmo para registrar o histórico resumido de cada expansão.

Cada item do histórico deve armazenar:

```python
{
    "numero_etapa": 0,
    "estado_atual": ...,
    "acao": ...,
    "g": ...,
    "h": ...,
    "f": ...,
    "open_resumida": [...],
    "closed_resumida": [...],
    "quantidade_open": 0,
    "quantidade_closed": 0
}
```

Para evitar excesso de informações na tela:

* mostre apenas os primeiros dez estados da Open List;
* mostre apenas os dez estados mais recentes da Closed List;
* mantenha também a quantidade total de itens em cada lista.

Adicione no terminal uma opção para ativar ou desativar a exibição detalhada do histórico.

---

# ETAPA 8 — Criar a interface gráfica com Tkinter

Agora implemente o arquivo `interface.py`.

Utilize Tkinter, sem bibliotecas externas.

Crie uma janela com:

* título do projeto;
* tabuleiro visual 3 × 3;
* painel de informações;
* painel resumido da Open List;
* painel resumido da Closed List;
* área para mostrar o caminho final;
* seleção da heurística;
* botões de controle.

A tela deve possuir os botões:

```text
Iniciar
Próximo passo
Passo anterior
Executar automático
Pausar
Reiniciar
```

O tabuleiro deve exibir as peças numeradas. A posição do valor `0` deve aparecer visualmente vazia.

O painel de informações deve mostrar:

```text
Movimento atual
g(n)
h(n)
f(n)
Número da etapa
Estados expandidos
Quantidade de estados na Open List
Quantidade de estados na Closed List
Heurística selecionada
```

Não misture a lógica do algoritmo com o código visual. A interface deve apenas consumir os dados registrados no histórico.

---

# ETAPA 9 — Adicionar navegação e animação

Atualize a interface gráfica.

Implemente:

* avanço manual com o botão `Próximo passo`;
* retorno com o botão `Passo anterior`;
* animação automática;
* pausa da animação;
* reinício da execução;
* intervalo aproximado de um segundo entre as etapas automáticas.

Utilize o método `after()` do Tkinter para a animação.

Não utilize `time.sleep()` na interface, pois isso pode travar a janela.

Ao mudar de etapa:

* atualize o tabuleiro;
* atualize os valores de `g`, `h` e `f`;
* atualize a Open List;
* atualize a Closed List;
* destaque o movimento executado.

---

# ETAPA 10 — Comparar as duas heurísticas

Atualize o projeto para executar duas versões:

```text
1. Distância de Manhattan admissível
2. Distância de Manhattan multiplicada por 2
```

Adicione uma seleção na interface utilizando botões de opção ou uma caixa de seleção.

Crie também uma área comparativa contendo:

```text
Heurística utilizada
Custo total
Quantidade de movimentos
Estados expandidos
Quantidade de etapas registradas
```

Permita executar cada heurística separadamente.

Adicione um botão:

```text
Comparar heurísticas
```

Ao clicar, mostre os resultados lado a lado.

Inclua uma observação textual:

* a heurística admissível não superestima o custo real;
* a heurística não admissível pode superestimar o custo;
* a heurística não admissível não garante a melhor solução;
* dependendo do tabuleiro utilizado, as duas heurísticas podem encontrar o mesmo caminho.

---

# ETAPA 11 — Criar testes automatizados e README

Implemente testes utilizando `unittest`.

No arquivo `test_estado.py`, verifique:

* validação de estados corretos;
* rejeição de estados repetidos;
* rejeição de estados com tamanho incorreto;
* localização do espaço vazio;
* movimentos válidos;
* detecção de estados solucionáveis e não solucionáveis.

No arquivo `test_astar.py`, verifique:

* solução do estado inicial de exemplo;
* custo total igual a `2`;
* caminho final correspondente ao objetivo;
* execução da heurística admissível;
* execução da heurística não admissível.

Crie o arquivo `README.md` contendo:

```text
Nome do projeto
Integrantes
Linguagem utilizada
Como executar
Arquivo principal
Problema resolvido
Heurística admissível utilizada
Heurística não admissível utilizada
Custo com heurística admissível
Custo com heurística não admissível
Observação sobre a comparação
Como executar os testes
```

---

# ETAPA 12 — Revisão final

Faça uma revisão completa do projeto.

Verifique:

1. se o programa inicia corretamente;
2. se o terminal funciona mesmo sem utilizar a interface;
3. se a janela gráfica funciona;
4. se o tabuleiro mostra corretamente o espaço vazio;
5. se os botões funcionam;
6. se a animação pode ser pausada;
7. se a Open List aparece resumidamente;
8. se a Closed List aparece resumidamente;
9. se o caminho encontrado está correto;
10. se o custo total aparece na tela;
11. se as duas heurísticas podem ser comparadas;
12. se os testes automatizados passam;
13. se o README está completo;
14. se todos os textos utilizam acentuação correta;
15. se o código possui comentários objetivos para facilitar a explicação no vídeo.

Ao finalizar, apresente:

* a árvore final de arquivos;
* os comandos necessários para executar o terminal;
* os comandos necessários para abrir a interface;
* os comandos para executar os testes;
* um resumo curto das principais funções;
* sugestões de quais telas mostrar durante o vídeo.
