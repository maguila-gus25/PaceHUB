import hashlib
import os

class Usuario:
    """
    Classe base com atributos de usuário e hashing de senha (RNF05).
    """
    def __init__(self, nome: str, cpf: str, email: str, senha: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha_hash = self._hash_senha(senha)

    def _hash_senha(self, senha: str) -> str:
        """Gera um hash seguro para a senha usando salt."""
        salt = os.urandom(32) # Gera um salt aleatório
        senha_com_salt = salt + senha.encode('utf-8')
        hash_obj = hashlib.sha256(senha_com_salt)
        return salt.hex() + ':' + hash_obj.hexdigest()

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Email: {self.email}")