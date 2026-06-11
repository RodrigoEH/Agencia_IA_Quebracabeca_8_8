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
        self.janela.configure(bg=COR_FUNDO)

        self.estado_inicial_atual = gerar_estado_embaralhado(movimentos=20)
        self.resultado_busca = None
        self.indice_solucao_atual = 0
        self.indice_analise_atual = 0
        self.execucao_automatica_ativa = False
        self.identificador_after = None
        self.heuristica_var = tk.StringVar(value="manhattan")
        self.modo_visualizacao_var = tk.StringVar(value="solucao")

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
        self.canvas_principal = None
        self.quadro_rolavel = None
        self.janela_canvas_id = None
        self.corpo = None
        self.painel_esquerdo = None
        self.painel_direito = None
        self.quadro_controles = None
        self.botoes_controle = []
        self.widgets_com_wrap = []

        self._configurar_janela_responsiva()
        self._criar_estilo()
        self._criar_layout()
        self._habilitar_rolagem_mouse()
        self._reiniciar_interface_visual()

    def _configurar_janela_responsiva(self):
        """ETAPA EXTRA: ajusta o tamanho inicial conforme a resolução da tela."""
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        largura_janela = min(1280, max(900, int(largura_tela * 0.94)))
        altura_janela = min(860, max(620, int(altura_tela * 0.90)))

        posicao_x = max((largura_tela - largura_janela) // 2, 0)
        posicao_y = max((altura_tela - altura_janela) // 2, 0)

        self.janela.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")
        self.janela.minsize(840, 620)

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

        area_rolagem = tk.Frame(self.janela, bg=COR_FUNDO)
        area_rolagem.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        area_rolagem.grid_rowconfigure(0, weight=1)
        area_rolagem.grid_columnconfigure(0, weight=1)

        self.canvas_principal = tk.Canvas(
            area_rolagem,
            bg=COR_FUNDO,
            highlightthickness=0,
        )
        barra_vertical = ttk.Scrollbar(
            area_rolagem,
            orient="vertical",
            command=self.canvas_principal.yview,
        )
        self.canvas_principal.configure(yscrollcommand=barra_vertical.set)

        self.canvas_principal.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")

        self.quadro_rolavel = tk.Frame(self.canvas_principal, bg=COR_FUNDO)
        self.janela_canvas_id = self.canvas_principal.create_window(
            (0, 0),
            window=self.quadro_rolavel,
            anchor="nw",
        )

        self.quadro_rolavel.bind("<Configure>", self._ao_configurar_conteudo)
        self.canvas_principal.bind("<Configure>", self._ao_configurar_canvas)
        self.janela.bind("<Configure>", self._ao_redimensionar_janela)

        self.corpo = tk.Frame(self.quadro_rolavel, bg=COR_FUNDO)
        self.corpo.pack(fill="both", expand=True)
        self.corpo.grid_columnconfigure(0, weight=3)
        self.corpo.grid_columnconfigure(1, weight=2)
        self.corpo.grid_rowconfigure(0, weight=1)

        self.painel_esquerdo = tk.Frame(self.corpo, bg=COR_FUNDO)
        self.painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.painel_esquerdo.grid_columnconfigure(0, weight=1)

        self.painel_direito = tk.Frame(self.corpo, bg=COR_FUNDO)
        self.painel_direito.grid(row=0, column=1, sticky="nsew")
        self.painel_direito.grid_columnconfigure(0, weight=1)
        for linha in range(4):
            self.painel_direito.grid_rowconfigure(linha, weight=1)

        self._criar_painel_tabuleiro_e_heuristica(self.painel_esquerdo)
        self._criar_painel_informacoes(self.painel_esquerdo)
        self._criar_painel_controles(self.painel_esquerdo)

        self.texto_open = self._criar_painel_texto(
            self.painel_direito,
            "Open List resumida",
            "Mostra os próximos estados que ainda podem ser explorados pela busca.",
            0,
            8,
        )
        self.texto_closed = self._criar_painel_texto(
            self.painel_direito,
            "Closed List resumida",
            "Mostra os estados que já foram expandidos e analisados pelo algoritmo.",
            1,
            8,
        )
        self._criar_painel_comparacao(self.painel_direito, 2)
        self.texto_caminho = self._criar_painel_texto(
            self.painel_direito,
            "Caminho final",
            "Apresenta a sequência de passos da solução encontrada até o estado objetivo.",
            3,
            8,
        )
        self._ajustar_layout_responsivo()

    def _ao_configurar_conteudo(self, _evento):
        """Atualiza a região rolável sempre que o conteúdo muda."""
        self.canvas_principal.configure(scrollregion=self.canvas_principal.bbox("all"))

    def _ao_configurar_canvas(self, evento):
        """Mantém a largura do conteúdo alinhada ao espaço visível do canvas."""
        self.canvas_principal.itemconfigure(self.janela_canvas_id, width=evento.width)
        self._ajustar_layout_responsivo()

    def _ao_redimensionar_janela(self, evento):
        """Reorganiza a interface quando a janela muda de tamanho."""
        if evento.widget == self.janela:
            self._ajustar_layout_responsivo()

    def _habilitar_rolagem_mouse(self):
        """Permite rolagem com a roda do mouse."""
        self.canvas_principal.bind_all("<MouseWheel>", self._rolar_mousewheel)

    def _rolar_mousewheel(self, evento):
        """Executa a rolagem vertical da interface."""
        if self.canvas_principal is None:
            return
        self.canvas_principal.yview_scroll(int(-1 * (evento.delta / 120)), "units")

    def _registrar_widget_com_wrap(self, widget, largura_ampla, largura_estreita):
        """Guarda widgets que precisam adaptar a quebra de linha."""
        self.widgets_com_wrap.append((widget, largura_ampla, largura_estreita))

    def _ajustar_layout_responsivo(self):
        """ETAPA EXTRA: reorganiza o conteúdo para telas menores."""
        if self.corpo is None:
            return

        largura_atual = max(self.janela.winfo_width(), self.janela.winfo_reqwidth())
        modo_estreito = largura_atual < 1180

        self.painel_esquerdo.grid_forget()
        self.painel_direito.grid_forget()

        if modo_estreito:
            self.corpo.grid_columnconfigure(0, weight=1)
            self.corpo.grid_columnconfigure(1, weight=0)
            self.painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 10))
            self.painel_direito.grid(row=1, column=0, sticky="nsew", padx=0)
            colunas_botoes = 2
        else:
            self.corpo.grid_columnconfigure(0, weight=3)
            self.corpo.grid_columnconfigure(1, weight=2)
            self.painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
            self.painel_direito.grid(row=0, column=1, sticky="nsew", padx=0)
            colunas_botoes = 3

        self._organizar_botoes_controle(colunas_botoes)

        for widget, largura_ampla, largura_estreita in self.widgets_com_wrap:
            widget.configure(wraplength=largura_estreita if modo_estreito else largura_ampla)

    def _organizar_botoes_controle(self, quantidade_colunas):
        """Redistribui os botões para caber melhor em telas estreitas."""
        if self.quadro_controles is None or not self.botoes_controle:
            return

        for indice_coluna in range(4):
            self.quadro_controles.grid_columnconfigure(indice_coluna, weight=0)

        for indice, botao in enumerate(self.botoes_controle):
            linha = indice // quantidade_colunas
            coluna = indice % quantidade_colunas
            botao.grid_configure(row=linha, column=coluna, padx=6, pady=8, sticky="ew")

        for indice_coluna in range(quantidade_colunas):
            self.quadro_controles.grid_columnconfigure(indice_coluna, weight=1)

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

        ttk.Label(
            area_opcoes,
            text="Modo de visualização",
            style="InfoNome.TLabel",
        ).grid(row=3, column=0, sticky="w", pady=(8, 4))

        ttk.Radiobutton(
            area_opcoes,
            text="Ver caminho final",
            variable=self.modo_visualizacao_var,
            value="solucao",
            style="Opcao.TRadiobutton",
            command=self.alterar_para_modo_solucao,
        ).grid(row=4, column=0, sticky="w", pady=2)

        ttk.Radiobutton(
            area_opcoes,
            text="Ver análise da busca",
            variable=self.modo_visualizacao_var,
            value="analise",
            style="Opcao.TRadiobutton",
            command=self.alterar_para_modo_analise,
        ).grid(row=5, column=0, sticky="w", pady=2)

        self.label_estado_atual = tk.Label(
            area_opcoes,
            text="Estado atual: embaralhado para teste",
            justify="left",
            bg=COR_FUNDO,
            fg="#5b5248",
            font=("Georgia", 10, "bold"),
        )
        self.label_estado_atual.grid(row=6, column=0, sticky="w", pady=(10, 2))
        self._registrar_widget_com_wrap(self.label_estado_atual, 420, 300)

        self.label_movimento_destacado = tk.Label(
            area_opcoes,
            text="Movimento destacado: aguardando início",
            justify="left",
            bg=COR_FUNDO,
            fg=COR_ACAO,
            font=("Georgia", 11, "bold"),
        )
        self.label_movimento_destacado.grid(row=7, column=0, sticky="w", pady=(4, 4))
        self._registrar_widget_com_wrap(self.label_movimento_destacado, 420, 300)

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
        self.quadro_controles = ttk.LabelFrame(
            container,
            text="Botões de controle",
            style="Painel.TLabelframe",
        )
        self.quadro_controles.grid(row=2, column=0, sticky="ew")

        botoes = [
            ("Iniciar", self.iniciar_busca),
            ("Próximo passo", self.proximo_passo),
            ("Passo anterior", self.passo_anterior),
            ("Executar automático", self.executar_automatico),
            ("Pausar", self.pausar_execucao),
            ("Reiniciar", self.reiniciar),
            ("Embaralhar", self.embaralhar_estado),
            ("Comparar heurísticas", self.comparar_heuristicas),
            ("Ver análise da busca", self.alterar_para_modo_analise),
        ]

        for indice, (texto, comando) in enumerate(botoes):
            botao = ttk.Button(
                self.quadro_controles,
                text=texto,
                command=comando,
                style="Acao.TButton",
            )
            self.botoes_controle.append(botao)

        self._organizar_botoes_controle(3)

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
            bg=COR_FUNDO,
            fg="#5a5148",
            font=("Georgia", 9),
        )
        label_descricao.grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2))
        self._registrar_widget_com_wrap(label_descricao, 380, 300)

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
            bg=COR_FUNDO,
            fg="#5a5148",
            font=("Georgia", 9),
        )
        label_descricao.grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2))
        self._registrar_widget_com_wrap(label_descricao, 420, 320)

        self.texto_comparacao_esquerda = self._criar_texto_interno(quadro, 0, 1)
        self.texto_comparacao_direita = self._criar_texto_interno(quadro, 1, 1)

        self.label_observacao = tk.Label(
            quadro,
            text="As observações comparativas aparecerão após a execução da comparação.",
            justify="left",
            bg=COR_FUNDO,
            fg="#5a5148",
            font=("Georgia", 9),
        )
        self.label_observacao.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 2))
        self._registrar_widget_com_wrap(self.label_observacao, 420, 320)

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
        self.modo_visualizacao_var.set("solucao")
        self._atualizar_tabuleiro(self.estado_inicial_atual, set())
        self.label_estado_atual.config(text="Estado atual: embaralhado para teste")
        self.label_movimento_destacado.config(text="Movimento destacado: aguardando início")

        for nome_campo, label in self.valores_info.items():
            if nome_campo == "Heurística selecionada":
                label.config(text=self._titulo_heuristica_atual())
            else:
                label.config(text="—")

        self._preencher_texto(
            self.texto_open,
            "A Open List resumida aparecerá no modo 'Ver análise da busca'.",
        )
        self._preencher_texto(
            self.texto_closed,
            "A Closed List resumida aparecerá no modo 'Ver análise da busca'.",
        )
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

    def _modo_visualizacao_atual(self):
        """Retorna o modo atual da interface."""
        return self.modo_visualizacao_var.get()

    def _obter_item_historico_atual(self):
        """Retorna o item atual do histórico, quando disponível."""
        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return None
        return self.resultado_busca["historico"][self.indice_analise_atual]

    def _obter_item_solucao_atual(self):
        """Retorna o passo atual do caminho solução, quando disponível."""
        if not self.resultado_busca or not self.resultado_busca["caminho"]:
            return None
        return self.resultado_busca["caminho"][self.indice_solucao_atual]

    def _obter_estado_anterior(self, modo):
        """Retorna o estado anterior conforme o modo de visualização."""
        if not self.resultado_busca:
            return None

        if modo == "solucao":
            if not self.resultado_busca["caminho"] or self.indice_solucao_atual == 0:
                return None
            return self.resultado_busca["caminho"][self.indice_solucao_atual - 1]["estado"]

        if not self.resultado_busca["historico"] or self.indice_analise_atual == 0:
            return None
        return self.resultado_busca["historico"][self.indice_analise_atual - 1]["estado_atual"]

    def _calcular_indices_destacados(self, estado_atual, modo):
        """Calcula quais posições mudaram em relação à etapa anterior."""
        estado_anterior = self._obter_estado_anterior(modo)
        if estado_anterior is None:
            return set()

        return {
            indice
            for indice, (anterior, atual) in enumerate(zip(estado_anterior, estado_atual))
            if anterior != atual
        }

    def _atualizar_info_solucao(self):
        """Mostra os dados do passo atual do caminho final."""
        passo = self._obter_item_solucao_atual()
        if passo is None:
            return

        descricao_acao = passo["acao"] or "Estado inicial"
        self.valores_info["Movimento atual"].config(text=descricao_acao)
        self.valores_info["g(n)"].config(text=str(passo["g"]))
        self.valores_info["h(n)"].config(text=str(passo["h"]))
        self.valores_info["f(n)"].config(text=str(passo["f"]))
        self.valores_info["Número da etapa"].config(
            text=f"{self.indice_solucao_atual} de {len(self.resultado_busca['caminho']) - 1}"
        )
        self.valores_info["Estados expandidos"].config(text=str(self.resultado_busca["estados_expandidos"]))
        self.valores_info["Quantidade de estados na Open List"].config(text="Ver análise da busca")
        self.valores_info["Quantidade de estados na Closed List"].config(text="Ver análise da busca")
        self.valores_info["Heurística selecionada"].config(text=self._titulo_heuristica_atual())
        self.label_estado_atual.config(text="Estado atual: caminho final da solução")
        self.label_movimento_destacado.config(text=f"Movimento destacado: {descricao_acao}")

    def _atualizar_info_analise(self):
        """Mostra os dados da etapa atual do histórico de expansão."""
        item = self._obter_item_historico_atual()
        if item is None:
            return

        descricao_acao = item["acao"] or "Estado inicial"
        self.valores_info["Movimento atual"].config(text=descricao_acao)
        self.valores_info["g(n)"].config(text=str(item["g"]))
        self.valores_info["h(n)"].config(text=str(item["h"]))
        self.valores_info["f(n)"].config(text=str(item["f"]))
        self.valores_info["Número da etapa"].config(
            text=f"{item['numero_etapa']} de {len(self.resultado_busca['historico']) - 1}"
        )
        self.valores_info["Estados expandidos"].config(text=str(item["numero_etapa"] + 1))
        self.valores_info["Quantidade de estados na Open List"].config(text=str(item["quantidade_open"]))
        self.valores_info["Quantidade de estados na Closed List"].config(text=str(item["quantidade_closed"]))
        self.valores_info["Heurística selecionada"].config(text=self._titulo_heuristica_atual())
        self.label_estado_atual.config(text="Estado atual: análise interna do A*")
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
        if self._modo_visualizacao_atual() != "analise":
            self._preencher_texto(
                self.texto_open,
                "No modo 'Ver caminho final', o tabuleiro mostra apenas a solução.\n\n"
                "Use 'Ver análise da busca' para inspecionar a Open List.",
            )
            self._preencher_texto(
                self.texto_closed,
                "No modo 'Ver caminho final', o tabuleiro mostra apenas a solução.\n\n"
                "Use 'Ver análise da busca' para inspecionar a Closed List.",
            )
            return

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
        modo = self._modo_visualizacao_atual()

        if modo == "solucao":
            passo = self._obter_item_solucao_atual()
            if passo is None:
                return
            indices_destacados = self._calcular_indices_destacados(passo["estado"], modo)
            self._atualizar_tabuleiro(passo["estado"], indices_destacados)
            self._atualizar_info_solucao()
        else:
            item = self._obter_item_historico_atual()
            if item is None:
                return
            indices_destacados = self._calcular_indices_destacados(item["estado_atual"], modo)
            self._atualizar_tabuleiro(item["estado_atual"], indices_destacados)
            self._atualizar_info_analise()

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
        self.indice_solucao_atual = 0
        self.indice_analise_atual = 0
        self.modo_visualizacao_var.set("solucao")
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

        if self._modo_visualizacao_atual() == "solucao":
            if not self.resultado_busca["caminho"]:
                return

            if self.indice_solucao_atual < len(self.resultado_busca["caminho"]) - 1:
                self.indice_solucao_atual += 1
                self._mostrar_etapa_atual()
            return

        if not self.resultado_busca["historico"]:
            return

        if self.indice_analise_atual < len(self.resultado_busca["historico"]) - 1:
            self.indice_analise_atual += 1
            self._mostrar_etapa_atual()

    def passo_anterior(self):
        """Retorna manualmente para a etapa anterior registrada."""
        if not self.resultado_busca:
            return

        if self._modo_visualizacao_atual() == "solucao":
            if self.indice_solucao_atual > 0:
                self.indice_solucao_atual -= 1
                self._mostrar_etapa_atual()
            return

        if not self.resultado_busca["historico"]:
            return

        if self.indice_analise_atual > 0:
            self.indice_analise_atual -= 1
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

        if self._modo_visualizacao_atual() == "solucao":
            chegou_ao_fim = self.indice_solucao_atual >= len(self.resultado_busca["caminho"]) - 1
        else:
            chegou_ao_fim = self.indice_analise_atual >= len(self.resultado_busca["historico"]) - 1

        if chegou_ao_fim:
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
        self.indice_solucao_atual = 0
        self.indice_analise_atual = 0
        self._reiniciar_interface_visual()

    def embaralhar_estado(self):
        """Gera um novo estado inicial embaralhado para testes."""
        self.pausar_execucao()
        self.estado_inicial_atual = gerar_estado_embaralhado(movimentos=20)
        self.resultado_busca = None
        self.indice_solucao_atual = 0
        self.indice_analise_atual = 0
        self._reiniciar_interface_visual()

    def alterar_para_modo_solucao(self):
        """Exibe o tabuleiro principal usando apenas o caminho final da solução."""
        self.modo_visualizacao_var.set("solucao")
        if self.resultado_busca:
            self._mostrar_etapa_atual()

    def alterar_para_modo_analise(self):
        """Exibe o tabuleiro principal usando o histórico de análise do A*."""
        self.modo_visualizacao_var.set("analise")
        if self.resultado_busca:
            self._mostrar_etapa_atual()

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
