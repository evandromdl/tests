#!/usr/bin/env python3
"""
Calculadora com Interface Gráfica
Suporta as 4 operações básicas: +, -, ×, ÷
"""

import tkinter as tk
from tkinter import messagebox


class Calculadora:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Calculadora")
        self.janela.geometry("320x480")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#2D2D2D")

        self.expressao = ""
        self.resultado_atual = ""

        self._criar_display()
        self._criar_botoes()

    def _criar_display(self):
        """Cria o display da calculadora."""
        frame_display = tk.Frame(self.janela, bg="#2D2D2D", height=120)
        frame_display.pack(fill=tk.X, padx=10, pady=(20, 10))
        frame_display.pack_propagate(False)

        # Expressão (texto menor em cima)
        self.label_expressao = tk.Label(
            frame_display,
            text="",
            font=("Segoe UI", 14),
            fg="#888888",
            bg="#2D2D2D",
            anchor="e"
        )
        self.label_expressao.pack(fill=tk.X, padx=5)

        # Resultado (texto grande)
        self.label_resultado = tk.Label(
            frame_display,
            text="0",
            font=("Segoe UI", 42, "bold"),
            fg="#FFFFFF",
            bg="#2D2D2D",
            anchor="e"
        )
        self.label_resultado.pack(fill=tk.X, padx=5, pady=(5, 0))

    def _criar_botoes(self):
        """Cria os botões da calculadora."""
        frame_botoes = tk.Frame(self.janela, bg="#2D2D2D")
        frame_botoes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Layout dos botões
        botoes = [
            ("C", "#FF6B6B", "#FFFFFF"),
            ("±", "#4A4A4A", "#FFFFFF"),
            ("%", "#4A4A4A", "#FFFFFF"),
            ("÷", "#FF9F43", "#FFFFFF"),
            ("7", "#3D3D3D", "#FFFFFF"),
            ("8", "#3D3D3D", "#FFFFFF"),
            ("9", "#3D3D3D", "#FFFFFF"),
            ("×", "#FF9F43", "#FFFFFF"),
            ("4", "#3D3D3D", "#FFFFFF"),
            ("5", "#3D3D3D", "#FFFFFF"),
            ("6", "#3D3D3D", "#FFFFFF"),
            ("-", "#FF9F43", "#FFFFFF"),
            ("1", "#3D3D3D", "#FFFFFF"),
            ("2", "#3D3D3D", "#FFFFFF"),
            ("3", "#3D3D3D", "#FFFFFF"),
            ("+", "#FF9F43", "#FFFFFF"),
            ("0", "#3D3D3D", "#FFFFFF"),
            (".", "#3D3D3D", "#FFFFFF"),
            ("⌫", "#4A4A4A", "#FFFFFF"),
            ("=", "#4ECB71", "#FFFFFF"),
        ]

        # Configurar grid
        for i in range(5):
            frame_botoes.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame_botoes.grid_columnconfigure(i, weight=1)

        # Criar botões
        for idx, (texto, cor_fundo, cor_texto) in enumerate(botoes):
            linha = idx // 4
            coluna = idx % 4

            btn = tk.Button(
                frame_botoes,
                text=texto,
                font=("Segoe UI", 20, "bold"),
                fg=cor_texto,
                bg=cor_fundo,
                activeforeground=cor_texto,
                activebackground=self._clarear_cor(cor_fundo),
                border=0,
                cursor="hand2",
                command=lambda t=texto: self._ao_clicar(t)
            )
            btn.grid(row=linha, column=coluna, padx=3, pady=3, sticky="nsew")

            # Efeitos hover
            btn.bind("<Enter>", lambda e, b=btn, c=cor_fundo: b.configure(bg=self._clarear_cor(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=cor_fundo: b.configure(bg=c))

    def _clarear_cor(self, cor_hex):
        """Clareia uma cor hexadecimal."""
        cor = cor_hex.lstrip("#")
        r, g, b = int(cor[:2], 16), int(cor[2:4], 16), int(cor[4:], 16)
        fator = 1.2
        r = min(255, int(r * fator))
        g = min(255, int(g * fator))
        b = min(255, int(b * fator))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _ao_clicar(self, valor):
        """Processa o clique em um botão."""
        if valor == "C":
            self.expressao = ""
            self.resultado_atual = ""
            self.label_expressao.config(text="")
            self.label_resultado.config(text="0")

        elif valor == "⌫":
            self.resultado_atual = self.resultado_atual[:-1]
            if self.resultado_atual == "" or self.resultado_atual == "-":
                self.resultado_atual = ""
                self.label_resultado.config(text="0")
            else:
                self.label_resultado.config(text=self.resultado_atual)

        elif valor == "±":
            if self.resultado_atual and self.resultado_atual != "0":
                if self.resultado_atual.startswith("-"):
                    self.resultado_atual = self.resultado_atual[1:]
                else:
                    self.resultado_atual = "-" + self.resultado_atual
                self.label_resultado.config(text=self.resultado_atual)

        elif valor == "%":
            if self.resultado_atual:
                try:
                    num = float(self.resultado_atual) / 100
                    self.resultado_atual = self._formatar_numero(num)
                    self.label_resultado.config(text=self.resultado_atual)
                except ValueError:
                    pass

        elif valor in "÷×-+":
            if self.resultado_atual:
                self.expressao += self.resultado_atual + " " + valor + " "
                self.label_expressao.config(text=self.expressao)
                self.resultado_atual = ""

        elif valor == "=":
            if self.expressao and self.resultado_atual:
                self.expressao += self.resultado_atual
                self.label_expressao.config(text=self.expressao + " =")
                try:
                    # Converter símbolos para operadores Python
                    expr_calc = self.expressao.replace("÷", "/").replace("×", "*")
                    resultado = eval(expr_calc)
                    self.resultado_atual = self._formatar_numero(resultado)
                    self.label_resultado.config(text=self.resultado_atual)
                    self.expressao = ""
                except ZeroDivisionError:
                    self.label_resultado.config(text="Erro: ÷ por 0")
                    self.expressao = ""
                    self.resultado_atual = ""
                except Exception:
                    self.label_resultado.config(text="Erro")
                    self.expressao = ""
                    self.resultado_atual = ""

        elif valor == ".":
            if "." not in self.resultado_atual:
                if self.resultado_atual == "":
                    self.resultado_atual = "0."
                else:
                    self.resultado_atual += "."
                self.label_resultado.config(text=self.resultado_atual)

        else:  # Números
            if self.resultado_atual == "0":
                self.resultado_atual = valor
            else:
                self.resultado_atual += valor
            self.label_resultado.config(text=self.resultado_atual)

    def _formatar_numero(self, num):
        """Formata o número para exibição."""
        if num == int(num):
            return str(int(num))
        else:
            # Limitar casas decimais e remover zeros à direita
            return f"{num:.10f}".rstrip("0").rstrip(".")

    def executar(self):
        """Inicia o loop principal da aplicação."""
        self.janela.mainloop()


if __name__ == "__main__":
    calc = Calculadora()
    calc.executar()
