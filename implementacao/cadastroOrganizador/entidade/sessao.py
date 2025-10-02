from datetime import datetime

class Sessao:
    def __init__(self, organizador_id: int, cpf: str, nome: str, data_login: datetime = None):
        self.organizador_id = organizador_id
        self.cpf = cpf
        self.nome = nome
        self.data_login = data_login if data_login else datetime.now()
        self.ativa = True

    def to_dict(self) -> dict:
        """Converte a sessão para dicionário"""
        return {
            'organizador_id': self.organizador_id,
            'cpf': self.cpf,
            'nome': self.nome,
            'data_login': self.data_login.strftime('%d/%m/%Y %H:%M:%S'),
            'ativa': self.ativa
        }

    def desativar(self):
        """Desativa a sessão"""
        self.ativa = False

    def __str__(self):
        return f"Sessão de {self.nome} (CPF: {self.cpf}) - {'Ativa' if self.ativa else 'Inativa'}"
