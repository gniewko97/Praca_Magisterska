from fibheap import *
import time
import tracemalloc

class Graf:
    def __init__(self, wielkosc):
        self.V = wielkosc
        self.kraw = {}
        self.przyleglosc = {}
        self.do_odw = makefheap()
        # słownik zawierający referencje do obiektów kopca do obniżania klucza
        self.kopiec_obiekt = {}

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

    def zbadaj_kraw(self,do_odw,v,odw):
        for e in self.przyleglosc[v]:
            if not odw[e]:
                if e not in self.kopiec_obiekt:
                    self.kopiec_obiekt[e] = fheappush(do_odw, [self.kraw[v, e], v, e])
                elif self.kraw[v, e] < self.kopiec_obiekt[e].key[0]:
                    self.do_odw.decrease_key(self.kopiec_obiekt[e], [self.kraw[v, e], v, e])

    def Prim(self):
        wynik = []
        suma = 0
        odw_wierzcholki = [0 for col in range(self.V)]
        pol_wierzcholki = 0
        odw_wierzcholki[0] = True
        self.zbadaj_kraw(self.do_odw, 0, odw_wierzcholki)
        while pol_wierzcholki < self.V -1:
            kraw = fheappop(self.do_odw)
            odw_wierzcholki[kraw[2]] = True
            wynik.append([kraw[1],kraw[2],kraw[0]])
            pol_wierzcholki +=1
            self.zbadaj_kraw(self.do_odw,kraw[2],odw_wierzcholki)
#         for u, v, w in wynik:
#             print("Krawedz:", u, v, end=" ")
#             print("-", w)
#             suma += w
#         print("Wielkość MSP:", suma)
#
# # Odczyt z pliku i dostosowanie zawartości do działania programu
# my_file = open("grafy/5n/5000/graf1", "r")
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
#         g.dod_kraw(int(line[0])-1,int(line[1])-1,int(line[2]))
#
# g.Prim()

#Parametry do odczytu z grafu i czasu i pamieci
jakie_n = 3
ilosc_wierzcholkow =[200, 500, 1_000, 2_000, 5_000, 10_000]
czas, pamiec = [], []


for j in range(0, len(ilosc_wierzcholkow)):
    czas, pamiec = [], []
    licznik = 0
    for i in range(1, 51):
        # print("odczyt pon")
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
        # print("odczyt kon")


        startTime = time.time()
        tracemalloc.start()
        g.Prim()
        pamiec.append(tracemalloc.get_traced_memory()[1])
        czas.append((time.time() - startTime))
        tracemalloc.stop()
        licznik += 1
        print(licznik)

    print(ilosc_wierzcholkow[j])
    print('czas: ', sum(czas)/len(czas))
    print('pamiec: ', sum(pamiec)/len(pamiec))




