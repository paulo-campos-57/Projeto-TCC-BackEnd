from models.bairro import Bairro


class BairroService:
    CONFIGURACOES_BAIRROS = {
        1: {
            'nome': 'Boa Viagem',
            'preco': 4,
            'tapioca': 4,
        },  # Saudável e Turística
        2: {
            'nome': 'Casa Forte',
            'preco': 5,
            'tapioca': 5,
        },  # Gourmet e Sofisticada
        3: {
            'nome': 'Várzea',
            'preco': 3,
            'tapioca': 3,
        },  # Variada e Estudantil
        4: {'nome': 'Ibura', 'preco': 1, 'tapioca': 1},  # Familiar e Econômica
        5: {
            'nome': 'Recife Antigo',
            'preco': 2,
            'tapioca': 2,
        },  # Criativa e Rápida
        6: {
            'nome': 'Areias',
            'preco': 1,
            'tapioca': 6,
        },  # Tradicional e Caseira
    }

    @staticmethod
    def gerar_configuracao_bairro(bairro_id: int):
        config = BairroService.CONFIGURACOES_BAIRROS.get(bairro_id)

        if not config:
            return Bairro(
                id=bairro_id,
                nome='Bairro Desconhecido',
                preferencia_preco=3,
                preferencia_tapioca=6,
                satisfacao_base=3,  # Valor que varia entre 1 e 10
            )

        return Bairro(
            id=bairro_id,
            nome=config['nome'],
            preferencia_preco=config['preco'],
            preferencia_tapioca=config['tapioca'],
            satisfacao_base=3,
        )
