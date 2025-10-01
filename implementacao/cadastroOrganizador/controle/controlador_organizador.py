import re
import PySimpleGUI as sg
import bcrypt
from entidade.organizador import Organizador
from persistencia.organizador_dao import OrganizadorDAO
from limite.tela_sistema import TelaSistema
from validadores import validar_nome_completo, validar_email, validar_cpf

class ControladorOrganizador:
    def __init__(self, tela_sistema: TelaSistema):
        self.organizador_dao = OrganizadorDAO()
        self.tela_sistema = tela_sistema
        self.janela_cadastro = None

    def _hash_senha(self, senha: str) -> str:
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)
        return hash_bytes.decode('utf-8')

    def abrir_tela_cadastro(self):
        self.janela_cadastro = self.tela_sistema.criar_janela_cadastro_organizador()
        
        while True:
            event, values = self.janela_cadastro.read()
            if event in ('-VOLTAR-', sg.WIN_CLOSED):
                break
            if event == '-CADASTRAR-':
                self.cadastrar_organizador(values)
        
        self.fechar_tela_cadastro()

    def fechar_tela_cadastro(self):
        if self.janela_cadastro:
            self.janela_cadastro.close()
            self.janela_cadastro = None

    def cadastrar_organizador(self, values):
        nome = values['-NOME-']
        cpf_input = values['-CPF-']
        email = values['-EMAIL-']
        senha = values['-SENHA-']

        if not all([nome, cpf_input, email, senha]):
            self.tela_sistema.exibir_popup_erro('Todos os campos com * são obrigatórios!')
            return
        if not validar_nome_completo(nome):
            self.tela_sistema.exibir_popup_erro('Por favor, insira seu nome completo (nome e sobrenome).')
            return
        if not validar_cpf(cpf_input):
            self.tela_sistema.exibir_popup_erro('O CPF inserido é inválido!')
            return
        if not validar_email(email):
            self.tela_sistema.exibir_popup_erro('O formato do e-mail inserido é inválido.')
            return
        
        if self.organizador_dao.cpf_ja_existe(cpf_input):
            self.tela_sistema.exibir_popup_erro(f'O CPF {cpf_input} já está cadastrado no sistema.')
            return

        cpf_limpo = ''.join(re.findall(r'\d', cpf_input))

        senha_hash = self._hash_senha(senha)
        organizador = Organizador(nome=nome, cpf=cpf_limpo, email=email)
        organizador.senha_hash = senha_hash
        
        self.organizador_dao.salvar(organizador)
        
        self.tela_sistema.exibir_popup_sucesso('Cadastro Realizado com Sucesso!', f"Dados cadastrados:\n\n{organizador}")
        self.fechar_tela_cadastro()