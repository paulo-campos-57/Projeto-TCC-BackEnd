class Bairro:
    def __init__(
        self,
        id: int,
        nome: str,
        pos: list,
        descricao: str,
        foco_preco_label: str,
        expectativa: str,
        preferencia_preco: int,
        preferencia_tapioca: int,
        satisfacao_base: int = 3,
    ):
        self.id = id
        self.nome = nome
        self.pos = pos
        self.descricao = descricao
        self.foco_preco_label = foco_preco_label
        self.expectativa = expectativa
        self.preferencia_preco = preferencia_preco
        self.preferencia_tapioca = preferencia_tapioca
        self.satisfacao_base = satisfacao_base

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'pos': self.pos,
            'descricao': self.descricao,
            'focoPreco': self.foco_preco_label,
            'expectativa': self.expectativa,
            'preferencia_preco': self.preferencia_preco,
            'preferencia_tapioca': self.preferencia_tapioca,
            'satisfacao_base': self.satisfacao_base,
        }
