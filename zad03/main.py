from PIL import Image
import numpy as np
from PIL import ImageChops
from PIL import ImageStat as stat
import matplotlib.pyplot as plt
import random


def rysuj_histogram_RGB(obraz):
    hist = obraz.histogram()
    plt.title("histogram  ")
    plt.bar(range(256), hist[:256], color='r', alpha=0.5)
    plt.bar(range(256), hist[256:2 * 256], color='g', alpha=0.4)
    plt.bar(range(256), hist[2 * 256:], color='b', alpha=0.3)
    plt.show()

def zlicz_piksele(obraz, kolor):
    obraz = obraz.convert("RGB")
    w, h = obraz.size
    for liczba, kolory in obraz.getcolors(maxcolors=w * h):
        if kolory == tuple(kolor):
            return liczba
    return 0

def mieszaj_kanaly(obraz):
    r, g, b = obraz.split()
    neg_obraz = ImageChops.invert(obraz)
    nr, ng, nb = neg_obraz.split()

    lista = [r, g, b, nr, ng, nb]
    temp = []
    for x in range(0, 3):
        z = random.choice(lista)
        temp.append(z)

    mix = Image.merge('RGB', (temp[0], temp[1], temp[2]))
    return mix


def rozpoznaj_mix(obraz, mix):
    r, g, b = obraz.split()
    nr, ng, nb = ImageChops.invert(obraz).split()

    kanaly = [r, g, b, nr, ng, nb]
    nazwy = ["r", "g", "b", "nr", "ng", "nb"]

    wynik = []
    for kanal_mix in mix.split():
        for i in range(len(kanaly)):
            if np.array_equal(np.array(kanal_mix), np.array(kanaly[i])):
                wynik.append(nazwy[i])
                break
    return wynik

def statystyki(obraz):
    s = stat.Stat(obraz)
    print("extrema ", s.extrema)
    print("count ", s.count)
    print("mean ", s.mean)
    print("median ", s.median)
    print("stddev ", s.stddev)



if __name__ == '__main__':
    # Zad 1 - setup
    im = Image.open("obraz.png")
    print(im.mode)

    # Zad 1 - a
    # rysuj_histogram_RGB(im)

    # Zad 1 - b
    hist = im.histogram()
    print("kanał r", hist[155])
    print("kanał g", hist[256+155])
    print("kanał b", hist[256*2+155])

    # Zad 1 - c
    liczba = zlicz_piksele(im, [155, 155, 155])
    print("pikseli [155,155,155]:", liczba)

    # Zad 1 - d
    im.save("obraz.jpg")
    im_jpg = Image.open("obraz.jpg")
    print("im_jpg:", im_jpg.mode, im_jpg.size)

    # Zad 2 - setup
    im.save("obraz.jpg")
    im_jpg = Image.open("obraz.jpg")
    print("im_jpg:", im_jpg.mode, im_jpg.size)

    # Zad 2 - a
    print("--- statystyki im ---")
    statystyki(im)
    print("--- statystyki im_jpg ---")
    statystyki(im_jpg)
    """
                Uzasadnienie
    
    Statystyki obu obrazów są prawie takie same,
    ale nie identyczne. Powodem jest to,
    że JPEG kompresuje stratnie i przy zapisie zmienia kolory pikseli.
    """

    # Zad 2 - b
    diff = ImageChops.difference(im, im_jpg)
    print("--- statystyki diff ---")
    statystyki(diff)

    """
        --- statystyki diff ---
    extrema  [(0, 84), (0, 62), (0, 67)]
    count  [1100800, 1100800, 1100800]
    mean  [5.552000363372093, 5.441155523255814, 6.526819585755814]
    median  [4, 4, 5]
    stddev  [5.438286279959025, 4.969431473869716, 6.155180612273178]
    
    Po zapisie do JPG kolory pikseli trochę się zmieniły: najmniejsza różnica to 0,
    a największa to 84 (extrema). Zwykle jednak piksel różni się tylko o około
    5 na 255 (mean i median), czyli bardzo mało, więc gołym okiem tego nie widać.
    """

    # Zad 2 - c
    im_jpg.save("obraz2.jpg")
    im_jpg2 = Image.open("obraz2.jpg")
    im_jpg2.save("obraz3.jpg")
    im_jpg3 = Image.open("obraz3.jpg")

    diff2 = ImageChops.difference(im_jpg, im_jpg2)
    print("--- statystyki diff dla jpg zapisanego raz a kilka ---")
    statystyki(diff2)

    """
    extrema  [(0, 30), (0, 31), (0, 29)]
    count  [1100800, 1100800, 1100800]
    mean  [0.3391678779069767, 0.3152516351744186, 0.4158566497093023]
    median  [0, 0, 0]
    stddev  [0.837946577925194, 0.774373539645807, 0.9728911965491245]
    
    Ponowny zapis do JPG zmienia obraz już bardzo mało: piksel różni się
    średnio o mniej niż 1 na 255, a mediana 0 oznacza, że ponad połowa
    pikseli w ogóle się nie zmieniła. Najwięcej traci się przy pierwszym
    zapisie z PNG do JPG, a każdy kolejny zapis psuje obraz już tylko odrobinę
    """

    # Zad 3 - a
    tab = np.asarray(im)
    t_r = tab[:, :, 0]
    t_g = tab[:, :, 1]
    t_b = tab[:, :, 2]

    im_r = Image.fromarray(t_r)
    im_g = Image.fromarray(t_g)
    im_b = Image.fromarray(t_b)
    im_r.save("im_r.png")
    im_g.save("im_g.png")
    im_b.save("im_b.png")
    print("im_r:", im_r.mode, im_r.size)

    # Zad 3 - b
    im1 = Image.merge('RGB', (im_r, im_g, im_b))
    diff3 = ImageChops.difference(im1, im)
    ImageChops.difference(im1, im).show()
    print("--- statystyki diff3 ---")
    statystyki(diff3)
    """
    --- statystyki diff3 ---
    extrema  [(0, 0), (0, 0), (0, 0)]
    count  [1100800, 1100800, 1100800]
    mean  [0.0, 0.0, 0.0]
    median  [0, 0, 0]
    stddev  [0.0, 0.0, 0.0]
    
    Nie różnią sie niczym
    """


    # Zad 3 - c
    plt.figure(figsize=(16, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(im)
    plt.title("im")
    plt.axis('off')
    plt.subplot(1, 3, 2)
    plt.imshow(im1)
    plt.title("im1")
    plt.axis('off')
    plt.subplot(1, 3, 3)
    plt.imshow(diff3)
    plt.title("różnica im1 - im")
    plt.axis('off')
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.savefig('fig1.png')
    plt.show()

    # Zad 3 - d
    """
    Różnić brak
    """

    # Zad 4 - a
    mix = mieszaj_kanaly(im)
    mix.save("mix.png")


    # Zad 4 - b
    print("mix powstał z kanałów:", rozpoznaj_mix(im, mix))

    # Zad 5
    r, g, b, a = im.split()
    r, g, b = im.convert("RGB").split()

    """
    Obraz jest w trybie RGBA wiec funckaj wwyrzca error!!!
    """
