# Nine-Mens-Morris

## O programu

Program ob zagonu požene igralno ploščo z privzetimi nastavitvami za igranje človek vs računalnik
V primeru da uporabnik želi igro igrati kako drugace, si le to lahko izbere v meniju o igri z klikom na opcijo `Nova igra`, kjer si izbrene želene nastavitve med ponujenimi.

## Struktura kode

Program je razdeljen v dve datoteki:
* `igra.py`
    ** Tu se nahajajo razredi in pa funkcije namenjene logiki in pravilom igre
* `Main.py`
    ** Tu se nahaja graficni umesnik in pa razredi razlicnih igralcev, ter racunalnikov algoritem, proti kateremu clovek igra
    
## Funkcije in metode na razredih:

### Razred graficnega umesnika `tkmlin`

Namenjen je postavljanju graficnega umesnika glede na izbrane nastavitve za novo igro

* `postavi_stranske` in `postavi_stranske2` sta metodi namenjeni nastavljanu stranskih figuric, ki sluzijo kot informacija za uporabnika (koliko zetonov se mora postaviti in koliko jih je ze izgubil)

