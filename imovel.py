from __future__ import annotations

from decimal import Decimal


class Imovel:
    """Representa um imóvel e calcula o aluguel mensal sem a taxa contratual."""

    TIPOS_VALIDOS = ("Apartamento", "Casa", "Estúdio")

    def __init__(
        self,
        tipo: str,
        quartos: int | None = None,
        vagas: int = 0,
        possui_criancas: bool | None = None,
    ) -> None:
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError("Selecione um tipo de imóvel válido.")
        if tipo in ("Apartamento", "Casa") and quartos not in (1, 2):
            raise ValueError("Casas e apartamentos devem ter 1 ou 2 quartos.")
        if tipo == "Estúdio" and quartos is not None:
            raise ValueError("Estúdios não possuem quantidade de quartos.")
        if vagas < 0:
            raise ValueError("A quantidade de vagas não pode ser negativa.")
        if tipo == "Apartamento" and possui_criancas is None:
            raise ValueError("Informe se há crianças no apartamento.")
        if tipo != "Apartamento" and possui_criancas is not None:
            raise ValueError("A informação sobre crianças só se aplica a apartamentos.")
        if tipo == "Estúdio" and vagas == 1:
            raise ValueError("O estacionamento do estúdio começa com um pacote de 2 vagas.")

        self.tipo = tipo
        self.quartos = quartos
        self.vagas = vagas
        self.possui_criancas = possui_criancas

    def calcular_aluguel_base(self) -> Decimal:
        if self.tipo == "Apartamento":
            return Decimal("700.00")
        if self.tipo == "Casa":
            return Decimal("900.00")
        return Decimal("1200.00")

    def calcular_adicional_quartos(self) -> Decimal:
        if self.tipo == "Apartamento" and self.quartos == 2:
            return Decimal("200.00")
        if self.tipo == "Casa" and self.quartos == 2:
            return Decimal("250.00")
        return Decimal("0.00")

    def calcular_adicional_estacionamento(self) -> Decimal:
        if self.tipo in ("Apartamento", "Casa"):
            return Decimal("300.00") if self.vagas == 1 else Decimal("0.00")
        if self.vagas >= 2:
            return Decimal("250.00") + Decimal( self.vagas - 2) * Decimal("60.00")
        return Decimal("0.00")

    def calcular_desconto(self) -> Decimal:
        if self.tipo == "Apartamento" and self.possui_criancas is False:
            subtotal = self.calcular_aluguel_base() + self.calcular_adicional_quartos() + self.calcular_adicional_estacionamento()
            return subtotal * Decimal("0.05")
        return Decimal("0.00")

    def calcular_aluguel_mensal(self) -> Decimal:
        subtotal = self.calcular_aluguel_base() + self.calcular_adicional_quartos() + self.calcular_adicional_estacionamento()
        return subtotal - self.calcular_desconto()
