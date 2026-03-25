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
