import PySimpleGUI as sg

# Janela 1: Cadastro de Kits (agora chamada por um botão)
def criar_janela_cadastro_kit(kits_atuais):
    sg.theme('DarkBlue14')

    layout_coluna_esquerda = [
        [sg.Text('Adicionar Novo Kit', font=('Helvetica', 16))],
        [sg.Text('Nome do Kit*', size=(12, 1)), sg.Input(key='-NOME_KIT-')],
        [sg.Text('Descrição*', size=(12, 1)), sg.Multiline(key='-DESCRICAO-', size=(35, 4))],
        [sg.Text('Valor (R$)*', size=(12, 1)), sg.Input(key='-VALOR-', size=(15,1))],
        [sg.Button('Adicionar Kit', key='-ADICIONAR_KIT-')]
    ]

    layout_coluna_direita = [
        [sg.Text('Kits do Evento', font=('Helvetica', 16))],
        [sg.Listbox(values=kits_atuais, key='-LISTA_KITS-', size=(30, 8))],
        [sg.Button('Remover Selecionado', key='-REMOVER_KIT-')]
    ]

    layout = [
        [sg.Column(layout_coluna_esquerda), sg.VSeperator(), sg.Column(layout_coluna_direita)],
        [sg.HorizontalSeparator()],
        [sg.Button('Salvar e Voltar', key='-SALVAR_KITS-')]
    ]
    
    # O modal=True faz com que a janela principal fique bloqueada até esta ser fechada
    return sg.Window('PaceHub - Cadastro de Kits do Evento', layout, finalize=True, modal=True)


# Janela 2: Criação do Evento (modificada com o novo botão)
def criar_janela_novo_evento():
    sg.theme('DarkBlue14')

    layout = [
        [sg.Text('Criar Novo Evento', font=('Helvetica', 20))],
        [sg.Text('Nome do Evento*', size=(25,1)), sg.Input(key='-NOME_EVENTO-')],
        [sg.Text('Data do Evento*', size=(25,1)), sg.Input(key='-DATA_EVENTO-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_EVENTO-', format='%d/%m/%Y')],
        [sg.Text('Distância (km)*', size=(25,1)), sg.Combo(['5k', '10k', '21k', '42k'], key='-DISTANCIA-', readonly=True)],

        # --- CAMPO MODIFICADO ---
        # Trocado os checkboxes por um botão que abre uma nova janela para cadastrar os kits.
        [sg.Text('Kits do Evento*', size=(25,1)), sg.Button('Cadastrar Kits', key='-CADASTRAR_KITS-'), sg.Text('', key='-STATUS_KITS-')],
        
        [sg.Text('Local de Largada*', size=(25,1)), sg.Input(key='-LOCAL-')],
        [sg.Text('Tempo de Corte*', size=(25,1)),
         sg.Input(key='-HORAS-', size=(4,1)), sg.Text('horas e'),
         sg.Input(key='-MINUTOS-', size=(4,1)), sg.Text('minutos')],
        [sg.Text('Data Limite para Cancelamento*', size=(25,1)), sg.Input(key='-DATA_CANCEL-', size=(12,1)), sg.CalendarButton('Selecionar', target='-DATA_CANCEL-', format='%d/%m/%Y')],
        [sg.Text('* Campos obrigatórios', text_color='red')],
        [sg.Button('Salvar Evento', key='-SALVAR_EVENTO-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]

    return sg.Window('PaceHub - Novo Evento', layout, finalize=True, resizable=True)


# --- LÓGICA PRINCIPAL ---
if __name__ == '__main__':
    janela_principal = criar_janela_novo_evento()
    kits_do_evento = [] # Lista para armazenar os kits cadastrados

    while True:
        window, event, values = sg.read_all_windows()

        if window == janela_principal and event in (sg.WIN_CLOSED, '-CANCELAR-'):
            break

        # Evento para abrir a janela de cadastro de kits
        if event == '-CADASTRAR_KITS-':
            janela_kits = criar_janela_cadastro_kit(kits_do_evento)
            
            # Loop para a janela secundária de kits
            while True:
                event_kit, values_kit = janela_kits.read()
                if event_kit in (sg.WIN_CLOSED, '-SALVAR_KITS-'):
                    break
                
                if event_kit == '-ADICIONAR_KIT-':
                    nome = values_kit['-NOME_KIT-']
                    valor = values_kit['-VALOR-']
                    if nome and valor:
                        # Formata a string para exibição na lista
                        kit_formatado = f"{nome} - R$ {valor}"
                        kits_do_evento.append(kit_formatado)
                        janela_kits['-LISTA_KITS-'].update(values=kits_do_evento)
                        # Limpa os campos de input
                        janela_kits['-NOME_KIT-'].update('')
                        janela_kits['-DESCRICAO-'].update('')
                        janela_kits['-VALOR-'].update('')
                    else:
                        sg.popup_error('Nome e Valor do kit são obrigatórios.')
                
                if event_kit == '-REMOVER_KIT-':
                    # Pega os itens selecionados para remover
                    selecionados = values_kit['-LISTA_KITS-']
                    if selecionados:
                        # Remove os itens da lista principal
                        kits_do_evento = [kit for kit in kits_do_evento if kit not in selecionados]
                        janela_kits['-LISTA_KITS-'].update(values=kits_do_evento)

            janela_kits.close()
            # Atualiza o status na janela principal para dar feedback ao usuário
            janela_principal['-STATUS_KITS-'].update(f'{len(kits_do_evento)} kit(s) cadastrado(s).', text_color='lime')


        # Evento para salvar o evento principal
        if event == '-SALVAR_EVENTO-':
            campos_texto_obrigatorios = ['-NOME_EVENTO-', '-DATA_EVENTO-', '-DISTANCIA-', '-LOCAL-', '-HORAS-', '-MINUTOS-', '-DATA_CANCEL-']
            campos_vazios = [campo for campo in campos_texto_obrigatorios if not values[campo]]

            if campos_vazios or not kits_do_evento:
                sg.popup_error('Por favor, preencha todos os campos e cadastre pelo menos um kit para o evento.')
                continue

            sg.popup('Evento criado com sucesso!')
            break

    janela_principal.close()