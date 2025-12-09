import PySimpleGUI as sg

def criar_janela_meus_resultados():
    sg.theme('DarkBlue14')
    
    meus_eventos = [
        ["Maratona de Floripa", "25/10/2025", "03:45:10", "42k", "150º"],
        ["Meia de São José", "15/11/2024", "01:50:20", "21k", "80º"],
    ]
    headings = ['Evento', 'Data', 'Tempo', 'Distância', 'Posição Geral']

    layout = [
        [sg.Text('Meus Resultados', font=('Helvetica', 20))],
        [sg.Table(values=meus_eventos, headings=headings,
                  justification='left',
                  num_rows=10,
                  expand_x=True)],
        [sg.Button('Ver Detalhes', key='-DETALHES-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]
    
    return sg.Window('PaceHub - Meus Resultados', layout, finalize=True)

if __name__ == '__main__':
    janela_resultados = criar_janela_meus_resultados()
    
    while True:
        event, values = janela_resultados.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
            
    janela_resultados.close()