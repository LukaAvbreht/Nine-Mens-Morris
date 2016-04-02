# Nine-Mens-Morris

## O programu

Program ob zagonu požene igralno ploščo z privzetimi nastavitvami za igranje človek vs računalnik
V primeru da uporabnik želi igro igrati kako drugace, si le to lahko izbere v meniju o igri z klikom na opcijo `Nova igra`, kjer si izbrene želene nastavitve med ponujenimi.

## Struktura kode

Program je razdeljen v dve datoteki:
* `igra.py`
    * Tu se nahajajo razredi in pa funkcije namenjene logiki in pravilom igre
* `Main.py`
    * Tu se nahaja graficni umesnik in pa razredi razlicnih igralcev, ter racunalnikov algoritem, proti kateremu clovek igra
    
Igra je razdeljena po fazah, V prvi fazi igralca na polje postavljata igralne figurice, v drugi fazi igralca premikata igralne zatone po pločši, zadnja faza je ko je igra konec (ko eden izmed igralcev nemore izvesti veljavne poteze, oz ko enemu izmed igralcev ostaneta le se dva zetona). Obstaja pa tudi umesna faza, ki se zgodi, ko kateri izmed igralcev doseže mlin, ter lahko nasprotniku vzame eno izmed figur
    
## Funkcije in metode na razredih:

### Razred graficnega umesnika `tkmlin`

Namenjen je postavljanju graficnega umesnika glede na izbrane nastavitve za novo igro

* `postavi_stranske(self)` in `postavi_stranske2(self,playerbarva)` sta metodi namenjeni nastavljanu stranskih figuric, ki sluzijo kot informacija za uporabnika (koliko zetonov se mora postaviti in koliko jih je ze izgubil)
* `nasprotnik(self)` je metoda, ki vrne nasprotnika od igralca, ki je trenutno na potezi
* `zamenjaj_na_potezi(self)` spremeni stanje igre, ter od nasprotnika pricakuje igranje poteze, ter nastavi vse potrebno na plošči
* `klik(self,event)` metoda ki vrne id polja, na katerega je pritisnil uporabnik(event), ce je uporabnik pritisnil na katerokoli polje
* `zmagovalno_okno(self,zmagovalec)` metoda namenjena generiranju zmagovalnega okna ki se odpre, ko kateri izmed igralcev zmaga, ter ga tako o tem obvesti
* `nova_igra(self, igralec1, igralec2)` je metoda ki gledena podane nastavitve o igralcih generira novo igro (uporabljamo jo v metodah `newgame` in `newgamerac` ki sta le bliznici (nekaksni privzeti nastavitvi dveh najpogostejsih opciji)
* `izbira_nove_igre(self)` je metoda, ki odpre novo okno, kjer si uporabnik lahko izbere, s kaksnimi nastavitvami zeli igrati igro
* `ponastavi(self)` metoda namenjena resetiranju vseh nastavitev, za zacetek nove igre
* `izvedi_potezo(self, id_1=False, id_2=False)` je metoda ki prestavi oz postavi polje na igralno plosco odvisno od faze, v kateri se igra nahaja (v prvi fazi postavi polje na id_1, v drugi pazi pa premakne figuro iz id_2 na id_1)
* `izvedi_posebno_potezo(self,id_1,id_2=False)` metoda, ki se obnasa zelo podobno, kot izvedi potezo, le da je namenjena racunalniskemu igralcu
* `vzami_zeton(self, id_1)` je metoda, ki se poklice, ko igralec doseze mlin in odstrani figuro iz igralne plošče (figurico z id-jem id_1)

### Razred človeškega igralca `Igralec`

Namenjen je temu, da uporabnik lahko z kliki na polje igra igro

* `ponastavi(self)` je metoda ki resetira igrelčevo potezo na nevtralno vrednost, ta metoda se pokliče, ko uporabnik ne izvede veljavne poteze
* `jemljem(self)` metoda preveri, če lahko izbrani žeton odstranimo z igralne plošče, in če je to možno tudi stori
* `uporabnikova_poteza(self)` Metoda ki naredi potezo (preveri njeno veljavnost in naroci igralni plosci da jo zapise v igralno polje ter igro)

### Razred računalniškega igralca `Racunalnik`

Namenjen je racunalniku, da izvaja poteze po plošči in igra poteze ki jih izracuna v razredu `Alpha_betta`

* `ponastavi(self)` je metoda ki resetira dosedanjo potezo
* `jemljem(self)` in pa `uporabnikova_poteza` sta metodi, ki ju racunalnik ignorira, jih pa rabi zaradi oblike sklicevanja v razredu `tkmlin`
* `igraj_potezo(self)` metoda, ki jo racunalnik izvede ko algoritem izracuna potezo, kar pa preverja vsakih 100ms
* `preveri_potezo(self)` metoda, ki vsakih 100ms preveri ali je algoritem izracunal potezo in jo, ko se to zgodi tudi izvede

### Razred algoritme `Alpha_betta`

Namenjen je izracunu optimalne poteze glede na trenutno stanje igre

* `izracunaj_potezo(self,igra)` je metoda ki pozene algoritem, da le ta zacne racunati optimalno potezo v igri, ki jo igramo
* `vrednost_pozicije(self)` je metoda ki po tem ko `minimax` doseše želeno globino oceni vrednost igralne plošče 
* `minimax(self, globina, maksimiziramo)` metoda, ki "odigra" igro za globina potez naprej, ter nato vrne optimalno potezo, ki jo kasneje racunalnik odigra (ce maksimiziramo iščemo čimolšo potezo za igralca na potezi, cene zanj najslabšo)

### Razred logike igre `Igra`

Namenjen je preverjanu veljavnosti potez in pa sledenju pravilom igre

* `kopija(self)` je metoda ki skopira igro ter jo pripravi, da lahko na njej racunalnik izvaja algoritem ter izracuna optimalno potezo
* `razveljavi(self)` metoda ki razveljavi zadnjo potezo
* `razveljavi_jemanje(self)` metoda ki razveljavi zadnje jemanje
* `kopiraj_plosco(self)` naredi hard-copy nase igralne plošče
* `je_veljavna(self,i, j, a = "PRAZNO", b = "PRAZNO")` metoda preveri, ali je poteza ki jo zelimo izvesti veljavna 
* `postavljen_mlin(self,poteza)` je metoda, ki glede na zadnjo potezo ugotovi, ali je poteza pripeljala do tega da je postavljen nov mlin
* `veljavne_poteze(self)` metoda ki vrne seznam vseh veljavnih potez gledena to kdo je napotezi in v kateri fazi je igra
* `veljavna_jemanja(self)` metoda ki vrne seznam vseh žetonov, ki jih je dovoljeno pojesti
* `lahko_jemljem(self, i, j)` metoda preveri, ali lahko izbrani zeton vzamemo
* `poteza(self, i, j, a="PRAZNO", b="PRAZNO")` metoda ki izvede potezo iz poja (a,b) na polje (i,j), oz le postavi figuro na polje (i,j) (odvisno od faze igre)
* `odstrani_figurico(self, i, j)` metoda ki odstrani nasprotnikovo figuricao na koordinatah (i,j) ce je to dovoljeno