import requests, xmltodict
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk #Vooraf pillow inladen, aangezien de originele PIL niet werkt op python 3.x

stationsLijst = []

#Kolomnamen voor weergave vertrektijden
columns = ("Tijd", "Vervoerder", "Soort trein", "Bestemming", "Spoor")

# Checken of configuratie file aanwezig is
try:
    with open("machineLocatie.csv") as file:
        standaardStation = file.readline()
        standaardStation = standaardStation.rstrip()
        if standaardStation is "":
            messagebox._show("Fout!", "Geen station ingevoerd in machineLocatie.csv", _icon="error")
            quit()

except FileNotFoundError:
    messagebox._show("Fout!", "machineLocatie.csv niet gevonden!", _icon="error")
    quit()

# Class voor de buttons en frame
class ReisInformatie:

    def __init__(self, master):
        frame = Frame(master)
        frame.grid(row=3, column=2, sticky=S)

        self.loadButton = Button(frame, text="Haal tijden op", command=getVertrekTijden)
        self.loadButton.pack(side=LEFT)
        self.loadButton.configure(font=("Arial", 15, "bold"))
        self.loadButton.config(background="#003399")
        self.loadButton.config(foreground="white")

        self.quitButton = Button(frame, text="Stoppen", command=frame.quit)
        self.quitButton.pack(side=RIGHT)
        self.quitButton.configure(font=("Arial", 15, "bold"))
        self.quitButton.config(background="red")
        self.quitButton.config(foreground="white")


# aanvragen van stations bij de NS, en deze wegzetten in de stationslijst
def getStationsLijst():
    auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
    r = requests.get("http://webservices.ns.nl/ns-api-stations-v2", auth=auth)
    
    # omzetten van XML naar een dict
    stationsXML = xmltodict.parse(r.text)
    for naam in stationsXML['Stations']['Station']:
        if naam['Land'] == "NL":
            langeNaam = naam['Namen']['Lang']
            stationsLijst.append(langeNaam)


# Table fill functie
def getVertrekTijden():
    
    # Mocht de vrije input niet kloppen, wordt er een messagebox weergegeven    
    if station.get() not in stationsLijst:
        messagebox._show("Fout", "Station niet herkend")
    else:
        colorCondition = True
        # Tabel clear
        for i in tree.get_children():
            tree.delete(i)
        try:
            # aanvraag vertrektijden bij NS, en omzetten naar dict
            voorkeuren = {'station': station.get()}
            auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
            r = requests.get("http://webservices.ns.nl/ns-api-avt", params=voorkeuren, auth=auth)
            vertrekXML = xmltodict.parse(r.text)
            
            # Columns in de tabel plaatsen
            for column in columns:
                tree.heading(column, text=column.title())
            
            # Tabel opvullen met info uit de dict
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
        
        # Error voor als er geen reisdata gevonden is, komt vaak voor bij 'NS-bus' stations
        except KeyError:
            tree.insert('', 'end', values=("Geen", "reisdata", "gevonden", "probeer", "opnieuw"), tags = ('rood',))


root = Tk()
root.title("NS Vertrektijden")
getStationsLijst() # eenmalig aanvragen van stationslijst

station = StringVar(root)
station.set(standaardStation)

# Selecteren van stations in de combobox
beginStation = ttk.Combobox(root, textvariable=station, font=('Arial', 13))
beginStation.grid(row=2, column=2)
beginStation['values'] = stationsLijst

# Locatie van tabel in frame
tree = ttk.Treeview(columns=columns, show="headings")
tree.grid(row=1, column=1, rowspan=3)

# Scrollbar in tree view
scrollbar = Scrollbar(root)
scrollbar.grid(sticky=NE + S,row=1,column=1, rowspan=3)
scrollbar.config(command = tree.yview )
tree.configure(yscrollcommand=scrollbar.set)
root.configure(background='#fece22')

# Weergave NS logo
try:
    image = Image.open("NS-thumb.png")
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo, background='#fece22')
    label.grid(row=1, column=2)
except FileNotFoundError:   # Indien file niet aanwezig
    pass

b = ReisInformatie(root)
tree.tag_configure('blauw', background='#D7E2E6', foreground='#003399',font=('Arial', 13))
tree.tag_configure('wit', background='white', foreground='#003399',font=('Arial', 13))
tree.tag_configure('rood', background='red', foreground='white',font=('Arial', 13))
getVertrekTijden()

root.mainloop()
