import requests,xmltodict
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

stationsLijst = []
columns = ("Tijd", "Vervoerder", "Soort trein", "Bestemming", "Spoor")

class reisInformatie:

    def __init__(self,master):
        frame = Frame(master)
        frame.grid(row=2,column=2)

        self.loadButton = Button(frame, text="Load", command=getVertrekTijden)
        self.loadButton.pack(side=LEFT)

        self.quitButton = Button(frame,text="Quit",command=frame.quit)
        self.quitButton.pack(side=RIGHT)

        self.quitButton.config(background="#003399")
        self.quitButton.config(foreground="white")

        self.loadButton.config(background="#003399")
        self.loadButton.config(foreground="white")


def getStationsLijst():
    auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
    r = requests.get("http://webservices.ns.nl/ns-api-stations-v2", auth=auth)
    stationsXML = xmltodict.parse(r.text)
    for naam in stationsXML['Stations']['Station']:
        if naam['Land'] == "NL":
            langeNaam = naam['Namen']['Lang']
            stationsLijst.append(langeNaam)
    return stationsXML

def getVertrekTijden():
    if station.get() not in stationsLijst:
        messagebox._show("Fout","Station niet herkend")
    else:
        for i in tree.get_children():
            tree.delete(i)
        voorkeuren = {'station':station.get()}
        auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
        r = requests.get("http://webservices.ns.nl/ns-api-avt",params=voorkeuren, auth=auth)
        vertrekXML = xmltodict.parse(r.text)
        for column in columns:
            tree.heading(column, text=column.title())
        for trein in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            eindBestemming = trein['EindBestemming']
            vertrekTijd = trein['VertrekTijd']
            vertrekTijd = vertrekTijd[11:16]
            vervoerder = trein['Vervoerder']
            treinSoort = trein['TreinSoort']
            vertrekSpoor = trein['VertrekSpoor']['#text']
            if trein['VertrekSpoor']['@wijziging'] == "true":
                vertrekSpoor += " Spoor gewijzigd"
            tree.insert('', 'end', values=(vertrekTijd, vervoerder, treinSoort, eindBestemming, vertrekSpoor))
        return vertrekXML

def getStoringen():
    auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
    parameters = {'station':stations.get, 'actual':'true'}
    r = requests.get("http://webservices.ns.nl/ns-api-storingen",auth=auth,params=parameters)
    print(r.text)

root = Tk()
getStationsLijst()
station = StringVar(root)
station.set("Utrecht Centraal")
beginStation = ttk.Combobox(root, textvariable=station)
beginStation.grid(row=1,column=2)
beginStation['values'] = stationsLijst
tree = ttk.Treeview(columns= columns, show="headings")
tree.grid(row=1,column=1)
root.title("NS Vertrektijden")
root.configure(background='#fece22')
b = reisInformatie(root)
root.mainloop()
