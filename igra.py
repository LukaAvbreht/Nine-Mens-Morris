__author__ = 'LukaAvbreht, SamoKralj'

IGRALEC_BELI = "B"
IGRALEC_CRNI = "C"


class Igra():
    """Program namenjen logiki in pravilom igre"""

    def __init__(self):
        self.plosca =[[None," "," ",None," "," ",None],
                      [" ",None," ",None," ",None," "],
                      [" "," ",None,None,None," "," "],
                      [None,None,None," ",None,None,None],
                      [" "," ",None,None,None," "," "],
                      [" ",None," ",None," ",None," "],
                      [None," "," ",None," "," ",None]]
        #None polja so prosta polja, " " so samo fillerji.
        self.na_potezi = IGRALEC_BELI
        
        self.belih_figuric = 0
        self.crnih_figuric = 0
        #bi sproti spremljali koliko ima kdo figuric in v primeru, da je vrednost 2, 3 naredimo svoje
        #nam ni treba po vsaki potezi steti koliko ima kdo figuric
        self.zgodovina = []
        #Predlagam obliko: (pozicija, zadnja poteza, True - False, Pobrana figurica)
        #kjer True, False pove ali je bil vzpostavljen mlin in nato katera figurica je bil vzeta
        #bi po vsaki potezi belega in črnega shranili pozicijo?

        def je_veljavna(self, i, j):
            return self.plosca[i][j] == None:

        def postavljen_mlin(self, poteza):
            
                
        
