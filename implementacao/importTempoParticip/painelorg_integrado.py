import FreeSimpleGUI as sg
from limite.tela_importar_resultados import executar_janela_importacao
from limite.tela_visualizar_ranking import executar_janela_rankings, mostrar_estatisticas_evento, executar_busca_atleta
from entidade.evento import EVENTOS_MOCK
from controlador.controlador_ranking import ControladorRanking


def criar_painel_organizador():
    """
    Cria o painel do organizador integrado com funcionalidades de importação e visualização de resultados.
    Baseado no arquivo casos-de-uso/painelorg.py com melhorias e integração completa.
    """
    sg.theme('DarkBlue14')
    
    # Dados de exemplo (mockdata dos eventos)
    meus_eventos = []
    for evento in EVENTOS_MOCK:
        # Simular número de inscritos baseado no status
        if evento.status == "Concluído":
            inscritos = 1200 + (evento.id * 100)  # Simular diferentes números
        elif evento.status == "Inscrições Abertas":
            inscritos = 500 + (evento.id * 50)
        else:
            inscritos = 0
        
        meus_eventos.append([
            evento.nome,
            evento.data,
            inscritos,
            evento.status
        ])
    
    # --- CRIAÇÃO DO LAYOUT DINÂMICO ---
    
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
        
        # Verificar se tem resultados importados
        controlador_ranking = ControladorRanking()
        tem_resultados = controlador_ranking.verificar_evento_tem_resultados(idx + 1)
        pode_ver_resultados = tem_resultados
        
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
                    sg.Button('Ver Resultados', key=('-VER_RESULTADOS-', idx), size=(12,1), disabled=not pode_ver_resultados),
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
        [sg.Column(eventos_rows, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(1300, 300))],
        [sg.HorizontalSeparator()],
        [sg.Text('Ações Rápidas:', font=('Helvetica', 12, 'bold'))],
        [sg.Button('Estatísticas Gerais', key='-STATS_GERAIS-', size=(15, 1)),
         sg.Button('Buscar Atleta', key='-BUSCAR_ATLETA-', size=(15, 1)),
         sg.Button('Sair', key='-SAIR-', size=(10, 1))]
    ]
    
    return sg.Window('PaceHub - Painel do Organizador', layout, size=(1400, 600), finalize=True, resizable=True)


