"""
Testes unitários para services/jogo_service.py

Cobre:
- _delta_preco: zona ideal, acima, muito acima, abaixo, subprecificação severa
- _delta_receita: receita idêntica, distância parcial, completamente diferente
- _combinar_deltas: pesos e clamp nos limites
- _taxas_desistencia: desistência separada por causa
- avancar_dia: reset correto dos campos, preservação do estoque
- processar_dia: integração das mecânicas (mockando aleatoriedade)
"""

from unittest.mock import patch

import pytest

from models.ingrediente import Ingrediente
from models.sessao_jogo import SessaoJogo
from services.jogo_service import JogoService


def make_sessao(bairro_id=5, preco=12.0, **kwargs) -> SessaoJogo:
    defaults = dict(
        sessao_id='test-id',
        id_bairro=bairro_id,
        tempo_de_jogo='1 semana',
        budget=100.0,
        satisfacao=5,
        estoque=Ingrediente.estoque_inicial(),
        receita={
            'Goma de Tapioca': 1,
            'Queijo Coalho': 0,
            'Coco Ralado': 0,
            'Leite Condensado': 0,
        },
        preco_tapioca=preco,
    )
    defaults.update(kwargs)
    return SessaoJogo(**defaults)


class TestDeltaPreco:
    def test_preco_no_ideal_delta_zero(self):
        assert JogoService._delta_preco(12.0, 'Várzea') == 0

    def test_preco_dentro_da_tolerancia_delta_zero(self):
        assert JogoService._delta_preco(10.0, 'Várzea') == 0
        assert JogoService._delta_preco(14.0, 'Várzea') == 0

    def test_preco_um_pouco_acima_delta_negativo(self):
        delta = JogoService._delta_preco(18.0, 'Várzea')
        assert delta < 0

    def test_preco_muito_acima_clamp_menos_cinco(self):
        delta = JogoService._delta_preco(30.0, 'Várzea')
        assert delta == -5

    def test_preco_levemente_abaixo_delta_positivo(self):
        delta = JogoService._delta_preco(9.0, 'Várzea')
        assert delta > 0

    def test_preco_muito_abaixo_penalidade_bilateral(self):
        delta = JogoService._delta_preco(3.0, 'Várzea')
        assert delta < 0

    def test_delta_sempre_dentro_do_intervalo(self):
        for preco in [1, 5, 10, 12, 15, 20, 50]:
            delta = JogoService._delta_preco(float(preco), 'Várzea')
            assert (
                -5 <= delta <= 5
            ), f'preco={preco} → delta={delta} fora do range'


class TestDeltaReceita:
    def test_receita_identica_ao_ideal_delta_cinco(self):
        receita_ideal = Ingrediente.receita_ideal('Várzea')
        delta = JogoService._delta_receita(receita_ideal, 'Várzea')
        assert delta == 5

    def test_receita_completamente_errada_delta_negativo(self):
        receita_errada = {
            'Goma de Tapioca': 0,
            'Queijo Coalho': 5,
            'Coco Ralado': 5,
            'Leite Condensado': 0,
        }
        delta = JogoService._delta_receita(receita_errada, 'Várzea')
        assert delta < 0

    def test_receita_vazia_delta_neutro(self):
        delta = JogoService._delta_receita({}, 'Várzea')
        assert delta == 0

    def test_delta_sempre_dentro_do_intervalo(self):
        for receita in [
            {},
            {'Goma de Tapioca': 10},
            Ingrediente.receita_ideal('Várzea'),
        ]:
            delta = JogoService._delta_receita(receita, 'Várzea')
            assert -5 <= delta <= 5, f'delta={delta} fora do range'


class TestCombinarDeltas:
    def test_ambos_maximos_resulta_dez(self):
        assert JogoService._combinar_deltas(5, 5) == 10

    def test_ambos_minimos_resulta_menos_dez(self):
        assert JogoService._combinar_deltas(-5, -5) == -10

    def test_ambos_zero_resulta_zero(self):
        assert JogoService._combinar_deltas(0, 0) == 0

    def test_pesos_corretos_preco_40_receita_60(self):
        assert JogoService._combinar_deltas(0, 5) == 6

    def test_clamp_superior_em_dez(self):
        assert JogoService._combinar_deltas(5, 5) == 10

    def test_clamp_inferior_em_menos_dez(self):
        assert JogoService._combinar_deltas(-5, -5) == -10


