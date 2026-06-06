# -*- coding: utf-8 -*-
"""ETAPAS 8, 9, 10 E EXTRA: interface gráfica com navegação, animação, comparação e embaralhamento."""

import tkinter as tk
from tkinter import messagebox, ttk

from agente_astar import resolver_astar
from estado import ESTADO_OBJETIVO
from exemplos import gerar_estado_embaralhado
from heuristicas import distancia_manhattan, distancia_manhattan_nao_admissivel

TITULO_PROJETO = "AGENTE A* — QUEBRA-CABEÇA DE 8 PEÇAS"
INTERVALO_AUTOMATICO_MS = 1000

COR_FUNDO = "#f4efe6"
COR_TEXTO = "#2a231d"
COR_PECA = "#dac6ad"
COR_VAZIO = "#fbf8f2"
COR_DESTAQUE = "#e6bc59"
COR_DESTAQUE_VAZIO = "#f6df95"
COR_ACAO = "#8e4f1a"

HEURISTICAS_DISPONIVEIS = {
    "manhattan": {
        "titulo": "Distância de Manhattan admissível",
        "funcao": distancia_manhattan,
    },
    "manhattan_x2": {
        "titulo": "Distância de Manhattan multiplicada por 2",
        "funcao": distancia_manhattan_nao_admissivel,
    },
}


def formatar_tabuleiro_em_bloco(estado):
    """Converte um estado em texto de três linhas."""
    linhas = []
    for indice in range(0, 9, 3):
        linha = estado[indice:indice + 3]
        linhas.append(" ".join(str(valor) for valor in linha))
    return "\n".join(linhas)


def resumir_resultado_comparativo(chave_heuristica, resultado):
    """Monta o resumo textual para a área comparativa."""
    titulo = HEURISTICAS_DISPONIVEIS[chave_heuristica]["titulo"]
    custo_total = resultado["custo_total"] if resultado["custo_total"] is not None else "—"
    quantidade_movimentos = custo_total

    return (
        f"Heurística utilizada: {titulo}\n"
        f"Custo total: {custo_total}\n"
        f"Quantidade de movimentos: {quantidade_movimentos}\n"
        f"Estados expandidos: {resultado['estados_expandidos']}\n"
        f"Quantidade de etapas registradas: {len(resultado['historico'])}"
    )


