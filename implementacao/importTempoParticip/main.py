#!/usr/bin/env python3
"""
Sistema de Importação de Tempos de Participantes - PaceHub
Ponto de entrada principal para o sistema completo.

Este sistema implementa o caso de uso de importação de resultados de corrida
via arquivo CSV e visualização de rankings por categoria, seguindo arquitetura UML.

Autor: Sistema PaceHub
Versão: 1.0
"""

import os
import sys
import PySimpleGUI as sg

# Adicionar o diretório atual ao path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from inicializar_banco import inicializar_banco, verificar_banco
from painelorg_integrado import executar_painel_organizador, mostrar_ajuda
from limite.tela_importar_resultados import executar_janela_importacao
from limite.tela_visualizar_ranking import executar_janela_rankings
from controlador.controlador_ranking import ControladorRanking
from entidade.evento import EVENTOS_MOCK


def mostrar_menu_principal():
    """
    Mostra o menu principal do sistema.
    """
    sg.theme('DarkBlue14')
    
    layout = [
        [sg.Text('PaceHub - Sistema de Importação de Resultados', font=('Helvetica', 20))],
        [sg.Text('Sistema completo para importação de tempos e visualização de rankings', font=('Helvetica', 12))],
        [sg.HorizontalSeparator()],
        [sg.Text('Escolha uma opção:', font=('Helvetica', 14, 'bold'))],
        [sg.Button('🏃‍♂️ Painel do Organizador', key='-PAINEL-', size=(25, 2))],
        [sg.Button('📊 Importar Resultados', key='-IMPORTAR-', size=(25, 2))],
        [sg.Button('🏆 Visualizar Rankings', key='-RANKINGS-', size=(25, 2))],
        [sg.Button('🔍 Buscar Atleta', key='-BUSCAR-', size=(25, 2))],
        [sg.HorizontalSeparator()],
        [sg.Text('Ferramentas:', font=('Helvetica', 12, 'bold'))],
        [sg.Button('⚙️ Verificar Banco', key='-VERIFICAR-', size=(15, 1)),
         sg.Button('❓ Ajuda', key='-AJUDA-', size=(15, 1)),
         sg.Button('🚪 Sair', key='-SAIR-', size=(15, 1))]
    ]
    
    return sg.Window('PaceHub - Menu Principal', layout, size=(500, 400), finalize=True)


def executar_menu_principal():
    """
    Executa o menu principal do sistema.
    """
    janela = mostrar_menu_principal()
    
    while True:
        event, values = janela.read()
        
        if event in (sg.WIN_CLOSED, '-SAIR-'):
            break
        
        elif event == '-PAINEL-':
            janela.hide()
            executar_painel_organizador()
            janela.un_hide()
        
        elif event == '-IMPORTAR-':
            janela.hide()
            # Mostrar lista de eventos para importação
            eventos_disponiveis = [e for e in EVENTOS_MOCK if e.status == 'Concluído']
            
            if not eventos_disponiveis:
                sg.popup_error("Nenhum evento concluído disponível para importação.")
                janela.un_hide()
                continue
            
            # Criar lista de seleção
            lista_eventos = []
            for evento in eventos_disponiveis:
                lista_eventos.append(f"{evento.nome} - {evento.data}")
            
            evento_selecionado = sg.popup_get_text(
                f"Selecione o evento para importação:\n\n" + 
                "\n".join(f"{i+1}. {evento}" for i, evento in enumerate(lista_eventos)),
                title="Selecionar Evento",
                default_text="1"
            )
            
            if evento_selecionado:
                try:
                    indice_evento = int(evento_selecionado) - 1
                    if 0 <= indice_evento < len(eventos_disponiveis):
                        evento_id = eventos_disponiveis[indice_evento].id
                        executar_janela_importacao(evento_id)
                    else:
                        sg.popup_error("Número de evento inválido.")
                except ValueError:
                    sg.popup_error("Por favor, digite um número válido.")
            
            janela.un_hide()
        
        elif event == '-RANKINGS-':
            janela.hide()
            # Mostrar lista de eventos com resultados
            controlador_ranking = ControladorRanking()
            eventos_com_resultados = []
            
            for evento in EVENTOS_MOCK:
                if controlador_ranking.verificar_evento_tem_resultados(evento.id):
                    eventos_com_resultados.append(evento)
            
            if not eventos_com_resultados:
                sg.popup_error("Nenhum evento possui resultados importados.")
                janela.un_hide()
                continue
            
            # Criar lista de seleção
            lista_eventos = []
            for evento in eventos_com_resultados:
                lista_eventos.append(f"{evento.nome} - {evento.data}")
            
            evento_selecionado = sg.popup_get_text(
                f"Selecione o evento para visualizar rankings:\n\n" + 
                "\n".join(f"{i+1}. {evento}" for i, evento in enumerate(lista_eventos)),
                title="Selecionar Evento",
                default_text="1"
            )
            
            if evento_selecionado:
                try:
                    indice_evento = int(evento_selecionado) - 1
                    if 0 <= indice_evento < len(eventos_com_resultados):
                        evento_id = eventos_com_resultados[indice_evento].id
                        executar_janela_rankings(evento_id)
                    else:
                        sg.popup_error("Número de evento inválido.")
                except ValueError:
                    sg.popup_error("Por favor, digite um número válido.")
            
            janela.un_hide()
        
        elif event == '-BUSCAR-':
            janela.hide()
            # Mostrar lista de eventos com resultados para busca
            controlador_ranking = ControladorRanking()
            eventos_com_resultados = []
            
            for evento in EVENTOS_MOCK:
                if controlador_ranking.verificar_evento_tem_resultados(evento.id):
                    eventos_com_resultados.append(evento)
            
            if not eventos_com_resultados:
                sg.popup_error("Nenhum evento possui resultados importados.")
                janela.un_hide()
                continue
            
            # Criar lista de seleção
            lista_eventos = []
            for evento in eventos_com_resultados:
                lista_eventos.append(f"{evento.nome} - {evento.data}")
            
            evento_selecionado = sg.popup_get_text(
                f"Selecione o evento para busca:\n\n" + 
                "\n".join(f"{i+1}. {evento}" for i, evento in enumerate(lista_eventos)),
                title="Selecionar Evento",
                default_text="1"
            )
            
            if evento_selecionado:
                try:
                    indice_evento = int(evento_selecionado) - 1
                    if 0 <= indice_evento < len(eventos_com_resultados):
                        evento_id = eventos_com_resultados[indice_evento].id
                        from limite.tela_visualizar_ranking import executar_busca_atleta
                        executar_busca_atleta(evento_id)
                    else:
                        sg.popup_error("Número de evento inválido.")
                except ValueError:
                    sg.popup_error("Por favor, digite um número válido.")
            
            janela.un_hide()
        
        elif event == '-VERIFICAR-':
            janela.hide()
            verificar_banco()
            janela.un_hide()
        
        elif event == '-AJUDA-':
            janela.hide()
            mostrar_ajuda()
            janela.un_hide()
    
    janela.close()


