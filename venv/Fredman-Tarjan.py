from fibheap import *
import random
import time
import tracemalloc
import numpy
import decimal


class Graf:
    def __init__(self, wielkosc):
        #inicjalizacja strukltury
        self.V = wielkosc
        #słownik zawierający krawędzie w grafie
        self.kraw = {}
        #self.org_kraw = {}
        #słownik zawierający sąsiadów wierzchołków w grafie
        self.przyleglosc = {}
        #kolejka kolejnych krawędzi do sprawdzenia
        self.do_odw = makefheap()
        #słownik zawierający odniesienia do jakiego drzewa należy dany wierzchołek
        self.wierzcholki_do_drzew = {}
        #słownik zawierający odniesienie jakie wierzchołki należą do danego drzewa
        self.drzewa_do_wierzcholkow = {}
        #słownik zawierający atrybuty danego drzewa
        self.drzewa = {}
        #słownik zawierający referencje do obiektów kopca do obniżania klucza
        self.kopiec_obiekt = {}


    def dod_kraw(self, u, v, w): #Funkcja dodająca krawędzie do grafu, oraz ustawiająca ich sąsiadów
        if u<v: #sprawdzanie który wierzchołek jest mniejszy, aby trzymać się zapisu o mniejszym wierzchołku z przodu
            self.kraw[u, v] = [w, u, v] #w słowniku trzymana jest [0] koszt krawędzi oraz [1] i [2] czyli oryginalne wierzchołki które krawędź łączy
        else:
            self.kraw[v, u] = [w, v, u]
        if u not in self.przyleglosc: #dodajemy do słownika przyległości sąsiadów dla obu wierzchołków
            self.przyleglosc[u] = [v]
        elif v not in self.przyleglosc[u]:
            self.przyleglosc[u].append(v)
        if v not in self.przyleglosc:
            self.przyleglosc[v] = [u]
        elif u not in self.przyleglosc[v]:
            self.przyleglosc[v].append(u)

    def zbadaj_kraw(self, v, max_nr_drzewa):
        #print('dodajemy do drzewa:',max_nr_drzewa, ' poczatkowy wierzhcołek:', v)
        org_v = v #zapamiętaj jaki wierzchołek badasz
        #print('sasiedzi:',self.przyleglosc[v])
        for e in self.przyleglosc[v]: #sprawdź wszystkich sąsiadów tego wierzchołka
            if self.wierzcholki_do_drzew[e] == max_nr_drzewa: #sprawdź czy badany wierzchołek nie jest już częścią aktualnego drzewa
                continue
            org_e = e #zapamiętaj którego sąsiada badasz
            v = org_v #przywróc orginalny wierzchołek początkowy
            if v>e: #sprawdź czy początkowy wierzchołek nie jest większy
                v, e = e, v #jak jest to zamień miejscami
            #print('ile elem na kopcu', self.do_odw.num_nodes)
            #print('elem na kopcu')
            # for a in self.kopiec_obiekt:
            #     print(self.kopiec_obiekt[a].key)
            #print('elem',org_e, 'klucz kraw',self.kraw[v, e][0], ' drzewo:',self.wierzcholki_do_drzew[org_e], 'Klucz drzewa',self.drzewa[self.wierzcholki_do_drzew[org_e]][0])
            #print(self.drzewa)
            if self.drzewa[self.wierzcholki_do_drzew[org_e]][0] == float('inf'): #sprawdź czy do danego drzewa istnieje juz potencjalna łacząca krawędź
                self.kopiec_obiekt[self.wierzcholki_do_drzew[org_e]] = fheappush(self.do_odw, [self.kraw[v, e][0], org_v, org_e]) #jeśli nie to dodaje tą krawędź do kolejki
                self.drzewa[self.wierzcholki_do_drzew[org_e]][0] = self.kraw[v, e][0] #ustawia też klucz drzewa na koszt tej krawędzi
            elif self.kraw[v, e][0] < self.drzewa[self.wierzcholki_do_drzew[org_e]][0]: #jeśli krawędź już istnieje to sprawdza czy koszt tej krawędzi jest mniejszy od klucza drzewa
                #print('elem na kopcu do zmiany', self.kopiec_obiekt[org_e].key)
                # print("ORG")
                # print(self.drzewa[self.wierzcholki_do_drzew[org_e]][0])
                # print("ZM")
                # print(self.kraw[v, e][0])
                #print (v, e, org_v, org_e, self.kraw[v, e][0], self.kopiec_obiekt[org_e], self.drzewa[self.wierzcholki_do_drzew[org_e]][0])
                self.do_odw.decrease_key(self.kopiec_obiekt[self.wierzcholki_do_drzew[org_e]], [self.kraw[v, e][0], org_v, org_e]) #zmniejsz klucz krawędzi w kopcu
                self.drzewa[self.wierzcholki_do_drzew[org_e]][0] = self.kraw[v, e][0] #zmień klucz w drzewie


    def Freed_Tar(self):
        #początkowe parametery
        wynik = [] #tablica trzymająca wyniki w formacie [z, do, koszt]
        wyniki = 0
        suma = 0 #zmienna z kosztem końcowym wyniku
        odw_wierzcholki = 1 #licznik ile wierzchołków zostało już zbadanych w danym cyklu na początku jest 1 ponieważ zaczynamy z losowym wierzchołkiem
        pol_wierzcholki = 0 #licznik ile wierzchołków zostało dodanych do własnie tworzonego drzewa
        liczba_drzew = self.V #licznik ile drzew jest w grafie po poprzednim cyklu
        org_liczba_kraw = len(self.kraw) #licznik ile krawędzi było w początkowym grafie
        k = decimal.Decimal(numpy.power(decimal.Decimal(2), decimal.Decimal(2) * decimal.Decimal(org_liczba_kraw) / decimal.Decimal(liczba_drzew))) #wyliczenie startowego k
        aktualne_drzewo = 1 #licznik które drzewo jest aktualnie rozrastane
        max_nr_drzewa = liczba_drzew + 1 #zmienna trzymająca numer aktualnie tworzonego drzewa unikalny w skali algorytmu
        nieodw_drzewa = {} #słownik zawierający nieodwiedzone jeszcze w tym cyklu wierzchołki
        #odw_wierzcholki[0] = True
        for a in self.przyleglosc.keys(): #dla wszystkich wierzchołków grafu
            self.wierzcholki_do_drzew[a] = a #Do jakiego drzewa należy dany wierzchołek
            self.drzewa[a] = [float('inf'), False] #słownik drzew w formacie [koszt dołączenia drzewa do aktualnie tworzonego,czy drzewo było już odwiedzone w tym cyklu]
            nieodw_drzewa[a] = True #oznaczenie każdego drzewa na jeszcze nie odwiedzone
        self.drzewa[max_nr_drzewa] = [0, True]
        self.wierzcholki_do_drzew[1] = max_nr_drzewa
        self.drzewa_do_wierzcholkow[max_nr_drzewa] = [1]
        self.zbadaj_kraw(1, max_nr_drzewa) #zbadaj sąsiadów i dodaj do kopca
        del nieodw_drzewa[1]

        #początek cyklów
        while liczba_drzew > 1: #Dopóki drzew w grafie jest więcej niż 1
            while odw_wierzcholki <= liczba_drzew - 1: #każdy cykl trwa dopóki nie odwiedzisz każdego wierzchołka/drzewa w grafie

                # jeżeli liczba dodanych wierzchołków staje się większa niż k przerywaj rozrost
                if pol_wierzcholki > k:
                    # print('Nowe drzewo')
                    # print("")
                    pol_wierzcholki = 0 #zerowanie licznika
                    self.do_odw = makefheap()
                    for a in self.drzewa:
                        self.drzewa[a][0] = float('inf')
                    wyb = random.choice(list(nieodw_drzewa.keys())) #wybierz jeszcze nie odwiedzony wierzchołek
                    self.kopiec_obiekt = {}
                    aktualne_drzewo += 1
                    max_nr_drzewa += 1
                    self.drzewa[max_nr_drzewa] = [0, True]
                    self.wierzcholki_do_drzew[wyb] = max_nr_drzewa
                    del nieodw_drzewa[wyb]
                    odw_wierzcholki += 1
                    # print('murek s')
                    # print('start',wyb)
                    # print(self.przyleglosc[wyb])
                    self.zbadaj_kraw(wyb, max_nr_drzewa)
                    # print(self.do_odw.num_nodes)
                    self.drzewa_do_wierzcholkow[max_nr_drzewa] = [wyb]
                    # print('murek f')

                #normalna część
                if odw_wierzcholki > liczba_drzew - 1:
                    continue
                # if self.do_odw.num_nodes == 0:
                #     pol_wierzcholki = k + 1  # wymuszamy w kolejnym obrocie pętli zaczęcie rozrastania nowego drzewa
                #     continue
                # print('odw wierzchołki w cyklu: ',odw_wierzcholki)
                u = fheappop(self.do_odw) #kolejna krawędź z kopca do sprawdzenia
                wyniki += 1
                if u[1]>u[2]: #zależnie który wierzchołek ma większy numer dodajemy do wyniku właśnie użytą do połączenia krawędź
                    #if [self.kraw[u[2], u[1]][1], self.kraw[u[2], u[1]][2], u[0]] not in wynik:
                    wynik.append([self.kraw[u[2], u[1]][1], self.kraw[u[2], u[1]][2], u[0]])
                else:
                    #if [self.kraw[u[1], u[2]][1], self.kraw[u[1], u[2]][2], u[0]] not in wynik:
                    wynik.append([self.kraw[u[1], u[2]][1], self.kraw[u[1], u[2]][2], u[0]])
                # print('wynik: ',wyniki)
                if wyniki == self.V - 1:
                    break
                #print('napotkane drzewo', self.drzewa[self.wierzcholki_do_drzew[u[2]]])
                if self.drzewa[self.wierzcholki_do_drzew[u[2]]][1]: #jeżeli drzewo zostało już odwiedzone
                    # print('lacze drzewa')
                    pol_wierzcholki = k + 1 #wymuszamy w kolejnym obrocie pętli zaczęcie rozrastania nowego drzewa
                    #self.wierzcholki_do_drzew[u[1]] = self.wierzcholki_do_drzew[u[2]]
                    stare_drzewo = self.wierzcholki_do_drzew[u[2]] #do jakiego drzewa należy właśnie dodany wierzchołek
                    for d in self.drzewa_do_wierzcholkow[max_nr_drzewa]: #wszystkie wierzchołki własnie rozrastanego drzewa dodajemy do starego właśnie napotkanego drzewa
                        self.drzewa_do_wierzcholkow[stare_drzewo].append(d)
                        self.wierzcholki_do_drzew[d] = stare_drzewo
                    del self.drzewa_do_wierzcholkow[max_nr_drzewa] #czyścimy to co należało do właśnie rozrastanego drzewa
                    aktualne_drzewo -= 1 #cofamy licznik drzew ponieważ zaczniemy od nowa rozrastać to drzewo
                    max_nr_drzewa -= 1
                else:
                    self.drzewa[self.wierzcholki_do_drzew[u[2]]][1] = True #oznaczamy drzewo jako zbadane
                    self.zbadaj_kraw(u[2], max_nr_drzewa) #dodaj do kopca sąsiadów właśnie dodanego wierzchołka
                    pol_wierzcholki += 1
                    del nieodw_drzewa[u[2]]
                    self.wierzcholki_do_drzew[u[2]] = max_nr_drzewa
                    odw_wierzcholki += 1
                    self.drzewa_do_wierzcholkow[max_nr_drzewa].append(u[2])
                #print(self.drzewa[self.wierzcholki_do_drzew[u[2]]][1])


            #czyszczenie po cyklu
            # print('czyszczenie')
            liczba_drzew = aktualne_drzewo #ustalenie nowej liczby drzew/wierzchołków w grafie
            if liczba_drzew == 1:
                continue
            k = decimal.Decimal(numpy.power(decimal.Decimal(2), decimal.Decimal(2) * decimal.Decimal(org_liczba_kraw) / decimal.Decimal(liczba_drzew))) # wyliczenie nowego k
            self.do_odw = makefheap() #czyszczenie kopca
            kraw_temp = {} #tymczasowy nowu słownik krawędzi
            self.przyleglosc = {} #czyszczenie słownika sąsiadów
            for e in self.kraw:
                temp_a = self.wierzcholki_do_drzew[e[0]] #ustaw drzewo z którego wychodzi krawędź
                temp_b = self.wierzcholki_do_drzew[e[1]] #ustaw drzewo do którego wchodzi krawędź
                if temp_a != temp_b: #sprawdzaj czy nie należą do tego samego drzewa
                    if temp_a > temp_b:#sprawdzaj który wierzchołek ma większy numer
                        temp_a, temp_b = temp_b, temp_a
                    if (temp_a, temp_b) in kraw_temp:
                        if kraw_temp[temp_a, temp_b][0] > self.kraw[e][0]:
                            kraw_temp[temp_a, temp_b] = self.kraw[e]
                    else:
                        kraw_temp[temp_a, temp_b] = self.kraw[e]
                        if temp_a not in self.przyleglosc:  # dodajemy do słownika przyległości sąsiadów dla obu wierzchołków
                            self.przyleglosc[temp_a] = [temp_b]
                        elif temp_b not in self.przyleglosc[temp_a]:
                            self.przyleglosc[temp_a].append(temp_b)
                        if temp_b not in self.przyleglosc:
                            self.przyleglosc[temp_b] = [temp_a]
                        elif temp_a not in self.przyleglosc[temp_b]:
                            self.przyleglosc[temp_b].append(temp_a)
            self.kraw = kraw_temp
            self.kopiec_obiekt = {}
            nieodw_drzewa = {}  # słownik zawierający nieodwiedzone jeszcze w tym cyklu wierzchołki
            odw_wierzcholki = 1  # licznik ile wierzchołków zostało już zbadanych w danym cyklu na początku jest 1 ponieważ zaczynamy z losowym wierzchołkiem
            pol_wierzcholki = 0  # licznik ile wierzchołków zostało dodanych do własnie tworzonego drzewa
            aktualne_drzewo = 1  # licznik które drzewo z cyklu jest aktualnie rozrastane
            self.wierzcholki_do_drzew = {}
            self.drzewa_do_wierzcholkow = {}
            for a in self.przyleglosc.keys():  # dla wszystkich wierzchołków grafu
                self.wierzcholki_do_drzew[a] = a  # Do jakiego drzewa należy dany wierzchołek
                self.drzewa[a] = [float('inf'), False]  # słownik drzew w formacie [koszt dołączenia drzewa do aktualnie tworzonego,czy drzewo było już odwiedzone w tym cyklu]
                nieodw_drzewa[a] = True  # oznaczenie każdego drzewa na jeszcze nie odwiedzone
            self.drzewa[max_nr_drzewa] = [0, True]
            max_nr_drzewa += 1
            self.wierzcholki_do_drzew[max_nr_drzewa - 1] = max_nr_drzewa
            self.drzewa_do_wierzcholkow[max_nr_drzewa] = [max_nr_drzewa - 1]
            self.zbadaj_kraw(max_nr_drzewa - 1, max_nr_drzewa)  # zbadaj sąsiadów i dodaj do kopca
            del nieodw_drzewa[max_nr_drzewa - 1]


        # #wypisanie wyniku
        # for u, v, w in wynik:
        #     print("Krawedz:", u, v, end=" ")
        #     print("-", w)
        #     suma += w
        # print("Wielkość MSP:", suma)


