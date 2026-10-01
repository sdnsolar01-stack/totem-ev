import tkinter as tk
from PIL import Image, ImageTk
import os

LARGURA_ECRA = 1080
ALTURA_ECRA = 900
IMAGEM_INICIAL = "tela1_inicio.jpg"
IMAGEM_SEGUNDA = "tela2_valores.jpg"
IMAGEM_PAGAMENTO = "tela3_pagamento.jpg"
IMAGEM_CARREGANDO = "tela4_carregando.jpg"

class TotemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SDN EV - Totem")
        self.root.geometry("1080x900")
        self.root.configure(bg="black")

        if not os.path.exists(IMAGEM_INICIAL):
            print(f"ERRO: A imagem '{IMAGEM_INICIAL}' não foi encontrada!")
            self.root.destroy()
            return

        self.canvas = tk.Canvas(root, width=LARGURA_ECRA, height=ALTURA_ECRA, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.timer_id = None
        self.mostrar_tela_1()

    def cancelar_timers(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def mostrar_tela_1(self):
        self.cancelar_timers()
        img_pil = Image.open(IMAGEM_INICIAL).resize((LARGURA_ECRA, ALTURA_ECRA), Image.Resampling.LANCZOS)
        self.img1 = ImageTk.PhotoImage(img_pil)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img1, anchor="nw")
        
        # Botão invisível da setinha (Passo 4)
        self.canvas.create_rectangle(800, 370, 1010, 520, outline="", tags="btn_passo4")
        self.canvas.tag_bind("btn_passo4", "<Button-1>", self.mostrar_tela_2)

    def mostrar_tela_2(self, event):
        print("Avançou para a Tela 2: Seleção de Valores")
        
        if not os.path.exists(IMAGEM_SEGUNDA):
            print(f"AVISO: Coloca a imagem '{IMAGEM_SEGUNDA}' na pasta!")
            self.root.destroy()
            return

        img_pil2 = Image.open(IMAGEM_SEGUNDA).resize((LARGURA_ECRA, ALTURA_ECRA), Image.Resampling.LANCZOS)
        self.img2 = ImageTk.PhotoImage(img_pil2)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img2, anchor="nw")
        
        # Áreas clicáveis dos valores calibradas
        self.canvas.create_rectangle(40, 370, 1040, 465, outline="", tags="val_20")
        self.canvas.tag_bind("val_20", "<Button-1>", lambda e: self.selecionar_valor(20))

        self.canvas.create_rectangle(40, 475, 1040, 570, outline="", tags="val_30")
        self.canvas.tag_bind("val_30", "<Button-1>", lambda e: self.selecionar_valor(30))

        self.canvas.create_rectangle(40, 565, 1040, 645, outline="", tags="val_40")
        self.canvas.tag_bind("val_40", "<Button-1>", lambda e: self.selecionar_valor(40))

        self.canvas.create_rectangle(40, 646, 1040, 790, outline="", tags="val_50")
        self.canvas.tag_bind("val_50", "<Button-1>", lambda e: self.selecionar_valor(50))

    def selecionar_valor(self, valor):
        print(f"Recarga selecionada: R$ {valor},00. A carregar Tela de Pagamento...")
        self.mostrar_tela_pagamento(valor)

    def mostrar_tela_pagamento(self, valor):
        if not os.path.exists(IMAGEM_PAGAMENTO):
            print(f"AVISO: A imagem '{IMAGEM_PAGAMENTO}' não foi encontrada na pasta!")
            self.root.destroy()
            return

        img_pil3 = Image.open(IMAGEM_PAGAMENTO).resize((LARGURA_ECRA, ALTURA_ECRA), Image.Resampling.LANCZOS)
        self.img3 = ImageTk.PhotoImage(img_pil3)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img3, anchor="nw")
        
        # Texto verde futurista com o valor selecionado
        self.canvas.create_text(
            LARGURA_ECRA / 2, 150, 
            text=f"VALOR SELECIONADO: R$ {valor},00", 
            fill="#00FF66", 
            font=("Consolas", 26, "bold")
        )
        print(f"Pagamento em aberto para R$ {valor},00. A aguardar 5 segundos...")

        # Aguardar 5 segundos e avançar para a carga
        self.timer_id = self.root.after(5000, self.iniciar_carregamento)

    def iniciar_carregamento(self):
        if not os.path.exists(IMAGEM_CARREGANDO):
            print(f"AVISO: A imagem '{IMAGEM_CARREGANDO}' não foi encontrada na pasta!")
            self.root.destroy()
            return

        img_pil4 = Image.open(IMAGEM_CARREGANDO).resize((LARGURA_ECRA, ALTURA_ECRA), Image.Resampling.LANCZOS)
        self.img4 = ImageTk.PhotoImage(img_pil4)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img4, anchor="nw")
        
        # Variáveis da simulação de contagem
        self.kWh_atual = 0.0
        self.tempo_atual = 0
        self.porcentagem_atual = 0

        # Criar os textos dinâmicos em cima dos gráficos da imagem
        # 1. Energia Entregue (kWh) - canto inferior esquerdo
        self.txt_kwh = self.canvas.create_text(
            175, 745, text="0,00 kWh", fill="white", font=("Consolas", 24, "bold")
        )
        # 2. Tempo de Carregamento (min) - centro inferior
        self.txt_tempo = self.canvas.create_text(
            495, 745, text="0 min", fill="white", font=("Consolas", 24, "bold")
        )
        # 3. Percentagem (%) - BEM SUBIDA (de 685 para 450, puxada totalmente para cima)
        self.txt_porc = self.canvas.create_text(
            845, 450, text="0%", fill="white", font=("Consolas", 22, "bold")
        )

        print("Início da Carga: A simulação de números começou!")
        self.atualizar_simulacao()

    def atualizar_simulacao(self):
        self.kWh_atual += 1.84
        self.tempo_atual += 3
        self.porcentagem_atual += 7

        if self.porcentagem_atual >= 100:
            self.porcentagem_atual = 100
            self.kWh_atual = 18.40
            self.tempo_atual = 32

        self.canvas.itemconfig(self.txt_kwh, text=f"{self.kWh_atual:.2f} kWh".replace('.', ','))
        self.canvas.itemconfig(self.txt_tempo, text=f"{self.tempo_atual} min")
        self.canvas.itemconfig(self.txt_porc, text=f"{self.porcentagem_atual}%")

        if self.porcentagem_atual >= 100:
            print("Carga concluída a 100%! A reiniciar...")
            self.timer_id = self.root.after(4000, self.mostrar_tela_1)
        else:
            self.timer_id = self.root.after(1000, self.atualizar_simulacao)

if __name__ == "__main__":
    root = tk.Tk()
    app = TotemApp(root)
    root.mainloop()