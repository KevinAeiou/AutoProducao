import customtkinter as ctk
from modelos.logger import MeuLogger
from strings.minhasStrings import *

ctk.set_default_color_theme('dark-blue')
ctk.set_appearance_mode('dark')
class AplicacaoCRUD(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__loggerCRUD: MeuLogger= MeuLogger(nome= stringCrudLogger)
        self.__confguraTela()

    def configuraComponenteTitulo(self):
        self.title(stringTitulo)

    def configuraComponenteTela(self):
        alturaTelaInteira: int = self.winfo_screenheight()
        larguraTelaInteira: int = self.winfo_screenwidth()
        alturaTela: int = int(0.75 * alturaTelaInteira)
        larguraTela: int = int(0.75 * larguraTelaInteira)
        y: int = 0
        x: int = int((larguraTelaInteira//2)-(larguraTela//4))
        dimencaoTela = f'{larguraTela//2}x{alturaTela}+{x}+{y}'
        self.geometry(dimencaoTela)
        self.resizable(False, False)

    def __confguraTela(self):
        self.configuraComponenteTela()
        self.configuraComponenteTitulo()
        # Criação de um frame para conter o canvas e a scrollbar
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Criação de um canvas com scrollbar horizontal
        canvas = ctk.CTkCanvas(container, highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(container, orientation="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)

        # Empacotando o canvas e a scrollbar
        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        # Criação de um frame interno para colocar os botões
        inner_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Adicionando CTkButton ao frame interno
        for i in range(20):  # Adiciona 20 botões como exemplo
            button = ctk.CTkButton(inner_frame, text=f"Button {i+1}", width=100, height=30)
            button.pack(side="left", padx=5, pady=5)

        # Atualizar a região de rolagem do canvas
        inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    pass