# # Odczyt z pliku i dostosowanie zawartości do działania programu
# my_file = open("grafy/5n/200/graf1", "r")
# content_list = my_file.read().splitlines()
# fin_list = []
# for i in content_list:
#     fin_list.append(i.split(','))
#
# flag = 0
#
# for line in fin_list:
#     if flag == 0:
#         g = Graf(int(line[0]))
#         flag = 1
#     else:
#         g.dod_kraw(int(line[0]) , int(line[1]), int(line[2]))
#
# g.Freed_Tar()
# czas, pamiec = [], []

#Parametry do odczytu z grafu i czasu i pamieci
jakie_n = 'n'
ilosc_wierzcholkow =[200, 500, 1_000, 2_000, 5_000, 10_000]
#ilosc_wierzcholkow =[10_000]
czas, pamiec = [], []

for j in range(0, len(ilosc_wierzcholkow)):
    czas, pamiec = [], []
    licznik = 0
    for i in range(1, 51):
        # Odczyt z pliku i dostosowanie zawartości do działania programu
        my_file = open("grafy/"+str(jakie_n)+"n/"+str(ilosc_wierzcholkow[j])+"/graf"+str(i), "r")
        content_list = my_file.read().splitlines()
        fin_list = []
        for i in content_list:
            fin_list.append(i.split(','))

        flag = 0

        for line in fin_list:
            if flag == 0:
                g = Graf(int(line[0]))
                flag = 1
            else:
                g.dod_kraw(int(line[0]) - 1, int(line[1]) - 1, int(line[2]))


        startTime = time.time()
        tracemalloc.start()
        g.Freed_Tar()
        pamiec.append(tracemalloc.get_traced_memory()[1])
        czas.append((time.time() - startTime))
        tracemalloc.stop()
        licznik += 1
        print(licznik)

    print(ilosc_wierzcholkow[j])
    print('czas: ', sum(czas)/len(czas))
    print('pamiec: ', sum(pamiec)/len(pamiec))