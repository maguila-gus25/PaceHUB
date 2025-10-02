from entidade.usuario import Usuario

class Organizador(Usuario):
    def __init__(self, nome: str, cpf: str, email: str):
        super().__init__(nome, cpf, email, perfil='Organizador')
        self.eventos = []

    def to_dict(self) -> dict:
        """Converte o organizador para dicionário"""
        return {
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'perfil': self.perfil,
            'eventos': len(self.eventos) if self.eventos else 0
        }

    def atualizar_dados(self, nome: str = None, email: str = None, senha_hash: str = None) -> bool:
        """Atualiza os dados do organizador"""
        try:
            if nome is not None:
                self.nome = nome
            if email is not None:
                self.email = email
            if senha_hash is not None:
                self.senha_hash = senha_hash
            return True
        except Exception:
            return False

    def adicionar_evento(self, evento):
        """Adiciona um evento à lista de eventos do organizador"""
        if evento not in self.eventos:
            self.eventos.append(evento)

    def remover_evento(self, evento):
        """Remove um evento da lista de eventos do organizador"""
        if evento in self.eventos:
            self.eventos.remove(evento)

    def get_cpf_formatado(self) -> str:
        """Retorna o CPF formatado (XXX.XXX.XXX-XX)"""
        cpf = self.cpf
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.get_cpf_formatado()}\n"
                f"Email: {self.email}\n"
                f"Eventos: {len(self.eventos) if self.eventos else 0}")