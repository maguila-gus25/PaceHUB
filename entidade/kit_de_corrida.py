class KitDeCorrida:
    def __init__(self, nome: str, descricao: str, valor: float):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor

    def __str__(self):
        return f"{self.nome} - R$ {self.valor:.2f}"