class Graf:
    def __init__(self, wieloksc):
        self.V = wieloksc
        self.graf = []

    def dod_kraw(self, u, v, w):
        self.graf.append([u, v, w])

    def szukaj(self, zbior, i, o):
        if zbior[i] == i:
            zbior[o] = i
            return i
        return self.szukaj(zbior, zbior[i], o)

    def zlacz(self, zbior, poziom, x, y):
        xk = self.szukaj(zbior, x, x)
        yk = self.szukaj(zbior, y, y)
        if poziom[xk] < poziom[yk]:
            zbior[xk] = yk
        elif poziom[xk] > poziom[yk]:
            zbior[yk] = xk
        else:
            zbior[yk] = xk
            poziom[xk] += 1

    def kruskal(self):
        wynik = []
        i, e = 0, 0
        suma = 0
        self.graf = sorted(self.graf, key=lambda kraw: kraw[2])
        zbior = []
        poziom = []
        for kraw in range(self.V):
            zbior.append(kraw)
            poziom.append(0)
        while e < self.V - 1:
            u, v, w = self.graf[i]
            i = i + 1
            x = self.szukaj(zbior, u, u)
            y = self.szukaj(zbior, v, v)
            if x != y:
                e = e + 1
                wynik.append([u, v, w])
                self.zlacz(zbior, poziom, x, y)
        for u, v, w in wynik:
            print("Krawedz:", u, v, end=" ")
            print("-", w)
            suma += w
        print("Wielkość MSP:",suma)


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
        
g.kruskal()