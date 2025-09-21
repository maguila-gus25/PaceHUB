# controller.py

import PySimpleGUI as sg
from organizador import Organizador
from organizador_model import OrganizadorModel
from view import criar_janela_login, criar_janela_cadastro, exibir_popup_erro, exibir_popup_sucesso
from validations import validar_nome_completo, validar_email, validar_cpf

class OrganizadorController:
    def __init__(self):
        self.organizador_model = OrganizadorModel()
        self.janela_login = criar_janela_login()
        self.janela_cadastro = None

    def run(self):
        """Inicia o loop principal de eventos da aplicação."""
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
        """Processa e valida os dados do formulário de cadastro."""
        nome = values['-NOME-']
        cpf = values['-CPF-']
        email = values['-EMAIL-']
        senha = values['-SENHA-']

        # Validações
        if not all([nome, cpf, email, senha]):
            exibir_popup_erro('Todos os campos com * são obrigatórios!')
            return
        if not validar_nome_completo(nome):
            exibir_popup_erro('Por favor, insira seu nome completo (nome e sobrenome).')
            return
        if not validar_email(email):
            exibir_popup_erro('O formato do e-mail inserido é inválido.')
            return
        if not validar_cpf(cpf):
            exibir_popup_erro('O CPF inserido é inválido!')
            return
        
        # Interação com o Modelo para verificar regra de negócio (RN12)
        if self.organizador_model.cpf_ja_existe(cpf):
            exibir_popup_erro(f'O CPF {cpf} já está cadastrado no sistema.')
            return

        # Cria a instância do organizador
        organizador = Organizador(nome=nome, cpf=cpf, email=email, senha=senha)
        # Adiciona ao nosso "banco de dados" em memória
        self.organizador_model.adicionar_organizador(organizador)
        
        # --- [NOVA ADIÇÃO] IMPRESSÃO DOS DADOS NO TERMINAL ---
        print("\n--- [DEBUG] Dados do Organizador a serem salvos ---")
        print(f"Nome: {organizador.nome}")
        print(f"CPF: {organizador.cpf}")
        print(f"Email: {organizador.email}")
        print(f"Senha Hash: {organizador.senha_hash}") # Importante: Imprimindo o HASH, não a senha original (RNF05)
        print("--------------------------------------------------\n")
        # --- FIM DA ADIÇÃO ---

        # Atualização da Visão com o resultado
        exibir_popup_sucesso('Cadastro Realizado com Sucesso!', f"Dados cadastrados:\n\n{organizador}")
        self.fechar_janela_cadastro()

if __name__ == '__main__':
    controller = OrganizadorController()
    controller.run()