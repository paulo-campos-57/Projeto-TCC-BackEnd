class Bairro:
    def __init__(
        self,
        id: int,
        nome: str,
        preferencia_preco: int,
        preferencia_tapioca: int,
        satisfacao_base: int,
    ):
        self.id = id
        self.nome = nome
        self.preferencia_preco = preferencia_preco
        self.preferencia_tapioca = preferencia_tapioca
        self.satisfacao_base = satisfacao_base

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preferencia_preco': self.preferencia_preco,
            'preferencia_tapioca': self.preferencia_tapioca,
            'satisfacao_base': self.satisfacao_base,
        }
