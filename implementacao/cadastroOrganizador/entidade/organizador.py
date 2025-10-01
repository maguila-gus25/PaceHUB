from entidade.usuario import Usuario

class Organizador(Usuario):
    def __init__(self, nome: str, cpf: str, email: str):
        super().__init__(nome, cpf, email, perfil='Organizador')
        self.eventos = []