import re
from organizador import Organizador
from database import Database

class OrganizadorModel:
    def __init__(self):
        self.db = Database()

    def adicionar_organizador(self, organizador: Organizador):
        self.db.salvar_organizador(organizador)

    def cpf_ja_existe(self, cpf: str) -> bool:
        organizadores = self.db.carregar_organizadores()
        cpf_limpo = ''.join(re.findall(r'\d', cpf))
        for org in organizadores:
            if org.cpf == cpf_limpo:
                return True
        return False