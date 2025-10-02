from controle.controlador_sistema import ControladorSistema


if __name__ == '__main__':
    print("=== PaceHub - Sistema de Gestão de Organizadores ===")
    print("Sistema de Autenticação e Perfil")
    print("Iniciando sistema...")
    
    try:
        controlador = ControladorSistema()
        controlador.iniciar()
        print("Sistema finalizado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar o sistema: {e}")
        input("Pressione Enter para sair...")
