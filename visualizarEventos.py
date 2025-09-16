import PySimpleGUI as sg

def criar_janela_visualizar_eventos():
    sg.theme('DarkBlue14')
    
    eventos_disponiveis = [
        ["Maratona de Floripa", "42k", "25/10/2025", "Disponível"],
        ["Meia de São José", "21k", "15/11/2025", "Disponível"],
        ["Corrida de Verão", "10k", "05/12/2025", "Disponível"],
        ["Night Run", "5k", "20/12/2025", "Disponível"],
    ]
    
    headings = ['Nome do Evento', 'Distância', 'Data', 'Status']

    layout = [
        [sg.Text('Painel do Atleta', font=('Helvetica', 20))],
        [sg.Text('Bem-vindo, [Nome do Atleta]!')],
        [sg.HorizontalSeparator()],
        [sg.Text('Eventos Disponíveis', font=('Helvetica', 15))],
        [sg.Table(values=eventos_disponiveis, headings=headings,
                  auto_size_columns=False,
                  justification='left',
                  num_rows=10,
                  key='-TABELA_EVENTOS-',
                  row_height=25,
                  expand_x=True)],
        [sg.Button('Inscrever-se no Evento', key='-INSCREVER-'), 
         sg.Button('Ver Meus Resultados', key='-RESULTADOS-'), 
         sg.Button('Cancelar Inscrição', key='-CANCELAR-')]
    ]
    
    return sg.Window('PaceHub - Painel do Atleta', layout, size=(700, 400), finalize=True)

if __name__ == '__main__':
    janela_atleta = criar_janela_visualizar_eventos()
    
    while True:
        event, values = janela_atleta.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-INSCREVER-':
            if values['-TABELA_EVENTOS-']:
                sg.popup('Abrindo tela de inscrição...')
            else:
                sg.popup_error('Por favor, selecione um evento na tabela primeiro.')

    janela_atleta.close()