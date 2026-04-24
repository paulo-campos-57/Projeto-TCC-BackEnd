from sqlalchemy import desc

from database import db
from models.resultado import Resultado


class ResultadoService:
    @staticmethod
    def salvar_resultado(
        user_id: str,
        bairro: str,
        tempo_de_jogo: str,
        dias_jogados: int,
        faturamento: float,
        lucro_liquido: float,
        satisfacao_media: float,
        satisfacao_final: int,
    ) -> Resultado:
        resultado = Resultado(
            user_id=user_id,
            bairro=bairro,
            tempo_de_jogo=tempo_de_jogo,
            dias_jogados=dias_jogados,
            faturamento=round(faturamento, 2),
            lucro_liquido=round(lucro_liquido, 2),
            satisfacao_media=round(satisfacao_media, 2),
            satisfacao_final=satisfacao_final,
        )
        db.session.add(resultado)
        db.session.commit()
        return resultado

    @staticmethod
    def listar_por_usuario(user_id: str) -> list[Resultado]:
        return (
            Resultado.query.filter_by(user_id=user_id)
            .order_by(Resultado.criado_em.desc())
            .all()
        )

    @staticmethod
    def obter_estatisticas(user_id: str) -> dict:
        partidas = (
            Resultado.query.filter_by(user_id=user_id)
            .order_by(Resultado.criado_em.asc())
            .all()
        )

        if not partidas:
            return None

        total_partidas = len(partidas)
        lucro_total = sum(p.lucro_liquido for p in partidas)

        labels = [p.criado_em.strftime('%d/%m') for p in partidas]
        data_lucro = [float(p.lucro_liquido) for p in partidas]
        data_satisfacao = [float(p.satisfacao_media) for p in partidas]

        return {
            'geral': {
                'total_partidas': total_partidas,
                'lucro_acumulado': float(lucro_total),
                'media_satisfacao': round(
                    sum(p.satisfacao_media for p in partidas) / total_partidas,
                    2,
                ),
                'melhor_lucro': float(max(p.lucro_liquido for p in partidas)),
            },
            'graficos': {
                'labels': labels,
                'lucro_por_partida': data_lucro,
                'satisfacao_por_partida': data_satisfacao,
            },
        }

    @staticmethod
    def obter_ranking(bairro=None, ordenar_por='lucro_liquido') -> list:
        query = Resultado.query

        if bairro:
            query = query.filter(Resultado.bairro == bairro)

        ordenacao_map = {
            'lucro': Resultado.lucro_liquido,
            'satisfacao': Resultado.satisfacao_media,
            'faturamento': Resultado.faturamento,
        }

        coluna_ordenacao = ordenacao_map.get(
            ordenar_por, Resultado.lucro_liquido
        )

        rank_results = query.order_by(desc(coluna_ordenacao)).limit(10).all()

        return [
            {
                'posicao': i + 1,
                'nome': str(r.user_id),
                'bairro': r.bairro,
                'lucro': float(r.lucro_liquido),
                'satisfacao': float(r.satisfacao_media),
                'data': r.criado_em.strftime('%d/%m/%Y'),
            }
            for i, r in enumerate(rank_results)
        ]
