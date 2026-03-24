import random

from services.bairro_service import BairroService


class JogoService:
    TOLERANCIA_PRECO = 3
    CLIENTES_POR_DIA_MIN = 15
    CLIENTES_POR_DIA_MAX = 40

    @staticmethod
    def processar_dia(
        id_bairro: int,
        preco_tapioca: float,
        estoque_disponivel: int,
    ) -> dict:
        bairro = BairroService.buscar_por_id(id_bairro)
        if not bairro:
            return {
                'erro': 'Bairro nao encontrado.',
                'lucro': 0,
                'clientes_totais': 0,
                'clientes_atendidos': 0,
                'clientes_perdidos': 0,
                'estoque_esgotado': False,
                'satisfacao_delta': 0,
                'mensagem': 'Bairro invalido.',
            }

        clientes_totais = JogoService._gerar_clientes_do_dia(
            bairro.preferencia_tapioca
        )
        satisfacao_delta = JogoService._calcular_satisfacao(
            preco_tapioca, bairro.preferencia_preco
        )
        taxa_desistencia = JogoService._taxa_desistencia(satisfacao_delta)

        clientes_interessados = round(clientes_totais * (1 - taxa_desistencia))
        clientes_perdidos = clientes_totais - clientes_interessados

        estoque_esgotado = clientes_interessados > estoque_disponivel
        clientes_atendidos = (
            estoque_disponivel if estoque_esgotado else clientes_interessados
        )

        lucro = round(clientes_atendidos * preco_tapioca, 2)
        mensagem = JogoService._gerar_mensagem(
            satisfacao_delta=satisfacao_delta,
            clientes_atendidos=clientes_atendidos,
            clientes_perdidos=clientes_perdidos,
            estoque_esgotado=estoque_esgotado,
            nome_bairro=bairro.nome,
        )

        return {
            'lucro': lucro,
            'clientes_totais': clientes_totais,
            'clientes_atendidos': clientes_atendidos,
            'clientes_perdidos': clientes_perdidos,
            'estoque_esgotado': estoque_esgotado,
            'satisfacao_delta': satisfacao_delta,
            'mensagem': mensagem,
        }

    @staticmethod
    def _gerar_clientes_do_dia(preferencia_tapioca: int) -> int:
        bonus = round(preferencia_tapioca * 1.5)
        return random.randint(
            JogoService.CLIENTES_POR_DIA_MIN + bonus,
            JogoService.CLIENTES_POR_DIA_MAX + bonus,
        )

    @staticmethod
    def _calcular_satisfacao(
        preco_jogador: float, preferencia_preco: int
    ) -> int:
        expectativas = {1: 8.0, 2: 12.0, 3: 15.0, 4: 20.0, 5: 28.0}
        expectativa = expectativas.get(preferencia_preco, 15.0)
        diferenca = preco_jogador - expectativa
        sensibilidade = (6 - preferencia_preco) / 5
        if abs(diferenca) <= JogoService.TOLERANCIA_PRECO:
            return 0
        penalidade_bruta = round(diferenca * sensibilidade)
        return max(-10, min(10, -penalidade_bruta))

    @staticmethod
    def _taxa_desistencia(satisfacao_delta: int) -> float:
        if satisfacao_delta >= 0:
            return 0.0
        return min(0.8, abs(satisfacao_delta) * 0.08)

    @staticmethod
    def _gerar_mensagem(
        satisfacao_delta: int,
        clientes_atendidos: int,
        clientes_perdidos: int,
        estoque_esgotado: bool,
        nome_bairro: str,
    ) -> str:
        partes = []
        if satisfacao_delta > 3:
            partes.append(
                f'Preco excelente para {nome_bairro}! Os clientes adoraram.'
            )
        elif satisfacao_delta >= 0:
            partes.append('Preco justo — boa aceitacao no bairro.')
        elif satisfacao_delta >= -4:
            partes.append(
                f'Preco um pouco acima do esperado em {nome_bairro}.'
            )
        else:
            partes.append(
                f'Preco muito alto para {nome_bairro}. '
                f'Muitos clientes foram embora.'
            )
        partes.append(
            f'{clientes_atendidos} vendas realizadas'
            + (
                f', {clientes_perdidos} desistiram.'
                if clientes_perdidos
                else '.'
            )
        )
        if estoque_esgotado:
            partes.append('Estoque esgotado antes do fim do dia!')
        return ' '.join(partes)
