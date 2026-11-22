from PIL import Image
import numpy as np

def rysuj_ramki_szare(w, h, grub, kolor_start, zmiana_koloru):
    tab = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            odleglosc = min(i, h - 1 - i, j, w - 1 - j)
            numer_ramki = odleglosc // grub
            tab[i, j] = (kolor_start + numer_ramki * zmiana_koloru) % 256
    return Image.fromarray(tab)


def rysuj_pasy_pionowe_szare(w, h, grub, kolor_start, zmiana_koloru):
    tab = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            numer_pasa = j // grub
            tab[i, j] = (kolor_start + numer_pasa * zmiana_koloru) % 256
    return Image.fromarray(tab)

def rysuj_ramki_kolorowe(w, kolor, zmiana_koloru_r, zmiana_koloru_g, zmiana_koloru_b):
    t = (w, w, 3)
    tab = np.zeros(t, dtype=np.uint8)
    kolor_r = kolor[0]
    kolor_g = kolor[1]
    kolor_b = kolor[2]
    z = w
    for k in range(int(w / 2)):
        for i in range(k, z - k):
            for j in range(k, z - k):
                tab[i, j] = [kolor_r, kolor_g, kolor_b]
        kolor_r = (kolor_r - zmiana_koloru_r) % 256
        kolor_g = (kolor_g - zmiana_koloru_g) % 256
        kolor_b = (kolor_b - zmiana_koloru_b) % 256
    return Image.fromarray(tab)

def rysuj_po_skosie_szare(h,w, a, b):
    t = (h, w)
    tab = np.zeros(t, dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            tab[i, j] = (a*i + b*j) % 256
    return Image.fromarray(tab)

def negatyw(obraz):
    typy= ["RGB", "L", "1"]
    if obraz.mode in typy:
        tab = np.asarray(obraz)
        if obraz.mode == "1":
            tab_neg = np.invert(tab)
        else:
            tab_neg = 255 - tab
        return Image.fromarray(tab_neg)
    else:
        print("Zły typ")
        return None

def koloruj_w_paski(obraz, grub, kolor_start, zmiana_koloru):
    t_obraz = np.asarray(obraz)
    h, w = t_obraz.shape
    tab = np.ones((h, w, 3), dtype=np.uint8)
    for i in range(h):
        k = i // grub
        kolor = [(kolor_start[0] + k * zmiana_koloru[0]) % 256,
                 (kolor_start[1] + k * zmiana_koloru[1]) % 256,
                 (kolor_start[2] + k * zmiana_koloru[2]) % 256]
        for j in range(w):
            if t_obraz[i, j] == False:
                tab[i, j] = kolor
            else:
                tab[i, j] = [255, 255, 255]
    return Image.fromarray(tab)


def rgb_to_cmyk(rgb_array):
    rgb = rgb_array.astype(float) / 255
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    k = 1 - np.max(rgb, axis=2)

    c = (1 - r - k) / (1 - k + 1e-8)
    m = (1 - g - k) / (1 - k + 1e-8)
    y = (1 - b - k) / (1 - k + 1e-8)

    cmyk = np.stack((c, m, y, k), axis=2) * 255
    return cmyk.astype(np.uint8)

if __name__ == '__main__':
    # Zadanie 1
    ramki = rysuj_ramki_szare(120, 60, 10, 50, 60)
    print("tryb ramek:", ramki.mode)
    ramki.save("ramki_szare.png")
    ramki.show()

    pasy = rysuj_pasy_pionowe_szare(300, 200, 20, 30, 15)
    print("tryb pasów:", pasy.mode)
    pasy.save("pasy_pionowe_szare.png")
    pasy.show()

    # Zadanie 2
    gwiazdka = Image.open("gwiazdka.bmp")
    negatyw(gwiazdka).save("gwiazdka_neg.png")

    ramki = rysuj_ramki_kolorowe(200, [20, 120, 220], 5, 7, -5)
    ramki.save("ramki_kolorowe.png")
    negatyw(ramki).save("ramki_kolorowe_neg.png")

    skos = rysuj_po_skosie_szare(100, 300, 5, 7)
    skos.save("skos.png")
    negatyw(skos).save("skos_neg.png")

    # Zadanie 3
    # a) inicjały z lab1 (PP.bmp ma tryb 'P': 0 = tło, 1 = litery) -> tryb '1'
    tab_pp = np.asarray(Image.open("PP.bmp"))
    inicjaly = Image.fromarray(tab_pp == 0)   # True = białe tło, False = litery
    print("tryb inicjałów:", inicjaly.mode)
    inicjaly.save("inicjaly.png")

    obraz3 = koloruj_w_paski(inicjaly, 4, [255, 0, 0], [0, 60, 90])
    print("tryb obrazu 3:", obraz3.mode)
    obraz3.show()

    # b) zapis w PNG i JPG oraz porównanie
    obraz3.save("obraz3.png")
    obraz3.save("obraz3.jpg")
    t_png = np.asarray(Image.open("obraz3.png"))
    t_jpg = np.asarray(Image.open("obraz3.jpg"))
    roznica = np.abs(t_png.astype(int) - t_jpg.astype(int))
    print("takie same:", np.array_equal(t_png, t_jpg))
    print("liczba różnych wartości:", np.count_nonzero(roznica))
    print("max różnica:", roznica.max())

    # Zadanie 4
    print(np.array([328, -24]).astype(np.uint8))
    # 328 - 256 = 72,  -24 + 256 = 232
    # Z tego wynika ze nastpępuje swoiste obrócenie licznika

    # Zadanie 5
    r = np.asarray(rysuj_pasy_pionowe_szare(300, 200, 10, 0, 20))
    g = np.asarray(rysuj_pasy_pionowe_szare(300, 200, 18, 0, 20))
    b = np.asarray(rysuj_pasy_pionowe_szare(300, 200, 26, 0, 20))

    tab_rgb = np.stack((r, g, b), axis=2)
    obraz5 = Image.fromarray(tab_rgb)
    print("tryb:", obraz5.mode)
    obraz5.save("obraz5.png")

    # Zadanie 6
    r = np.asarray(rysuj_pasy_pionowe_szare(300, 200, 10, 0, 20))
    g = np.asarray(rysuj_pasy_pionowe_szare(300, 200, 18, 0, 20))
    b = np.asarray(rysuj_pasy_pionowe_szare(300, 200, 26, 0, 20))
    a = np.asarray(rysuj_po_skosie_szare(200, 300, 5, 7))
    tab_rgba = np.stack((r, g, b, a), axis=2)
    obraz6 = Image.fromarray(tab_rgba)
    print("tryb:", obraz6.mode)
    obraz6.save("obraz6.png")

    # Zadanie 7
    t_cmyk = rgb_to_cmyk(tab_rgb)
    obraz7 = Image.fromarray(t_cmyk, mode="CMYK")
    obraz7.save("obraz7.jpg")

    # Na oko: Obraz z zadania 5 wydaję się być ciemniejszy niż obraz z Zadania 7 oraz posiada niebieską poświatę
    # Sposób na porównanie to sprawdzenie czy obrazy są dokładnym negatywem siebie
    print(np.array_equal(c, 255 - r))