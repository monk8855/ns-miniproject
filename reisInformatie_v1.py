import requests,xmltodict
from tkinter import *
from tkinter import ttk
stationsLijst = []
vertrekXML = {}

def getStationsLijst():
    auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
    r = requests.get("http://webservices.ns.nl/ns-api-stations-v2", auth=auth)
    stationsXML = xmltodict.parse(r.text)
    for naam in stationsXML['Stations']['Station']:
        if naam['Land'] == "NL":
            langeNaam = naam['Namen']['Lang']
            stationsLijst.append(langeNaam)
    return stationsXML

def getVertrekTijden(station):
    global vertrekXML
    getStationsLijst()
    if station not in stationsLijst:
        print("Station niet herkend")
    else:
        voorkeuren = {'station':station}
        auth = ('bob.vanaanhold@student.hu.nl', '9MrYI28kCZWxrk7cBexYHGSEaNujLq7SQDcuSI_HUlwf8N4GteMP4g')
        r = requests.get("http://webservices.ns.nl/ns-api-avt",params=voorkeuren, auth=auth)
        vertrekXML = xmltodict.parse(r.text)
        if False:
            print('Dit zijn de vertrekkende treinen:')
            for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
                eindbestemming = vertrek['EindBestemming']
                vertrektijd = vertrek['VertrekTijd']
                vertrektijd = vertrektijd[11:16]
                print('Om '+vertrektijd+' vertrekt een trein naar '+ eindbestemming)
        return vertrekXML


#def toDict(a):
#    global legeDict
#    legeDict = a

def main():
    getStationsLijst()
    root = Tk()
    root.title("NS Reisinformatie")
    stationvar = StringVar()
    beginStation = ttk.Combobox(root,textvariable=stationvar)
    beginStation.pack()
    beginStation['values'] = stationsLijst

    widget = Button(None, text ='Klik hier maar eens.')
    widget.pack()
    widget.bind('<Button-1>', print('Hello!!'))

    loadButton = ttk.Button(root,text="Load")
    loadButton.pack()
    loadButton.config(command=lambda: print(getVertrekTijden(beginStation.get())))
    root.mainloop()

main()

