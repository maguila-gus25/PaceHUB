import PySimpleGUI as sg

# --- DEFINIÇÃO DAS CLASSES ---

class Usuario:
    """
    Classe base simplificada com atributos essenciais de um usuário.
    """
    def __init__(self, nome, cpf, email, senha):
        self.nome = nome
        self.cpf = cpf 
        self.email = email
        self.senha = senha 

    def __str__(self):
        return (f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Email: {self.email}")

class Organizador(Usuario):
    """
    Representa um usuário com perfil de Organizador.
    Herda todos os atributos de Usuario.
    """
    def __init__(self, nome, cpf, email, senha):
        super().__init__(nome, cpf, email, senha)

# --- FUNÇÕES DAS JANELAS ---

def criar_janela_login():
    """
    Cria a janela inicial de login e cadastro.
    Baseado no arquivo autenticarUsuario.py.
    """
    sg.theme('DarkBlue14')
    
    layout = [
        [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
        [sg.Text('Sua plataforma de gestão de corridas.', font=('Helvetica', 12), justification='center', expand_x=True)],
        [sg.VPush()],
        [sg.Text('CPF*'), sg.Input(key='-CPF_LOGIN-')],
        [sg.Text('Senha*'), sg.Input(key='-SENHA_LOGIN-', password_char='*')],
        [sg.Text('* Campos obrigatórios', text_color='red')],
        [sg.Button('Login', size=(10, 1), expand_x=True)],
        [sg.Text('_' * 40)],
        [sg.Text('Ainda não tem uma conta? Cadastre-se agora!')],
        [sg.Button('Cadastrar como Atleta', key='-CADASTRO_ATLETA-', expand_x=True)],
        [sg.Button('Cadastrar como Organizador', key='-CADASTRO_ORGANIZADOR-', expand_x=True)],
        [sg.VPush()],
    ]

    return sg.Window('PaceHub - Bem-vindo', layout, size=(400, 350), finalize=True)

def criar_janela_cadastro(perfil):
    """
    Cria a janela de cadastro para um perfil específico ('Atleta' ou 'Organizador').
    """
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text(f'Cadastro de {perfil}', font=('Helvetica', 20))],
        [sg.Text('Nome Completo*', size=(15, 1)), sg.Input(key='-NOME-')],
        [sg.Text('CPF*', size=(15, 1)), sg.Input(key='-CPF-')],
        [sg.Text('Email*', size=(15,1)), sg.Input(key='-EMAIL-')],
        [sg.Text('Senha*', size=(15,1)), sg.Input(key='-SENHA-', password_char='*')],
        [sg.Text('* Todos os campos são obrigatórios.', text_color='red')],
        [sg.Button('Cadastrar', key='-CADASTRAR-', size=(10, 1))],
        [sg.Button('Voltar', key='-VOLTAR-', size=(10, 1))]
    ]

    return sg.Window(f'PaceHub - Cadastro de {perfil}', [layout], finalize=True)

# --- LÓGICA PRINCIPAL ---
if __name__ == '__main__':
    janela_login = criar_janela_login()

    while True:
        # Lê eventos da janela ativa
        window, event, values = sg.read_all_windows()

        if window == janela_login and event in (sg.WIN_CLOSED, 'Sair'):
            break

        if event == 'Login':
            sg.popup(f"Lógica de login a ser implementada para o CPF: {values['-CPF_LOGIN-']}")
        
        # --- FLUXO DE CADASTRO DE ORGANIZADOR ---
        if event == '-CADASTRO_ORGANIZADOR-':
            janela_login.hide() # Esconde a janela de login
            janela_cadastro_org = criar_janela_cadastro('Organizador')

            while True:
                event_cad, values_cad = janela_cadastro_org.read()
                
                if event_cad in (sg.WIN_CLOSED, '-VOLTAR-'):
                    janela_cadastro_org.close()
                    janela_login.un_hide() # Mostra a janela de login novamente
                    break
                
                if event_cad == '-CADASTRAR-':
                    campos_obrigatorios = ['-NOME-', '-CPF-', '-EMAIL-', '-SENHA-']
                    if any(not values_cad[key] for key in campos_obrigatorios):
                        sg.popup_error('Todos os campos com * são obrigatórios!')
                    else:
                        organizador = Organizador(
                            nome=values_cad['-NOME-'],
                            cpf=values_cad['-CPF-'],
                            email=values_cad['-EMAIL-'],
                            senha=values_cad['-SENHA-']
                        )
                        sg.popup('Cadastro de Organizador Realizado!', f"Dados cadastrados:\n\n{organizador}")
                        janela_cadastro_org.close()
                        janela_login.un_hide()
                        break

    janela_login.close()