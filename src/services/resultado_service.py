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
