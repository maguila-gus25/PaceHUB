import PySimpleGUI as sg
from datetime import datetime

def criar_janela_painel_atleta():
    sg.theme('DarkBlue14')

    # --- SIMULAÇÃO DE DADOS ---
    # Dados que viriam de um banco de dados em uma aplicação real
    
    eventos_disponiveis = [
        ["Maratona de Floripa", "42k", "25/10/2025", "Inscrições Abertas"],
        ["Meia de São José", "21k", "15/11/2025", "Inscrições Abertas"],
        ["Corrida de Verão", "10k", "05/12/2025", "Inscrições Abertas"],
    ]
    
    eventos_inscritos = [
        ["Night Run", "5k", "20/12/2025", "Confirmada"],
    ]
    
    historico_eventos = [
        ["Corrida de Inverno", "10k", "15/07/2025", "00:55:32", "152º"],
        ["Desafio da Serra", "15k", "01/05/2025", "01:25:10", "88º"],
    ]

    # --- DEFINIÇÃO DOS LAYOUTS DAS ABAS ---

    headings_disponiveis = ['Nome do Evento', 'Distância', 'Data', 'Status']
    layout_aba_disponiveis = [
        [sg.Table(values=eventos_disponiveis, headings=headings_disponiveis,
                  auto_size_columns=False, justification='left', num_rows=10,
                  key='-TABELA_DISPONIVEIS-', row_height=25, expand_x=True, expand_y=True)],
        [sg.Button('Inscrever-se no Evento', key='-INSCREVER-')]
    ]

    headings_inscritos = ['Nome do Evento', 'Distância', 'Data', 'Status da Inscrição']
    layout_aba_inscritos = [
        [sg.Table(values=eventos_inscritos, headings=headings_inscritos,
                  auto_size_columns=False, justification='left', num_rows=10,
                  key='-TABELA_INSCRITOS-', row_height=25, expand_x=True, expand_y=True)],
        [sg.Button('Cancelar Inscrição', key='-CANCELAR-')]
    ]

    headings_historico = ['Nome do Evento', 'Distância', 'Data', 'Tempo Final', 'Colocação']
    layout_aba_historico = [
        [sg.Table(values=historico_eventos, headings=headings_historico,
                  auto_size_columns=False, justification='left', num_rows=10,
                  key='-TABELA_HISTORICO-', row_height=25, expand_x=True, expand_y=True)],
        # O botão de resultados não é mais necessário, pois a própria aba já mostra
    ]

    # --- LAYOUT PRINCIPAL COM AS ABAS ---

    tab_group_layout = [[
        sg.Tab('Eventos Disponíveis', layout_aba_disponiveis, key='-TAB_DISPONIVEIS-'),
        sg.Tab('Meus Eventos (Inscritos)', layout_aba_inscritos, key='-TAB_INSCRITOS-'),
        sg.Tab('Histórico de Resultados', layout_aba_historico, key='-TAB_HISTORICO-')
    ]]

    layout_principal = [
        [sg.Text('Painel do Atleta', font=('Helvetica', 20))],
        [sg.Text('Bem-vindo, Atleta!', size=(70,1))], # Placeholder para o nome
        [sg.HorizontalSeparator()],
        [sg.TabGroup(tab_group_layout, expand_x=True, expand_y=True)]
    ]
    
    return sg.Window('PaceHub - Painel do Atleta', layout_principal, size=(800, 500), finalize=True, resizable=True)

# --- LÓGICA PRINCIPAL ---
if __name__ == '__main__':
    janela_atleta = criar_janela_painel_atleta()
    
    # Extrai os dados das tabelas para poder manipulá-los
    dados_disponiveis = janela_atleta['-TABELA_DISPONIVEIS-'].get()
    dados_inscritos = janela_atleta['-TABELA_INSCRITOS-'].get()
    
    while True:
        event, values = janela_atleta.read()
        if event == sg.WIN_CLOSED:
            break

        # Lógica para se inscrever em um evento
        if event == '-INSCREVER-':
            indices_selecionados = values['-TABELA_DISPONIVEIS-']
            if indices_selecionados:
                # Pega o primeiro evento selecionado
                indice_evento = indices_selecionados[0]
                evento_selecionado = dados_disponiveis.pop(indice_evento)
                
                # Altera o status para "Confirmada" e adiciona na lista de inscritos
                evento_selecionado[3] = "Confirmada" 
                dados_inscritos.append(evento_selecionado)
                
                # Atualiza as duas tabelas na interface
                janela_atleta['-TABELA_DISPONIVEIS-'].update(values=dados_disponiveis)
                janela_atleta['-TABELA_INSCRITOS-'].update(values=dados_inscritos)
                
                sg.popup('Inscrição realizada com sucesso!')
            else:
                sg.popup_error('Por favor, selecione um evento disponível para se inscrever.')

        # Lógica para cancelar uma inscrição
        if event == '-CANCELAR-':
            indices_selecionados = values['-TABELA_INSCRITOS-']
            if indices_selecionados:
                indice_evento = indices_selecionados[0]
                evento_cancelado = dados_inscritos.pop(indice_evento)

                # Altera o status de volta para "Inscrições Abertas"
                evento_cancelado[3] = "Inscrições Abertas"
                dados_disponiveis.append(evento_cancelado)

                # Atualiza as duas tabelas na interface
                janela_atleta['-TABELA_DISPONIVEIS-'].update(values=dados_disponiveis)
                janela_atleta['-TABELA_INSCRITOS-'].update(values=dados_inscritos)

                sg.popup('Inscrição cancelada com sucesso.')
            else:
                sg.popup_error('Por favor, selecione um evento para cancelar a inscrição.')


    janela_atleta.close()