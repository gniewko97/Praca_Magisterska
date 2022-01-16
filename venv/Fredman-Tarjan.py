from fibheap import *
import random


class Graf:
    def __init__(self, wielkosc):
        self.V = wielkosc
        #self.org_V = wielkosc
        self.m = 0
        self.drzewa = wielkosc
        self.graf = []
        self.przyleglosc = [[0 for col in range(wielkosc)] for row in range(wielkosc)]
        self.do_odw = makefheap()
        self.pol_wierzcholki = 0
        self.wynik = []
        self.suma = 0
        self.odw_wierzcholki = [0 for col in range(self.V)]
        self.drzewa_wierzchołki = [0 for col in range(self.V)]
        self.stos = 0
        self.nowa_przyleg = []

    def dod_kraw(self, u, v, w):
        self.graf.append([u, v, w])
        self.przyleglosc[u][v] = w
        self.przyleglosc[v][u] = w

    def zbadaj_kraw(self, do_odw, v):
        for e in range(self.V):
            if self.przyleglosc[v][e] != 0:
                fheappush(do_odw, [self.przyleglosc[v][e], v, e])
                self.stos += 1

    def Freedman_Tarjan(self):
        k = 2 ** (2 * self.m / self.drzewa)
        #print(self.przyleglosc)
        drzew = 1
        while (self.pol_wierzcholki < self.V - 1):
            while (0 in self.odw_wierzcholki):
                self.Prim(k, drzew)
                drzew += 1
                self.do_odw = makefheap()
                self.stos = 0
                #print(self.drzewa_wierzchołki)
                #print(k)
            self.drzewa = drzew
            k = 2 ** (2 * self.m / self.drzewa)
            drzew = 1
            #print(self.nowa_przyleg)
            #print(len(self.nowa_przyleg))
            #self.V = len(self.nowa_przyleg)
            self.przyleglosc = [[0 for col in range(self.V)] for row in range(self.V)]
            self.graf = []
            self.drzewa_wierzchołki = [-1 for col in range(self.V)]
            for line in self.nowa_przyleg:
                if ([line[1], line[2], line[0]] not in self.graf) and ([line[2], line[1], line[0]] not in self.graf):
                    g.dod_kraw(line[1], line[2], line[0])
                    self.odw_wierzcholki[line[1]] = 0
                    self.odw_wierzcholki[line[2]] = 0
                    self.drzewa_wierzchołki[line[1]] = 0
                    self.drzewa_wierzchołki[line[2]] = 0
            print(self.graf)
            print(self.nowa_przyleg)
            self.nowa_przyleg = []
            print(self.odw_wierzcholki)
            print(self.drzewa_wierzchołki)
            print(self.pol_wierzcholki)
            #break
        self.Wyn()


    def Prim(self,k,d):
        licz = 0
        flag = 0
        wyb = random.randint(0, self.V-1)
        while(self.odw_wierzcholki[wyb] != False):
            wyb = random.randint(0, self.V-1)
        self.odw_wierzcholki[wyb] = True
        self.drzewa_wierzchołki[wyb] = d
        self.zbadaj_kraw(self.do_odw, wyb)
        while self.pol_wierzcholki < self.V - 1 and licz <= k and self.stos > 0:
            kraw = fheappop(self.do_odw)
            self.stos -= 1
            #print(kraw[2])
            #print(self.odw_wierzcholki)
            if self.drzewa_wierzchołki[kraw[2]] == 0:
                #print("działa wchodzi w " + str(kraw[2]))
                self.odw_wierzcholki[kraw[2]] = True
                self.drzewa_wierzchołki[kraw[2]] = d
                licz += 1
                self.wynik.append([kraw[1], kraw[2], kraw[0]])
                self.pol_wierzcholki += 1
                self.zbadaj_kraw(self.do_odw, kraw[2])
                #print("nowe tab")
                #print(self.odw_wierzcholki)
                #print(self.drzewa_wierzchołki)
                #print("Stos:"+str(self.stos))
            elif self.drzewa_wierzchołki[kraw[2]] != d:
                flag = 1
                self.nowa_przyleg.append(kraw)
                print("inne drzewo")
                break
        if flag == 0 and self.stos > 0:
            kraw = fheappop(self.do_odw)
            self.stos -= 1
            while self.drzewa_wierzchołki[kraw[2]] != 0 and self.drzewa_wierzchołki[kraw[2]] == d:
                if self.stos < 1:
                    flag = 1
                    break
                kraw = fheappop(self.do_odw)
                self.stos -= 1
            if flag == 0:
                self.nowa_przyleg.append(kraw)
                print("koniec k lub brak")

    def Wyn(self):
        for u, v, w in self.wynik:
            print("Krawedz:", u, v, end=" ")
            print("-", w)
            self.suma += w
        print("Wielkość MSP:", self.suma)


# Odczyt z pliku i dostosowanie zawartości do działania programu
my_file = open("losowy_graf.txt", "r")
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
        g.m += 1

g.Freedman_Tarjan()