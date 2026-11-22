# RentSmart

Sistema desktop de orçamento de locação da imobiliária fictícia R.M Imóveis, desenvolvido para demonstrar Python, pensamento algorítmico e programação orientada a objetos.

## Tecnologias

Python 3, Tkinter/ttk, `decimal`, `csv` e `pathlib`. Não há dependências externas nem banco de dados.

## Estrutura

```text
RentSmart/
├── main.py          # Interface Tkinter e validações
├── imovel.py        # Regras do imóvel e do aluguel
├── contrato.py      # Taxa, parcelas, projeção e CSV
├── README.md
└── exportacoes/     # Criada automaticamente ao exportar
```

## Executar no Windows

No terminal integrado do VS Code, estando na pasta do projeto:

```powershell
cd D:\RentSmart
python main.py
```

O comando também pode ser executado com `py main.py`. O Python deve ter Tkinter disponível (a instalação padrão do Windows normalmente já inclui essa biblioteca).

## Classes

- `Imovel`: armazena tipo, quartos, vagas e crianças; calcula base, adicionais, desconto e aluguel mensal.
- `Contrato`: controla a taxa fixa de R$ 2.000,00, o parcelamento, a projeção de 12 meses e a exportação CSV.
- `RentSmartApp`: constrói a janela, valida escolhas, cria os objetos e apresenta o orçamento.

## Uso

1. Selecione o tipo de imóvel e preencha os campos exibidos.
2. Escolha de 1 a 5 parcelas para a taxa contratual.
3. Clique em **CALCULAR ORÇAMENTO**.
4. Após o cálculo, clique em **EXPORTAR CSV**. O arquivo `orcamento_rentsmart.csv` será salvo em `exportacoes` com UTF-8 BOM, `;` e vírgula decimal.
5. Use **LIMPAR CAMPOS** para iniciar um novo orçamento.
