from abc import ABC

class Usuario(ABC):
    def __init__(self, nome: str, cpf: str, email: str, perfil: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.perfil = perfil
        self.senha_hash = None

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Email: {self.email}")