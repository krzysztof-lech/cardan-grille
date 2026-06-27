"""
Szyfr „grilla Kardano”, n – nieparzyste.

Aby uniknąć sytuacji, że w momencie obrotu karty trafimy na miejsce, które jest już wypełnione podzieliłem kartę
na ćwiartki i przy kolejnych obrotach pierwsza ćwiartka przechodzi na drugą, potem na trzecią i na czwartą ćwiartkę.
Jest jedna ćwiartka podstawowa i losowane są z niej elementy, które powinny trafić do innych ćwiartek.
Tak żeby jak uzyskamy ostatecznie tą kartę to żeby te puste miejsca w karcie były po całej karcie.
Ten algorytm jak rozmieści te puste miejsca w tej karcie to następnie przyporządkowuje nową pozycję dla liter
i te nowe pozycje tworzą klucz.
Tak że w przypadku karty 5na5 uzyskujemy klucz o długości 25 elementów.

Została wykorzystana funkcja atakPop. Funkcja ta najpierw tworzy losową populacje kart. Dla każdej karty jest obliczany score
Karty są sortowane tak aby najlepsze karty były na początku. Następnie karty z najgorszym scorem są usuwane z populacji.
Później z najlepszych kart są tworzone karty dzieci.
Potem dodawane są nowe karty.
Następnie dla 20% najlepszych kart zastosowano wyszukiwanie wspinaczkowe. Polega to na tym, że każdy element jest obracany 4 razy
i dla każdego obrotu obliczany jest score. Następnie najlepsze ułożenie jest wybierane dla każdej karty. Następnie wybierana
jest karta z najlepszym score

- grillcardano.py
Zawiera funkcję do generowania karty, do szyfrowania i deszyfrowania oraz do przeprowadzania ataku metodą populacyjno-wspinaczkowa.

- ngram.py
Zawiera funkcję do wczytywania bigramów i do oceny zdeszyfrowanego tekstu. Ocena ta odbywa się w taki sposób, że dla
każdego bigramu, który występuje w tekście jest odszukiwana ocena bazująca na częstotliwości występowania danego bigramu
w danym języku. I później są te wszystkie oceny tych wszystkich bigramów sumowane dla danego tekstu.

- grillEncrypt.py
Tam jest wczytywanie pliku tj.txt, który zawiera tekst do zaszyfrowania. Program po wczytaniu tego szyfru generuje
kartę Cardana i następnie szyfruje tekst przy pomocy klucza, który odpowiada danej karcie. I następnie klucz jest zapisywany
do pliku kt_klucz.txt. Zapisuje wygenerowaną kartę oraz odpowiadający jej klucz. Natomiast do pliku kt.txt zapisuje szyfrogram.

- grillDecrypt.py
To jest program, który czyta szyfrogram z pliku kt.txt i próbuje funkcjq atakPop rozszyfrować ten szyfrogram.
Później ta odszyfrowana informacja jest zapisywana do pliku dt.txt

- grillTest.py
Program ten generuje kartę wraz z odpowiadającym jej kluczem. Szyfruje pewną informację a następnie próbuje funkcja atakPop
rozszyfrować ten szyfrogram.
"""

import random
from ngram import Ngram_score

ng = Ngram_score( 'bigrams.txt')

