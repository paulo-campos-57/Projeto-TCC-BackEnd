import pytest

from models.ingrediente import Ingrediente
from models.sessao_jogo import SessaoJogo


def make_sessao(**kwargs) -> SessaoJogo:
    defaults = dict(
        sessao_id='test-id',
        id_bairro=1,
        tempo_de_jogo='1 semana',
        estoque=Ingrediente.estoque_inicial(),
        receita={
            'Goma de Tapioca': 1,
            'Queijo Coalho': 0,
            'Coco Ralado': 0,
            'Leite Condensado': 0,
        },
    )
    defaults.update(kwargs)
    return SessaoJogo(**defaults)


class TestTapiocasPossiveis:
    def test_gargalo_pelo_ingrediente_com_menos_estoque(self):
        sessao = make_sessao()
        goma = next(i for i in sessao.estoque if i.nome == 'Goma de Tapioca')
        queijo = next(i for i in sessao.estoque if i.nome == 'Queijo Coalho')
        goma.quantidade = 10
        queijo.quantidade = 6
        sessao.receita = {'Goma de Tapioca': 2, 'Queijo Coalho': 1}
        assert sessao.tapiocas_possiveis() == 5

    def test_sem_estoque_retorna_zero(self):
        sessao = make_sessao()
        for ing in sessao.estoque:
            ing.quantidade = 0
        assert sessao.tapiocas_possiveis() == 0

    def test_receita_vazia_retorna_zero(self):
        sessao = make_sessao()
        sessao.receita = {'Goma de Tapioca': 0, 'Queijo Coalho': 0}
        assert sessao.tapiocas_possiveis() == 0

    def test_ingrediente_na_receita_com_estoque_zero(self):
        sessao = make_sessao()
        goma = next(i for i in sessao.estoque if i.nome == 'Goma de Tapioca')
        queijo = next(i for i in sessao.estoque if i.nome == 'Queijo Coalho')
        goma.quantidade = 0
        queijo.quantidade = 10
        sessao.receita = {'Goma de Tapioca': 1, 'Queijo Coalho': 1}
        assert sessao.tapiocas_possiveis() == 0

    def test_apenas_goma_na_receita(self):
        sessao = make_sessao()
        goma = next(i for i in sessao.estoque if i.nome == 'Goma de Tapioca')
        goma.quantidade = 5
        sessao.receita = {'Goma de Tapioca': 1}
        assert sessao.tapiocas_possiveis() == 5


class TestComprarIngrediente:
    def test_compra_basica_dia_1_sem_inflacao(self):
        sessao = make_sessao(budget=100.0, dia_atual=1)
        resultado = sessao.comprar_ingrediente('Goma de Tapioca')
        assert resultado['ok'] is True
        assert resultado['quantidade'] == 5  # porcao da Goma
        assert resultado['budget'] == pytest.approx(90.0)  # 100 - 10
        assert resultado['gasto_hoje'] == pytest.approx(10.0)

    def test_compra_dia_5_aplica_inflacao(self):
        sessao = make_sessao(budget=100.0, dia_atual=5)
        resultado = sessao.comprar_ingrediente('Goma de Tapioca')
        assert resultado['ok'] is True
        assert resultado['budget'] == pytest.approx(89.0)  # 100 - 11
        assert resultado['gasto_hoje'] == pytest.approx(11.0)

    def test_saldo_insuficiente_retorna_erro(self):
        sessao = make_sessao(budget=5.0, dia_atual=1)
        resultado = sessao.comprar_ingrediente('Goma de Tapioca')
        assert resultado['ok'] is False
        assert 'erro' in resultado
        assert sessao.budget == pytest.approx(5.0)

    def test_ingrediente_inexistente_retorna_erro(self):
        sessao = make_sessao()
        resultado = sessao.comprar_ingrediente('Ingrediente Inventado')
        assert resultado['ok'] is False

    def test_multiplas_compras_acumulam_gasto_hoje(self):
        sessao = make_sessao(budget=100.0, dia_atual=1)
        sessao.comprar_ingrediente('Goma de Tapioca')  # -10
        sessao.comprar_ingrediente('Goma de Tapioca')  # -10
        assert sessao.gasto_hoje == pytest.approx(20.0)
        assert sessao.budget == pytest.approx(80.0)


