import random
import numpy
from collections import defaultdict
from fibheap import *


class Graf:
    def __init__(self, wielkosc):
        self.V = wielkosc
        self.m = 0
        self.drzewa = wielkosc
        self.iter = 0
        self.kraw = defaultdict(list)
        self.graf_p = defaultdict(list)
        self.graf_np = defaultdict(list)
        self.przyleglosc = defaultdict(list)
        self.do_odw = makefheap()
        self.pol_wierzcholki = 0
        self.wynik = []
        self.suma = 0
        self.odw_wierzcholki = [0 for col in range(self.V)]
        self.drzewa_wierzcholki = [0 for col in range(self.V)]
        self.stos = 0
        self.nowa_przyleg = []

    def dod_kraw(self, u, v, w, i):
        self.kraw[u, v] = w
        self.kraw[v, u] = w
        if u not in self.przyleglosc:
            self.przyleglosc[u] = [v]
        elif v not in self.przyleglosc[u]:
            self.przyleglosc[u].append(v)
        if v not in self.przyleglosc:
            self.przyleglosc[v] = [u]
        elif u not in self.przyleglosc[v]:
            self.przyleglosc[v].append(u)
        if i == 1:
            if "u, v" not in self.graf_p:
                self.graf_p[u, v] = [w, u, v]
                self.graf_p[v, u] = [w, v, u]

    def zbadaj_kraw(self, do_odw, v):
        for e in self.przyleglosc[v]:
            fheappush(do_odw, [self.kraw[v, e], v, e])
            self.stos += 1

    def Freedman_Tarjan(self):
        drzewa = 0
        k = numpy.power(2, (2 * self.m / self.drzewa))
        # print(self.przyleglosc)
        while (self.pol_wierzcholki < self.V - 1):
            while (0 in self.odw_wierzcholki):
                drzewa += 1
                self.Prim(k, drzewa)
                self.do_odw = makefheap()
                self.stos = 0
                # print(self.drzewa_wierzchołki)
                # print(k)
            if drzewa == 1:
                break
            k = numpy.power(2, (2 * self.m / self.drzewa))
            self.iter += 1
            #print("stara przyleg:", self.przyleglosc)
            #print(self.nowa_przyleg)
            #print("drzewa: ", self.drzewa_wierzcholki)
            # print(len(self.nowa_przyleg))
            # self.V = len(self.nowa_przyleg)
            self.przyleglosc = defaultdict(list)
            self.kraw = defaultdict(list)
            if self.iter % 2 == 1:
                self.graf_np = defaultdict(list)
                for line in self.nowa_przyleg:
                    xx = self.drzewa_wierzcholki[line[1]] - 1
                    yy = self.drzewa_wierzcholki[line[2]] - 1
                    if "xx, yy" not in self.graf_np:
                        #print("NP:", xx, yy)
                        self.graf_np[xx, yy] = [line[0], self.graf_p[line[1], line[2]][1],
                                                self.graf_p[line[1], line[2]][2]]
                        self.graf_np[yy, xx] = [line[0], self.graf_p[line[2], line[1]][1],
                                                self.graf_p[line[2], line[1]][2]]
                        self.dod_kraw(xx, yy, line[0], 0)
            else:
                self.graf_p = defaultdict(list)
                for line in self.nowa_przyleg:
                    xx = self.drzewa_wierzcholki[line[1]]
                    yy = self.drzewa_wierzcholki[line[2]]
                    if "xx, yy" not in self.graf_p:
                        #print("P:", xx, yy)
                        self.graf_p[xx, yy] = [line[0], self.graf_np[line[1], line[2]][1],
                                               self.graf_np[line[1], line[2]][2]]
                        self.graf_p[yy, xx] = [line[0], self.graf_np[line[2], line[1]][1],
                                               self.graf_np[line[2], line[1]][2]]
                        self.dod_kraw(xx, yy, line[0], 0)
            # print(self.graf)
            # print(self.nowa_przyleg)
            self.drzewa_wierzcholki = [0 for col in range(drzewa)]
            self.odw_wierzcholki = [0 for col in range(drzewa)]
            self.nowa_przyleg = []
            self.drzewa = drzewa
            drzewa = 0
            #print("Graf_P:", self.graf_p)
            #print("Graf_NP:", self.graf_np)
            #print("nowa przyleg:", self.przyleglosc)
            # print(self.odw_wierzcholki)
            # print(self.drzewa_wierzchołki)
            # print(self.pol_wierzcholki)
            # break
        self.Wyn()

    def Prim(self, k, d):
        licz = 0
        flag = 0
        wyb = random.randint(0, self.drzewa - 2)
        while (self.odw_wierzcholki[wyb] != False):
            wyb = random.randint(0, self.drzewa - 2)
        self.odw_wierzcholki[wyb] = True
        self.drzewa_wierzcholki[wyb] = d
        self.zbadaj_kraw(self.do_odw, wyb)
        while self.pol_wierzcholki < self.V - 1 and licz <= k and self.stos > 0:
            kraw = fheappop(self.do_odw)
            self.stos -= 1
            # print(kraw[2])
            # print(self.odw_wierzcholki)
            if self.drzewa_wierzcholki[kraw[2]] == 0:
                # print("działa wchodzi w " + str(kraw[2]))
                self.odw_wierzcholki[kraw[2]] = True
                self.drzewa_wierzcholki[kraw[2]] = d
                licz += 1
                if self.iter % 2 == 1:
                    self.wynik.append([self.graf_np[kraw[1], kraw[2]][1], self.graf_np[kraw[1], kraw[2]][2], kraw[0]])
                else:
                    self.wynik.append([self.graf_p[kraw[1], kraw[2]][1], self.graf_p[kraw[1], kraw[2]][2], kraw[0]])
                self.pol_wierzcholki += 1
                self.zbadaj_kraw(self.do_odw, kraw[2])
                # print("nowe tab")
                # print(self.odw_wierzcholki)
                # print(self.drzewa_wierzchołki)
                # print("Stos:"+str(self.stos))
            elif self.drzewa_wierzcholki[kraw[2]] != d:
                if [kraw[0], kraw[2], kraw[1]] not in self.nowa_przyleg:
                    #print("inne drzewo z: ", self.drzewa_wierzcholki[kraw[1]], " do: ",
                                #self.drzewa_wierzcholki[kraw[2]])
                    flag = 1
                    self.nowa_przyleg.append(kraw)
                    # print("inne drzewo")
                    break
                else:
                    break
        if flag == 0 and self.stos > 0:
            flag2 = 0
            kraw = fheappop(self.do_odw)
            self.stos -= 1
            #print("badana kraw:", kraw)
            #print("działa z: ", d, " idzie do: ", self.drzewa_wierzcholki[kraw[2]])
            while flag2 == 0:
                # if self.drzewa_wierzcholki[kraw[2]] == 0:
                # flag2 = 1
                # continue
                if self.drzewa_wierzcholki[kraw[2]] != d:
                    if [kraw[0], kraw[2], kraw[1]] not in self.nowa_przyleg:
                        flag2 = 1
                        continue
                if self.stos < 1:
                    flag = 1
                    break
                kraw = fheappop(self.do_odw)
                self.stos -= 1
            if flag == 0:
                #print("koniec k z: ", self.drzewa_wierzcholki[kraw[1]], " do: ", self.drzewa_wierzcholki[kraw[2]])
                #print("pozostało na stosie: ", self.stos)
                self.nowa_przyleg.append(kraw)
                # print("koniec k lub brak")

    def Wyn(self):
        for u, v, w in self.wynik:
            print("Krawedz:", u, v, end=" ")
            print("-", w)
            self.suma += w
        print("Wielkość MSP:", self.suma)
        print("ilość rund:", self.iter)


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
        g.dod_kraw(int(line[0]) - 1, int(line[1]) - 1, int(line[2]), 1)
        g.m += 1

g.Freedman_Tarjan()
