from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Ingrediente:
    nome: str
    preco_base: float
    porcao: int
    quantidade: int = 0

    @property
    def preco_total(self) -> float:
        return self.preco_base

    CATALOGO: ClassVar[list[dict]] = [
        {'nome': 'Goma de Tapioca', 'preco_base': 10, 'porcao': 5},
        {'nome': 'Queijo Coalho', 'preco_base': 15, 'porcao': 3},
        {'nome': 'Coco Ralado', 'preco_base': 8, 'porcao': 4},
        {'nome': 'Leite Condensado', 'preco_base': 12, 'porcao': 5},
    ]

    RECEITAS_IDEAIS: ClassVar[dict[str, dict[str, int]]] = {
        'Casa Forte': {
            'Goma de Tapioca': 2,
            'Queijo Coalho': 2,
            'Coco Ralado': 1,
            'Leite Condensado': 0,
        },
        'Recife Antigo': {
            'Goma de Tapioca': 1,
            'Queijo Coalho': 1,
            'Coco Ralado': 0,
            'Leite Condensado': 1,
        },
        'Ibura': {
            'Goma de Tapioca': 1,
            'Queijo Coalho': 0,
            'Coco Ralado': 1,
            'Leite Condensado': 1,
        },
        'Boa Viagem': {
            'Goma de Tapioca': 1,
            'Queijo Coalho': 1,
            'Coco Ralado': 1,
            'Leite Condensado': 0,
        },
        'Várzea': {
            'Goma de Tapioca': 1,
            'Queijo Coalho': 1,
            'Coco Ralado': 0,
            'Leite Condensado': 1,
        },
        'Areias': {
            'Goma de Tapioca': 1,
            'Queijo Coalho': 1,
            'Coco Ralado': 1,
            'Leite Condensado': 0,
        },
    }

    PRECOS_IDEAIS: ClassVar[dict[str, float]] = {
        'Casa Forte': 22.0,
        'Recife Antigo': 15.0,
        'Ibura': 7.0,
        'Boa Viagem': 18.0,
        'Várzea': 12.0,
        'Areias': 10.0,
    }

    # Inflação
    @staticmethod
    def fator_inflacao(dia_atual: int) -> float:
        return 1.0 + (dia_atual // 5) * 0.10

    @classmethod
    def preco_com_inflacao(cls, nome: str, dia_atual: int) -> float:
        item = next((i for i in cls.CATALOGO if i['nome'] == nome), None)
        if item is None:
            return 0.0
        return round(item['preco_base'] * cls.fator_inflacao(dia_atual), 2)

    # Consultas
    @classmethod
    def receita_ideal(cls, nome_bairro: str) -> dict[str, int]:
        return cls.RECEITAS_IDEAIS.get(
            nome_bairro,
            {
                'Goma de Tapioca': 1,
                'Queijo Coalho': 0,
                'Coco Ralado': 0,
                'Leite Condensado': 0,
            },
        )

    @classmethod
    def preco_ideal(cls, nome_bairro: str) -> float:
        return cls.PRECOS_IDEAIS.get(nome_bairro, 15.0)

    @classmethod
    def catalogo_para_cliente(cls, dia_atual: int = 1) -> list[dict]:
        fator = cls.fator_inflacao(dia_atual)
        return [
            {
                'nome': i['nome'],
                'preco': round(i['preco_base'] * fator, 2),
                'porcao': i['porcao'],
            }
            for i in cls.CATALOGO
        ]

    @classmethod
    def estoque_inicial(cls) -> list['Ingrediente']:
        return [cls(**i) for i in cls.CATALOGO]
