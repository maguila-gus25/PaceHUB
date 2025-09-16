import PySimpleGUI as sg

def criar_janela_novo_evento():
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Criar Novo Evento', font=('Helvetica', 20))],
        [sg.Text('Nome do Evento*', size=(25,1)), sg.Input(key='-NOME_EVENTO-')],
        [sg.Text('Data do Evento*', size=(25,1)), sg.Input(key='-DATA_EVENTO-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_EVENTO-', format='%d/%m/%Y')],
        [sg.Text('Distância (km)*', size=(25,1)), sg.Combo(['5k', '10k', '21k', '42k'], key='-DISTANCIA-', readonly=True)],
        [sg.Text('Local de Largada*', size=(25,1)), sg.Input(key='-LOCAL-')],
        [sg.Text('Data Limite para Cancelamento*', size=(25,1)), sg.Input(key='-DATA_CANCEL-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_CANCEL-', format='%d/%m/%Y')],
        [sg.Text('* Campos obrigatórios', text_color='red')],
        [sg.Button('Salvar Evento', key='-SALVAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]

    return sg.Window('PaceHub - Novo Evento', layout, finalize=True)

if __name__ == '__main__':
    janela_novo_evento = criar_janela_novo_evento()

    while True:
        event, values = janela_novo_evento.read()
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            break
        if event == '-SALVAR-':
            if all(values.values()):
                sg.popup('Evento criado com sucesso!')
                break
            else:
                sg.popup_error('Por favor, preencha todos os campos obrigatórios.')

    janela_novo_evento.close()