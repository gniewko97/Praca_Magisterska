from fibheap import *

class Graf:
    def __init__(self, wielkosc):
        self.V = wielkosc
        self.kraw = {}
        self.przyleglosc = {}
        self.do_odw = makefheap()

    def dod_kraw(self, u, v, w):
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

    def zbadaj_kraw(self,do_odw,v):
        for e in self.przyleglosc[v]:
            fheappush(do_odw,[self.kraw[v,e],v,e])

    def Prim(self):
        wynik = []
        suma = 0
        odw_wierzcholki = [0 for col in range(self.V)]
        pol_wierzcholki = 0
        odw_wierzcholki[0] = True
        self.zbadaj_kraw(self.do_odw, 0)
        while pol_wierzcholki < self.V -1:
            kraw = fheappop(self.do_odw)
            if not odw_wierzcholki[kraw[2]]:
                odw_wierzcholki[kraw[2]] = True
                wynik.append([kraw[1],kraw[2],kraw[0]])
                pol_wierzcholki +=1
                self.zbadaj_kraw(self.do_odw,kraw[2])
        for u, v, w in wynik:
            print("Krawedz:", u, v, end=" ")
            print("-", w)
            suma += w
        print("Wielkość MSP:", suma)

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
        g.dod_kraw(int(line[0])-1,int(line[1])-1,int(line[2]))

g.Prim()