#!/usr/bin/env python3
"""
Calculadora com Interface Gráfica
Suporta as 4 operações básicas: +, -, ×, ÷
Compatível com macOS, Windows e Linux
"""

import tkinter as tk
from tkinter import ttk
import sys


class Calculadora:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Calculadora")
        self.janela.geometry("320x480")
        self.janela.resizable(False, False)

        # Cores do tema
        self.cor_fundo = "#2D2D2D"
        self.cor_display = "#1E1E1E"

        self.janela.configure(bg=self.cor_fundo)

        # Detectar sistema operacional para fonte apropriada
        if sys.platform == "darwin":  # macOS
            self.fonte_familia = "SF Pro Display"
            self.fonte_fallback = "Helvetica Neue"
        elif sys.platform == "win32":  # Windows
            self.fonte_familia = "Segoe UI"
            self.fonte_fallback = "Arial"
        else:  # Linux
            self.fonte_familia = "Ubuntu"
            self.fonte_fallback = "DejaVu Sans"

        self.expressao = ""
        self.resultado_atual = ""

        self._criar_display()
        self._criar_botoes()

    def _obter_fonte(self, tamanho, peso="normal"):
        """Retorna fonte compatível com o sistema."""
        return (self.fonte_familia, tamanho, peso)

    def _criar_display(self):
        """Cria o display da calculadora."""
        frame_display = tk.Frame(self.janela, bg=self.cor_display, height=130)
        frame_display.pack(fill=tk.X, padx=8, pady=(15, 8))
        frame_display.pack_propagate(False)

        # Expressão (texto menor em cima)
        self.label_expressao = tk.Label(
            frame_display,
            text="",
            font=self._obter_fonte(14),
            fg="#888888",
            bg=self.cor_display,
            anchor="e"
        )
        self.label_expressao.pack(fill=tk.X, padx=10, pady=(10, 0))

        # Resultado (texto grande)
        self.label_resultado = tk.Label(
            frame_display,
            text="0",
            font=self._obter_fonte(40, "bold"),
            fg="#FFFFFF",
            bg=self.cor_display,
            anchor="e"
        )
        self.label_resultado.pack(fill=tk.X, padx=10, pady=(5, 10))

    def _criar_botao(self, parent, texto, cor_fundo, cor_texto, linha, coluna):
        """Cria um botão estilizado."""
        # Frame para dar efeito de borda arredondada
        frame = tk.Frame(parent, bg=self.cor_fundo)
        frame.grid(row=linha, column=coluna, padx=4, pady=4, sticky="nsew")

        btn = tk.Button(
            frame,
            text=texto,
            font=self._obter_fonte(18, "bold"),
            fg=cor_texto,
            bg=cor_fundo,
            activeforeground=cor_texto,
            activebackground=self._clarear_cor(cor_fundo),
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=lambda t=texto: self._ao_clicar(t)
        )
        btn.pack(fill=tk.BOTH, expand=True)

        # Efeitos hover
        btn.bind("<Enter>", lambda e, b=btn, c=cor_fundo: b.configure(bg=self._clarear_cor(c)))
        btn.bind("<Leave>", lambda e, b=btn, c=cor_fundo: b.configure(bg=c))

        return btn

    def _criar_botoes(self):
        """Cria os botões da calculadora."""
        frame_botoes = tk.Frame(self.janela, bg=self.cor_fundo)
        frame_botoes.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 8))

        # Layout dos botões: (texto, cor_fundo, cor_texto)
        botoes = [
            ("C", "#FF6B6B", "#FFFFFF"),
            ("+/-", "#505050", "#FFFFFF"),
            ("%", "#505050", "#FFFFFF"),
            ("/", "#FF9F43", "#FFFFFF"),
            ("7", "#3D3D3D", "#FFFFFF"),
            ("8", "#3D3D3D", "#FFFFFF"),
            ("9", "#3D3D3D", "#FFFFFF"),
            ("x", "#FF9F43", "#FFFFFF"),
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
            ("DEL", "#505050", "#FFFFFF"),
            ("=", "#4ECB71", "#FFFFFF"),
        ]

        # Configurar grid com peso igual
        for i in range(5):
            frame_botoes.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            frame_botoes.grid_columnconfigure(i, weight=1, uniform="col")

        # Criar botões
        for idx, (texto, cor_fundo, cor_texto) in enumerate(botoes):
            linha = idx // 4
            coluna = idx % 4
            self._criar_botao(frame_botoes, texto, cor_fundo, cor_texto, linha, coluna)

    def _clarear_cor(self, cor_hex):
        """Clareia uma cor hexadecimal para efeito hover."""
        cor = cor_hex.lstrip("#")
        r, g, b = int(cor[:2], 16), int(cor[2:4], 16), int(cor[4:], 16)
        fator = 1.25
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

        elif valor == "DEL":
            self.resultado_atual = self.resultado_atual[:-1]
            if self.resultado_atual == "" or self.resultado_atual == "-":
                self.resultado_atual = ""
                self.label_resultado.config(text="0")
            else:
                self.label_resultado.config(text=self.resultado_atual)

        elif valor == "+/-":
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

        elif valor in "/x-+":
            if self.resultado_atual:
                simbolo_display = valor if valor != "x" else "x"
                self.expressao += self.resultado_atual + " " + simbolo_display + " "
                self.label_expressao.config(text=self.expressao)
                self.resultado_atual = ""

        elif valor == "=":
            if self.expressao and self.resultado_atual:
                self.expressao += self.resultado_atual
                self.label_expressao.config(text=self.expressao + " =")
                try:
                    # Converter símbolos para operadores Python
                    expr_calc = self.expressao.replace("x", "*")
                    resultado = eval(expr_calc)
                    self.resultado_atual = self._formatar_numero(resultado)
                    self.label_resultado.config(text=self.resultado_atual)
                    self.expressao = ""
                except ZeroDivisionError:
                    self.label_resultado.config(text="Erro")
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
            return f"{num:.10f}".rstrip("0").rstrip(".")

    def executar(self):
        """Inicia o loop principal da aplicação."""
        self.janela.mainloop()


if __name__ == "__main__":
    calc = Calculadora()
    calc.executar()
