__author__ = 'LukaAvbreht, SamoKralj'

IGRALEC_BELI = "B"
IGRALEC_CRNI = "C"

def nasprotnik(igralec):
    """ Pove nasprotnega igralca. Koristno pri metodi poteza. """
    if igralec == IGRALEC_BELI:
        return IGRALEC_CRNI
    else:
        return IGRALEC_BELI


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
        self.zadnja_poteza = None  #to pomoje ne rabimo

        self.figurice = {IGRALEC_BELI: 0 , IGRALEC_CRNI: 0}
        #bi sproti spremljali koliko ima kdo figuric in v primeru, da je vrednost 2, 3 naredimo svoje
        #nam ni treba po vsaki potezi steti koliko ima kdo figuric

        self.faza = 0

        self.postavljenih = 0 #števec ki steje koliko figur je ze bilo postavljenih

        # self.faza = 0  --> Faza postavljanja figuric
        # self.faza = 1  --> Faza premikanja figuric
        
        self.zgodovina = []
        #Predlagam obliko: (pozicija, zadnja poteza, True - False, Pobrana figurica)
        #kjer True, False pove ali je bil vzpostavljen mlin in nato katera figurica je bil vzeta
        #bi po vsaki potezi belega in črnega shranili pozicijo?

    def izpisi_plosco(self):  #to je funkcija namenjena programerju
        """ Izpise trenutno ploščo na lep način. Vsako vrstico posebej."""
        for vrstica in self.plosca:
            print(vrstica)

    def je_veljavna(self, i, j):
        """Preveri, če je polje prazno"""
        return self.plosca[i][j] == None

    def postavljen_mlin(self, poteza):
        """Glede na zadnjo potezo ugotovi ali je bil to potezo postavljen mlin. Vrne True ali False"""
        kombinacije = [
            #Vodoravne
            [(0,0),(0,3),(0,6)],
            [(6,0),(6,3),(6,6)],
            [(1,1),(1,3),(1,5)],
            [(5,1),(5,3),(5,5)],
            [(2,2),(2,3),(2,4)],
            [(4,2),(4,3),(4,4)],
            [(3,0),(3,1),(3,2)],
            [(3,4),(3,5),(3,6)],
            #Navpične
            [(0,0),(3,0),(6,0)],
            [(0,6),(3,6),(6,6)],
            [(1,1),(3,1),(5,1)],
            [(1,5),(3,5),(5,5)],
            [(2,2),(3,2),(4,2)],
            [(2,4),(3,4),(4,4)],
            [(0,0),(0,3),(0,6)],
            [(0,3),(1,3),(2,6)],
            [(4,3),(5,3),(6,3)]]
        for trojka in kombinacije: #poteza oblike (i,j)
            if poteza in trojka:
                trojica = []
                for polje in trojka:
                    trojica.append(self.plosca[polje[0]][polje[1]])
                if trojica == [IGRALEC_BELI, IGRALEC_BELI, IGRALEC_BELI] or trojica == [IGRALEC_CRNI, IGRALEC_CRNI, IGRALEC_CRNI]:
                    return True
        return False

    def veljavne_poteze(self):
        """ Glede na trenutno fazo vrne mogoče možne poteze. """
        if self.faza == 0:
            mozne_poteze = []
            for i in range(7):
                for j in range(7):
                    if self.je_veljavna(i,j):
                        mozne_poteze.append((i,j))
            return mozne_poteze

        #faza premikanja figuric
        #odvisno od tega kdo je na potezi in koliko figuric še ima
        else:
            pass

    def poteza(self, i, j):  #poteza od kod kam + nekaksen sistem da lahko postaviva nov kamen (za prvih 18 potez)
        """Izvede potezo. """
        if self.je_veljavna(i,j):
            self.plosca[i][j] = self.na_potezi
            self.zadnja_poteza = (i,j)
            if self.postavljen_mlin((i,j)):
                self.odstrani_figurico()
            self.na_potezi = nasprotnik(self.na_potezi)
        else:
            print("Poteza ni mogoča")

    def odstrani_figurico(self):
        """Odstrani nasprotnikovo figurico v primeru da jo je veljavno odstraniti"""
        i = input('Prva koordinata: ')
        j = input('Druga koordinata: ')
        i = int(i)
        j = int(j)
        trenutni_nasprotnik = nasprotnik(self.na_potezi)
        if self.plosca[i][j] == trenutni_nasprotnik:
            if self.postavljen_mlin((i,j)):
                print("Ta figurica je del aktivnega mlina")
            else:
                self.plosca[i][j] = None
                self.figurice[trenutni_nasprotnik] -=1
                self.zmaga1()
        else:
            self.odstrani_figurico()

    def zmaga1(self):
        """ preveri, ali smo z mlinom nasprotniku odstranili sedmo figuro"""
        if self.faza == 1:
            if self.figurice[nasprotnik(self.na_potezi)] < 3:
                return True
        else:
            return False
