# arquivo: usuario.py (modificado)

class Usuario:
    def __init__(self, nome: str, cpf: str, email: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha_hash = None # Será definido pelo controlador

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Email: {self.email}")