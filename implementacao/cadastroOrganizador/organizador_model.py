import re
from organizador import Organizador

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