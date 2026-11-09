from PIL import Image
import numpy as np


def rysuj_ramke_w_obrazie(obraz, grub):
    obraz = np.asarray(obraz).astype(np.uint8)
    h, w = obraz.shape

    for i in range(h):
        for j in range(grub):
            obraz[i][j] = 0
        for j in range(w - grub, w):
            obraz[i][j] = 0

    for i in range(grub):
        for j in range(w):
            obraz[i][j] = 0

    for i in range(h - grub, h):
        for j in range(w):
            obraz[i][j] = 0

    tab = obraz.astype(bool)
    return Image.fromarray(tab)

def rysuj_ramki(w, h, grub):
    tab = np.zeros((h, w), dtype=bool)

    for i in range(h):
        for j in range(w):
            odleglosc = min(i, h - 1 - i, j, w - 1 - j)
            numer_ramki = odleglosc // grub

            if numer_ramki % 2 != 0:
                tab[i][j] = True
    return Image.fromarray(tab)

def rysuj_pasy_pionowe(w, h, grub):
    tab = np.zeros((h, w), dtype=bool)

    for i in range(h):
        for j in range(w):
            odleglosc = j
            numer_ramki = odleglosc // grub
            if numer_ramki % 2 != 0:
                tab[i][j] = True
    return Image.fromarray(tab)

def rysuj_pasy_poziome(w, h, grub):
    tab = np.zeros((h, w), dtype=bool)

    for i in range(h):
        for j in range(w):
            odleglosc = i
            numer_ramki = odleglosc // grub
            if numer_ramki % 2 != 0:
                tab[i][j] = True
    return Image.fromarray(tab)


def rysuj_wlasne(w, h, grub):
    tab = np.zeros((h, w), dtype=bool)
    srodek_i = h // 2
    srodek_j = w // 2

    for i in range(h):
        for j in range(w):
            odleglosc = ((i - srodek_i) ** 2 + (j - srodek_j) ** 2) ** 0.5
            numer_kola = int(odleglosc // grub)
            if numer_kola % 2 != 0:
                tab[i][j] = True
    return Image.fromarray(tab)


def wstaw_obraz_w_obraz(obraz_bazowy, obraz_wstawiany, m, n):
    tab_bazowy = np.asarray(obraz_bazowy).astype(np.uint8).copy()
    tab_wstawiany = np.asarray(obraz_wstawiany).astype(np.uint8)

    h_o, w_o = tab_bazowy.shape
    h_t, w_t = tab_wstawiany.shape

    h_w = min(h_o, n + h_t)
    w_w = min(w_o, m + w_t)
    n_p = max(0, n)
    m_p = max(0, m)

    # 4. Przepisanie pikseli
    for i in range(n_p, h_w):
        for j in range(m_p, w_w):
            tab_bazowy[i][j] = tab_wstawiany[i - n][j - m]

    tab = tab_bazowy.astype(bool)
    return Image.fromarray(tab)


def main():
    # Zad1
    img = Image.open("bs.bmp")
    img_ramka = rysuj_ramke_w_obrazie(img, 4)
    img_ramka.save("wyjscie_z_ramka.png")

    # Zad 2.1
    obraz = rysuj_ramki(200, 200, 10)
    obraz.save("moje_ramki.png")

    # Zad 2.2
    obraz2 = rysuj_pasy_pionowe(200, 100, 10)
    obraz2.save("moje_ramki2.png")

    # Zad 2.3
    obraz3 = rysuj_wlasne(200, 200, 10)
    obraz3.save("moje_ramki3.png")

    #Zad 3
    obraz_bazowy = Image.fromarray(np.zeros((300, 300), dtype=bool))
    obraz_wstawiany = Image.fromarray(np.ones((50, 50), dtype=bool))
    wynik = wstaw_obraz_w_obraz(obraz_bazowy, obraz_wstawiany, m=100, n=50)
    wynik.save("wynik_wstawiania.png")


if __name__ == "__main__":
    main()
