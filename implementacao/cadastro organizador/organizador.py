# organizador.py

from usuario import Usuario
from evento import Evento

class Organizador(Usuario):
    """Define um Organizador, que é um tipo de Usuário."""
    def __init__(self, nome: str, cpf: str, email: str, senha: str):
        super().__init__(nome, cpf, email, senha)
        self.eventos = []

    def adicionar_evento(self, evento: Evento):
        self.eventos.append(evento)

    def __str__(self):
        return super().__str__()