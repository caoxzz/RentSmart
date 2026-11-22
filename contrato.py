from __future__ import annotations

import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from imovel import Imovel


CENTAVOS = Decimal("0.01")


class Contrato:
    """Controla a taxa contratual, as parcelas e a projeção de 12 meses."""

    TAXA_CONTRATUAL = Decimal("2000.00")

    def __init__(self, imovel: Imovel, quantidade_parcelas: int) -> None:
        if not 1 <= quantidade_parcelas <= 5:
            raise ValueError("A taxa contratual deve ser parcelada de 1 a 5 vezes.")
        self.imovel = imovel
        self.quantidade_parcelas = quantidade_parcelas

    @property
    def aluguel_mensal(self) -> Decimal:
        return self.imovel.calcular_aluguel_mensal().quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    @property
    def valor_parcela(self) -> Decimal:
        return (self.TAXA_CONTRATUAL / Decimal(self.quantidade_parcelas)).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    def parcela_no_mes(self, mes: int) -> Decimal:
        if not 1 <= mes <= 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        return self.valor_parcela if mes <= self.quantidade_parcelas else Decimal("0.00")

    def gerar_projecao(self, meses: int = 12) -> list[dict[str, Decimal | int]]:
        return [
            {
                "mes": mes,
                "aluguel": self.aluguel_mensal,
                "parcela": self.parcela_no_mes(mes),
                "total": (self.aluguel_mensal + self.parcela_no_mes(mes)).quantize(CENTAVOS),
            }
            for mes in range(1, meses + 1)
        ]

    def custo_total_12_meses(self) -> Decimal:
        return sum((linha["total"] for linha in self.gerar_projecao()), Decimal("0.00"))

    def exportar_csv(self, pasta: str | Path = "exportacoes") -> Path:
        destino = Path(pasta)
        destino.mkdir(parents=True, exist_ok=True)
        arquivo = destino / "orcamento_rentsmart.csv"
        with arquivo.open("w", newline="", encoding="utf-8-sig") as csvfile:
            escritor = csv.writer(csvfile, delimiter=";")
            escritor.writerow(("Mês", "Aluguel mensal", "Parcela da taxa contratual", "Total do mês"))
            for linha in self.gerar_projecao():
                escritor.writerow((
                    linha["mes"],
                    self._formatar_valor(linha["aluguel"]),
                    self._formatar_valor(linha["parcela"]),
                    self._formatar_valor(linha["total"]),
                ))
        return arquivo.resolve()

    @staticmethod
    def _formatar_valor(valor: Decimal) -> str:
        return f"{valor:.2f}".replace(".", ",")
