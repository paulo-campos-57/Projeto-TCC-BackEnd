import pytest

from models.ingrediente import Ingrediente


class TestFatorInflacao:
    def test_dias_1_a_4_sem_inflacao(self):
        for dia in [1, 2, 3, 4]:
            assert Ingrediente.fator_inflacao(dia) == 1.0, f'dia={dia}'

    def test_dias_5_a_9_dez_porcento(self):
        for dia in [5, 6, 7, 8, 9]:
            assert Ingrediente.fator_inflacao(dia) == pytest.approx(
                1.1
            ), f'dia={dia}'

    def test_dias_10_a_14_vinte_porcento(self):
        for dia in [10, 11, 14]:
            assert Ingrediente.fator_inflacao(dia) == pytest.approx(
                1.2
            ), f'dia={dia}'

    def test_dia_15_trinta_porcento(self):
        assert Ingrediente.fator_inflacao(15) == pytest.approx(1.3)

    def test_dia_30_sessenta_porcento(self):
        assert Ingrediente.fator_inflacao(30) == pytest.approx(1.6)

    def test_fator_nunca_negativo(self):
        for dia in range(1, 31):
            assert Ingrediente.fator_inflacao(dia) >= 1.0


class TestPrecoComInflacao:
    def test_goma_dia_1_sem_inflacao(self):
        assert Ingrediente.preco_com_inflacao(
            'Goma de Tapioca', 1
        ) == pytest.approx(10.0)

    def test_goma_dia_5_com_inflacao(self):
        assert Ingrediente.preco_com_inflacao(
            'Goma de Tapioca', 5
        ) == pytest.approx(11.0)

    def test_goma_dia_10_com_inflacao(self):
        assert Ingrediente.preco_com_inflacao(
            'Goma de Tapioca', 10
        ) == pytest.approx(12.0)

    def test_queijo_dia_5_com_inflacao(self):
        assert Ingrediente.preco_com_inflacao(
            'Queijo Coalho', 5
        ) == pytest.approx(16.5)

    def test_ingrediente_inexistente_retorna_zero(self):
        assert (
            Ingrediente.preco_com_inflacao('Ingrediente Inexistente', 1) == 0.0
        )

    def test_todos_ingredientes_existem_no_catalogo(self):
        nomes = [
            'Goma de Tapioca',
            'Queijo Coalho',
            'Coco Ralado',
            'Leite Condensado',
        ]
        for nome in nomes:
            assert (
                Ingrediente.preco_com_inflacao(nome, 1) > 0
            ), f'{nome} não encontrado'


class TestCatalogParaCliente:
    def test_retorna_quatro_ingredientes(self):
        catalogo = Ingrediente.catalogo_para_cliente(dia_atual=1)
        assert len(catalogo) == 4

    def test_estrutura_de_cada_item(self):
        catalogo = Ingrediente.catalogo_para_cliente(dia_atual=1)
        for item in catalogo:
            assert 'nome' in item
            assert 'preco' in item
            assert 'porcao' in item

    def test_precos_aumentam_com_inflacao(self):
        catalogo_dia1 = Ingrediente.catalogo_para_cliente(dia_atual=1)
        catalogo_dia5 = Ingrediente.catalogo_para_cliente(dia_atual=5)
        for item1, item5 in zip(catalogo_dia1, catalogo_dia5):
            assert (
                item5['preco'] > item1['preco']
            ), f"{item1['nome']}: preço não aumentou"

    def test_nao_expoe_preco_base_diretamente(self):
        catalogo = Ingrediente.catalogo_para_cliente(dia_atual=1)
        for item in catalogo:
            assert 'preco_base' not in item


class TestReceitaEPrecoIdeal:
    def test_receita_ideal_bairro_valido(self):
        receita = Ingrediente.receita_ideal('Casa Forte')
        assert isinstance(receita, dict)
        assert 'Goma de Tapioca' in receita

    def test_receita_ideal_bairro_desconhecido_retorna_default(self):
        receita = Ingrediente.receita_ideal('Bairro Inexistente')
        assert receita['Goma de Tapioca'] == 1
        assert receita['Queijo Coalho'] == 0

    def test_preco_ideal_bairro_valido(self):
        assert Ingrediente.preco_ideal('Casa Forte') == pytest.approx(22.0)
        assert Ingrediente.preco_ideal('Ibura') == pytest.approx(7.0)

    def test_preco_ideal_bairro_desconhecido_retorna_default(self):
        assert Ingrediente.preco_ideal('Bairro Inexistente') == pytest.approx(
            15.0
        )

    def test_todos_os_seis_bairros_tem_receita(self):
        bairros = [
            'Casa Forte',
            'Recife Antigo',
            'Ibura',
            'Boa Viagem',
            'Várzea',
            'Areias',
        ]
        for bairro in bairros:
            receita = Ingrediente.receita_ideal(bairro)
            assert len(receita) > 0, f'{bairro} sem receita'

    def test_todos_os_seis_bairros_tem_preco(self):
        bairros = [
            'Casa Forte',
            'Recife Antigo',
            'Ibura',
            'Boa Viagem',
            'Várzea',
            'Areias',
        ]
        for bairro in bairros:
            preco = Ingrediente.preco_ideal(bairro)
            assert preco > 0, f'{bairro} sem preço ideal'