def executar_teste_rapido():
    """
    Executa um teste rápido do sistema.
    """
    print("=== TESTE RÁPIDO DO SISTEMA ===")
    
    # 1. Verificar banco
    print("1. Verificando banco de dados...")
    verificar_banco()
    
    # 2. Testar controladores
    print("\n2. Testando controladores...")
    from controlador.controlador_importacao import ControladorImportacao
    from controlador.controlador_ranking import ControladorRanking
    
    controlador_importacao = ControladorImportacao()
    controlador_ranking = ControladorRanking()
    
    print("   ✓ Controladores criados com sucesso")
    
    # 3. Verificar eventos
    print("\n3. Verificando eventos...")
    print(f"   Total de eventos: {len(EVENTOS_MOCK)}")
    for evento in EVENTOS_MOCK:
        tem_resultados = controlador_ranking.verificar_evento_tem_resultados(evento.id)
        print(f"   - {evento.nome}: {'✓' if tem_resultados else '✗'} resultados")
    
    # 4. Testar validações
    print("\n4. Testando validações...")
    cpfs_validos = ["11111111111", "123.456.789-01"]
    cpfs_invalidos = ["123", "abc"]
    
    for cpf in cpfs_validos:
        valido = controlador_importacao._validar_cpf(cpf)
        print(f"   CPF {cpf}: {'✓' if valido else '✗'}")
    
    for cpf in cpfs_invalidos:
        valido = controlador_importacao._validar_cpf(cpf)
        print(f"   CPF {cpf}: {'✓' if valido else '✗'}")
    
    print("\n=== TESTE RÁPIDO CONCLUÍDO ===")


def main():
    """
    Função principal do sistema.
    """
    print("=" * 60)
    print("=== PACEHUB - SISTEMA DE IMPORTAÇÃO DE RESULTADOS ===")
    print("=== Versão 1.0 - Arquitetura UML ===")
    print("=" * 60)
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == 'init':
            print("Inicializando banco de dados...")
            inicializar_banco(forcar_repopular=True)
            return
        
        elif comando == 'check':
            print("Verificando banco de dados...")
            verificar_banco()
            return
        
        elif comando == 'test':
            print("Executando teste rápido...")
            executar_teste_rapido()
            return
        
        elif comando == 'help':
            print("Comandos disponíveis:")
            print("  python main.py          - Executa o sistema completo")
            print("  python main.py init     - Inicializa o banco de dados")
            print("  python main.py check     - Verifica o estado do banco")
            print("  python main.py test      - Executa teste rápido")
            print("  python main.py help      - Mostra esta ajuda")
            return
        
        else:
            print(f"Comando desconhecido: {comando}")
            print("Use 'python main.py help' para ver comandos disponíveis.")
            return
    
    # Execução normal do sistema
    try:
        # SEMPRE inicializar banco (cria tabelas se não existir, popula eventos se vazio)
        print("\n[MAIN] Inicializando banco de dados...")
        sucesso_init = inicializar_banco()
        
        if not sucesso_init:
            print("[MAIN] ERRO: Falha na inicialização do banco!")
            sg.popup_error("Erro ao inicializar banco de dados!")
            return
        
        # Abrir DIRETO o painel do organizador (sem menu)
        print("[MAIN] Abrindo painel do organizador...\n")
        executar_painel_organizador()
        
    except Exception as e:
        print(f"[MAIN] ERRO ao executar sistema: {e}")
        import traceback
        traceback.print_exc()
        sg.popup_error(f"Erro ao executar sistema: {e}")
    
    print("\n[MAIN] Sistema finalizado.")


if __name__ == "__main__":
    main()
