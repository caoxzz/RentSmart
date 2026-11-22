from __future__ import annotations

import tkinter as tk
from decimal import Decimal
from pathlib import Path
from tkinter import messagebox, ttk

from contrato import Contrato
from imovel import Imovel


class RentSmartApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("RentSmart - Sistema de Orçamento de Locação")
        self.root.geometry("1050x700")
        self.root.minsize(900, 620)
        self.root.configure(bg="#171717")
        self.contrato: Contrato | None = None
        self._configurar_estilos()
        self._criar_variaveis()
        self._criar_interface()
        self._atualizar_campos()

    def _configurar_estilos(self) -> None:
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#171717")
        estilo.configure("TLabel", background="#171717", foreground="#f5f5f5", font=("Segoe UI", 10))
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 24, "bold"), foreground="#ffffff")
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 11), foreground="#bdbdbd")
        estilo.configure("Secao.TLabelframe", background="#171717", foreground="#ffffff", bordercolor="#555555")
        estilo.configure("Secao.TLabelframe.Label", background="#171717", foreground="#ffffff", font=("Segoe UI", 11, "bold"))
        estilo.configure("TButton", padding=8, font=("Segoe UI", 10, "bold"))
        estilo.configure("Resultado.TLabel", background="#242424", foreground="#ffffff", padding=3)
        estilo.configure("Destaque.TLabel", background="#242424", foreground="#ffffff", font=("Segoe UI", 11, "bold"), padding=3)

    def _criar_variaveis(self) -> None:
        self.tipo_var = tk.StringVar(value="Apartamento")
        self.quartos_var = tk.StringVar(value="1")
        self.vagas_var = tk.StringVar(value="0")
        self.criancas_var = tk.StringVar(value="Não informado")
        self.parcelas_var = tk.StringVar(value="1")
        self.resultado_vars = {chave: tk.StringVar(value="-") for chave in (
            "tipo", "base", "quartos", "estacionamento", "desconto", "aluguel", "taxa", "parcelas", "valor_parcela", "durante", "apos", "total"
        )}

    def _criar_interface(self) -> None:
        ttk.Label(self.root, text="RentSmart", style="Titulo.TLabel").pack(pady=(18, 0))
        ttk.Label(self.root, text="Sistema de Orçamento de Locação", style="Subtitulo.TLabel").pack(pady=(0, 14))
        corpo = ttk.Frame(self.root)
        corpo.pack(fill="both", expand=True, padx=22, pady=4)
        corpo.columnconfigure(0, weight=1)
        corpo.columnconfigure(1, weight=2)
        corpo.rowconfigure(0, weight=1)

        config = ttk.LabelFrame(corpo, text=" 1. Configuração do imóvel ", style="Secao.TLabelframe", padding=18)
        config.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        resultado = ttk.LabelFrame(corpo, text=" 2. Resultado do orçamento ", style="Secao.TLabelframe", padding=14)
        resultado.grid(row=0, column=1, sticky="nsew")

        self._campo_combo(config, "Tipo de imóvel", self.tipo_var, ("Apartamento", "Casa", "Estúdio"), 0, self._tipo_alterado)
        self.quartos_label = ttk.Label(config, text="Quantidade de quartos")
        self.quartos_label.grid(row=2, column=0, sticky="w", pady=(16, 4))
        self.quartos_combo = ttk.Combobox(config, textvariable=self.quartos_var, values=("1", "2"), state="readonly", width=22)
        self.quartos_combo.grid(row=3, column=0, sticky="ew")
        self.vagas_label = ttk.Label(config, text="Garagem / vagas")
        self.vagas_label.grid(row=4, column=0, sticky="w", pady=(16, 4))
        self.vagas_combo = ttk.Combobox(config, textvariable=self.vagas_var, values=("0", "1"), state="readonly", width=22)
        self.vagas_combo.grid(row=5, column=0, sticky="ew")
        self.criancas_label = ttk.Label(config, text="Possui crianças?")
        self.criancas_label.grid(row=6, column=0, sticky="w", pady=(16, 4))
        self.criancas_combo = ttk.Combobox(config, textvariable=self.criancas_var, values=("Sim", "Não"), state="readonly", width=22)
        self.criancas_combo.grid(row=7, column=0, sticky="ew")
        ttk.Label(config, text="Parcelas da taxa (1 a 5)").grid(row=8, column=0, sticky="w", pady=(16, 4))
        ttk.Combobox(config, textvariable=self.parcelas_var, values=("1", "2", "3", "4", "5"), state="readonly", width=22).grid(row=9, column=0, sticky="ew")
        config.columnconfigure(0, weight=1)

        labels = (("tipo", "Tipo de imóvel"), ("base", "Aluguel-base"), ("quartos", "Adicional de quartos"), ("estacionamento", "Adicional de estacionamento"), ("desconto", "Desconto aplicado"), ("aluguel", "Aluguel final mensal"), ("taxa", "Taxa contratual"), ("parcelas", "Quantidade de parcelas"), ("valor_parcela", "Valor de cada parcela"), ("durante", "Total mensal durante parcelamento"), ("apos", "Total mensal após parcelamento"), ("total", "Custo projetado (12 meses)"))
        for linha, (chave, texto) in enumerate(labels):
            ttk.Label(resultado, text=f"{texto}:", style="Resultado.TLabel").grid(row=linha, column=0, sticky="ew", padx=(0, 8), pady=2)
            ttk.Label(resultado, textvariable=self.resultado_vars[chave], style="Destaque.TLabel" if chave in ("aluguel", "total") else "Resultado.TLabel").grid(row=linha, column=1, sticky="ew", pady=2)
        resultado.columnconfigure(0, weight=1)
        resultado.columnconfigure(1, weight=1)

        acoes = ttk.Frame(self.root)
        acoes.pack(fill="x", padx=22, pady=(10, 20))
        ttk.Button(acoes, text="CALCULAR ORÇAMENTO", command=self.calcular).pack(side="left", expand=True, fill="x", padx=(0, 6))
        self.exportar_button = ttk.Button(acoes, text="EXPORTAR CSV", command=self.exportar, state="disabled")
        self.exportar_button.pack(side="left", expand=True, fill="x", padx=6)
        ttk.Button(acoes, text="LIMPAR CAMPOS", command=self.limpar).pack(side="left", expand=True, fill="x", padx=(6, 0))

    def _campo_combo(self, parent: ttk.Frame, texto: str, variable: tk.StringVar, valores: tuple[str, ...], linha: int, comando) -> None:
        ttk.Label(parent, text=texto).grid(row=linha, column=0, sticky="w", pady=(0, 4))
        combo = ttk.Combobox(parent, textvariable=variable, values=valores, state="readonly", width=22)
        combo.grid(row=linha + 1, column=0, sticky="ew")
        combo.bind("<<ComboboxSelected>>", comando)

    def _tipo_alterado(self, _evento=None) -> None:
        self._atualizar_campos()
        self._invalidar_orcamento()

    def _atualizar_campos(self) -> None:
        tipo = self.tipo_var.get()
        if tipo == "Estúdio":
            self.quartos_label.grid_remove(); self.quartos_combo.grid_remove()
            self.criancas_label.grid_remove(); self.criancas_combo.grid_remove()
            self.vagas_combo["values"] = ("0", "2", "3", "4", "5")
        else:
            self.quartos_label.grid(); self.quartos_combo.grid()
            self.criancas_label.grid() if tipo == "Apartamento" else self.criancas_label.grid_remove()
            self.criancas_combo.grid() if tipo == "Apartamento" else self.criancas_combo.grid_remove()
            self.vagas_combo["values"] = ("0", "1")
        self.vagas_var.set("0")

    def _invalidar_orcamento(self) -> None:
        self.contrato = None
        self.exportar_button.configure(state="disabled")

    @staticmethod
    def _dinheiro(valor: Decimal) -> str:
        return f"R$ {valor:.2f}".replace(".", ",")

    def calcular(self) -> None:
        try:
            tipo = self.tipo_var.get()
            vagas = int(self.vagas_var.get())
            quartos = None if tipo == "Estúdio" else int(self.quartos_var.get())
            criancas = None if tipo != "Apartamento" else {"Sim": True, "Não": False}.get(self.criancas_var.get())
            imovel = Imovel(tipo, quartos, vagas, criancas)
            contrato = Contrato(imovel, int(self.parcelas_var.get()))
        except (ValueError, TypeError) as erro:
            messagebox.showerror("Dados inválidos", str(erro))
            return
        self.contrato = contrato
        self.exportar_button.configure(state="normal")
        self._mostrar_resultado(contrato)

    def _mostrar_resultado(self, contrato: Contrato) -> None:
        imovel = contrato.imovel
        valores = {"tipo": imovel.tipo, "base": self._dinheiro(imovel.calcular_aluguel_base()), "quartos": self._dinheiro(imovel.calcular_adicional_quartos()), "estacionamento": self._dinheiro(imovel.calcular_adicional_estacionamento()), "desconto": self._dinheiro(imovel.calcular_desconto()), "aluguel": self._dinheiro(contrato.aluguel_mensal), "taxa": self._dinheiro(contrato.TAXA_CONTRATUAL), "parcelas": str(contrato.quantidade_parcelas), "valor_parcela": self._dinheiro(contrato.valor_parcela), "durante": self._dinheiro(contrato.aluguel_mensal + contrato.valor_parcela), "apos": self._dinheiro(contrato.aluguel_mensal), "total": self._dinheiro(contrato.custo_total_12_meses())}
        for chave, valor in valores.items(): self.resultado_vars[chave].set(valor)

    def exportar(self) -> None:
        if self.contrato is None:
            messagebox.showerror("Exportação", "Calcule um orçamento antes de exportar.")
            return
        arquivo = self.contrato.exportar_csv(Path(__file__).parent / "exportacoes")
        messagebox.showinfo("Exportação concluída", f"Arquivo gerado em:\n{arquivo}")

    def limpar(self) -> None:
        self.tipo_var.set("Apartamento"); self.quartos_var.set("1"); self.vagas_var.set("0"); self.criancas_var.set("Não informado"); self.parcelas_var.set("1")
        self._atualizar_campos(); self._invalidar_orcamento()
        for variavel in self.resultado_vars.values(): variavel.set("-")


if __name__ == "__main__":
    janela = tk.Tk()
    RentSmartApp(janela)
    janela.mainloop()
