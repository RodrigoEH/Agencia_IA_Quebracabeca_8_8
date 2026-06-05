# -*- coding: utf-8 -*-
"""ETAPA 8: interface gráfica em Tkinter para visualizar a execução do A*."""

import tkinter as tk
from tkinter import messagebox, ttk

from agente_astar import resolver_astar
from estado import ESTADO_OBJETIVO
from heuristicas import distancia_manhattan, distancia_manhattan_nao_admissivel

TITULO_PROJETO = "AGENTE A* — QUEBRA-CABEÇA DE 8 PEÇAS"
ESTADO_INICIAL = (1, 2, 3, 4, 0, 6, 7, 5, 8)


HEURISTICAS_DISPONIVEIS = {
    "Distância de Manhattan (admissível)": distancia_manhattan,
    "2 × Distância de Manhattan (não admissível)": distancia_manhattan_nao_admissivel,
}


def formatar_tabuleiro_em_bloco(estado):
    """Converte um estado em texto de três linhas para exibição resumida."""
    linhas = []
    for indice in range(0, 9, 3):
        linha = estado[indice:indice + 3]
        linhas.append(" ".join(str(valor) for valor in linha))
    return "\n".join(linhas)


class InterfaceAStar:
    """Controla a interface gráfica sem misturar a lógica visual com a busca."""

    def __init__(self, janela):
        self.janela = janela
        self.janela.title(TITULO_PROJETO)
        self.janela.geometry("1280x860")
        self.janela.minsize(1160, 760)
        self.janela.configure(bg="#f2efe8")

        self.resultado_busca = None
        self.indice_etapa_atual = 0
        self.execucao_automatica_ativa = False
        self.identificador_after = None

        self.heuristica_var = tk.StringVar(
            value="Distância de Manhattan (admissível)"
        )

        self.labels_tabuleiro = []
        self.valores_info = {}

        self._criar_estilo()
        self._criar_layout()
        self._reiniciar_interface_visual()

    def _criar_estilo(self):
        """Define o estilo visual base da interface."""
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Painel.TLabelframe", background="#f2efe8", borderwidth=2)
        estilo.configure(
            "Painel.TLabelframe.Label",
            background="#f2efe8",
            foreground="#2f2a24",
            font=("Georgia", 11, "bold"),
        )
        estilo.configure(
            "Titulo.TLabel",
            background="#f2efe8",
            foreground="#2f2a24",
            font=("Georgia", 18, "bold"),
        )
        estilo.configure(
            "InfoNome.TLabel",
            background="#f2efe8",
            foreground="#5b534b",
            font=("Georgia", 10, "bold"),
        )
        estilo.configure(
            "InfoValor.TLabel",
            background="#f2efe8",
            foreground="#1d1a16",
            font=("Consolas", 11),
        )
        estilo.configure(
            "Acao.TButton",
            font=("Georgia", 10, "bold"),
            padding=8,
        )

    def _criar_layout(self):
        """Monta os painéis principais da aplicação."""
        cabecalho = ttk.Label(
            self.janela,
            text=TITULO_PROJETO,
            style="Titulo.TLabel",
            anchor="center",
        )
        cabecalho.pack(fill="x", padx=18, pady=(14, 6))

        corpo = tk.Frame(self.janela, bg="#f2efe8")
        corpo.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        corpo.grid_columnconfigure(0, weight=3)
        corpo.grid_columnconfigure(1, weight=2)
        corpo.grid_rowconfigure(0, weight=1)

        painel_esquerdo = tk.Frame(corpo, bg="#f2efe8")
        painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        painel_esquerdo.grid_columnconfigure(0, weight=1)

        painel_direito = tk.Frame(corpo, bg="#f2efe8")
        painel_direito.grid(row=0, column=1, sticky="nsew")
        painel_direito.grid_columnconfigure(0, weight=1)
        painel_direito.grid_rowconfigure(0, weight=1)
        painel_direito.grid_rowconfigure(1, weight=1)
        painel_direito.grid_rowconfigure(2, weight=1)

        self._criar_painel_superior_esquerdo(painel_esquerdo)
        self._criar_painel_informacoes(painel_esquerdo)
        self._criar_painel_controles(painel_esquerdo)

        self.texto_open = self._criar_painel_texto(
            painel_direito,
            "Open List resumida",
            0,
        )
        self.texto_closed = self._criar_painel_texto(
            painel_direito,
            "Closed List resumida",
            1,
        )
        self.texto_caminho = self._criar_painel_texto(
            painel_direito,
            "Caminho final",
            2,
        )

    def _criar_painel_superior_esquerdo(self, container):
        """Cria o tabuleiro e a seleção de heurística."""
        quadro = ttk.LabelFrame(
            container,
            text="Tabuleiro e heurística",
            style="Painel.TLabelframe",
        )
        quadro.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        quadro.grid_columnconfigure(0, weight=1)
        quadro.grid_columnconfigure(1, weight=1)

        area_tabuleiro = tk.Frame(quadro, bg="#f2efe8")
        area_tabuleiro.grid(row=0, column=0, padx=16, pady=16, sticky="nw")

        for linha in range(3):
            area_tabuleiro.grid_rowconfigure(linha, weight=1)
            area_tabuleiro.grid_columnconfigure(linha, weight=1)

        for indice in range(9):
            linha = indice // 3
            coluna = indice % 3
            label = tk.Label(
                area_tabuleiro,
                width=4,
                height=2,
                relief="ridge",
                borderwidth=2,
                font=("Georgia", 24, "bold"),
                bg="#d6c9b8",
                fg="#2f2a24",
            )
            label.grid(row=linha, column=coluna, padx=4, pady=4, sticky="nsew")
            self.labels_tabuleiro.append(label)

        area_heuristica = tk.Frame(quadro, bg="#f2efe8")
        area_heuristica.grid(row=0, column=1, padx=8, pady=16, sticky="nsew")
        area_heuristica.grid_columnconfigure(0, weight=1)

        ttk.Label(
            area_heuristica,
            text="Seleção da heurística",
            style="InfoNome.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.combo_heuristica = ttk.Combobox(
            area_heuristica,
            textvariable=self.heuristica_var,
            values=list(HEURISTICAS_DISPONIVEIS.keys()),
            state="readonly",
            font=("Georgia", 11),
        )
        self.combo_heuristica.grid(row=1, column=0, sticky="ew")

        descricao = (
            "A interface consome apenas o histórico gerado pela busca.\n"
            "Use os controles para navegar pelas expansões registradas."
        )
        tk.Label(
            area_heuristica,
            text=descricao,
            justify="left",
            wraplength=250,
            bg="#f2efe8",
            fg="#5b534b",
            font=("Georgia", 10),
        ).grid(row=2, column=0, sticky="w", pady=(16, 0))

    def _criar_painel_informacoes(self, container):
        """Cria o painel com os dados resumidos da etapa atual."""
        quadro = ttk.LabelFrame(
            container,
            text="Painel de informações",
            style="Painel.TLabelframe",
        )
        quadro.grid(row=1, column=0, sticky="nsew", pady=(0, 12))
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
            ).grid(row=linha, column=0, sticky="w", padx=14, pady=6)

            valor = ttk.Label(
                quadro,
                text="—",
                style="InfoValor.TLabel",
            )
            valor.grid(row=linha, column=1, sticky="w", padx=(0, 14), pady=6)
            self.valores_info[nome_campo] = valor

    def _criar_painel_controles(self, container):
        """Cria os botões de controle da simulação."""
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
                padx=8,
                pady=10,
                sticky="ew",
            )
            quadro.grid_columnconfigure(indice % 3, weight=1)

    def _criar_painel_texto(self, container, titulo, linha):
        """Cria um painel de texto com rolagem vertical."""
        quadro = ttk.LabelFrame(
            container,
            text=titulo,
            style="Painel.TLabelframe",
        )
        quadro.grid(row=linha, column=0, sticky="nsew", pady=(0, 12) if linha < 2 else 0)
        quadro.grid_rowconfigure(0, weight=1)
        quadro.grid_columnconfigure(0, weight=1)

        texto = tk.Text(
            quadro,
            wrap="word",
            height=10,
            font=("Consolas", 10),
            bg="#fffdf8",
            fg="#2f2a24",
            relief="flat",
            padx=10,
            pady=10,
        )
        texto.grid(row=0, column=0, sticky="nsew")

        barra = ttk.Scrollbar(quadro, orient="vertical", command=texto.yview)
        barra.grid(row=0, column=1, sticky="ns")
        texto.configure(yscrollcommand=barra.set, state="disabled")
        return texto

    def _reiniciar_interface_visual(self):
        """Restaura a interface para o estado inicial antes da busca."""
        self._atualizar_tabuleiro(ESTADO_INICIAL)

        for nome_campo, label in self.valores_info.items():
            if nome_campo == "Heurística selecionada":
                label.config(text=self.heuristica_var.get())
            else:
                label.config(text="—")

        self._preencher_texto(self.texto_open, "A Open List resumida aparecerá após iniciar a busca.")
        self._preencher_texto(self.texto_closed, "A Closed List resumida aparecerá após iniciar a busca.")
        self._preencher_texto(self.texto_caminho, "O caminho final será exibido após a execução.")

    def _preencher_texto(self, widget_texto, conteudo):
        """Atualiza o conteúdo de um painel de texto."""
        widget_texto.config(state="normal")
        widget_texto.delete("1.0", tk.END)
        widget_texto.insert("1.0", conteudo)
        widget_texto.config(state="disabled")

    def _atualizar_tabuleiro(self, estado):
        """Desenha visualmente o tabuleiro 3 × 3."""
        for label, valor in zip(self.labels_tabuleiro, estado):
            if valor == 0:
                label.config(text="", bg="#fbf7ef", relief="sunken")
            else:
                label.config(text=str(valor), bg="#d6c9b8", relief="ridge")

    def _obter_item_historico_atual(self):
        """Retorna o item atual do histórico, quando disponível."""
        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return None
        return self.resultado_busca["historico"][self.indice_etapa_atual]

    def _atualizar_info_etapa(self):
        """Mostra as informações da etapa atual no painel de dados."""
        item = self._obter_item_historico_atual()
        if item is None:
            return

        self.valores_info["Movimento atual"].config(
            text=item["acao"] or "Estado inicial"
        )
        self.valores_info["g(n)"].config(text=str(item["g"]))
        self.valores_info["h(n)"].config(text=str(item["h"]))
        self.valores_info["f(n)"].config(text=str(item["f"]))
        self.valores_info["Número da etapa"].config(text=str(item["numero_etapa"]))
        self.valores_info["Estados expandidos"].config(text=str(item["numero_etapa"] + 1))
        self.valores_info["Quantidade de estados na Open List"].config(
            text=str(item["quantidade_open"])
        )
        self.valores_info["Quantidade de estados na Closed List"].config(
            text=str(item["quantidade_closed"])
        )
        self.valores_info["Heurística selecionada"].config(text=self.heuristica_var.get())

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

        self._preencher_texto(
            self.texto_open,
            self._formatar_lista_resumida(item["open_resumida"]),
        )
        self._preencher_texto(
            self.texto_closed,
            self._formatar_lista_resumida(item["closed_resumida"]),
        )

    def _atualizar_painel_caminho(self):
        """Exibe o caminho final completo retornado pela busca."""
        if not self.resultado_busca:
            return

        if not self.resultado_busca["encontrou_solucao"]:
            self._preencher_texto(
                self.texto_caminho,
                f"Erro: {self.resultado_busca['mensagem']}",
            )
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
        """Sincroniza o tabuleiro e os painéis com a etapa atualmente selecionada."""
        item = self._obter_item_historico_atual()
        if item is None:
            return

        self._atualizar_tabuleiro(item["estado_atual"])
        self._atualizar_info_etapa()
        self._atualizar_paineis_resumidos()
        self._atualizar_painel_caminho()

    def iniciar_busca(self):
        """Executa a busca e prepara a navegação do histórico na interface."""
        self.pausar_execucao()

        nome_heuristica = self.heuristica_var.get()
        funcao_heuristica = HEURISTICAS_DISPONIVEIS[nome_heuristica]

        self.resultado_busca = resolver_astar(
            estado_inicial=ESTADO_INICIAL,
            estado_objetivo=ESTADO_OBJETIVO,
            funcao_heuristica=funcao_heuristica,
            registrar_historico=True,
        )

        self.indice_etapa_atual = 0
        self._atualizar_painel_caminho()

        if not self.resultado_busca["historico"]:
            self._preencher_texto(
                self.texto_open,
                "Sem histórico disponível para este caso.",
            )
            self._preencher_texto(
                self.texto_closed,
                "Sem histórico disponível para este caso.",
            )
            self.valores_info["Heurística selecionada"].config(text=nome_heuristica)
            messagebox.showerror("Busca A*", self.resultado_busca["mensagem"])
            return

        self._mostrar_etapa_atual()

        if not self.resultado_busca["encontrou_solucao"]:
            messagebox.showerror("Busca A*", self.resultado_busca["mensagem"])

    def proximo_passo(self):
        """Avança para a próxima etapa do histórico."""
        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return

        if self.indice_etapa_atual < len(self.resultado_busca["historico"]) - 1:
            self.indice_etapa_atual += 1
            self._mostrar_etapa_atual()

    def passo_anterior(self):
        """Retorna para a etapa anterior do histórico."""
        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return

        if self.indice_etapa_atual > 0:
            self.indice_etapa_atual -= 1
            self._mostrar_etapa_atual()

    def _executar_automatico_loop(self):
        """Percorre o histórico automaticamente usando o agendador do Tkinter."""
        if not self.execucao_automatica_ativa:
            return

        if not self.resultado_busca or not self.resultado_busca["historico"]:
            self.execucao_automatica_ativa = False
            return

        if self.indice_etapa_atual >= len(self.resultado_busca["historico"]) - 1:
            self.execucao_automatica_ativa = False
            self.identificador_after = None
            return

        self.proximo_passo()
        self.identificador_after = self.janela.after(1200, self._executar_automatico_loop)

    def executar_automatico(self):
        """Inicia a navegação automática do histórico."""
        if not self.resultado_busca:
            self.iniciar_busca()

        if not self.resultado_busca or not self.resultado_busca["historico"]:
            return

        self.execucao_automatica_ativa = True
        self._executar_automatico_loop()

    def pausar_execucao(self):
        """Pausa a navegação automática do histórico."""
        self.execucao_automatica_ativa = False

        if self.identificador_after is not None:
            self.janela.after_cancel(self.identificador_after)
            self.identificador_after = None

    def reiniciar(self):
        """Reinicia a interface para o estado inicial visual."""
        self.pausar_execucao()
        self.resultado_busca = None
        self.indice_etapa_atual = 0
        self._reiniciar_interface_visual()


def executar_interface():
    """Cria e executa a interface gráfica principal."""
    janela = tk.Tk()
    InterfaceAStar(janela)
    janela.mainloop()


if __name__ == "__main__":
    executar_interface()
