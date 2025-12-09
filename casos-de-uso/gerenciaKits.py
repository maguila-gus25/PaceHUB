import PySimpleGUI as sg

def criar_janela_gerenciar_kits():
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Gerenciar Entrega de Kits', font=('Helvetica', 20))],
        [sg.Text('Buscar por Nome ou CPF:'), sg.Input(key='-BUSCA-'), sg.Button('Buscar', key='-BUSCAR-')],
        [sg.HorizontalSeparator()],
        [sg.Text('Nome do Atleta: [Nome do Atleta]', key='-NOME_ATLETA-')],
        [sg.Text('CPF: [CPF do Atleta]', key='-CPF_ATLETA-')],
        [sg.Checkbox('Kit Entregue', key='-KIT_ENTREGUE-')],
        [sg.Button('Salvar', key='-SALVAR-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Gerenciar Kits', layout, finalize=True)

if __name__ == '__main__':
    janela_gerenciar_kits = criar_janela_gerenciar_kits()

    while True:
        event, values = janela_gerenciar_kits.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
        if event == '-BUSCAR-':
            # Simulação de busca
            janela_gerenciar_kits['-NOME_ATLETA-'].update('Nome do Atleta: João da Silva')
            janela_gerenciar_kits['-CPF_ATLETA-'].update('CPF: 123.456.789-00')
        if event == '-SALVAR-':
            sg.popup('Status do kit atualizado!')

    janela_gerenciar_kits.close()