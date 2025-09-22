import json
import os
from organizador import Organizador

class Database:
    def __init__(self, db_file='organizadores.json'):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def carregar_organizadores(self):
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
        
        organizadores = []
        for org_data in data:
            organizador = Organizador(
                nome=org_data['nome'],
                cpf=org_data['cpf'],
                email=org_data['email']
            )
            organizador.senha_hash = org_data['senha_hash']
            organizadores.append(organizador)
            
        return organizadores

    def salvar_organizador(self, organizador):
        with open(self.db_file, 'r') as f:
            try:
                organizadores_data = json.load(f)
            except json.JSONDecodeError:
                organizadores_data = []

        novo_org_data = {
            'nome': organizador.nome,
            'cpf': organizador.cpf,
            'email': organizador.email,
            'senha_hash': organizador.senha_hash
        }
        organizadores_data.append(novo_org_data)

        with open(self.db_file, 'w') as f:
            json.dump(organizadores_data, f, indent=4)