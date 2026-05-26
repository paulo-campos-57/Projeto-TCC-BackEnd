from unittest.mock import patch

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
        satisfacao_historico=[],
        faturamento_total=0.0,
        gasto_total=0.0,
        gasto_hoje=0.0,
        dia_atual=1,
    )
    defaults.update(kwargs)
    return SessaoJogo(**defaults)


class TestTaxasDesistencia:
    def test_deltas_positivos_sem_desistencia(self):
        taxa_p, taxa_r = JogoService._taxas_desistencia(3, 4, 12.0, 12.0)
        assert taxa_p == 0.0
        assert taxa_r == 0.0

    def test_delta_preco_negativo_gera_taxa(self):
        taxa_p, taxa_r = JogoService._taxas_desistencia(-3, 0, 15.0, 12.0)
        assert taxa_p > 0.0
        assert taxa_r == 0.0

    def test_preco_abusivo_gera_desistencia_total(self):
        taxa_p, taxa_r = JogoService._taxas_desistencia(-5, 0, 20.0, 12.0)
        assert taxa_p == 1.0
        assert taxa_r == 0.0

    def test_taxa_receita_limitada_mesmo_com_preco_alto(self):
        _, taxa_r = JogoService._taxas_desistencia(0, -5, 12.0, 12.0)
        assert taxa_r <= 0.5


class TestGerarMensagem:
    def test_mensagem_preco_abusivo(self):
        msg = JogoService._gerar_mensagem(
            delta_preco=-5,
            delta_receita=0,
            satisfacao_delta=-2,
            clientes_atendidos=0,
            clientes_perdidos_preco=20,
            clientes_perdidos_receita=0,
            estoque_esgotado=False,
            nome_bairro='Várzea',
            preco_ideal=12.0,
            preco_jogador=25.0,
            dia_atual=1,
        )
        assert 'abusivo' in msg.lower()
        assert 'Ninguém aceitou pagar' in msg

    def test_mensagem_vendas_sucesso(self):
        msg = JogoService._gerar_mensagem(
            delta_preco=0,
            delta_receita=5,
            satisfacao_delta=2,
            clientes_atendidos=10,
            clientes_perdidos_preco=0,
            clientes_perdidos_receita=0,
            estoque_esgotado=False,
            nome_bairro='Várzea',
            preco_ideal=12.0,
            preco_jogador=12.0,
            dia_atual=1,
        )
        assert '10 vendas realizadas' in msg
        assert 'sucesso absoluto' in msg


class TestProcessarDiaIntegracao:
    def _prepara_sessao_com_estoque(self, preco=12.0):
        sessao = make_sessao(preco=preco)
        goma = next(i for i in sessao.estoque if i.nome == 'Goma de Tapioca')
        goma.quantidade = 100  # Garante estoque
        return sessao

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_vendas_zeradas_por_preco_abusivo(self, _mock):
        sessao = self._prepara_sessao_com_estoque(preco=50.0)
        resultado = JogoService.processar_dia(sessao)

        assert resultado['clientes_atendidos'] == 0
        assert resultado['lucro'] == 0
        assert resultado['clientes_perdidos'] == resultado['clientes_totais']
        assert 'abusivo' in resultado['mensagem']

    @patch('services.jogo_service.random.randint', return_value=20)
    def test_processamento_normal(self, _mock):
        sessao = self._prepara_sessao_com_estoque(preco=12.0)
        resultado = JogoService.processar_dia(sessao)

        assert resultado['clientes_atendidos'] > 0
        assert resultado['lucro'] > 0
        assert 'vendas realizadas' in resultado['mensagem']
