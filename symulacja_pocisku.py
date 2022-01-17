"""
Symulacja pocisku by:
    Maciej Grabowski
    Jakub Gryszczuk
    AiR 2022
"""
#zalaczenie biblioteki graficznej tkinter i jej skladnikow
from tkinter import Tk, Label, Button, Entry
#zalaczenie biblioteki graficznej do animowanych wykresow
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


#tworzenie okna aplikacji
root = Tk()
root.title("Symulacja Pocisku 1.0")
#tworzenie tytulu
myLabel = Label(root, text="Symulacja pocisku")
#wyswietlanie okien ze zmiennymi okienkowymi
myLabel.grid(row=0, column=1)
#definiowanie okna do pobierania danych
label_v0=Label(root, text="Wprowadz predkosc poczatkowa (m/s)")
label_v0.grid(row=1,column=0)
wejscie_v0 = Entry(root, width = 20, bg="white")
wejscie_v0.grid(row=1,column=1)

label_kat=Label(root, text="Wprowadz kat wystrzalu (deg)") 
label_kat.grid(row=2,column=0)
wejscie_kat = Entry(root, width = 20, bg="white")
wejscie_kat.grid(row=2,column=1)
#numeracja wierszy
global wiersz
wiersz=3
#numeracja do tekstu (nr przeszkody)
global j
j=1
#numeracja odleglosci i wysokosci
wysokosci = []
odleglosci = []
#funkcja tworzaca przeszkody o numerze i
def stworz_przeszkode (): 
    global j
    global wiersz
    #tekst
    txt1='Wysokosc przeszkody '
    txt2='Odlegosc od przeszkody '
    w=str(j)
    txt1=txt1+w
    txt2=txt2+w
    przeszkoda_txt1=Label(root, text=txt1)
    przeszkoda_txt1.grid(row=wiersz,column=0)
    przeszkoda_txt2=Label(root, text=txt2)
    przeszkoda_txt2.grid(row=wiersz,column=2)
    #okno do wpisywania wartosci
    przeszkoda_wysokosc=Entry(root, bg="white")
    przeszkoda_wysokosc.grid(row=wiersz,column=1)
    wysokosci.append(przeszkoda_wysokosc)
    przeszkoda_odleglosc=Entry(root, bg="white")
    przeszkoda_odleglosc.grid(row=wiersz,column=3)
    odleglosci.append(przeszkoda_odleglosc)
    #iteracja
    wiersz=wiersz+1
    j=j+1
#tworzenie przycisku
dodaj_przeszkode=Button(root,text="Dodaj przeszkode", command=lambda: stworz_przeszkode())
dodaj_przeszkode.grid(row = 1,column =2)
#definiowanie funkcji przycisku
def przycisk_ok():
    global j
    #pobieranie danych jako zmienne
    v0=wejscie_v0.get()
    v0=float(v0)
    kat=wejscie_kat.get()
    kat=float(kat)
    katr=kat*np.pi/180
    #definiowanie wykresu oraz wzoru funkcji
    fig, ax = plt.subplots()
    g = 9.8
    theta = katr
    t = 2 * v0 * np.sin(theta) / g
    t = np.arange(0, 0.1, 0.01)
    x = np.arange(0, 0.1, 0.01)
    line, = ax.plot(x, v0 * np.sin(theta) * x - (0.5) * g * x**2)
    y_max=(v0**2)/(2*g)
    print(y_max)
    #obliczanie zasiegu
    czas=2*v0*np.sin(katr)/9.81
    czas=float(czas)
    zasieg=v0*np.cos(katr)*czas
    zasieg=float(zasieg)
    #sprawdzanie czy wszytsko dziala poprawnie - czy dane zostaly pomyslnie wprowadzone
    iteracja=0
    while iteracja<j-1:
        print(wysokosci[iteracja].get(),' ')
        print(odleglosci[iteracja].get())
        iteracja=iteracja+1
        
    zasieg=(v0*v0)/g*np.sin(2*katr)
    #funkcja animujaca
    def animate(i):
        """zmien i by otrzymac szybsza (ale mniej precyzyjna) animacje """
        line.set_xdata(v0 * np.cos(theta) * (t + i /100.0))
        line.set_ydata(v0 * np.sin(theta) * (x + i /100.0) - (0.5) * g * (x + i / 100.0)**2)  
        return line,
    
    #ograniczanie wykresu
    plt.axis([0.0, zasieg, 0.0, y_max])
    ax.set_autoscale_on(False)
    
    plt.xlabel("Wysokosc (m)")
    plt.ylabel("Odleglosc (m)")
    
    print (zasieg)
    #ustalanie lacznej liczby klatek i wywolanie zamiaru animacji
    ani = animation.FuncAnimation(fig, animate, np.arange(1, 1000))
    #badanie przeszkod
    for i in range (j-1):
        #ustawianie odpowiedniego koloru preszkod - trafiona - czerwona, nietrafiona - zielona
        if (( float(odleglosci[i].get())*np.tan(katr)-(g/(2*((v0)**2)*(np.cos(katr))**2))*((float(odleglosci[i].get()))**2)) < (float(wysokosci[i].get()))):
            plt.vlines(float(odleglosci[i].get()),0,float(wysokosci[i].get()),colors='r')
        if (( float(odleglosci[i].get())*np.tan(katr)-(g/(2*((v0)**2)*(np.cos(katr))**2))*((float(odleglosci[i].get()))**2)) >= (float(wysokosci[i].get()))):
            plt.vlines(float(odleglosci[i].get()),0,float(wysokosci[i].get()),colors='g')
    #przedstawienie wykresu
    plt.show()
    #ustalenie sposobu zapisu i ilosci klatek na sekunde
    writergif = animation.PillowWriter(fps=24)
    ani.save('wykres.gif',writer=writergif)
    
    #sam juz nie wiem
    fig, ax = plt.subplots()
    #zakonczenie funkcji
    return None
#definiowanie funkcji przycisku oblicz i jego pozycji
oblicz_trajektorie=Button(root, text="Oblicz", command=przycisk_ok)
oblicz_trajektorie.grid(row=1,column=3)

#pozostaw okno wlaczone
root.mainloop() 

