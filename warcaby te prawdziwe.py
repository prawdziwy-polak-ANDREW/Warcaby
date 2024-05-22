from tkinter import *
import random
import time

tablica = [[0] * 8 for a in range(8)]


def czy_legalny_ruch(xstart, ystart, xend, yend):
    kolor = plansza[xstart][ystart]
    xs = int((xstart + xend) / 2)
    ys = int((ystart + yend) / 2)
    if kolor != ostatni:
        if kolor == 'C':
            if xstart + 1 == xend:
                if (ystart - yend) ** 2 == 1:
                    if 0 <= xend <= 7 and 0 <= yend <= 7:
                        if plansza[xend][yend] == ' ':
                            return 'ok'
            elif xstart + 2 == xend and (ystart - yend) ** 2 == 4:
                if 0 <= xend <= 7 and 0 <= yend <= 7:
                    if plansza[xend][yend] == ' ' and plansza[xs][ys] == 'B':
                        plansza[xs][ys] = ' '
                        return 'ok'

        elif kolor == 'B':
            if xstart - 1 == xend:
                if (ystart - yend) ** 2 == 1:
                    if 0 <= xend <= 7 and 0 <= yend <= 7:
                        if plansza[xend][yend] == ' ':
                            return 'ok'

            elif xstart - 2 == xend and (ystart - yend) ** 2 == 4:
                if 0 <= xend <= 7 and 0 <= yend <= 7:
                    if plansza[xend][yend] == ' ' and plansza[xs][ys] == 'C':
                        plansza[xs][ys] = ' '
                        return 'ok'


def czy_legalny_ruch_damka(xstart, ystart, xend, yend):
    kolor = plansza[xstart][ystart]
    if kolor[0] != ostatni:

        if kolor[-1] == 'D':
            if plansza[xend][yend] == ' ':
                liczba_bialych = 0
                for i in range(1, abs(xstart - xend) + 1):
                    p_przeciwnika1 = xstart + i * znak(xstart, xend)
                    p_przeciwnika2 = ystart + i * znak(ystart, yend)
                    if plansza[p_przeciwnika1][p_przeciwnika2][0] == kolor[0]:
                        liczba_bialych += 1
                if liczba_bialych == 0:
                    for i in range(0, abs(xstart - xend) + 1):
                        p_przeciwnika1 = xstart + i * znak(xstart, xend)
                        p_przeciwnika2 = ystart + i * znak(ystart, yend)
                        if plansza[p_przeciwnika1][p_przeciwnika2] != ' ':
                            plansza[p_przeciwnika1][p_przeciwnika2] = ' '
                    return 'ok'


def znak(a, b):
    if a - b > 0:
        return -1
    return 1


def rysuj_szachownice():
    for i in range(len(tablica)):
        for j in range(len(tablica[i])):
            kolor = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(i * 20 + 50, j * 20 + 50, i * 20 + 70, j * 20 + 70, outline="black", fill=kolor,
                                    width=2)
            canvas.pack()


def wykonaj_ruch(xstart, ystart, xend, yend):
    status = 0
    k = plansza[xstart][ystart]
    global ostatni

    if czy_legalny_ruch(xstart, ystart, xend, yend) == 'ok':
        ostatni = k[0]
        plansza[xend][yend] = k
        plansza[xstart][ystart] = ' '

        if k == 'B' and xend == 0:
            plansza[xend][yend] = 'BD'
        if k == 'C' and xend == 7:
            plansza[xend][yend] = 'CD'
        status = 1

    if czy_legalny_ruch_damka(xstart, ystart, xend, yend) == 'ok':
        ostatni = k[0]
        plansza[xend][yend] = k
        plansza[xstart][ystart] = ' '
        status = 1

    if status == 1:
        pokaz_pionki()
        if sprawdz_wygrana():
            return
        ruch_komputera()
        pokaz_pionki()
        sprawdz_wygrana()


def ruch_komputera():
    xstart = random.randint(0, 7)
    ystart = random.randint(0, 7)
    xend = random.randint(0, 7)
    yend = random.randint(0, 7)
    while czy_legalny_ruch(xstart, ystart, xend, yend) != "ok":
        xstart = random.randint(0, 7)
        ystart = random.randint(0, 7)
        xend = random.randint(0, 7)
        yend = random.randint(0, 7)
    k = plansza[xstart][ystart]
    time.sleep(1)
    global ostatni
    ostatni = k[0]
    plansza[xend][yend] = k
    plansza[xstart][ystart] = ' '
    if k == 'C' and xend == 7:
        plansza[xend][yend] = 'CD'


def pokaz_pionki():
    canvas.delete('all')
    rysuj_szachownice()
    for i in range(len(plansza)):
        for j in range(len(plansza[i])):
            if plansza[i][j] != ' ':
                kolor = 'black' if plansza[i][j][0] == 'C' else 'white'
                canvas.create_oval(j * 20 + 53, i * 20 + 53, j * 20 + 67, i * 20 + 67, outline="black", fill=kolor,
                                   width=2, tags="oval")
                canvas.pack()
                if plansza[i][j][-1] == 'D':
                    canvas.create_text(j * 20 + 60, i * 20 + 60, text="D", fill="red", font=('Helvetica 8 bold'))
                    canvas.pack()
    root.update()


def klik(e):
    a = int((e.x - 50) / 20)
    b = int((e.y - 50) / 20)
    if plansza[b][a] != ' ':
        with open(".venv/ruch.txt", "w") as f:
            f.write(str(b) + str(a))
    if plansza[b][a] == ' ':
        with open(".venv/ruch.txt", "r") as f:
            x = f.read()
        wykonaj_ruch(int(x[0]), int(x[1]), b, a)


def sprawdz_wygrana():
    liczba_bialych = 0
    liczba_czarnych = 0
    for i in range(8):
        for j in range(8):
            if plansza[i][j][0] == 'B':
                liczba_bialych += 1
            elif plansza[i][j][0] == 'C':
                liczba_czarnych += 1

    if liczba_bialych == 0:
        napis_wygrana.set("Czarne wygrywają!")
        label_wygrana.config(font=("Helvetica", 22))
        root.update()
        root.quit()

        return True
    elif liczba_czarnych == 0:
        napis_wygrana.set("Białe wygrywają!")
        label_wygrana.config(font=("Helvetica", 22))
        root.update()
        root.quit()
        return True
    return False


plansza = [
    [' ', 'C', ' ', 'C', ' ', 'C', ' ', 'C'],
    ['C', ' ', 'C', ' ', 'C', ' ', 'C', ' '],
    [' ', 'C', ' ', 'C', ' ', 'C', ' ', 'C'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
    [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
    ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' ']
]

ostatni = 'C'

root = Tk()
canvas = Canvas(root, width=400, height=400)
canvas.pack()
napis_wygrana = StringVar()
label_wygrana = Label(root, textvariable=napis_wygrana)
label_wygrana.pack()
root.title("WARCABY")
root.bind("<Button-1>", klik)

rysuj_szachownice()
pokaz_pionki()
root.mainloop()
