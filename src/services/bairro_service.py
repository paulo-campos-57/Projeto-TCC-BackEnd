from models.bairro import Bairro


class BairroService:
    DADOS_MAPA = {
        1: {
            'nome': 'Casa Forte',
            'pos': [-8.0305, -34.9235],
            'descricao': (
                'Bairro tradicional e arborizado, conhecido por sua '
                'tranquilidade e charme histórico.'
            ),
            'focoPreco': 'Alto',
            'expectativa': 'Gourmet e Sofisticada',
            'pref_preco': 5,
            'pref_tapioca': 5,
        },
        2: {
            'nome': 'Recife Antigo',
            'pos': [-8.0628, -34.8713],
            'descricao': (
                'Centro histórico da cidade, repleto de cultura, arte '
                'e vida noturna animada.'
            ),
            'focoPreco': 'Moderado a Alto',
            'expectativa': 'Criativa e Rápida',
            'pref_preco': 2,
            'pref_tapioca': 2,
        },
        3: {
            'nome': 'Ibura',
            'pos': [-8.1265, -34.9378],
            'descricao': (
                'Região popular e vibrante, com forte senso de '
                'comunidade e vida cotidiana intensa.'
            ),
            'focoPreco': 'Baixo',
            'expectativa': 'Familiar e Econômica',
            'pref_preco': 1,
            'pref_tapioca': 1,
        },
        4: {
            'nome': 'Boa Viagem',
            'pos': [-8.1198, -34.9023],
            'descricao': (
                'Área nobre à beira-mar, famosa por sua praia e comércio movimentado.'
            ),
            'focoPreco': 'Moderado a Alto',
            'expectativa': 'Saudável e Turística',
            'pref_preco': 4,
            'pref_tapioca': 4,
        },
        5: {
            'nome': 'Várzea',
            'pos': [-8.0443, -34.9512],
            'descricao': (
                'Bairro universitário e residencial, com atmosfera calma e verde.'
            ),
            'focoPreco': 'Moderado',
            'expectativa': 'Variada e Estudantil',
            'pref_preco': 3,
            'pref_tapioca': 3,
        },
        6: {
            'nome': 'Areias',
            'pos': [-8.0916, -34.9367],
            'descricao': (
                'Zona urbana popular, com comércio diversificado e '
                'moradores acolhedores.'
            ),
            'focoPreco': 'Moderado a Baixo',
            'expectativa': 'Tradicional e Caseira',
            'pref_preco': 1,
            'pref_tapioca': 6,
        },
    }

    @staticmethod
    def buscar_por_id(id_bairro: int):
        dados = BairroService.DADOS_MAPA.get(id_bairro)
        if not dados:
            return None

        return Bairro(
            id=id_bairro,
            nome=dados['nome'],
            pos=dados['pos'],
            descricao=dados['descricao'],
            foco_preco_label=dados['focoPreco'],
            expectativa=dados['expectativa'],
            preferencia_preco=dados['pref_preco'],
            preferencia_tapioca=dados['pref_tapioca'],
        )

    @staticmethod
    def listar_todos():
        return [
            BairroService.buscar_por_id(id_b)
            for id_b in BairroService.DADOS_MAPA.keys()
        ]
