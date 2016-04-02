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

* `postavi_stranske` in `postavi_stranske2` sta metodi namenjeni nastavljanu stranskih figuric, ki sluzijo kot informacija za uporabnika (koliko zetonov se mora postaviti in koliko jih je ze izgubil)
* `nasprotnik` je metoda, ki vrne nasprotnika od igralca, ki je trenutno na potezi
* `zamenjaj_na_potezi` spremeni stanje igre, ter od nasprotnika pricakuje igranje poteze, ter nastavi vse potrebno na plošči
* `klik` metoda ki vrne id polja, na katerega je pritisnil uporabnik, ce je uporabnik pritisnil na katerokoli polje
* `zmagovalno_okno` metoda namenjena generiranju zmagovalnega okna ki se odpre, ko kateri izmed igralcev zmaga, ter ga tako o tem obvesti
* `nova_igra` je metoda ki gledena podane nastavitve o igralcih generira novo igro (uporabljamo jo v metodah `newgame` in `newgamerac` ki sta le bliznici (nekaksni privzeti nastavitvi dveh najpogostejsih opciji)
* `izbira_nove_igre` je metoda, ki odpre novo okno, kjer si uporabnik lahko izbere, s kaksnimi nastavitvami zeli igrati igro
* `ponastavi` metoda namenjena resetiranju vseh nastavitev, za zacetek nove igre
* `izvedi_potezo` je metoda ki prestavi oz postavi polje na igralno plosco odvisno od faze, v kateri se igra nahaja
* `izvedi_posebno_potezo` metoda, ki se obnasa zelo podobno, kot izvedi potezo, le da je namenjena racunalniskemu igralcu
* `vzami_zeton` je metoda, ki se poklice, ko igralec doseze mlin in odstrani figuro iz igralne plošče

### Razred človeškega igralca `Igralec`

Namenjen je temu, da uporabnik lahko z kliki na polje igra igro

* `ponastavi` je metoda ki resetira igrelčevo potezo na nevtralno vrednost, ta metoda se pokliče, ko uporabnik ne izvede veljavne poteze
* `jemljem` metoda preveri, če lahko izbrani žeton odstranimo z igralne plošče, in če je to možno tudi stori
* `uporabnikova_poteza` Metoda ki naredi potezo (preveri njeno veljavnost in naroci igralni plosci da jo zapise v igralno polje ter igro)