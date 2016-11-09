import requests, xmltodict
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

stationsLijst = []
columns = ("Tijd", "Vervoerder", "Soort trein", "Bestemming", "Spoor")

# Checken of configuratie file aanwezig is
try:
    with open("machineLocatie.csv") as file:
        standaardStation = file.readline()
        standaardStation = standaardStation.rstrip()

except FileNotFoundError:
    messagebox._show("Fout!", "machineLocatie.csv niet gevonden!", _icon="error")
    quit()

# Class voor de buttons en frame
class ReisInformatie:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid(row=2, column=2)


        self.loadButton = Button(frame, text="Haal tijden op", command=getVertrekTijden)
        self.loadButton.pack(side=LEFT)
        self.loadButton.configure(font=("Arial", 15, "bold"))

        self.quitButton = Button(frame, text="Stoppen", command=frame.quit)
        self.quitButton.pack(side=RIGHT)
        self.quitButton.configure(font=("Arial", 15, "bold"))

        self.quitButton.config(background="red")
        self.quitButton.config(foreground="white")


        self.loadButton.config(background="#003399")
        self.loadButton.config(foreground="white")


# Functie die de stationsLijst vult.
def getStationsLijst():
    auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
    r = requests.get("http://webservices.ns.nl/ns-api-stations-v2", auth=auth)
    stationsXML = xmltodict.parse(r.text)
    for naam in stationsXML['Stations']['Station']:
        if naam['Land'] == "NL":
            langeNaam = naam['Namen']['Lang']
            stationsLijst.append(langeNaam)

# Table fill functie
def getVertrekTijden():
    # Mocht de vrije input niet kloppen word er een messagebox weergegeven
    if station.get() not in stationsLijst:
        messagebox._show("Fout", "Station niet herkend")
    else:
        colorCondition = True
        # Tabel clear
        for i in tree.get_children():
            tree.delete(i)
        try:
            #API call en xmltodict
            voorkeuren = {'station': station.get()}
            auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
            r = requests.get("http://webservices.ns.nl/ns-api-avt", params=voorkeuren, auth=auth)
            vertrekXML = xmltodict.parse(r.text)
            # Zorgt voor de coluns in de tabel
            for column in columns:
                tree.heading(column, text=column.title())
            # Vult de tabel met rijen aan info
            for trein in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
                eindBestemming = trein['EindBestemming']
                vertrekTijd = trein['VertrekTijd']
                vertrekTijd = vertrekTijd[11:16]
                vervoerder = trein['Vervoerder']
                treinSoort = trein['TreinSoort']
                vertrekSpoor = trein['VertrekSpoor']['#text']
                if trein['VertrekSpoor']['@wijziging'] == "true":
                    vertrekSpoor += " Spoor gewijzigd"
                #Rode kleur voor gewijzigde sporen
                if "Spoor gewijzigd" in vertrekSpoor:
                    tree.insert('', 'end', values=(vertrekTijd, vervoerder, treinSoort, eindBestemming, vertrekSpoor), tags = ('rood',))
                #Blauwe en wit voor opmaak
                elif colorCondition:
                    tree.insert('', 'end', values=(vertrekTijd, vervoerder, treinSoort, eindBestemming, vertrekSpoor), tags = ('blauw',))
                else:
                    tree.insert('', 'end', values=(vertrekTijd, vervoerder, treinSoort, eindBestemming, vertrekSpoor), tags = ('wit',))
                colorCondition = not colorCondition
        #Error voor als er geen reisdata gevonden is
        except KeyError:
            tree.insert('', 'end', values=("Geen", "reisdata", "gevonden", "probeer", "opnieuw"), tags = ('rood',))

# Functie in aanbouw om storingen ook te weergeven
#def getStoringen():
#    auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
#    parameters = {'station': station.get, 'actual': 'true'}
#    r = requests.get("http://webservices.ns.nl/ns-api-storingen", auth=auth, params=parameters)
#    print(r.text)


root = Tk()
root.title("NS Vertrektijden")
getStationsLijst()
station = StringVar(root)
station.set(standaardStation)
beginStation = ttk.Combobox(root, textvariable=station, font=('Arial', 13))
beginStation.grid(row=1, column=2)
beginStation['values'] = stationsLijst
tree = ttk.Treeview(columns=columns, show="headings")
tree.grid(row=1, column=1)
root.configure(background='#fece22')
b = ReisInformatie(root)
tree.tag_configure('blauw', background='#D7E2E6', foreground='#003399',font=('Arial', 13))
tree.tag_configure('wit', background='white', foreground='#003399',font=('Arial', 13))
tree.tag_configure('rood', background='red', foreground='white',font=('Arial', 13))
getVertrekTijden()
root.mainloop()
#NS logo toevoegen