class TestDevolverIngrediente:
    def test_devolucao_restaura_budget(self):
        sessao = make_sessao(budget=100.0, dia_atual=1)
        sessao.comprar_ingrediente('Goma de Tapioca')  # budget=90
        resultado = sessao.devolver_ingrediente('Goma de Tapioca')
        assert resultado['ok'] is True
        assert resultado['budget'] == pytest.approx(100.0)
        assert resultado['quantidade'] == 0

    def test_devolucao_sem_estoque_retorna_erro(self):
        sessao = make_sessao()
        resultado = sessao.devolver_ingrediente('Goma de Tapioca')
        assert resultado['ok'] is False
        assert 'erro' in resultado

    def test_devolucao_ingrediente_inexistente_retorna_erro(self):
        sessao = make_sessao()
        resultado = sessao.devolver_ingrediente('Nao Existe')
        assert resultado['ok'] is False

    def test_devolucao_reduz_gasto_hoje(self):
        sessao = make_sessao(budget=100.0, dia_atual=1)
        sessao.comprar_ingrediente('Goma de Tapioca')
        sessao.devolver_ingrediente('Goma de Tapioca')
        assert sessao.gasto_hoje == pytest.approx(0.0)


class TestAtualizarReceita:
    def test_atualiza_receita_valida(self):
        sessao = make_sessao()
        nova = {'Goma de Tapioca': 2, 'Queijo Coalho': 1}
        resultado = sessao.atualizar_receita(nova)
        assert resultado['ok'] is True
        assert sessao.receita['Goma de Tapioca'] == 2

    def test_retorna_tapiocas_possiveis_atualizado(self):
        sessao = make_sessao()
        goma = next(i for i in sessao.estoque if i.nome == 'Goma de Tapioca')
        goma.quantidade = 10
        resultado = sessao.atualizar_receita({'Goma de Tapioca': 2})
        assert 'tapiocas_possiveis' in resultado
        assert resultado['tapiocas_possiveis'] == 5

    def test_porcao_negativa_retorna_erro(self):
        sessao = make_sessao()
        resultado = sessao.atualizar_receita({'Goma de Tapioca': -1})
        assert resultado['ok'] is False


class TestDefinirPreco:
    def test_preco_valido_atualiza(self):
        sessao = make_sessao()
        resultado = sessao.definir_preco(20.0)
        assert resultado['ok'] is True
        assert sessao.preco_tapioca == pytest.approx(20.0)

    def test_preco_zero_retorna_erro(self):
        sessao = make_sessao()
        resultado = sessao.definir_preco(0.0)
        assert resultado['ok'] is False

    def test_preco_negativo_retorna_erro(self):
        sessao = make_sessao()
        resultado = sessao.definir_preco(-5.0)
        assert resultado['ok'] is False


class TestSnapshotPublico:
    def test_campos_obrigatorios_presentes(self):
        sessao = make_sessao()
        snap = sessao.snapshot_publico()
        campos = [
            'sessao_id',
            'dia_atual',
            'budget',
            'satisfacao',
            'preco_tapioca',
            'preco_dia_anterior',
            'gasto_hoje',
            'tapiocas_possiveis',
            'estoque',
            'receita',
            'finalizado',
            'fator_inflacao',
        ]
        for campo in campos:
            assert campo in snap, f"Campo '{campo}' ausente no snapshot"

    def test_preco_dia_anterior_nulo_no_inicio(self):
        sessao = make_sessao()
        snap = sessao.snapshot_publico()
        assert snap['preco_dia_anterior'] is None

    def test_fator_inflacao_exposto_corretamente(self):
        sessao = make_sessao(dia_atual=5)
        snap = sessao.snapshot_publico()
        assert snap['fator_inflacao'] == pytest.approx(1.1)

    def test_estoque_nao_expoe_preco_unitario(self):
        sessao = make_sessao()
        snap = sessao.snapshot_publico()
        for item in snap['estoque']:
            assert 'preco' not in item
            assert 'preco_unitario' not in item
