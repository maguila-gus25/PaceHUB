# arquivo: usuario.py (modificado)

import bcrypt

class Usuario:
    def __init__(self, nome: str, cpf: str, email: str, senha: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        # O construtor agora verifica se a 'senha' já é um hash antes de processar
        if senha.startswith('$2b$'):
            self.senha_hash = senha
        else:
            self.senha_hash = self._hash_senha(senha)

    def _hash_senha(self, senha: str) -> str:
        """
        Gera um hash seguro para a senha usando bcrypt.
        """
        # Converte a senha para bytes
        senha_bytes = senha.encode('utf-8')
        
        # Gera o salt e cria o hash
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)
        
        # Decodifica o hash de bytes para string para ser salvo no JSON
        return hash_bytes.decode('utf-8')

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Email: {self.email}")