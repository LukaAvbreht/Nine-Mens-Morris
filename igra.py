__author__ = 'LukaAvbreht, SamoKralj'
import logging

IGRALEC_ENA = "B"
IGRALEC_DVA = "C"

def nasprotnik(igralec):
    """ Pove nasprotnega igralca. Koristno pri metodi poteza. """
    if igralec == IGRALEC_ENA:
        return IGRALEC_DVA
    else:
        return IGRALEC_ENA


class Igra():
    """Program namenjen logiki in pravilom igre"""

    def __init__(self):  #remove nepotrebna polja
        self.plosca =[[None," "," ",None," "," ",None],
                      [" ",None," ",None," ",None," "],
                      [" "," ",None,None,None," "," "],
                      [None,None,None," ",None,None,None],
                      [" "," ",None,None,None," "," "],
                      [" ",None," ",None," ",None," "],
                      [None," "," ",None," "," ",None]]
        #None polja so prosta polja, " " so samo fillerji.
        self.na_potezi = IGRALEC_ENA

        self.figurice = {IGRALEC_ENA: 0 , IGRALEC_DVA: 0}
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

        self.stanje = ("V TEKU", None)
        #moznosti tega stanja so : ni konec, zmaga

        self.mlin = False #pove ali smo postavili mlin

        self.sosedi = {(0,0) : [(0,3),(3,0)],
                  (0,3) : [(0,0),(0,6),(1,3)],
                  (0,6) : [(0,3),(3,6)],
                  (1,1) : [(1,3),(3,1)],
                  (1,3) : [(1,1),(1,5),(2,3),(0,3)],
                  (1,5) : [(1,3),(3,5)],
                  (2,2) : [(2,3),(3,2)],
                  (2,3) : [(2,2),(2,4),(1,3)],
                  (2,4) : [(2,3),(3,4)],
                  (3,0) : [(0,0),(6,0),(3,1)],
                  (3,1) : [(3,0),(3,2),(1,1),(5,1)],
                  (3,2) : [(3,1),(2,2),(4,2)],
                  (3,4) : [(2,4),(4,4),(3,5)],
                  (3,5) : [(3,4),(3,6),(1,5),(5,5)],
                  (3,6) : [(0,6),(6,6),(3,5)],
                  (4,2) : [(3,2),(4,3)],
                  (4,3) : [(4,2),(4,4),(5,3)],
                  (4,4) : [(4,3),(3,4)],
                  (5,1) : [(5,3),(3,1)],
                  (5,3) : [(5,1),(5,5),(4,3),(6,3)],
                  (5,5) : [(5,3),(3,5)],
                  (6,0) : [(3,0),(6,3)],
                  (6,3) : [(6,0),(6,6),(5,3)],
                  (6,6) : [(6,3),(3,6)],
                  }

    def kopiraj_plosco(self):
        novaplosca = []
        for vrstica in self.plosca:
            novaplosca.append(vrstica[:])
        return novaplosca

    def izpisi_plosco(self):  #to je funkcija namenjena programerju
        """ Izpise trenutno ploščo na lep način. Vsako vrstico posebej."""
        for vrstica in self.plosca:
            print(vrstica)

    def je_veljavna(self, i, j, a = False, b = False):
        """Preveri, če je poteza veljavna.poteza na (i,j) iz (a,b)"""
        if self.faza == 0:
            return self.plosca[i][j] == None
        else:
            if self.plosca[i][j] == None and self.plosca[a][b] == self.na_potezi:
                if self.figurice[self.na_potezi] == 3:
                    return True
                else:
                    return (i,j) in self.sosedi[(a,b)]
            else:
                return False

    def postavljen_mlin(self, poteza, pomni, a = False, b = False): #pomni doloci ali potezo namisljeno igramo ali ne
        """Glede na zadnjo potezo ugotovi ali je bil to potezo postavljen mlin. Vrne True ali False."""
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
            [(0,3),(1,3),(2,3)],
            [(4,3),(5,3),(6,3)]]
        if pomni:
            shrani1 = self.plosca[poteza[0]][poteza[1]]
            self.plosca[poteza[0]][poteza[1]] = self.na_potezi
            shrani2 = self.plosca[a][b]
            self.plosca[a][b] = None
            for trojka in kombinacije: #poteza oblike (i,j)
                if poteza in trojka:
                    trojica = []
                    for polje in trojka:
                        trojica.append(self.plosca[polje[0]][polje[1]])
                    if trojica == [IGRALEC_ENA, IGRALEC_ENA, IGRALEC_ENA] or trojica == [IGRALEC_DVA, IGRALEC_DVA, IGRALEC_DVA]:
                        self.plosca[poteza[0]][poteza[1]] = shrani1
                        self.plosca[a][b] = shrani2
                        return True
            self.plosca[poteza[0]][poteza[1]] = shrani1
            self.plosca[a][b] = shrani2
            return False
        else:
            for trojka in kombinacije: #poteza oblike (i,j)
                if poteza in trojka:
                    trojica = []
                    for polje in trojka:
                        trojica.append(self.plosca[polje[0]][polje[1]])
                    if trojica == [IGRALEC_ENA, IGRALEC_ENA, IGRALEC_ENA] or trojica == [IGRALEC_DVA, IGRALEC_DVA, IGRALEC_DVA]:
                        return True
            return False

    def veljavne_poteze(self):
        """ Glede na trenutno fazo vrne mogoče možne poteze. """
        if self.faza == 0:  #trenba preverit ce si naredu mlin in smiselno dodati to v potezo
                            # Za potezo bi preverila le ce je mogoca, ce jemljes bi to stela kot svojo potezo
            mozne_poteze = []
            for i in range(7):
                for j in range(7):
                    if self.je_veljavna(i,j):
                        mozne_poteze.append((i,j,False,False))
            return mozne_poteze
        elif self.faza == 1 and self.figurice[self.na_potezi] > 3:
            mozne_poteze = []
            for i in range(7):
                for j in range(7):
                    if self.plosca[i][j] == self.na_potezi:
                        for sos in self.sosedi[(i,j)]:
                            if self.plosca[sos[0]][sos[1]] == None:
                                dod = (sos[0],sos[1],i,j)
                                mozne_poteze.append(dod)
            return mozne_poteze
        else: #v primeru, da lahko letimo
            mozne_poteze = []
            prosta_polja = []
            #poiscemo vsa prosta polja
            for i in range(7):
                for j in range(7):
                    if self.plosca[i][j] == None:
                        prosta_polja.append((i,j))
            #poiscemo vse 3 nase zetone in jih povezemo s prostimi polji
            for i in range(7):
                for j in range(7):
                    if self.plosca[i][j] == self.na_potezi:
                        for (prva,druga) in prosta_polja:
                            poteza = (prva, druga, i, j)
                            mozne_poteze.append(poteza)
            return mozne_poteze

    def veljavna_jemanja(self):
        """Funkcija vrne vse žetone, ki jih lahko pojemo. """
        lahko_vzamemo = [] #zetoni, ki jih lahko jemljemo
        vsi_naspr_zetoni = [] #vsi zetoni
        for i in range(7):
            for j in range(7):
                if self.plosca[i][j] == nasprotnik(self.na_potezi):
                    vsi_naspr_zetoni.append((i, j))
                    if self.postavljen_mlin((i, j), False) == False: #preverimo, ce je v mlinu
                        lahko_vzamemo.append((i, j))
        if len(lahko_vzamemo) == 0: #če zetonov ni ali so vsi zetoni v mlinu,
                                    #lahko vzamemo karkoli. Situacija ko zetonov ni
                                    #je seveda trivialna in ni mogoča.
            return vsi_naspr_zetoni
        else: #drugače vrnemo vse, ki jih lahko jemljemo!
            return lahko_vzamemo
                                            
    def lahko_jemljem(self, i, j):
        """Funkcija pove, ali izbrani zeton lahko pojemo."""
        return (i, j) in self.veljavna_jemanja()

    def poteza(self, i, j, a=False, b=False):  #poteza od kod kam + nekaksen sistem da lahko postaviva nov kamen (za prvih 18 potez)
        """Izvede potezo. kam (i,j) od kje (a,b). """
        if self.faza == 0:
            if self.je_veljavna(i,j):
                self.figurice[self.na_potezi] +=1
                self.postavljenih += 1
                if self.postavljenih >= 18: #V primeru, da je konec faze postavljanja
                    self.faza = 1
                self.plosca[i][j] = self.na_potezi
                if self.postavljen_mlin((i,j), False):
                    self.mlin = True
                else:
                    self.na_potezi = nasprotnik(self.na_potezi)
                    if len(self.veljavne_poteze()) == 0:
                        if self.na_potezi == IGRALEC_ENA:
                            self.stanje = ("ZMAGA", IGRALEC_DVA)
                        else:
                            self.stanje = ("ZMAGA", IGRALEC_ENA)
            else:
                print("Poteza ni mogoča",self.na_potezi,i,j)
        else:
            if self.plosca[a][b] == self.na_potezi: #preveri da premikas svojo figurico
                if self.je_veljavna(i, j, a, b):  #preveri ali lahko tja premaknes svojo figurico (napisati je potrebno se da
                    # je mozno prestaviti figurico le na sosednja polja
                    self.plosca[a][b] = None
                    self.plosca[i][j] = self.na_potezi
                    if self.postavljen_mlin((i,j), False):
                        self.mlin = True
                    else:
                        self.na_potezi = nasprotnik(self.na_potezi)
                        if len(self.veljavne_poteze()) == 0:
                            if self.na_potezi == IGRALEC_ENA:
                                self.stanje = ("ZMAGA", IGRALEC_DVA)
                            else:
                                self.stanje = ("ZMAGA", IGRALEC_ENA)
                else:
                    print('Poteza iz ' + str((a,b)) + ' na polje ' + str((i,j)) + ' ni mogoča!' )
            else:
                print('tole pa ni tvoja figurica, Izberi svojo figuro',self.na_potezi,i,j)



    def odstrani_figurico(self, i, j):
        """Odstrani nasprotnikovo figurico v primeru da jo je veljavno odstraniti."""
        if self.lahko_jemljem(i,j):
            polje = self.plosca[i][j]
            self.figurice[polje] -= 1
            self.plosca[i][j] = None
            self.na_potezi = nasprotnik(self.na_potezi)
            self.mlin = False
            if self.faza != 0:
                if self.figurice[self.na_potezi] < 3 or len(self.veljavne_poteze()) == 0:
                    if self.na_potezi == IGRALEC_ENA:
                        self.stanje = ("ZMAGA", IGRALEC_DVA)
                    else:
                        self.stanje = ("ZMAGA", IGRALEC_ENA)

