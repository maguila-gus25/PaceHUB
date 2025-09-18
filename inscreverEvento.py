import PySimpleGUI as sg

def criar_janela_inscricao(nome_evento):
    sg.theme('DarkBlue14')

    termo_responsabilidade = """
Declaro que participo deste evento por livre e espontânea vontade,
isentando de qualquer responsabilidade os organizadores, patrocinadores
e realizadores, em meu nome e de meus sucessores. Declaro estar em
boas condições de saúde e ter treinado apropriadamente para a prova.
"""

    layout = [
        [sg.Text(f'Inscrição: {nome_evento}', font=('Helvetica', 20))],
        [sg.HorizontalSeparator()],
        [sg.Text('Confirme seus dados cadastrais:')],
        [sg.Text('Nome: [Nome do Atleta]')],
        [sg.Text('CPF: [CPF do Atleta]')],
        
        # --- LINHA ADICIONADA ---
        # Dropdown para a escolha do kit.
        [sg.Text('Escolha do Kit*', size=(15,1)), sg.Combo(['Completo R$75,00', 'Camiseta R$50,00', 'Sem Kit'], default_value='Completo', readonly=True, key='-KIT-')],

        [sg.HorizontalSeparator()],
        [sg.Text('Ficha Médica e Termo de Responsabilidade', font=('Helvetica', 12))],
        [sg.Multiline(default_text=termo_responsabilidade, disabled=True, size=(60, 8), autoscroll=True)],
        [sg.Checkbox('Li e aceito os termos de responsabilidade e isenção de riscos.', key='-TERMO_ACEITO-')],
        [sg.Checkbox('Atesto que estou em condições de saúde aptas para a prática da atividade física.', key='-SAUDE_OK-')],
        [sg.VPush()],
        [sg.Button('Confirmar Inscrição', key='-CONFIRMAR-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window('PaceHub - Inscrição', layout, size=(500, 500), finalize=True, resizable=True)

# Bloco principal para executar a janela
if __name__ == '__main__':
    # Simulação de um evento selecionado
    evento = "Maratona de Floripa"
    janela_inscricao = criar_janela_inscricao(evento)

    while True:
        event, values = janela_inscricao.read()
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            break
        if event == '-CONFIRMAR-':
            if values['-TERMO_ACEITO-'] and values['-SAUDE_OK-']:
                # --- POPUP MODIFICADO ---
                # Coleta o valor do kit selecionado e o exibe na confirmação.
                kit_selecionado = values['-KIT-']
                sg.popup(f'Inscrição confirmada com sucesso!\n\nKit Selecionado: {kit_selecionado}')
                break
            else:
                sg.popup_error('Você precisa aceitar os termos e confirmar sua condição de saúde para se inscrever.')
                
    janela_inscricao.close()