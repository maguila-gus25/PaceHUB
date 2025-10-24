import PySimpleGUI as sg

def criar_janela_login():
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