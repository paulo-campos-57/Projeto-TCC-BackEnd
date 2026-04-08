import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from database import db


class Resultado(db.Model):
    __tablename__ = 'game_result'
    __table_args__ = {'schema': 'public'}

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text('gen_random_uuid()'),
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('public.user_table.id', ondelete='CASCADE'),
        nullable=False,
    )

    bairro = db.Column(db.String(100), nullable=False)
    tempo_de_jogo = db.Column(db.String(50), nullable=False)
    dias_jogados = db.Column(db.Integer, nullable=False)

    faturamento = db.Column(db.Numeric(10, 2), nullable=False)
    lucro_liquido = db.Column(db.Numeric(10, 2), nullable=False)

    satisfacao_media = db.Column(db.Numeric(4, 2), nullable=False)
    satisfacao_final = db.Column(db.Integer, nullable=False)

    criado_em = db.Column(
        db.DateTime(timezone=True),
        server_default=sa.text('CURRENT_TIMESTAMP'),
    )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'bairro': self.bairro,
            'tempo_de_jogo': self.tempo_de_jogo,
            'dias_jogados': self.dias_jogados,
            'faturamento': float(self.faturamento),
            'lucro_liquido': float(self.lucro_liquido),
            'satisfacao_media': float(self.satisfacao_media),
            'satisfacao_final': self.satisfacao_final,
            'criado_em': self.criado_em.isoformat()
            if self.criado_em
            else None,
        }
