import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TelaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.evento_retornado = None
        self.valores_retornados = None

    def exibir_janela_login(self):
        self.evento_retornado = None

        janela_login = tk.Toplevel(self.root)
        janela_login.title("PaceHub - Bem-vindo")
        janela_login.geometry("400x400")  # Aumentei um pouco a altura para garantir
        janela_login.resizable(False, False)

        frame = ttk.Frame(janela_login, padding=20)
        frame.pack(expand=True, fill='both')

        def on_login():
            self.evento_retornado = 'Login'
            self.valores_retornados = {
                '-CPF_LOGIN-': entry_cpf.get(),
                '-SENHA_LOGIN-': entry_senha.get()
            }
            janela_login.destroy()

        def on_cadastro_atleta():
            self.evento_retornado = '-CADASTRO_ATLETA-'
            janela_login.destroy()

        def on_cadastro_organizador():
            self.evento_retornado = '-CADASTRO_ORGANIZADOR-'
            janela_login.destroy()

        def on_listar_atletas():
            self.evento_retornado = '-LISTAR_ATLETAS-'
            janela_login.destroy()

        ttk.Label(frame, text="PaceHub", font=("Helvetica", 25)).pack(pady=10)
        ttk.Label(frame, text="Sua plataforma de gestão de corridas.", font=("Helvetica", 12)).pack()

        frame_login = ttk.Frame(frame)
        frame_login.pack(pady=20)

        ttk.Label(frame_login, text="CPF*").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        entry_cpf = ttk.Entry(frame_login)
        entry_cpf.grid(row=0, column=1, sticky='ew')

        ttk.Label(frame_login, text="Senha*").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        entry_senha = ttk.Entry(frame_login, show='*')
        entry_senha.grid(row=1, column=1, sticky='ew')

        ttk.Button(frame, text="Login", command=on_login).pack(fill='x', ipady=5)
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

        ttk.Label(frame, text="Ainda não tem uma conta? Cadastre-se agora!").pack()
        ttk.Button(frame, text="Cadastrar como Atleta", command=on_cadastro_atleta).pack(fill='x', pady=5)
        ttk.Button(frame, text="Cadastrar como Organizador", command=on_cadastro_organizador).pack(fill='x')

        ttk.Button(frame, text="Listar Atletas", command=on_listar_atletas).pack(fill='x', pady=(10, 0))

        janela_login.grab_set()
        self.root.wait_window(janela_login)

        return self.evento_retornado, self.valores_retornados

    def exibir_popup_erro(self, mensagem: str):
        messagebox.showerror("Erro", mensagem, parent=self.root)

    def exibir_popup_sucesso(self, mensagem: str):
        messagebox.showinfo("Sucesso", mensagem, parent=self.root)