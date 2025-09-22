import tkinter as tk
from tkinter import ttk


class TelaCadastro:
    def __init__(self, root):
        self.root = root
        self.evento_retornado = None
        self.valores_retornados = None

    def exibir_janela_cadastro(self, perfil: str):

        janela_cadastro = tk.Toplevel(self.root)
        janela_cadastro.title(f"PaceHub - Cadastro de {perfil}")

        frame = ttk.Frame(janela_cadastro, padding=20)
        frame.grid(row=0, column=0, sticky='nsew')

        vars = {
            '-NOME-': tk.StringVar(),
            '-CPF-': tk.StringVar(),
            '-EMAIL-': tk.StringVar(),
            '-SENHA-': tk.StringVar(),
            '-DATA_NASC-': tk.StringVar(),
            '-GENERO-': tk.StringVar(),
            '-PCD_SIM-': tk.BooleanVar(value=False),
        }

        def on_cadastrar():
            self.evento_retornado = '-CADASTRAR-'
            self.valores_retornados = {key: var.get() for key, var in vars.items()}
            janela_cadastro.destroy()

        def on_voltar():
            self.evento_retornado = '-VOLTAR-'
            janela_cadastro.destroy()

        ttk.Label(frame, text=f"Cadastro de {perfil}", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2,
                                                                                    pady=10)

        frame_dados = ttk.Frame(frame, padding=10, borderwidth=1, relief='solid')
        frame_dados.grid(row=1, column=0, columnspan=2, sticky='ew')

        ttk.Label(frame_dados, text="Nome Completo*").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(frame_dados, textvariable=vars['-NOME-']).grid(row=0, column=1, sticky='ew')

        ttk.Label(frame_dados, text="CPF*").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(frame_dados, textvariable=vars['-CPF-']).grid(row=1, column=1, sticky='ew')

        if perfil == 'Atleta':
            ttk.Label(frame_dados, text="Data de Nascimento*").grid(row=2, column=0, sticky='w', padx=5, pady=5)
            ttk.Entry(frame_dados, textvariable=vars['-DATA_NASC-']).grid(row=2, column=1, sticky='ew')
            ttk.Label(frame_dados, text="(dd/mm/aaaa)", font=("Helvetica", 8)).grid(row=2, column=2, sticky='w')

            ttk.Label(frame_dados, text="Gênero*").grid(row=3, column=0, sticky='w', padx=5, pady=5)
            ttk.Combobox(frame_dados, values=['Masculino', 'Feminino', 'Outro'], textvariable=vars['-GENERO-']).grid(
                row=3, column=1, sticky='ew')

            pcd_frame = ttk.Frame(frame_dados)
            pcd_frame.grid(row=4, column=1, sticky='w')
            ttk.Label(frame_dados, text="PCD*").grid(row=4, column=0, sticky='w', padx=5, pady=5)
            ttk.Radiobutton(pcd_frame, text="Sim", variable=vars['-PCD_SIM-'], value=True).pack(side='left')
            ttk.Radiobutton(pcd_frame, text="Não", variable=vars['-PCD_SIM-'], value=False).pack(side='left')

        ttk.Label(frame_dados, text="Email*").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(frame_dados, textvariable=vars['-EMAIL-']).grid(row=5, column=1, sticky='ew')

        ttk.Label(frame_dados, text="Senha*").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(frame_dados, show="*", textvariable=vars['-SENHA-']).grid(row=6, column=1, sticky='ew')

        ttk.Button(frame, text="Cadastrar", command=on_cadastrar).grid(row=2, column=1, sticky='e', pady=20)
        ttk.Button(frame, text="Voltar", command=on_voltar).grid(row=2, column=0, sticky='w', pady=20)

        janela_cadastro.grab_set()
        self.root.wait_window(janela_cadastro)

        return self.evento_retornado, self.valores_retornados