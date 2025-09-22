import PySimpleGUI as sg
import re

from modelo import Organizador, OrganizadorModel, validar_nome_completo, validar_email, validar_cpf
from visao import criar_janela_login, criar_janela_cadastro, exibir_popup_erro, exibir_popup_sucesso

class OrganizadorController:
    def __init__(self):
        self.organizador_model = OrganizadorModel()
        self.janela_login = criar_janela_login()
        self.janela_cadastro = None

    def run(self):
        while True:
            window, event, values = sg.read_all_windows()

            if window == self.janela_login and event in (sg.WIN_CLOSED, 'Sair'):
                break
            
            if event == 'Login':
                # A lógica de login seria implementada aqui
                pass

            if event == '-CADASTRO_ORGANIZADOR-':
                self.abrir_janela_cadastro()

            if window == self.janela_cadastro:
                if event in (sg.WIN_CLOSED, '-VOLTAR-'):
                    self.fechar_janela_cadastro()
                elif event == '-CADASTRAR-':
                    self.cadastrar_organizador(values)
        
        self.janela_login.close()

    def abrir_janela_cadastro(self):
        self.janela_login.hide()
        self.janela_cadastro = criar_janela_cadastro('Organizador')

    def fechar_janela_cadastro(self):
        if self.janela_cadastro:
            self.janela_cadastro.close()
            self.janela_cadastro = None
        self.janela_login.un_hide()

    def cadastrar_organizador(self, values):
        nome = values['-NOME-']
        cpf_input = values['-CPF-']
        email = values['-EMAIL-']
        senha = values['-SENHA-']

        if not all([nome, cpf_input, email, senha]):
            exibir_popup_erro('Todos os campos com * são obrigatórios!')
            return
        if not validar_nome_completo(nome):
            exibir_popup_erro('Por favor, insira seu nome completo (nome e sobrenome).')
            return
        if not validar_cpf(cpf_input):
            exibir_popup_erro('O CPF inserido é inválido!')
            return
        if not validar_email(email):
            exibir_popup_erro('O formato do e-mail inserido é inválido.')
            return
        
        if self.organizador_model.cpf_ja_existe(cpf_input):
            exibir_popup_erro(f'O CPF {cpf_input} já está cadastrado no sistema.')
            return

        cpf_limpo = ''.join(re.findall(r'\d', cpf_input))

        organizador = Organizador(nome=nome, cpf=cpf_limpo, email=email, senha=senha)
        
        self.organizador_model.adicionar_organizador(organizador)
        
        print("\n--- [DEBUG] Dados do Organizador Salvo ---")
        print(f"Nome: {organizador.nome}")
        print(f"CPF: {organizador.cpf}")
        print(f"Email: {organizador.email}")
        print(f"Senha Hash: {organizador.senha_hash}")
        print("-------------------------------------------\n")

        exibir_popup_sucesso('Cadastro Realizado com Sucesso!', f"Dados cadastrados:\n\n{organizador}")
        self.fechar_janela_cadastro()

if __name__ == '__main__':
    try:
        import PySimpleGUI as sg
    except ImportError:
        print("Erro: PySimpleGUI não está instalado.")
        print("Por favor, instale usando: pip install PySimpleGUI")
        exit()
        
    controller = OrganizadorController()
    controller.run()