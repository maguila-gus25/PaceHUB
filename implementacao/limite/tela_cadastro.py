import PySimpleGUI as sg

def criar_janela_cadastro(perfil: str):
    sg.theme('DarkBlue14')
    layout_usuario = [
        [sg.Text(f'Cadastro de {perfil}', font=('Helvetica', 20))],
        [sg.Frame('Dados Pessoais', [
            [sg.Text('Nome Completo*', size=(15, 1)), sg.Input(key='-NOME-')],
            [sg.Text('CPF*', size=(15, 1)), sg.Input(key='-CPF-')],
            [sg.Text('Email*', size=(15,1)), sg.Input(key='-EMAIL-')],
            [sg.Text('Senha*', size=(15,1)), sg.Input(key='-SENHA-', password_char='*')],
        ])],
        [sg.Text('* Todos os campos são obrigatórios.', text_color='red')],
        [sg.Button('Cadastrar', key='-CADASTRAR-', size=(10, 1))],
        [sg.Button('Voltar', key='-VOLTAR-', size=(10, 1))]
    ]
    return sg.Window(f'PaceHub - Cadastro de {perfil}', [layout_usuario], finalize=True, resizable=True)