import PySimpleGUI as sg

def criar_painel_organizador():
    sg.theme('DarkBlue14')

    # Dados de exemplo que seriam carregados de um banco de dados
    meus_eventos = [
        ["Meia Maratona de Inverno", "10/08/2025", 1530, "Concluído"],
        ["Corrida Solidária", "30/09/2025", 875, "Inscrições Abertas"],
        ["Maratona de Floripa", "25/10/2025", 450, "Inscrições Abertas"],
        ["Night Run - Edição Halloween", "31/10/2025", 0, "Concluído"],
    ]
    
    # --- CRIAÇÃO DO LAYOUT DINÂMICO (SUBSTITUINDO A TABELA) ---

    headings = ['Nome do Evento', 'Data', 'Inscritos', 'Status']
    header = [sg.Text(h, font=('Helvetica', 10, 'bold'), pad=(5,5), size=(20 if h == 'Nome do Evento' else 10, 1)) for h in headings]

    # Lista que vai conter todas as linhas de eventos
    eventos_rows = [header, [sg.HorizontalSeparator()]]

    # Loop para criar uma linha de layout para cada evento
    for idx, evento in enumerate(meus_eventos):
        nome, data, inscritos, status = evento
        
        # Lógica para desabilitar botões conforme o status do evento
        pode_cancelar = status != "Concluído"
        pode_importar = status == "Concluído"
        pode_publicar = status == "Concluído"

        linha_layout = [
            sg.Text(nome, size=(22, 2)),
            sg.Text(data, size=(12, 2)),
            sg.Text(inscritos, size=(10, 2), justification='center'),
            sg.Text(status, size=(18, 2)),
        # Botões de ação para esta linha específica
        sg.Column([
            [
                sg.Button('Editar', key=('-EDIT-', idx), size=(8,1)),
                sg.Button('Deletar', key=('-DELETE-', idx), size=(8,1)),
                sg.Button('Cad. Kits', key=('-CADASTRAR_KITS-', idx), size=(8,1)),
                sg.Button('Geren. Kits', key=('-GERENCIAR_KITS-', idx), size=(8,1)),
                sg.Button('Pub. Res.', key=('-PUBLISH-', idx), size=(8,1), disabled=not pode_publicar),
                sg.Button('Ver Inscritos', key=('-VER_INSCRITOS-', idx), size=(10,1)),
                sg.Button('Imp. Tempos', key=('-IMPORT-', idx), size=(10,1), disabled=not pode_importar),
            ]
        ])
        ]
        eventos_rows.append(linha_layout)
        eventos_rows.append([sg.HorizontalSeparator()])

    # --- LAYOUT PRINCIPAL ---

    layout = [
        [sg.Text('Painel do Organizador', font=('Helvetica', 20))],
        [sg.Text('Bem-vindo, Organizador!')],
        [sg.Button('Criar Novo Evento', key='-CRIAR_EVENTO-', size=(20, 2))],
        [sg.HorizontalSeparator()],
        [sg.Text('Meus Eventos', font=('Helvetica', 15))],
        # A coluna rolável contém o layout dinâmico que criamos
        [sg.Column(eventos_rows, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(1150, 300))]
    ]

    return sg.Window('PaceHub - Painel do Organizador', layout, size=(1200, 500), finalize=True, resizable=True)


# --- LÓGICA PRINCIPAL ---
if __name__ == '__main__':
    janela_organizador = criar_painel_organizador()
    
    # Simula os dados para que possam ser acessados no loop
    dados_eventos = [
        ["Meia Maratona de Inverno", "10/08/2025", 1530, "Concluído"],
        ["Corrida Solidária", "30/09/2025", 875, "Inscrições Abertas"],
        ["Maratona de Floripa", "25/10/2025", 450, "Inscrições Abertas"],
        ["Night Run - Edição Halloween", "31/10/2025", 0, "Planejado"],
    ]

    while True:
        event, values = janela_organizador.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-CRIAR_EVENTO-':
            # Abre a tela de gestão de evento em modo criação
            import gestaoEvento
            janela_gestao = gestaoEvento.criar_janela_gestao_evento()
            
            # Loop para a janela de gestão
            while True:
                event_gestao, values_gestao = janela_gestao.read()
                if event_gestao in (sg.WIN_CLOSED, '-VOLTAR-'):
                    break
                # Outros eventos da gestão são tratados na própria janela
            
            janela_gestao.close()
        
        # --- NOVO TRATAMENTO DE EVENTOS PARA OS BOTÕES DE LINHA ---
        # Verifica se o evento é uma tupla (ex: ('-EDIT-', 0))
        if isinstance(event, tuple):
            action, index = event
            evento_selecionado = dados_eventos[index]
            nome_evento = evento_selecionado[0]

            if action == '-EDIT-':
                # Importa e abre a tela de gestão de evento
                import gestaoEvento
                dados_evento = {
                    'nome': evento_selecionado[0],
                    'data': evento_selecionado[1],
                    'distancia': '21k',  # Valor padrão, seria carregado do banco
                    'local': 'Local padrão',  # Seria carregado do banco
                    'horas_corte': '3',
                    'minutos_corte': '30',
                    'data_cancelamento': '05/08/2025'
                }
                janela_gestao = gestaoEvento.criar_janela_gestao_evento(dados_evento)
                
                # Loop para a janela de gestão
                while True:
                    event_gestao, values_gestao = janela_gestao.read()
                    if event_gestao in (sg.WIN_CLOSED, '-VOLTAR-'):
                        break
                    # Outros eventos da gestão são tratados na própria janela
                
                janela_gestao.close()
            
            elif action == '-DELETE-':
                if sg.popup_yes_no(f'Tem certeza que deseja DELETAR o evento:\n"{nome_evento}"?\n\nEsta ação não pode ser desfeita.') == 'Yes':
                    sg.popup(f'Evento "{nome_evento}" deletado com sucesso.')
                    # Aqui você adicionaria a lógica para remover o evento da lista
            
            elif action == '-CADASTRAR_KITS-':
                sg.popup(f'Abrindo tela de cadastro de kits para:\n"{nome_evento}"')
                # Aqui você chamaria: import cadastroKits; cadastroKits.criar_janela_cadastro_kit()
            
            elif action == '-GERENCIAR_KITS-':
                sg.popup(f'Abrindo tela de gerenciamento de entrega de kits para:\n"{nome_evento}"')
                # Aqui você chamaria: import gerenciaKits; gerenciaKits.criar_janela_gerenciar_kits()
            
            elif action == '-VER_INSCRITOS-':
                sg.popup(f'Abrindo lista de inscritos para:\n"{nome_evento}"')
                # Aqui você chamaria: import listaInscritos; listaInscritos.criar_janela_lista_inscritos()
            
            elif action == '-IMPORT-':
                sg.popup(f'Abrindo janela para importar tempos do evento:\n"{nome_evento}"')
                # Aqui você chamaria: import importaResulta; importaResulta.criar_janela_importar_resultados()

            elif action == '-PUBLISH-':
                sg.popup(f'Resultados do evento "{nome_evento}" publicados!')


    janela_organizador.close()