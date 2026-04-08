import random

from models.ingrediente import Ingrediente
from models.sessao_jogo import SessaoJogo
from services.bairro_service import BairroService


class JogoService:
    TOLERANCIA_PRECO = 2

    CLIENTES_DIA_MIN = 15
    CLIENTES_DIA_MAX = 40

    PESO_PRECO = 0.4
    PESO_RECEITA = 0.6

    BONUS_CLIENTES_POR_SAT = 2

    ELASTICIDADE_PRECO = 0.7

    @staticmethod
    def processar_dia(sessao: SessaoJogo) -> dict:
        bairro = BairroService.buscar_por_id(sessao.id_bairro)
        if not bairro:
            return {'erro': 'Bairro nao encontrado.'}

        estoque_disponivel = sessao.tapiocas_possiveis()
        if estoque_disponivel == 0:
            return {'erro': 'Sem estoque para iniciar o dia.'}

        preco_ideal = Ingrediente.preco_ideal(bairro.nome)

        clientes_totais = JogoService._gerar_clientes(
            preferencia_tapioca=bairro.preferencia_tapioca,
            satisfacao_atual=sessao.satisfacao,
            preco_jogador=sessao.preco_tapioca,
            preco_ideal=preco_ideal,
        )

        delta_preco = JogoService._delta_preco(
            sessao.preco_tapioca, bairro.nome
        )
        delta_receita = JogoService._delta_receita(sessao.receita, bairro.nome)
        satisfacao_delta = JogoService._combinar_deltas(
            delta_preco, delta_receita
        )

        taxa_preco, taxa_receita = JogoService._taxas_desistencia(
            delta_preco, delta_receita
        )
        taxa_total = min(0.9, taxa_preco + taxa_receita)

        clientes_perdidos_preco = round(clientes_totais * taxa_preco)
        clientes_perdidos_receita = round(clientes_totais * taxa_receita)
        clientes_perdidos_total = round(clientes_totais * taxa_total)
        clientes_interessados = clientes_totais - clientes_perdidos_total

        estoque_esgotado = clientes_interessados > estoque_disponivel
        clientes_atendidos = (
            estoque_disponivel if estoque_esgotado else clientes_interessados
        )

        for ing in sessao.estoque:
            porcao = sessao.receita.get(ing.nome, 0)
            ing.quantidade = max(
                0, ing.quantidade - porcao * clientes_atendidos
            )

        lucro = round(clientes_atendidos * sessao.preco_tapioca, 2)
        sessao.budget += lucro
        sessao.faturamento_total += lucro
        sessao.gasto_total += sessao.gasto_hoje
        sessao.satisfacao = max(
            0, min(10, sessao.satisfacao + satisfacao_delta)
        )
        sessao.satisfacao_historico.append(sessao.satisfacao)

        mensagem = JogoService._gerar_mensagem(
            delta_preco=delta_preco,
            delta_receita=delta_receita,
            satisfacao_delta=satisfacao_delta,
            clientes_atendidos=clientes_atendidos,
            clientes_perdidos_preco=clientes_perdidos_preco,
            clientes_perdidos_receita=clientes_perdidos_receita,
            estoque_esgotado=estoque_esgotado,
            nome_bairro=bairro.nome,
            preco_ideal=preco_ideal,
            dia_atual=sessao.dia_atual,
        )

        return {
            'lucro': lucro,
            'clientes_totais': clientes_totais,
            'clientes_atendidos': clientes_atendidos,
            'clientes_perdidos': clientes_perdidos_total,
            'clientes_perdidos_preco': clientes_perdidos_preco,
            'clientes_perdidos_receita': clientes_perdidos_receita,
            'estoque_esgotado': estoque_esgotado,
            'satisfacao_delta': satisfacao_delta,
            'delta_preco': delta_preco,
            'delta_receita': delta_receita,
            'mensagem': mensagem,
            'sessao': sessao.snapshot_publico(),
        }

    @staticmethod
    def avancar_dia(sessao: SessaoJogo) -> None:
        sessao.preco_dia_anterior = sessao.preco_tapioca
        sessao.dia_atual += 1
        sessao.gasto_hoje = 0.0
        sessao.receita = {
            'Goma de Tapioca': 1,
            'Queijo Coalho': 0,
            'Coco Ralado': 0,
            'Leite Condensado': 0,
        }
        sessao.preco_tapioca = 15.0

    @staticmethod
    def _gerar_clientes(
        preferencia_tapioca: int,
        satisfacao_atual: int,
        preco_jogador: float,
        preco_ideal: float,
    ) -> int:
        ratio = preco_ideal / max(preco_jogador, 1.0)
        fator_preco = min(
            1.5, max(0.2, ratio**JogoService.ELASTICIDADE_PRECO)
        )

        bonus_tapioca = round(preferencia_tapioca * 1.5)
        bonus_sat = (satisfacao_atual - 5) * JogoService.BONUS_CLIENTES_POR_SAT

        base_min = max(
            5,
            round(JogoService.CLIENTES_DIA_MIN * fator_preco)
            + bonus_tapioca
            + bonus_sat,
        )
        base_max = max(
            10,
            round(JogoService.CLIENTES_DIA_MAX * fator_preco)
            + bonus_tapioca
            + bonus_sat,
        )
        return random.randint(base_min, base_max)

    @staticmethod
    def _delta_preco(preco_jogador: float, nome_bairro: str) -> int:
        ideal = Ingrediente.preco_ideal(nome_bairro)
        diferenca = preco_jogador - ideal

        if abs(diferenca) <= JogoService.TOLERANCIA_PRECO:
            return 0

        if diferenca > 0:
            raw = -round(diferenca * 0.5)
        else:
            pct_abaixo = abs(diferenca) / ideal
            if pct_abaixo <= 0.30:
                raw = round(abs(diferenca) * 0.3)
            else:
                raw = round(3 - (pct_abaixo - 0.30) * 10)

        return max(-5, min(5, raw))

    @staticmethod
    def _delta_receita(
        receita_jogador: dict[str, int], nome_bairro: str
    ) -> int:
        ideal = Ingrediente.receita_ideal(nome_bairro)
        ingredientes = list(ideal.keys())

        total_ideal = sum(ideal.values()) or 1

        distancia = sum(
            abs((receita_jogador.get(ing, 0)) - ideal.get(ing, 0))
            for ing in ingredientes
        )

        normalizado = min(1.0, distancia / (total_ideal * 2))
        delta = round(5 * (1 - 2 * normalizado))
        return max(-5, min(5, delta))

    @staticmethod
    def _combinar_deltas(delta_preco: int, delta_receita: int) -> int:
        combinado = (
            delta_preco * JogoService.PESO_PRECO
            + delta_receita * JogoService.PESO_RECEITA
        )
        return max(-10, min(10, round(combinado * 2)))

    @staticmethod
    def _taxas_desistencia(
        delta_preco: int, delta_receita: int
    ) -> tuple[float, float]:
        taxa_preco = (
            0.0 if delta_preco >= 0 else min(0.5, abs(delta_preco) * 0.06)
        )
        taxa_receita = (
            0.0 if delta_receita >= 0 else min(0.5, abs(delta_receita) * 0.04)
        )
        return taxa_preco, taxa_receita

    @staticmethod
    def _gerar_mensagem(
        delta_preco: int,
        delta_receita: int,
        satisfacao_delta: int,
        clientes_atendidos: int,
        clientes_perdidos_preco: int,
        clientes_perdidos_receita: int,
        estoque_esgotado: bool,
        nome_bairro: str,
        preco_ideal: float,
        dia_atual: int,
    ) -> str:
        partes = []

        if delta_preco >= 2:
            partes.append(
                f'Preco bem recebido pelos clientes de {nome_bairro} '
                f'— muitos compraram!'
            )
        elif delta_preco == 0 or delta_preco == 1:
            partes.append(
                f'Preco dentro do esperado para o perfil de {nome_bairro}.'
            )
        elif delta_preco <= -4:
            partes.append(
                f'Preco muito acima do esperado em {nome_bairro}. '
                f'Varios clientes foram embora.'
            )
        elif delta_preco <= -2:
            partes.append(
                f'Preco um pouco acima do que os clientes de {nome_bairro} '
                f'costumam pagar.'
            )
        else:
            partes.append(
                f'Preco muito abaixo do que o bairro de {nome_bairro} valoriza '
                f'— o produto pareceu de baixa qualidade.'
            )

        if delta_receita >= 4:
            partes.append('A receita foi exatamente o que o bairro queria!')
        elif delta_receita >= 1:
            partes.append('A receita foi bem recebida pelo bairro.')
        elif delta_receita == 0:
            partes.append('A receita esta proxima do gosto do bairro.')
        else:
            partes.append(
                'A receita nao combinou muito com o perfil do bairro — '
                'experimente os ingredientes sugeridos amanha.'
            )

        partes.append(f'{clientes_atendidos} vendas realizadas.')

        if clientes_perdidos_preco > 0:
            partes.append(f'{clientes_perdidos_preco} desistiram pelo preco.')
        if clientes_perdidos_receita > 0:
            partes.append(
                f'{clientes_perdidos_receita} nao gostaram da receita.'
            )

        fator = Ingrediente.fator_inflacao(dia_atual)
        if fator > 1.0:
            partes.append(
                f'Lembre-se: os insumos estao {round((fator - 1) * 100):.0f}% '
                f'mais caros do que no inicio do jogo.'
            )

        if estoque_esgotado:
            partes.append(
                'Estoque esgotado antes do fim do dia — '
                'considere comprar mais ingredientes amanha!'
            )

        return ' '.join(partes)
