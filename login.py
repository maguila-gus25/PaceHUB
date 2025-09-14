import PySimpleGUI as sg

def criar_janela_inicial():
    sg.theme('DarkBlue14')
    
    layout = [
        [sg.Text('PaceHub', font=('Helvetica', 25), justification='center', expand_x=True)],
        [sg.Text('Sua plataforma de gestão de corridas.', font=('Helvetica', 12), justification='center', expand_x=True)],
        [sg.VPush()],
        [sg.Text('Email'), sg.Input(key='-EMAIL-')],
        [sg.Text('Senha'), sg.Input(key='-SENHA-', password_char='*')],
        [sg.Button('Login', size=(10, 1), expand_x=True)],
        [sg.Text('_' * 40)],
        [sg.Text('Ainda não tem uma conta? Cadastre-se agora!')],
        [sg.Button('Cadastrar como Atleta', key='-CADASTRO_ATLETA-', expand_x=True)],
        [sg.Button('Cadastrar como Organizador', key='-CADASTRO_ORGANIZADOR-', expand_x=True)],
        [sg.VPush()],
    ]

    return sg.Window('PaceHub - Bem-vindo', layout, size=(400, 350), finalize=True)

# Bloco principal para executar a janela
if __name__ == '__main__':
    janela = criar_janela_inicial()

    while True:
        event, values = janela.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-CADASTRO_ATLETA-':
            sg.popup('Abrindo tela de cadastro de Atleta...')
            # Aqui você chamaria a função que cria a janela de cadastro de atleta
        if event == '-CADASTRO_ORGANIZADOR-':
            sg.popup('Abrindo tela de cadastro de Organizador...')
            # Aqui você chamaria a função que cria a janela de cadastro de organizador
        if event == 'Login':
            sg.popup(f"Tentando login com o email: {values['-EMAIL-']}")
            # Aqui entraria a lógica de validação de login
            
    janela.close()