__author__ = 'LukaAvbreht,SamoKralj'
from tkinter import *
from igra import *

class tkmlin:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=900, height=700)

        self.igra = Igra()

        #tuki si bos lahko zbiru kako barva tvoja polja
        self.barva1 = 'Black'
        self.barva2 = 'White'

        #Igralna plosca
        plosca = Canvas(master, width=700, height=700, bg='LemonChiffon')
        plosca.grid(row=0, column=0, rowspan=7, columnspan=7, sticky=N+S+E+W)

        #crte za igralno plosco
        plosca.create_line(50, 50, 650, 50)
        plosca.create_line(50, 650, 650, 650)
        plosca.create_line(50, 50, 50, 650)
        plosca.create_line(650, 50, 650, 650)

        plosca.create_line(150, 150, 550, 150)
        plosca.create_line(550, 150, 550, 550)
        plosca.create_line(150, 150, 150, 550)
        plosca.create_line(150, 550, 550, 550)

        plosca.create_line(250, 250, 450, 250)
        plosca.create_line(450, 250, 450, 450)
        plosca.create_line(250, 250, 250, 450)
        plosca.create_line(250, 450, 450, 450)

        plosca.create_line(350, 50, 350, 250)
        plosca.create_line(350, 450, 350, 650)
        plosca.create_line(50, 350, 250, 350)
        plosca.create_line(450, 350, 650, 350)

        #Gumpki namenjeni za igro
        gumb0_0 = self.naredi_figurico(plosca, 50, 50)
        gumb0_3 = self.naredi_figurico(plosca, 350, 50)
        gumb0_6 = self.naredi_figurico(plosca, 650, 50)
        gumb1_1 = self.naredi_figurico(plosca, 150, 150)
        gumb1_3 = self.naredi_figurico(plosca, 350, 150)
        gumb1_5 = self.naredi_figurico(plosca, 550, 150)
        gumb2_2 = self.naredi_figurico(plosca, 250, 250)
        gumb2_3 = self.naredi_figurico(plosca, 350, 250)
        gumb2_4 = self.naredi_figurico(plosca, 450, 250)
        gumb3_0 = self.naredi_figurico(plosca, 50, 350)
        gumb3_1 = self.naredi_figurico(plosca, 150, 350)
        gumb3_2 = self.naredi_figurico(plosca, 250, 350)
        gumb3_4 = self.naredi_figurico(plosca, 450, 350)
        gumb3_5 = self.naredi_figurico(plosca, 550, 350)
        gumb3_6 = self.naredi_figurico(plosca, 650, 350)
        gumb4_2 = self.naredi_figurico(plosca, 250, 450)
        gumb4_3 = self.naredi_figurico(plosca, 350, 450)
        gumb4_4 = self.naredi_figurico(plosca, 450, 450)
        gumb5_1 = self.naredi_figurico(plosca, 150, 550)
        gumb5_3 = self.naredi_figurico(plosca, 350, 550)
        gumb5_5 = self.naredi_figurico(plosca, 550, 550)
        gumb6_0 = self.naredi_figurico(plosca, 50, 650)
        gumb6_3 = self.naredi_figurico(plosca, 350, 650)
        gumb6_6 = self.naredi_figurico(plosca, 650, 650)

        self.matrikagumbov = [[gumb0_0," "," ",gumb0_3," "," ",gumb0_6],
                             [" ",gumb1_1," ",gumb1_3," ",gumb1_5," "],
                             [" "," ",gumb2_2,gumb2_3,gumb2_4," "," "],
                             [gumb3_0,gumb3_1,gumb3_2," ",gumb3_4,gumb3_5,gumb3_6],
                             [" "," ",gumb4_2,gumb4_3,gumb4_4," "," "],
                             [" ",gumb5_1," ",gumb5_3," ",gumb5_5," "],
                             [gumb6_0," "," ",gumb6_3," "," ",gumb6_6]]

        #generira gumbe ki niso povezani z igro
        gumb_novaigra = Button(master, text="Nova igra", command= self.newgame)
        gumb_novaigra.grid(row=0, column=9, columnspan=3)

    def newgame(self):
        return "to do"

    def naredi_figurico(self, kam, i, j, barva='Grey'): #none naredi neutralno polje
        x = kam.create_oval(i-25, j-25, i+25, j+25)
        print(x)

    def klik0(self): #ni smiselno
        i = event.x // 50
        j = event.y // 50
        if self.igra.na_potezi == IGRALEC_BELI:
            self.naredi_figurico(plosca, i, j, self.barva2)
        else:
            self.naredi_figurico(plosca, i, j, self.barva1)

    def klik1(self): # prav tako ni smiselno
        a = event.x // 50
        b = event.y // 50

    def poteza(self, i, j, a=False, b=False): #najprej pogleda v keri fazi smo, pol pa nardi v odvisnosti od tega potezo
        # ce smo v fazi 0 potem je prvi klik le postavljanje kamncka
        # ce smo v drugi fazi usaka poteza zahteva 2 klika
        if self.igra.faza == 0:
            self.klik0
        elif self.igra.faza == 1:
            self.klik1

    def zacni_igro(self, IGRALEC_BELI, IGRALEC_CRNI):
        self.igra = Igra()
        self.igralec_beli = IGRALEC_BELI
        self.igralec_crni = IGRALEC_CRNI

class Igralec():
    """cloveski igralec"""
    def __init__(self, tkmlin):
        self.gui = tkmlin

    def igraj(self):
        pass

if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Men\'s Morris')
    okno = tkmlin(root)
    root.mainloop()