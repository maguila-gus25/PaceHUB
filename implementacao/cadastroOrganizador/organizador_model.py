# arquivo: organizador_model.py (modificado)
import re
from organizador import Organizador
from database import Database

class OrganizadorModel:
    def __init__(self):
        """
        O Model agora se comunica com o banco de dados simulado.
        """
        self.db = Database()

    def adicionar_organizador(self, organizador: Organizador):
        """
        Delega a responsabilidade de salvar para a classe de banco de dados.
        """
        self.db.salvar_organizador(organizador)

    def cpf_ja_existe(self, cpf: str) -> bool:
        """
        Verifica a existência do CPF carregando os dados do banco.
        """
        organizadores = self.db.carregar_organizadores()
        cpf_limpo = ''.join(re.findall(r'\d', cpf))
        for org in organizadores:
            if org.cpf == cpf_limpo:
                return True
        return False