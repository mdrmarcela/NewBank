import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import locale
import gettext
import os
import tkinter.messagebox as messagebox

from repositorio import (
    criar_sessao,
    criar_titular,
    criar_conta,
    buscar_conta_por_id
)

def detectar_idioma_padrao():
    return locale.getdefaultlocale()[0] or "pt_BR"


def configurar_idioma(idioma):
    localedir = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "locale")
    lang = gettext.translation('banco', localedir=localedir, languages=[
                               idioma], fallback=True)
    lang.install()
    return lang.gettext


class BancoApp:
    def __init__(self, root):
        self.root = root
        self.session = criar_sessao()
        self.idioma = detectar_idioma_padrao()
        self._ = configurar_idioma(self.idioma)

        self.root.title(self._("Bem-vindo ao Banco"))
        self.root.geometry("400x350")

        self.tipos_conta = {
            "contacorrente": self._("Conta Corrente"),
            "poupanca": self._("Poupança"),
            "contasalario": self._("Conta Salário")
        }

        self.construir_interface()

    def construir_interface(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        ttk.Label(frame, text=self._("Bem-vindo ao NewBank"),
                  font=("Helvetica", 18, "bold")).pack(pady=15)

        ttk.Button(frame, text=self._("Criar Conta"), bootstyle="success",
                   command=self.criar_conta).pack(fill=X, pady=5)
        ttk.Button(frame, text=self._("Acessar Conta"), bootstyle="info",
                   command=self.acessar_conta).pack(fill=X, pady=5)
        ttk.Button(frame, text=self._("Sair"), bootstyle="danger",
                   command=self.root.quit).pack(fill=X, pady=20)

        ttk.Label(frame, text=self._("Idioma")).pack()
        idiomas = ["Português", "English", "Español"]
        self.combo_idioma = ttk.Combobox(
            frame, values=idiomas, state="readonly")
        try:
            idx = ["pt", "en", "es"].index(self.idioma.split("_")[0])
        except ValueError:
            idx = 0
        self.combo_idioma.current(idx)
        self.combo_idioma.pack()
        self.combo_idioma.bind("<<ComboboxSelected>>", self.trocar_idioma)

    def trocar_idioma(self, event):
        mapa = {"Português": "pt_BR", "English": "en_US", "Español": "es_ES"}
        self.idioma = mapa.get(self.combo_idioma.get(), "pt_BR")
        self._ = configurar_idioma(self.idioma)

        self.tipos_conta = {
            "contacorrente": self._("Conta Corrente"),
            "poupanca": self._("Poupança"),
            "contasalario": self._("Conta Salário")
        }

        for widget in self.root.winfo_children():
            widget.destroy()
        self.construir_interface()

    def criar_conta(self):
        janela = ttk.Toplevel(self.root)
        janela.title(self._("Criar Conta"))
        janela.geometry("300x400")

        ttk.Label(janela, text=self._("Nome:")).pack(pady=5)
        entry_nome = ttk.Entry(janela)
        entry_nome.pack()

        ttk.Label(janela, text=self._("Endereço:")).pack(pady=5)
        entry_endereco = ttk.Entry(janela)
        entry_endereco.pack()

        ttk.Label(janela, text=self._("Saldo Inicial:")).pack(pady=5)
        entry_saldo = ttk.Entry(janela)
        entry_saldo.pack()

        ttk.Label(janela, text=self._("Tipo de Conta:")).pack(pady=5)
        tipo_var = ttk.StringVar(value=self._("Conta Corrente"))
        tipo_combo = ttk.Combobox(
            janela, textvariable=tipo_var,
            values=list(self.tipos_conta.values()),
            state="readonly"
        )
        tipo_combo.pack()

        def salvar():
            nome = entry_nome.get()
            endereco = entry_endereco.get()
            saldo_texto = entry_saldo.get()
            tipo_legivel = tipo_var.get()

            if not nome or not endereco or not saldo_texto:
                messagebox.showerror(self._("Erro"), self._(
                    "Preencha todos os campos"))
                return

            try:
                saldo = float(saldo_texto)
                if saldo < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(self._("Erro"), self._("Saldo inválido"))
                return

            tipo_chave = next(
                (k for k, v in self.tipos_conta.items() if v == tipo_legivel), None)

            if not tipo_chave:
                messagebox.showerror(
                    self._("Erro"), self._("Tipo de conta inválido"))
                return

            titular = criar_titular(self.session, nome, endereco)
            criar_conta(self.session, tipo_chave,
                        titular.id, saldo_inicial=saldo)

            messagebox.showinfo(self._("Sucesso"), self._(
                "Conta criada com sucesso!"))
            janela.destroy()

        ttk.Button(janela, text=self._("Salvar"),
                   bootstyle="success", command=salvar).pack(pady=20)

    def acessar_conta(self):
        janela = ttk.Toplevel(self.root)
        janela.title(self._("Acessar Conta"))
        janela.geometry("300x250")

        ttk.Label(janela, text=self._("Digite o ID da Conta:")).pack(pady=10)
        entry_id = ttk.Entry(janela)
        entry_id.pack()

        def buscar():
            id_texto = entry_id.get()
            if not id_texto:
                messagebox.showerror(
                    self._("Erro"), self._("Informe o ID da conta."))
                return

            try:
                id_conta = int(id_texto)
            except ValueError:
                messagebox.showerror(self._("Erro"), self._("ID inválido."))
                return

            conta = buscar_conta_por_id(self.session, id_conta)
            if not conta:
                messagebox.showerror(
                    self._("Erro"), self._("Conta não encontrada."))
                return

            detalhes = (
                f"{self._('Nome')}: {conta.titular.nome}\n"
                f"{self._('Endereço')}: {conta.titular.endereco}\n"
                f"{self._('Tipo de Conta')}: {self.tipos_conta.get(conta.tipo, conta.tipo)}\n"
                f"{self._('Saldo')}: R$ {conta.saldo:.2f}"
            )
            messagebox.showinfo(self._("Detalhes da Conta"), detalhes)
            janela.destroy()

        ttk.Button(janela, text=self._("Buscar"),
                   bootstyle="primary", command=buscar).pack(pady=20)
        

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")  
    app = BancoApp(root)
    root.mainloop()