def executar_painel_organizador():
    """
    Executa o painel do organizador com todas as funcionalidades integradas.
    """
    janela_organizador = criar_painel_organizador()
    
    # Simula os dados para que possam ser acessados no loop
    dados_eventos = []
    for evento in EVENTOS_MOCK:
        dados_eventos.append([
            evento.nome,
            evento.data,
            1200 + (evento.id * 100) if evento.status == "Concluído" else 500 + (evento.id * 50),
            evento.status
        ])
    
    while True:
        event, values = janela_organizador.read()
        
        if event == sg.WIN_CLOSED:
            break
        
        if event == '-CRIAR_EVENTO-':
            sg.popup('Funcionalidade de criar evento será implementada em versão futura.')
        
        # --- TRATAMENTO DE EVENTOS PARA OS BOTÕES DE LINHA ---
        # Verifica se o evento é uma tupla (ex: ('-EDIT-', 0))
        if isinstance(event, tuple):
            action, index = event
            evento_selecionado = dados_eventos[index]
            nome_evento = evento_selecionado[0]
            evento_id = index + 1  # IDs começam em 1
            
            if action == '-EDIT-':
                sg.popup(f'Funcionalidade de editar evento será implementada em versão futura.\nEvento: "{nome_evento}"')
            
            elif action == '-DELETE-':
                if sg.popup_yes_no(f'Tem certeza que deseja DELETAR o evento:\n"{nome_evento}"?\n\nEsta ação não pode ser desfeita.') == 'Yes':
                    sg.popup(f'Evento "{nome_evento}" deletado com sucesso.')
                    # Aqui você adicionaria a lógica para remover o evento da lista
            
            elif action == '-CADASTRAR_KITS-':
                sg.popup(f'Funcionalidade de cadastro de kits será implementada em versão futura.\nEvento: "{nome_evento}"')
            
            elif action == '-GERENCIAR_KITS-':
                sg.popup(f'Funcionalidade de gerenciamento de kits será implementada em versão futura.\nEvento: "{nome_evento}"')
            
            elif action == '-VER_INSCRITOS-':
                sg.popup(f'Funcionalidade de visualizar inscritos será implementada em versão futura.\nEvento: "{nome_evento}"')
            
            elif action == '-IMPORT-':
                # NOVA FUNCIONALIDADE: Importar tempos
                print(f"\n[PAINEL] Botão 'Imp. Tempos' clicado para evento: {nome_evento} (ID: {evento_id})")
                sucesso = executar_janela_importacao(evento_id, nome_evento)
                
                if sucesso:
                    print(f"[PAINEL] Importação bem-sucedida para evento ID: {evento_id}")
                    sg.popup(f'Resultados importados com sucesso para:\n"{nome_evento}"')
                    # Atualizar interface para habilitar botão "Ver Resultados"
                    janela_organizador[('-VER_RESULTADOS-', index)].update(disabled=False)
                else:
                    print(f"[PAINEL] Importação cancelada para evento ID: {evento_id}")
                    sg.popup(f'Importação cancelada ou com erro para:\n"{nome_evento}"')
            
            elif action == '-VER_RESULTADOS-':
                # NOVA FUNCIONALIDADE: Ver resultados/rankings
                print(f"\n[PAINEL] Botão 'Ver Resultados' clicado para evento: {nome_evento} (ID: {evento_id})")
                sucesso = executar_janela_rankings(evento_id)
                
                if not sucesso:
                    print(f"[PAINEL] Erro ao exibir rankings para evento ID: {evento_id}")
                    sg.popup_error(f'Não foi possível exibir os rankings para:\n"{nome_evento}"')
            
            elif action == '-PUBLISH-':
                sg.popup(f'Resultados do evento "{nome_evento}" publicados!')
        
        # --- AÇÕES RÁPIDAS ---
        elif event == '-STATS_GERAIS-':
            sg.popup('Estatísticas gerais serão implementadas em versão futura.')
        
        elif event == '-BUSCAR_ATLETA-':
            # Permitir busca em qualquer evento que tenha resultados
            eventos_com_resultados = []
            controlador_ranking = ControladorRanking()
            
            for i, evento in enumerate(EVENTOS_MOCK):
                if controlador_ranking.verificar_evento_tem_resultados(i + 1):
                    eventos_com_resultados.append(f"{evento.nome} - {evento.data}")
            
            if not eventos_com_resultados:
                sg.popup_error("Nenhum evento possui resultados importados.")
                continue
            
            # Selecionar evento para busca
            evento_busca = sg.popup_get_text(
                f"Selecione o evento para busca:\n\n" + "\n".join(f"{i+1}. {evento}" for i, evento in enumerate(eventos_com_resultados)),
                title="Selecionar Evento",
                default_text="1"
            )
            
            if evento_busca:
                try:
                    indice_evento = int(evento_busca) - 1
                    if 0 <= indice_evento < len(eventos_com_resultados):
                        evento_id_busca = indice_evento + 1
                        executar_busca_atleta(evento_id_busca)
                    else:
                        sg.popup_error("Número de evento inválido.")
                except ValueError:
                    sg.popup_error("Por favor, digite um número válido.")
        
        elif event == '-SAIR-':
            if sg.popup_yes_no('Tem certeza que deseja sair?') == 'Yes':
                break
    
    janela_organizador.close()


def mostrar_ajuda():
    """
    Mostra janela de ajuda com instruções de uso.
    """
    ajuda_texto = """
=== AJUDA - PAINEL DO ORGANIZADOR ===

FUNCIONALIDADES IMPLEMENTADAS:

1. IMPORTAÇÃO DE RESULTADOS:
   - Clique em "Imp. Tempos" em um evento concluído
   - Selecione arquivo CSV com formato: CPF,Tempo
   - Sistema valida e importa automaticamente
   - Calcula rankings por categoria

2. VISUALIZAÇÃO DE RANKINGS:
   - Clique em "Ver Resultados" após importar
   - Visualize classificações por categoria
   - Abas: Geral, Júnior, Adulto, Master, PCD

3. BUSCA DE ATLETA:
   - Use "Buscar Atleta" para encontrar resultado específico
   - Digite CPF do atleta
   - Veja posição geral e na categoria

FORMATO DO CSV:
CPF,Tempo
12345678901,01:30:45
98765432100,01:25:30

REGRAS DE NEGÓCIO:
- RN04: Categoria pela idade em 31/12 do ano do evento
- RN06: Classificação Geral = Top 5 de cada gênero  
- RN07: Demais classificados por categoria (Júnior/Adulto/Master)
- PCD compete separadamente

FUNCIONALIDADES FUTURAS:
- Criar/Editar eventos
- Gerenciar kits
- Visualizar inscritos
- Estatísticas gerais
    """
    
    sg.popup_scrolled(ajuda_texto, title="Ajuda - Painel do Organizador", size=(600, 400))


if __name__ == "__main__":
    # Teste do painel integrado
    print("=== Teste do Painel Integrado ===")
    
    # Mostrar ajuda primeiro
    mostrar_ajuda()
    
    # Executar painel
    executar_painel_organizador()
    
    print("Painel executado com sucesso!")
