import random

p = input('Podaj liczbę wierzchołków: ')
p = int(p)

#Liczba krawędzi w grafie
if p % 2 == 0:
    k = p + 0.5 * p
else:
    k = p + 0.5 * p - 0.5

#Minimalna liczba krawędzi wychodząca z wierzchołka startu
min_star = 2

#Minimalna liczba krawędzi wchodząca do wierzchołka końcowego
min_kon = 2

#Maksymalny przepływ na krawędzi
max_flow = 10

#Minimalny przepływ na początkowych krawędziach
min_flow = 3

#Minimalny przepływ na końcowych krawędziach
min_flow_end = 2

list_p = list(range(2, p))

wyn = []

moz = []

#Stworzenie listy wszystkich możliwych krawędzi
for i in range(1, p):
    for j in range(i + 1, p + 1):
        moz.append([i, j])

#Stworzenie początkowej ścieżki w grafie
poz = 1
licz= 1

while len(list_p) > 0:
    wyb = random.choice(list_p)
    if wyb == poz:
        continue
    wyn.append([poz, wyb])
    del list_p[list_p.index(wyb)]
    poz = wyb
    licz += 1

wyn.append([poz, p])

#Stworzenie od nowa listy wierzchołków bez startowego i końcowego
list_p = list(range(2, p))

#Stworzenie list ze startowymi i końcowymi krawędziami
start = []
kon = []
start.append(wyn[0])
kon.append(wyn[-1])

#Usunięcie z listy wierzchołków tych, które już są użyte jako początkowe lub końcowe
del list_p[list_p.index(start[0][1])]
del list_p[list_p.index(kon[0][0])]

#Dodanie minimalnej liczby startowych krawędzi
for x in range(1, min_star):
    wyb = random.choice(list_p)
    del list_p[list_p.index(wyb)]
    wyn.append([1, wyb])
    start.append([1, wyb])
    licz += 1

#Dodanie minimalnej liczby końcowych krawędzi
for x in range(1, min_kon):
    wyb = random.choice(list_p)
    del list_p[list_p.index(wyb)]
    wyn.append([wyb, p])
    kon.append([wyb, p])
    licz += 1

#Usunięcie wykorzsytanych krawędzi
for i in wyn:
    if i[0] > i[1]:
        del moz[moz.index([i[1], i[0]])]
    else:
        del moz[moz.index(i)]

#Usunięcie krawędzi początkowa - końcowa
for i in start:
    del moz[moz.index([i[1], p])]

del moz[moz.index([1, p])]

for i in kon:
    del moz[moz.index([1, i[0]])]

#Dodanie pozostałych krawędzi
while licz <= k:
    wyb = random.choice(moz)
    if wyb[0] == 1:
        wyn.append(wyb)
    elif wyb[1] == p:
        wyn.append(wyb)
    else:
        los = random.randint(0, 1)
        if los == 0:
            wyn.append(wyb)
        else:
            wyn.append([wyb[1], wyb[0]])
        del moz[moz.index(wyb)]
    licz += 1

#Posortowanie krawędzi i dodanie przepływów
wyn_sor = []

for i in range(p+1):
    for j in range(p+1):
        if [i, j] in wyn:
            if i == 1:
                wyn_sor.append([i, j, random.randint(min_flow, max_flow)])
            elif j == p:
                wyn_sor.append([i, j, random.randint(min_flow_end, max_flow)])
            else:
                wyn_sor.append([i, j, random.randint(1, max_flow)])

f = open("losowy_graf.txt", "w")

f.write(str(p)+"\n")
for i in wyn_sor:
    f.write(str(i)[1:-1]+"\n")

f.close()