class InterfaceAStar:
    """Controla a interface gráfica sem misturar a lógica visual com o algoritmo."""

    def __init__(self, janela):
        self.janela = janela
        self.janela.title(TITULO_PROJETO)
        self.janela.geometry("1180x760")
        self.janela.minsize(980, 680)
        self.janela.configure(bg=COR_FUNDO)

        self.estado_inicial_atual = gerar_estado_embaralhado(movimentos=20)
        self.resultado_busca = None
        self.indice_etapa_atual = 0
        self.execucao_automatica_ativa = False
        self.identificador_after = None
        self.heuristica_var = tk.StringVar(value="manhattan")

        self.labels_tabuleiro = []
        self.valores_info = {}
        self.label_movimento_destacado = None
        self.label_estado_atual = None
        self.texto_open = None
        self.texto_closed = None
        self.texto_caminho = None
        self.texto_comparacao_esquerda = None
        self.texto_comparacao_direita = None
        self.label_observacao = None

        self._criar_estilo()
        self._criar_layout()
        self._reiniciar_interface_visual()

    def _criar_estilo(self):
        """Define o estilo visual principal da interface."""
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Painel.TLabelframe", background=COR_FUNDO, borderwidth=2)
        estilo.configure(
            "Painel.TLabelframe.Label",
            background=COR_FUNDO,
            foreground=COR_TEXTO,
            font=("Georgia", 10, "bold"),
        )
        estilo.configure(
            "Titulo.TLabel",
            background=COR_FUNDO,
            foreground=COR_TEXTO,
            font=("Georgia", 15, "bold"),
        )
        estilo.configure(
            "InfoNome.TLabel",
            background=COR_FUNDO,
            foreground="#5b5248",
            font=("Georgia", 9, "bold"),
        )
        estilo.configure(
            "InfoValor.TLabel",
            background=COR_FUNDO,
            foreground=COR_TEXTO,
            font=("Consolas", 10),
        )
        estilo.configure(
            "Acao.TButton",
            font=("Georgia", 9, "bold"),
            padding=6,
        )
        estilo.configure(
            "Opcao.TRadiobutton",
            background=COR_FUNDO,
            foreground=COR_TEXTO,
            font=("Georgia", 9),
        )

    def _criar_layout(self):
        """Monta os painéis principais da janela."""
        titulo = ttk.Label(
            self.janela,
            text=TITULO_PROJETO,
            style="Titulo.TLabel",
            anchor="center",
        )
        titulo.pack(fill="x", padx=14, pady=(10, 6))

        corpo = tk.Frame(self.janela, bg=COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        corpo.grid_columnconfigure(0, weight=3)
        corpo.grid_columnconfigure(1, weight=2)
        corpo.grid_rowconfigure(0, weight=1)

        painel_esquerdo = tk.Frame(corpo, bg=COR_FUNDO)
        painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        painel_esquerdo.grid_columnconfigure(0, weight=1)

        painel_direito = tk.Frame(corpo, bg=COR_FUNDO)
        painel_direito.grid(row=0, column=1, sticky="nsew")
        painel_direito.grid_columnconfigure(0, weight=1)
        for linha in range(4):
            painel_direito.grid_rowconfigure(linha, weight=1)

        self._criar_painel_tabuleiro_e_heuristica(painel_esquerdo)
        self._criar_painel_informacoes(painel_esquerdo)
        self._criar_painel_controles(painel_esquerdo)

        self.texto_open = self._criar_painel_texto(
            painel_direito,
            "Open List resumida",
            "Mostra os próximos estados que ainda podem ser explorados pela busca.",
            0,
            8,
        )
        self.texto_closed = self._criar_painel_texto(
            painel_direito,
            "Closed List resumida",
            "Mostra os estados que já foram expandidos e analisados pelo algoritmo.",
            1,
            8,
        )
        self._criar_painel_comparacao(painel_direito, 2)
        self.texto_caminho = self._criar_painel_texto(
            painel_direito,
            "Caminho final",
            "Apresenta a sequência de passos da solução encontrada até o estado objetivo.",
            3,
            8,
        )

    def _criar_painel_tabuleiro_e_heuristica(self, container):
        """Cria o tabuleiro visual e a seleção da heurística."""
        quadro = ttk.LabelFrame(
            container,
            text="Tabuleiro e heurística",
            style="Painel.TLabelframe",
        )
        quadro.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        quadro.grid_columnconfigure(0, weight=1)

        area_tabuleiro = tk.Frame(quadro, bg=COR_FUNDO)
        area_tabuleiro.grid(row=0, column=0, padx=12, pady=(10, 6), sticky="w")

        for indice in range(9):
            linha = indice // 3
            coluna = indice % 3
            label = tk.Label(
                area_tabuleiro,
                width=3,
                height=1,
                relief="ridge",
                borderwidth=2,
                font=("Georgia", 20, "bold"),
                bg=COR_PECA,
                fg=COR_TEXTO,
                padx=12,
                pady=10,
            )
            label.grid(row=linha, column=coluna, padx=4, pady=4, sticky="nsew")
            self.labels_tabuleiro.append(label)

        area_opcoes = tk.Frame(quadro, bg=COR_FUNDO)
        area_opcoes.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="ew")
        area_opcoes.grid_columnconfigure(0, weight=1)

        ttk.Label(
            area_opcoes,
            text="Seleção da heurística",
            style="InfoNome.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        ttk.Radiobutton(
            area_opcoes,
            text="Distância de Manhattan admissível",
            variable=self.heuristica_var,
            value="manhattan",
            style="Opcao.TRadiobutton",
        ).grid(row=1, column=0, sticky="w", pady=2)

        ttk.Radiobutton(
            area_opcoes,
            text="Distância de Manhattan multiplicada por 2",
            variable=self.heuristica_var,
            value="manhattan_x2",
            style="Opcao.TRadiobutton",
        ).grid(row=2, column=0, sticky="w", pady=2)

        self.label_estado_atual = tk.Label(
            area_opcoes,
            text="Estado atual: embaralhado para teste",
            justify="left",
            wraplength=420,
            bg=COR_FUNDO,
            fg="#5b5248",
            font=("Georgia", 10, "bold"),
        )
        self.label_estado_atual.grid(row=3, column=0, sticky="w", pady=(10, 2))

        self.label_movimento_destacado = tk.Label(
            area_opcoes,
            text="Movimento destacado: aguardando início",
            justify="left",
            wraplength=420,
            bg=COR_FUNDO,
            fg=COR_ACAO,
            font=("Georgia", 11, "bold"),
        )
        self.label_movimento_destacado.grid(row=4, column=0, sticky="w", pady=(4, 4))

    def _criar_painel_informacoes(self, container):
        """Cria o painel com os dados resumidos da etapa atual."""
        quadro = ttk.LabelFrame(
            container,
            text="Painel de informações",
            style="Painel.TLabelframe",
        )
        quadro.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        quadro.grid_columnconfigure(1, weight=1)

        campos = [
            "Movimento atual",
            "g(n)",
            "h(n)",
            "f(n)",
            "Número da etapa",
            "Estados expandidos",
            "Quantidade de estados na Open List",
            "Quantidade de estados na Closed List",
            "Heurística selecionada",
        ]

        for linha, nome_campo in enumerate(campos):
            ttk.Label(
                quadro,
                text=f"{nome_campo}:",
                style="InfoNome.TLabel",
            ).grid(row=linha, column=0, sticky="w", padx=12, pady=4)

            valor = ttk.Label(
                quadro,
                text="—",
                style="InfoValor.TLabel",
            )
            valor.grid(row=linha, column=1, sticky="w", padx=(0, 12), pady=4)
            self.valores_info[nome_campo] = valor

    def _criar_painel_controles(self, container):
        """Cria os botões de controle da execução."""
        quadro = ttk.LabelFrame(
            container,
            text="Botões de controle",
            style="Painel.TLabelframe",
        )
        quadro.grid(row=2, column=0, sticky="ew")

        botoes = [
            ("Iniciar", self.iniciar_busca),
            ("Próximo passo", self.proximo_passo),
            ("Passo anterior", self.passo_anterior),
            ("Executar automático", self.executar_automatico),
            ("Pausar", self.pausar_execucao),
            ("Reiniciar", self.reiniciar),
            ("Embaralhar", self.embaralhar_estado),
            ("Comparar heurísticas", self.comparar_heuristicas),
        ]

        for indice, (texto, comando) in enumerate(botoes):
            botao = ttk.Button(
                quadro,
                text=texto,
                command=comando,
                style="Acao.TButton",
            )
            botao.grid(
                row=indice // 3,
                column=indice % 3,
                padx=6,
                pady=8,
                sticky="ew",
            )
            quadro.grid_columnconfigure(indice % 3, weight=1)

    def _criar_painel_texto(self, container, titulo, descricao, linha, altura):
        """Cria um painel de texto com rolagem vertical."""
        quadro = ttk.LabelFrame(
            container,
            text=titulo,
            style="Painel.TLabelframe",
        )
        quadro.grid(row=linha, column=0, sticky="nsew", pady=(0, 10) if linha < 3 else 0)
        quadro.grid_rowconfigure(1, weight=1)
        quadro.grid_columnconfigure(0, weight=1)

        label_descricao = tk.Label(
            quadro,
            text=descricao,
            justify="left",
            wraplength=380,
            bg=COR_FUNDO,
            fg="#5a5148",
            font=("Georgia", 9),
        )
        label_descricao.grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2))

        texto = tk.Text(
            quadro,
            wrap="word",
            height=altura,
            font=("Consolas", 9),
            bg="#fffdf8",
            fg=COR_TEXTO,
            relief="flat",
            padx=8,
            pady=8,
        )
        texto.grid(row=1, column=0, sticky="nsew")

        barra = ttk.Scrollbar(quadro, orient="vertical", command=texto.yview)
        barra.grid(row=1, column=1, sticky="ns")
        texto.configure(yscrollcommand=barra.set, state="disabled")
        return texto

    def _criar_painel_comparacao(self, container, linha):
        """Cria a área comparativa com resultados lado a lado."""
        quadro = ttk.LabelFrame(
            container,
            text="Área comparativa",
            style="Painel.TLabelframe",
        )
        quadro.grid(row=linha, column=0, sticky="nsew", pady=(0, 10))
        quadro.grid_columnconfigure(0, weight=1)
        quadro.grid_columnconfigure(1, weight=1)
        quadro.grid_rowconfigure(1, weight=1)

        label_descricao = tk.Label(
            quadro,
            text=(
                "Compara lado a lado os resultados das duas heurísticas, "
                "incluindo custo, movimentos e estados expandidos."
            ),
            justify="left",
            wraplength=420,
            bg=COR_FUNDO,
            fg="#5a5148",
            font=("Georgia", 9),
        )
        label_descricao.grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2))

        self.texto_comparacao_esquerda = self._criar_texto_interno(quadro, 0, 1)
        self.texto_comparacao_direita = self._criar_texto_interno(quadro, 1, 1)

        self.label_observacao = tk.Label(
            quadro,
            text="As observações comparativas aparecerão após a execução da comparação.",
            justify="left",
            wraplength=420,
            bg=COR_FUNDO,
            fg="#5a5148",
            font=("Georgia", 9),
        )
        self.label_observacao.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 2))

    def _criar_texto_interno(self, container, coluna, linha):
        """Cria um painel de texto interno da comparação."""
        texto = tk.Text(
            container,
            wrap="word",
            height=7,
            font=("Consolas", 9),
            bg="#fffdf8",
            fg=COR_TEXTO,
            relief="flat",
            padx=8,
            pady=8,
        )
        texto.grid(row=linha, column=coluna, sticky="nsew", padx=(0, 4) if coluna == 0 else (4, 0))
        texto.configure(state="disabled")
        return texto

    def _reiniciar_interface_visual(self):
        """Restaura a interface para o estado inicial visual."""
        self._atualizar_tabuleiro(self.estado_inicial_atual, set())
        self.label_estado_atual.config(text="Estado atual: embaralhado para teste")
        self.label_movimento_destacado.config(text="Movimento destacado: aguardando início")

        for nome_campo, label in self.valores_info.items():
            if nome_campo == "Heurística selecionada":
                label.config(text=self._titulo_heuristica_atual())
            else:
                label.config(text="—")

        self._preencher_texto(self.texto_open, "A Open List resumida aparecerá após iniciar a busca.")
        self._preencher_texto(self.texto_closed, "A Closed List resumida aparecerá após iniciar a busca.")
        self._preencher_texto(self.texto_caminho, "O caminho final será exibido após a execução.")
        self._preencher_texto(self.texto_comparacao_esquerda, "Resultado da heurística 1 aparecerá aqui.")
        self._preencher_texto(self.texto_comparacao_direita, "Resultado da heurística 2 aparecerá aqui.")
        self.label_observacao.config(
            text="As observações comparativas aparecerão após a execução da comparação."
        )

    def _preencher_texto(self, widget_texto, conteudo):
        """Atualiza o conteúdo de um painel de texto."""
        widget_texto.config(state="normal")
        widget_texto.delete("1.0", tk.END)
        widget_texto.insert("1.0", conteudo)
        widget_texto.config(state="disabled")

    def _titulo_heuristica_atual(self):
        """Retorna o título da heurística atualmente selecionada."""
        return HEURISTICAS_DISPONIVEIS[self.heuristica_var.get()]["titulo"]

    def _atualizar_tabuleiro(self, estado, indices_destacados):
        """Atualiza o tabuleiro visual e destaca as posições alteradas."""
        for indice, (label, valor) in enumerate(zip(self.labels_tabuleiro, estado)):
            destacado = indice in indices_destacados

            if valor == 0:
                label.config(
                    text="",
                    bg=COR_DESTAQUE_VAZIO if destacado else COR_VAZIO,
                    relief="sunken",
                )
            else:
                label.config(
                    text=str(valor),
                    bg=COR_DESTAQUE if destacado else COR_PECA,
                    fg=COR_TEXTO,
                    relief="ridge",
                )

    def _obter_item_historico_atual(self):
        """Retorna o item atual do histórico, quando disponível."""
        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return None
        return self.resultado_busca["historico"][self.indice_etapa_atual]

    def _obter_estado_anterior(self):
        """Retorna o estado da etapa anterior para calcular o destaque do movimento."""
        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return None
        if self.indice_etapa_atual == 0:
            return None
        return self.resultado_busca["historico"][self.indice_etapa_atual - 1]["estado_atual"]

    def _calcular_indices_destacados(self, estado_atual):
        """Calcula quais posições mudaram em relação à etapa anterior."""
        estado_anterior = self._obter_estado_anterior()
        if estado_anterior is None:
            return set()

        return {
            indice
            for indice, (anterior, atual) in enumerate(zip(estado_anterior, estado_atual))
            if anterior != atual
        }

    def _atualizar_info_etapa(self):
        """Mostra as informações da etapa atual no painel de dados."""
        item = self._obter_item_historico_atual()
        if item is None:
            return

        descricao_acao = item["acao"] or "Estado inicial"
        self.valores_info["Movimento atual"].config(text=descricao_acao)
        self.valores_info["g(n)"].config(text=str(item["g"]))
        self.valores_info["h(n)"].config(text=str(item["h"]))
        self.valores_info["f(n)"].config(text=str(item["f"]))
        self.valores_info["Número da etapa"].config(text=str(item["numero_etapa"]))
        self.valores_info["Estados expandidos"].config(text=str(item["numero_etapa"] + 1))
        self.valores_info["Quantidade de estados na Open List"].config(text=str(item["quantidade_open"]))
        self.valores_info["Quantidade de estados na Closed List"].config(text=str(item["quantidade_closed"]))
        self.valores_info["Heurística selecionada"].config(text=self._titulo_heuristica_atual())
        self.label_movimento_destacado.config(text=f"Movimento destacado: {descricao_acao}")

    def _formatar_lista_resumida(self, estados):
        """Transforma uma lista de estados em texto legível."""
        if not estados:
            return "(vazia)"

        blocos = []
        for indice, estado in enumerate(estados, start=1):
            blocos.append(f"Estado {indice}\n{formatar_tabuleiro_em_bloco(estado)}")
        return "\n\n".join(blocos)

    def _atualizar_paineis_resumidos(self):
        """Atualiza Open List e Closed List com base na etapa atual."""
        item = self._obter_item_historico_atual()
        if item is None:
            return

        self._preencher_texto(self.texto_open, self._formatar_lista_resumida(item["open_resumida"]))
        self._preencher_texto(self.texto_closed, self._formatar_lista_resumida(item["closed_resumida"]))

    def _atualizar_painel_caminho(self):
        """Mostra o caminho final completo retornado pela busca."""
        if not self.resultado_busca:
            return

        if not self.resultado_busca["encontrou_solucao"]:
            self._preencher_texto(self.texto_caminho, f"Erro: {self.resultado_busca['mensagem']}")
            return

        blocos = []
        for indice, passo in enumerate(self.resultado_busca["caminho"]):
            descricao = passo["acao"] or "Estado inicial"
            blocos.append(
                f"Passo {indice} — {descricao}\n"
                f"{formatar_tabuleiro_em_bloco(passo['estado'])}\n"
                f"g={passo['g']}  h={passo['h']}  f={passo['f']}"
            )

        self._preencher_texto(self.texto_caminho, "\n\n".join(blocos))

    def _mostrar_etapa_atual(self):
        """Atualiza tabuleiro, painéis e destaque visual da etapa atual."""
        item = self._obter_item_historico_atual()
        if item is None:
            return

        indices_destacados = self._calcular_indices_destacados(item["estado_atual"])
        self._atualizar_tabuleiro(item["estado_atual"], indices_destacados)
        self._atualizar_info_etapa()
        self._atualizar_paineis_resumidos()
        self._atualizar_painel_caminho()

    def _executar_busca_por_chave(self, chave_heuristica):
        """Executa a busca usando a heurística indicada."""
        funcao_heuristica = HEURISTICAS_DISPONIVEIS[chave_heuristica]["funcao"]
        return resolver_astar(
            estado_inicial=self.estado_inicial_atual,
            estado_objetivo=ESTADO_OBJETIVO,
            funcao_heuristica=funcao_heuristica,
            registrar_historico=True,
        )

    def iniciar_busca(self):
        """Executa a busca da heurística atualmente selecionada."""
        self.pausar_execucao()
        self.resultado_busca = self._executar_busca_por_chave(self.heuristica_var.get())
        self.indice_etapa_atual = 0
        self._atualizar_painel_caminho()

        if not self.resultado_busca["historico"]:
            self._preencher_texto(self.texto_open, "Sem histórico disponível para este caso.")
            self._preencher_texto(self.texto_closed, "Sem histórico disponível para este caso.")
            self.valores_info["Heurística selecionada"].config(text=self._titulo_heuristica_atual())
            messagebox.showerror("Busca A*", self.resultado_busca["mensagem"])
            return

        self._mostrar_etapa_atual()

        if not self.resultado_busca["encontrou_solucao"]:
            messagebox.showerror("Busca A*", self.resultado_busca["mensagem"])

    def proximo_passo(self):
        """Avança manualmente para a próxima etapa registrada."""
        if not self.resultado_busca:
            self.iniciar_busca()
            return

        if not self.resultado_busca["historico"]:
            return

        if self.indice_etapa_atual < len(self.resultado_busca["historico"]) - 1:
            self.indice_etapa_atual += 1
            self._mostrar_etapa_atual()

    def passo_anterior(self):
        """Retorna manualmente para a etapa anterior registrada."""
        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return

        if self.indice_etapa_atual > 0:
            self.indice_etapa_atual -= 1
            self._mostrar_etapa_atual()

    def _executar_automatico_loop(self):
        """Anima a navegação pelo histórico usando after()."""
        if not self.execucao_automatica_ativa:
            return

        if not self.resultado_busca:
            self.iniciar_busca()

        if not self.resultado_busca or not self.resultado_busca["historico"]:
            self.execucao_automatica_ativa = False
            self.identificador_after = None
            return

        if self.indice_etapa_atual >= len(self.resultado_busca["historico"]) - 1:
            self.execucao_automatica_ativa = False
            self.identificador_after = None
            return

        self.proximo_passo()
        self.identificador_after = self.janela.after(
            INTERVALO_AUTOMATICO_MS,
            self._executar_automatico_loop,
        )

    def executar_automatico(self):
        """Inicia a animação automática com intervalo aproximado de um segundo."""
        if not self.resultado_busca:
            self.iniciar_busca()

        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return

        if self.execucao_automatica_ativa:
            return

        self.execucao_automatica_ativa = True
        self._executar_automatico_loop()

    def pausar_execucao(self):
        """Pausa a animação automática."""
        self.execucao_automatica_ativa = False
        if self.identificador_after is not None:
            self.janela.after_cancel(self.identificador_after)
            self.identificador_after = None

    def reiniciar(self):
        """Reinicia a execução e a visualização da interface mantendo o mesmo tabuleiro."""
        self.pausar_execucao()
        self.resultado_busca = None
        self.indice_etapa_atual = 0
        self._reiniciar_interface_visual()

    def embaralhar_estado(self):
        """Gera um novo estado inicial embaralhado para testes."""
        self.pausar_execucao()
        self.estado_inicial_atual = gerar_estado_embaralhado(movimentos=20)
        self.resultado_busca = None
        self.indice_etapa_atual = 0
        self._reiniciar_interface_visual()

    def comparar_heuristicas(self):
        """Executa as duas heurísticas e mostra os resultados lado a lado."""
        self.pausar_execucao()

        resultado_manhattan = self._executar_busca_por_chave("manhattan")
        resultado_manhattan_x2 = self._executar_busca_por_chave("manhattan_x2")

        self._preencher_texto(
            self.texto_comparacao_esquerda,
            resumir_resultado_comparativo("manhattan", resultado_manhattan),
        )
        self._preencher_texto(
            self.texto_comparacao_direita,
            resumir_resultado_comparativo("manhattan_x2", resultado_manhattan_x2),
        )

        observacao = (
            "Observações:\n"
            "• A heurística admissível não superestima o custo real.\n"
            "• A heurística não admissível pode superestimar o custo.\n"
            "• A heurística não admissível não garante a melhor solução.\n"
            "• Dependendo do tabuleiro utilizado, as duas heurísticas podem encontrar o mesmo caminho."
        )
        self.label_observacao.config(text=observacao)


def executar_interface():
    """Cria e inicia a janela principal da interface."""
    janela = tk.Tk()
    InterfaceAStar(janela)
    janela.mainloop()


if __name__ == "__main__":
    executar_interface()
