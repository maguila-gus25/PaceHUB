# usuario.py

import hashlib
import os

class Usuario:
    """Define a estrutura base de um usuário com seus dados e lógica de senha."""
    def __init__(self, nome: str, cpf: str, email: str, senha: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha_hash = self._hash_senha(senha)

    def _hash_senha(self, senha: str) -> str:
        """Gera um hash seguro para a senha usando salt (RNF05)."""
        salt = os.urandom(32)
        senha_com_salt = salt + senha.encode('utf-8')
        hash_obj = hashlib.sha256(senha_com_salt)
        return salt.hex() + ':' + hash_obj.hexdigest()

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Email: {self.email}")