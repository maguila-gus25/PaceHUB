from entidade.usuario import Usuario
from datetime import datetime

class Organizador(Usuario):
    def __init__(self, nome, cpf, email, senha_hash):
        super().__init__(cpf, nome, email, senha_hash)