import uuid
from dataclasses import dataclass, field

from models.ingrediente import Ingrediente


@dataclass
class SessaoJogo:
    sessao_id: str
    id_bairro: int
    tempo_de_jogo: str
    dia_atual: int = 1
    budget: float = 100.0
    satisfacao: int = 5  # 0-10
    estoque: list[Ingrediente] = field(default_factory=list)
    receita: dict[str, int] = field(default_factory=dict)
    preco_tapioca: float = 15.0
    preco_dia_anterior: float | None = None
    gasto_hoje: float = 0.0
    finalizado: bool = False

    def estoque_para_cliente(self) -> list[dict]:
        return [
            {'nome': ing.nome, 'quantidade': ing.quantidade}
            for ing in self.estoque
        ]

    def tapiocas_possiveis(self) -> int:
        limites = [
            ing.quantidade // (self.receita.get(ing.nome) or 1)
            for ing in self.estoque
            if (self.receita.get(ing.nome) or 0) > 0
        ]
        return min(limites) if limites else 0

    def comprar_ingrediente(self, nome: str) -> dict:
        ing = next((i for i in self.estoque if i.nome == nome), None)
        if ing is None:
            return {'ok': False, 'erro': 'Ingrediente nao encontrado.'}

        preco_real = Ingrediente.preco_com_inflacao(nome, self.dia_atual)
        if self.budget < preco_real:
            return {'ok': False, 'erro': 'Saldo insuficiente.'}

        ing.quantidade += ing.porcao
        self.budget -= preco_real
        self.gasto_hoje += preco_real
        return {
            'ok': True,
            'nome': ing.nome,
            'quantidade': ing.quantidade,
            'budget': round(self.budget, 2),
            'gasto_hoje': round(self.gasto_hoje, 2),
        }

    def devolver_ingrediente(self, nome: str) -> dict:
        ing = next((i for i in self.estoque if i.nome == nome), None)
        if ing is None:
            return {'ok': False, 'erro': 'Ingrediente nao encontrado.'}
        if ing.quantidade < ing.porcao:
            return {
                'ok': False,
                'erro': 'Estoque insuficiente para devolucao.',
            }

        preco_real = Ingrediente.preco_com_inflacao(nome, self.dia_atual)
        ing.quantidade -= ing.porcao
        self.budget += preco_real
        self.gasto_hoje -= preco_real
        return {
            'ok': True,
            'nome': ing.nome,
            'quantidade': ing.quantidade,
            'budget': round(self.budget, 2),
            'gasto_hoje': round(self.gasto_hoje, 2),
        }

    def atualizar_receita(self, nova_receita: dict[str, int]) -> dict:
        for nome, qtd in nova_receita.items():
            if qtd < 0:
                return {'ok': False, 'erro': f'Porcao invalida para {nome}.'}
        self.receita = nova_receita
        return {'ok': True, 'tapiocas_possiveis': self.tapiocas_possiveis()}

    def definir_preco(self, preco: float) -> dict:
        if preco <= 0:
            return {'ok': False, 'erro': 'Preco deve ser positivo.'}
        self.preco_tapioca = preco
        return {'ok': True}

    def snapshot_publico(self) -> dict:
        fator = Ingrediente.fator_inflacao(self.dia_atual)
        return {
            'sessao_id': self.sessao_id,
            'dia_atual': self.dia_atual,
            'budget': round(self.budget, 2),
            'satisfacao': self.satisfacao,
            'preco_tapioca': self.preco_tapioca,
            'preco_dia_anterior': self.preco_dia_anterior,
            'gasto_hoje': round(self.gasto_hoje, 2),
            'tapiocas_possiveis': self.tapiocas_possiveis(),
            'estoque': self.estoque_para_cliente(),
            'receita': dict(self.receita),
            'finalizado': self.finalizado,
            'fator_inflacao': round(fator, 2),
        }


_sessoes: dict[str, SessaoJogo] = {}


def criar_sessao(id_bairro: int, tempo_de_jogo: str) -> SessaoJogo:
    sid = str(uuid.uuid4())
    sessao = SessaoJogo(
        sessao_id=sid,
        id_bairro=id_bairro,
        tempo_de_jogo=tempo_de_jogo,
        estoque=Ingrediente.estoque_inicial(),
        receita={
            'Goma de Tapioca': 1,
            'Queijo Coalho': 0,
            'Coco Ralado': 0,
            'Leite Condensado': 0,
        },
    )
    _sessoes[sid] = sessao
    return sessao


def obter_sessao(sessao_id: str) -> SessaoJogo | None:
    return _sessoes.get(sessao_id)


def remover_sessao(sessao_id: str) -> None:
    _sessoes.pop(sessao_id, None)