class TestTaxasDesistencia:
    def test_deltas_positivos_sem_desistencia(self):
        taxa_p, taxa_r = JogoService._taxas_desistencia(3, 4)
        assert taxa_p == 0.0
        assert taxa_r == 0.0

    def test_delta_preco_negativo_gera_taxa(self):
        taxa_p, taxa_r = JogoService._taxas_desistencia(-3, 0)
        assert taxa_p > 0.0
        assert taxa_r == 0.0

    def test_delta_receita_negativo_gera_taxa(self):
        taxa_p, taxa_r = JogoService._taxas_desistencia(0, -3)
        assert taxa_p == 0.0
        assert taxa_r > 0.0

    def test_taxa_preco_nunca_passa_de_cinquenta_porcento(self):
        taxa_p, _ = JogoService._taxas_desistencia(-5, 0)
        assert taxa_p <= 0.5

    def test_taxa_receita_nunca_passa_de_cinquenta_porcento(self):
        _, taxa_r = JogoService._taxas_desistencia(0, -5)
        assert taxa_r <= 0.5


class TestAvancarDia:
    def test_dia_atual_incrementa(self):
        sessao = make_sessao()
        assert sessao.dia_atual == 1
        JogoService.avancar_dia(sessao)
        assert sessao.dia_atual == 2

    def test_gasto_hoje_reseta(self):
        sessao = make_sessao()
        sessao.gasto_hoje = 45.0
        JogoService.avancar_dia(sessao)
        assert sessao.gasto_hoje == pytest.approx(0.0)

    def test_preco_dia_anterior_salvo(self):
        sessao = make_sessao(preco=20.0)
        JogoService.avancar_dia(sessao)
        assert sessao.preco_dia_anterior == pytest.approx(20.0)

    def test_preco_tapioca_reseta_para_padrao(self):
        sessao = make_sessao(preco=30.0)
        JogoService.avancar_dia(sessao)
        assert sessao.preco_tapioca == pytest.approx(15.0)

    def test_estoque_nao_e_resetado(self):
        sessao = make_sessao()
        goma = next(i for i in sessao.estoque if i.nome == 'Goma de Tapioca')
        goma.quantidade = 20
        JogoService.avancar_dia(sessao)
        goma_depois = next(
            i for i in sessao.estoque if i.nome == 'Goma de Tapioca'
        )
        assert goma_depois.quantidade == 20

    def test_receita_reseta_para_padrao(self):
        sessao = make_sessao()
        sessao.receita = {'Goma de Tapioca': 3, 'Queijo Coalho': 2}
        JogoService.avancar_dia(sessao)
        assert sessao.receita['Goma de Tapioca'] == 1
        assert sessao.receita['Queijo Coalho'] == 0


class TestProcessarDia:
    def _prepara_sessao_com_estoque(self, preco=12.0):
        sessao = make_sessao(preco=preco)
        goma = next(i for i in sessao.estoque if i.nome == 'Goma de Tapioca')
        goma.quantidade = 50
        return sessao

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_retorna_campos_obrigatorios(self, _mock):
        sessao = self._prepara_sessao_com_estoque()
        resultado = JogoService.processar_dia(sessao)
        campos = [
            'lucro',
            'clientes_totais',
            'clientes_atendidos',
            'clientes_perdidos',
            'clientes_perdidos_preco',
            'clientes_perdidos_receita',
            'estoque_esgotado',
            'satisfacao_delta',
            'delta_preco',
            'delta_receita',
            'mensagem',
            'sessao',
        ]
        for campo in campos:
            assert campo in resultado, f"Campo '{campo}' ausente no resultado"

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_lucro_igual_atendidos_vezes_preco(self, _mock):
        sessao = self._prepara_sessao_com_estoque(preco=15.0)
        resultado = JogoService.processar_dia(sessao)
        atendidos = resultado['clientes_atendidos']
        assert resultado['lucro'] == pytest.approx(atendidos * 15.0)

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_budget_aumenta_apos_dia(self, _mock):
        sessao = self._prepara_sessao_com_estoque()
        budget_antes = sessao.budget
        JogoService.processar_dia(sessao)
        assert sessao.budget > budget_antes

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_satisfacao_historico_registrado(self, _mock):
        sessao = self._prepara_sessao_com_estoque()
        JogoService.processar_dia(sessao)
        assert len(sessao.satisfacao_historico) == 1

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_faturamento_total_acumulado(self, _mock):
        sessao = self._prepara_sessao_com_estoque()
        JogoService.processar_dia(sessao)
        assert sessao.faturamento_total > 0

    def test_sem_estoque_retorna_erro(self):
        sessao = make_sessao()
        resultado = JogoService.processar_dia(sessao)
        assert 'erro' in resultado

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_bairro_invalido_retorna_erro(self, _mock):
        sessao = make_sessao(bairro_id=999)
        resultado = JogoService.processar_dia(sessao)
        assert 'erro' in resultado
