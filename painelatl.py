import PySimpleGUI as sg

def criar_painel_atleta():
    sg.theme('DarkBlue14')
    
    # Dados de exemplo para a lista de eventos
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

# Bloco principal para executar a janela
if __name__ == '__main__':
    janela_atleta = criar_painel_atleta()
    
    while True:
        event, values = janela_atleta.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-INSCREVER-':
            # Verifica se alguma linha foi selecionada
            if values['-TABELA_EVENTOS-']:
                # Pega o índice da primeira linha selecionada
                indice_selecionado = values['-TABELA_EVENTOS-'][0]
                # Pega os dados da linha
                evento_selecionado = janela_atleta['-TABELA_EVENTOS-'].get()[indice_selecionado]
                sg.popup(f'Abrindo tela de inscrição para: {evento_selecionado[0]}')
            else:
                sg.popup_error('Por favor, selecione um evento na tabela primeiro.')

    janela_atleta.close()