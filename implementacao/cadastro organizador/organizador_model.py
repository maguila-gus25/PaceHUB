# organizador_model.py

from organizador import Organizador

class OrganizadorModel:
    """
    Gerencia a coleção de organizadores, simulando a camada de persistência.
    """
    def __init__(self):
        self._organizadores = []

    def adicionar_organizador(self, organizador: Organizador):
        self._organizadores.append(organizador)

    def cpf_ja_existe(self, cpf: str) -> bool:
        """Verifica se um CPF já foi cadastrado (RN12)."""
        for org in self._organizadores:
            if org.cpf == cpf:
                return True
        return False