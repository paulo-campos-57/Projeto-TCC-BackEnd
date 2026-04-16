import pytest

from models.ingrediente import Ingrediente
from models.sessao_jogo import SessaoJogo


@pytest.fixture
def sessao_padrao() -> SessaoJogo:
    return SessaoJogo(
        sessao_id='fixture-id',
        id_bairro=5,
        tempo_de_jogo='1 semana',
        estoque=Ingrediente.estoque_inicial(),
        receita={
            'Goma de Tapioca': 1,
            'Queijo Coalho': 0,
            'Coco Ralado': 0,
            'Leite Condensado': 0,
        },
    )


@pytest.fixture
def sessao_com_estoque(sessao_padrao) -> SessaoJogo:
    goma = next(
        i for i in sessao_padrao.estoque if i.nome == 'Goma de Tapioca'
    )
    goma.quantidade = 50
    return sessao_padrao