def kolumna( tj, dl, nr):    # nr < dl
    klmn = ''.join( [ tj[ i*dl + nr ] for i in range( len(tj) // dl ) ] )
    if nr < len(tj)%dl :
        klmn += tj[ (len(tj) // dl)*dl + nr ]
    return( klmn )
def encryptColumnTrans(tj,klucz):
    kt = ''
    dl = len(klucz)
    for x in klucz:
        kt += kolumna( tj, dl, x)   
    return(kt)

def decryptColumnTrans(kt,klucz):
    dl = len(klucz)
    lenkol = len(kt) // dl
    reszta = len(kt) % dl
    poz = 0
    ogon = 0
    tmp = {}
    for x in klucz:
        if x < reszta:
            ogon = 1
        else:
            ogon = 0
        tmp[x] = kt[ poz : poz + lenkol + ogon]
        poz += lenkol + ogon
    #print('tmp = ', tmp)
    tj = ''
    for i in range( lenkol + 1 ):
        for x in range( dl ):
            if i < lenkol or x < reszta:
               tj += tmp[x][i]
    return(tj)



def encrypt(tj,klucz):
    return( encryptColumnTrans(tj,klucz) )

def decrypt(tj,klucz):
    return( decryptColumnTrans(tj,klucz) )


# Funkcja generacjaKarty buduje karte cwiartkami
# Ma to na celu unikniecia sytuacji nakladania sie komorek przy obrotach
# np dla karty o rozmiarze 5 podzial na cwiartki jest nastepujacy
#  A A A A B
#  D A A B B
#  D D A B B
#  D D C C B
#  D C C C C
# Pierwsza cwiartka to cwiartka podstawowa
# Srodek nalezy do podstawowej cwiartki i nie zmienia sie przy obrotach
def generacjaKarty(bokKarty):
    ulozenia=generacjaUlozen(bokKarty)
    elemKarty=list()
    for u in ulozenia:
        losowyObrot=random.sample(range(0,4),1)[0] # Losujemy obrot elementu
        elemKarty.append([u[losowyObrot][0],u[losowyObrot][1]])
    elemKarty.sort()

    # Wydruk karty
    karta=list()
    for i in range(0, bokKarty):
        row=list()
        for j in range(0, bokKarty):
            row.append( "X")
        karta.append(row)
    for k in range(0,len(elemKarty)):
        elem=elemKarty[k]
        karta[elem[0]][elem[1]]=" "
    srodek=int(bokKarty / 2)
    karta[srodek][srodek]= " "

    klucz=kluczDlaKarty(elemKarty,bokKarty)

    return (klucz, karta, elemKarty)

def kopiujElementy(elemKarty):

    elemKartyKopia=[]
    for i in range(0, len(elemKarty)):
        elemKartyKopia.append( [elemKarty[i][0], elemKarty[i][1]])
    return elemKartyKopia

def kluczDlaKarty(elemKarty, rozmiarKarty):

    # Kopia elementow karty aby nie naruszac oryginalu
    elemKartyKopia=kopiujElementy(elemKarty)

    # Budowanie klucza
    # Elementy klucza to nowe pozycje znakow w zaszyfrowanej informacji
    klucz=list()
    for i in range(0,4):
        for j in range(0,len(elemKarty)):
            x=elemKartyKopia[j][0]
            y=elemKartyKopia[j][1]
            klucz.append(x*rozmiarKarty+y)
            # Elementy po dodaniu do listy sa obracane o 90 stopni
            elemKartyKopia[j][0]=y
            elemKartyKopia[j][1]= rozmiarKarty - x - 1
        if i==0:
            srodek=int(rozmiarKarty / 2)
            klucz.append(srodek * rozmiarKarty + srodek)
        elemKartyKopia.sort()
    return klucz

# Funkcja generacjaUlozen tworzy liste elementow podstawowej cwiartki
# a nastepnie obraca elementy podstawowej cwiartki o 90 stopni do pozostalych cwiartek
# zwraca 2 poziomowa liste
# Pierwszy poziom to elementy
# Drugi poziom to pozycje z podstawowej cwiartki i pozycje po obrotach
def generacjaUlozen(bokKarty):
    liczbaPodstaw=int(bokKarty * bokKarty / 4) # liczba elementów podstawowej cwiartki
    ulozenia=[]
    xPoczatekWiersza=0
    xKoniecWiersza= bokKarty - 2
    xKursor=0
    yKursor=0
    # Budowanie list z x i y pozycjami elementow podstawowej cwiartki
    for i in range(0,liczbaPodstaw):
        ulozenia.append([[xKursor,yKursor],[-1,-1],[-1,-1],[-1,-1]])
        if xKursor<xKoniecWiersza:
            xKursor=xKursor+1
        else: # Przejscie do nastepnego wiersza
            xPoczatekWiersza=xPoczatekWiersza+1
            xKoniecWiersza=xKoniecWiersza-1
            xKursor=xPoczatekWiersza
            yKursor=yKursor+1
    for u in ulozenia:
        x=u[0][0]
        y=u[0][1]
        for obrot in range(1,4):
            noweX=y
            noweY=bokKarty - x - 1
            u[obrot][0]=noweX
            u[obrot][1]=noweY
            x=noweX
            y=noweY
    return ulozenia

# Funkcja znajdzElement odszukuje element w liscie ulozen i zwraca pozycje elementu
# lub -1 gdy nie znajdzie
def znajdzElement(x,y,ulozenia):
    for i in range(0,len(ulozenia)):
        for obrot in range(0,4):
            if ulozenia[i][obrot][0] == x and ulozenia[i][obrot][1] == y:
                return i
    return -1

# Funkcja krzyzujKarty tworzy nowa karte na podstawie kart od rodzicow
# Jezeli rodzice maja wspolne elementy karty to sa one kopiowane do dziecka
# Gdy jakies elementy karty nie sa wspolne to losowo wybiera albo od jedno rodzica albo od drugiego
def krzyzujKarty(rodzic1, rodzic2, ulozenia):
    usedElem1=[[-1,-1] for i in range(len(rodzic1))]
    usedElem2=[[-1,-1] for i in range(len(rodzic2))]
    for e in rodzic1:
        elemPos = znajdzElement( e[0], e[1],ulozenia)
        if elemPos >= 0:
            usedElem1[elemPos][0] = e[0]
            usedElem1[elemPos][1] = e[1]
    for e in rodzic2:
        elemPos = znajdzElement( e[0], e[1],ulozenia)
        if elemPos >= 0:
            usedElem2[elemPos][0] = e[0]
            usedElem2[elemPos][1] = e[1]
    dziecko=[[-1,-1] for i in range(len(rodzic1))]
    for i in range( len(dziecko)):
        if usedElem1[i][0]==usedElem2[i][0] and usedElem1[i][1]==usedElem2[i][1]:
            dziecko[i][0] = usedElem1[i][0]
            dziecko[i][1] = usedElem2[i][1]
        else:
            los = random.randint(1,2)
            if los == 1:
                dziecko[i][0] = usedElem1[i][0]
                dziecko[i][1] = usedElem1[i][1]
            else:
                dziecko[i][0] = usedElem2[i][0]
                dziecko[i][1] = usedElem2[i][1]
    dziecko.sort()
    return dziecko

# Funkcja atakPop wykonuje atak na szyfr poprzez utworzenie losowej populacji kart
# Nastepnie dla 20% kart z najlepszym score jest przeprowadzane wyszukiwanie wspinaczkowe najlepszej kombinacji
# Poprzez obracanie kazdego elementu karty o 90 stopni i dobor ulozenia o najlepszym score
# Nastepnie sposrod najlepszych kombinacji dla wszystkich kart wybierana jest karta o najwiekszym score
def atakPop( kt, bokKarty, rozmPop, kryt=-2.5 ):

    ulozenia=generacjaUlozen(bokKarty)

    # Tworzenie populacji kart i obliczanie score dla kazdej z kart
    pop=list()
    for i in range(0,rozmPop):
        key,karta,elementy =generacjaKarty(bokKarty)
        score=ng.score(decrypt(kt,key))
        pop.append([score, elementy])


    # sortowanie aby karty z najlepszym score byly na poczatku listy
    pop.sort(reverse=True)
    bestScore=pop[0][0]
    bestElementy=pop[0][1]
    krok=0

    while bestScore<kryt*len(kt) and krok < 10:

        for j in range(0, int(rozmPop*0.2)): # Usuwamy najgorsze karty
            pop.pop()
        for j in range(0, int(rozmPop/10)): # Dodawanie dzieci dla 10% najlepszych kart
            dziecko=krzyzujKarty(pop[j][1],pop[j+1][1], ulozenia)
            key=kluczDlaKarty(dziecko,bokKarty)
            score=ng.score(decrypt(kt,key))
            pop.append([score,dziecko])
        for i in range(0,int(rozmPop*0.1)): # Dodawanie nowych osobnikow
            key,karta,elementy =generacjaKarty(bokKarty)
            score=ng.score(decrypt(kt,key))
            pop.append([score, elementy])

        # ponowne sortowanie aby karty z najlepszym score byly na poczatku listy
        pop.sort(reverse=True)

        # 20% najlepszych kart jest poddane poszukiwaniu wspinaczkowemu
        for j in range(0, int(len(pop)/5)):
            elementy=kopiujElementy(pop[j][1])
            bestScoreKarty= pop[j][0]
            bestElementyKarty = kopiujElementy(pop[j][1])

            # w kazdej karcie elementy sa obracane i wybierana jest najlepsza kombinacja
            for i in range(0, len(elementy)):
                for obrot in range(0,4):
                    x=elementy[i][0]
                    y=elementy[i][1]
                    elementy[i][0]=y
                    elementy[i][1]= bokKarty - x - 1
                    key=kluczDlaKarty(elementy,bokKarty)
                    score=ng.score(decrypt(kt,key))
                    if score>bestScoreKarty:
                        bestScoreKarty=score
                        bestElementyKarty=kopiujElementy(elementy)
                elementy=kopiujElementy(bestElementyKarty)
            if bestScoreKarty > bestScore or bestScore == 0:
                bestScore = bestScoreKarty
                bestElementy = kopiujElementy(bestElementyKarty)
        krok=krok+1
        print( 'Krok: ',krok,'Best Score:', bestScore, 'Oczekiwane Score: ', kryt*len(kt))
        bestKey=kluczDlaKarty(bestElementy,bokKarty)
        print(bestKey)
        print(decrypt(kt,bestKey))
    bestKey=kluczDlaKarty(bestElementy,bokKarty)
    print('Best Score=',bestScore)
    return bestKey






