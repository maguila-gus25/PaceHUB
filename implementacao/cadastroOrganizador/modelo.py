import hashlib
import os
import re

class Usuario:
    def __init__(self, nome: str, cpf: str, email: str, senha: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha_hash = self._hash_senha(senha)

    def _hash_senha(self, senha: str) -> str:
        salt = os.urandom(32)
        senha_com_salt = salt + senha.encode('utf-8')
        hash_obj = hashlib.sha256(senha_com_salt)
        return salt.hex() + ':' + hash_obj.hexdigest()

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Email: {self.email}")

class Evento:
    def __init__(self, nome: str, data: str, distancia: str, tempo_corte: str, data_limite_cancelamento: str, kit_corrida: str):
        self.nome = nome
        self.data = data
        self.distancia = distancia
        self.tempo_corte = tempo_corte
        self.data_limite_cancelamento = data_limite_cancelamento
        self.kit_de_corrida = kit_corrida
        self.lista_de_inscritos = []

    def __str__(self):
        return (f"  - Nome do Evento: {self.nome}\n"
                f"  - Data: {self.data}\n"
                f"  - Distância: {self.distancia} km\n"
                f"  - Tempo de Corte: {self.tempo_corte} horas")

class Organizador(Usuario):
    def __init__(self, nome: str, cpf: str, email: str, senha: str):
        super().__init__(nome, cpf, email, senha)
        self.eventos = []

    def adicionar_evento(self, evento: Evento):
        self.eventos.append(evento)

    def __str__(self):
        return super().__str__()

class OrganizadorModel:
    def __init__(self):
        self._organizadores = []

    def adicionar_organizador(self, organizador: Organizador):
        self._organizadores.append(organizador)

    def cpf_ja_existe(self, cpf: str) -> bool:
        cpf_limpo = ''.join(re.findall(r'\d', cpf))
        for org in self._organizadores:
            if org.cpf == cpf_limpo:
                return True
        return False

def validar_nome_completo(nome: str) -> bool:
    return len(nome.strip().split()) >= 2

def validar_email(email: str) -> bool:
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(padrao, email) is not None

def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(re.findall(r'\d', cpf))

    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False

    return True