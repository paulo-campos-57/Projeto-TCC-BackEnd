from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Ingrediente:
    nome: str
    preco_unitario: float
    porcao: int
    quantidade: int = 0

    CATALOGO: ClassVar[list[dict]] = [
        {'nome': 'Goma de Tapioca', 'preco_unitario': 10, 'porcao': 5},
        {'nome': 'Queijo Coalho', 'preco_unitario': 15, 'porcao': 3},
        {'nome': 'Coco Ralado', 'preco_unitario': 8, 'porcao': 4},
        {'nome': 'Leite Condensado', 'preco_unitario': 12, 'porcao': 5},
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
    def catalogo_para_cliente(cls) -> list[dict]:
        return [
            {
                'nome': i['nome'],
                'preco': i['preco_unitario'],
                'porcao': i['porcao'],
            }
            for i in cls.CATALOGO
        ]

    @classmethod
    def estoque_inicial(cls) -> list['Ingrediente']:
        return [cls(**i) for i in cls.CATALOGO]
