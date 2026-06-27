# Szyfr „Grill Kardano”

Projekt realizuje algorytm szyfrowania oraz kryptoanalizy (łamania) klasycznego szyfru – **Grilla Cardana** (dla macierzy o boku $n$ nieparzystym) przy użyciu algorytmu heurystycznego.

## Opis Działania Szyfru

Aby uniknąć sytuacji, że w momencie obrotu karty trafimy na miejsce, które jest już wypełnione, podzieliłem kartę na ćwiartki. 
Przy kolejnych obrotach pierwsza ćwiartka przechodzi na drugą, potem na trzecią i na czwartą ćwiartkę. 

Jest jedna ćwiartka podstawowa i losowane są z niej elementy, które powinny trafić do innych ćwiartek – tak, aby po uzyskaniu ostatecznej karty puste miejsca były rozmieszczone po całej matrycy. 
Następnie algorytm przyporządkowuje nową pozycję dla liter, a te nowe pozycje tworzą klucz. 
W przypadku karty o rozmiarze 5x5 uzyskujemy klucz o długości 25 elementów.

## Algorytm Ataku (Kryptoanaliza)

Do łamania szyfru wykorzystana została funkcja `atakPop`. Działa ona w następujący sposób:
1. Tworzy losową populację kart startowych.
2. Dla każdej karty obliczany jest wskaźnik dopasowania (*score*) na podstawie analizy statystycznej bigramów językowych.
3. Karty są sortowane tak, aby najlepsze osobniki znajdowały się na początku populacji.
4. Karty z najgorszym wynikiem są usuwane.
5. Z najlepszych kart (rodziców) tworzone są nowe karty (dzieci) poprzez proces krzyżowania.
6. Do populacji dodawane są również całkowicie nowe, losowe karty (mutacja/wprowadzenie nowej puli genowej).
7. Dla 20% najlepszych kart zastosowano **wyszukiwanie wspinaczkowe (Hill Climbing)**. Polega ono na tym, że każdy element karty jest obracany 4 razy i dla każdego obrotu obliczany jest *score*. 
8. Na koniec wybierane jest najlepsze ułożenie dla każdej karty, a z nich wyłaniana jest karta z najwyższym ostatecznym wynikiem dopasowania.

## Struktura Projektu

* **`grillCardana.py`** – Zawiera funkcje do generowania karty, szyfrowania, deszyfrowania oraz przeprowadzania ataku metodą populacyjno-wspinaczkową.
* **`ngram.py`** – Odpowiada za wczytywanie bazy bigramów i ocenę zdeszyfrowanego tekstu. Dla każdego bigramu występującego w tekście odszukiwana jest ocena bazująca na częstotliwości jego występowania w danym języku. Wszystkie oceny cząstkowe są sumowane dla całego tekstu.
* **`grillEncrypt.py`** – Skrypt wczytujący plik `tj.txt` (tekst jawny), generujący kartę Cardana oraz szyfrujący tekst przy pomocy klucza. Klucz oraz wygenerowana karta są zapisywane do pliku `kt_klucz.txt`, a sam szyfrogram trafia do `kt.txt`.
* **`grillDecrypt.py`** – Program, który odczytuje szyfrogram z pliku `kt.txt`, uruchamia funkcję `atakPop` i próbuje go złamać. Odszyfrowana informacja jest zapisywana do pliku `dt.txt`.
* **`grillTest.py`** – Skrypt testowy służący do weryfikacji działania algorytmu. Automatycznie generuje losową kartę wraz z kluczem, szyfruje tekst jawny, a następnie uruchamia funkcję atakPop, aby sprawdzić, czy proces kryptoanalizy zakończy się sukcesem.