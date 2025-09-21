import PySimpleGUI as sg

def criar_janela_gerenciar_perfil():
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Gerenciar Perfil', font=('Helvetica', 20))],
        [sg.Text('Nome Completo*', size=(15,1)), sg.Input(default_text='[Nome do Usuário]', key='-NOME-')],
        [sg.Text('CPF*', size=(15,1)), sg.Input(default_text='[CPF do Usuário]', key='-CPF-', disabled=True)],
        [sg.Text('Data de Nascimento*', size=(15,1)), sg.Input(default_text='[Data de Nascimento]', key='-DATA_NASC-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_NASC-', format='%d/%m/%Y')],
        [sg.Text('Gênero*', size=(15,1)), sg.Combo(['Masculino', 'Feminino', 'Outro'], default_value='[Gênero]', key='-GENERO-')],
        [sg.Text('Email*', size=(15,1)), sg.Input(default_text='[Email do Usuário]', key='-EMAIL-')],
        [sg.Text('Alterar Senha', size=(15,1)), sg.Input(key='-SENHA-', password_char='*')],
        [sg.Text('* Campos obrigatórios', text_color='red')],
        [sg.Button('Salvar Alterações', key='-SALVAR-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Gerenciar Perfil', layout, finalize=True)

if __name__ == '__main__':
    janela_gerenciar_perfil = criar_janela_gerenciar_perfil()

    while True:
        event, values = janela_gerenciar_perfil.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
        if event == '-SALVAR-':
            sg.popup('Perfil atualizado com sucesso!')
            break

    janela_gerenciar_perfil.close()