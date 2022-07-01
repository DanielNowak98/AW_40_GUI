'''
GUI Für das Autowerkstatt 4.0 Projekt

@author DanielNowak98

'''
import tkinter as tk
import json
from tkinter import filedialog as fd
from tkinter import messagebox
from parse import Parse_OBD
import pandas as pd
import numpy as np
import pathlib
from pathlib import Path
from datetime import datetime
import os
from PIL import ImageTk, Image



di = {}
obd_codes = []
scope_data = []
VIN = ""
Kilometerstand = ""
Date = ""
Kilometerstand = ""


def change_symptom_value(i,di):
    '''Checkfunktion. Diese Funktion stellt den Dictionary-Eintrag von "No" auf "Yes".'''
    if di[i] == False:
        di [i] = True
    return di
    

def symptome():
    '''Öffnet ein neues Fenster, in dem die Symptome zur Checkbox Auswahl liegen.'''
    global di

    window = tk.Toplevel(root)
    window.title("Symptome")
    window.geometry("400x400")
    root.eval(f'tk::PlaceWindow {str(window)} center')
    window.iconbitmap('prolab (1).ico')
    

    symptome = ["1","2","3","4","5","6","7","8","9","10","11","12"]
    

    # Symtpome innerhalb des dictionarys werden auf "No" gesetzt.
    for i in symptome:
        di[i] = False
    
    # 12 Checkboxen werden in 3 Spalten gesetzt
    for i in range(0, 12):
        if i % 3 == 0:
            checkbox = tk.Checkbutton(window, text=symptome[i], variable=i, command=lambda i=symptome[i]: change_symptom_value(i,di))
            checkbox.grid(row=i // 3, column=0)
        elif i % 3 == 1:
            checkbox = tk.Checkbutton(window, text=symptome[i], variable=i, command=lambda i=symptome[i]: change_symptom_value(i,di))
            checkbox.grid(row=i // 3, column=1)
        else:
            checkbox = tk.Checkbutton(window, text=symptome[i], variable=i, command=lambda i=symptome[i]: change_symptom_value(i,di))
            checkbox.grid(row=i // 3, column=2)
    
    # Knopf zum schließen des Fensters
    button = tk.Button(window, text="Close", command=window.destroy)
    button.grid(column=3, row=9)

    return di


def select_obd_file():
    '''
    Funktion zum einlesen des OBD-Logfiles. Rückgabewerte sind, bei richtig ausgewählter Datei die obd Fehlercodes als Liste, sowie die VIN als String. 
    '''
    obd = Parse_OBD()
    filename = fd.askopenfilename()
    global obd_codes
    global VIN
    global Date
    global Kilometerstand

    MsgBox = tk.messagebox.askquestion('Exit App','Richtige Datei ausgewählt? \n' + filename ,icon = 'question')

    if MsgBox == 'yes':
      ### Hier wird die Datei im angegebenen Pfad in ein JSON File gelegt
      
      obd_codes = obd.get_Fehlercodes(filename)

      VIN = obd.get_Fahrzeugident(filename)

      Date = obd.get_Datetime(filename)

      Kilometerstand = obd.get_Kilometerstand(filename)



    else:
      ### Hier wird nach der neuen Datei gefragt, danach wird sie gespeichert. 
        filename = fd.askopenfilename()

    
    

def select_scope_file():
    '''Funktion zum einlesen der CSV-Dateien. Bei richtig ausgewählter Datei werden die Messdaten in ein Datafram gelegt, welches weiterhin in ein
       Dictionary geschrieben wird.
    '''
    filename = fd.askopenfilename()
    global scope_data

    MsgBox = tk.messagebox.askquestion('Exit App','Richtige Datei ausgewählt? \n' + filename ,icon = 'question')
    

    if MsgBox == 'yes':
      ### Hier wird die Datei im angegebenen Pfad in ein JSON File gelegt
      path = Path(filename)
      df = pd.read_csv(path, sep = ';') #.values
      df = df.drop('Zeit', 1)
      df = df.drop(0)
      scope_data = df.to_numpy()
      scope_data = np.array(scope_data).tolist()

    else:
      ### Hier wird nach der neuen Datei gefragt, danach wird sie gespeichert. 
        filename = fd.askopenfilename()


def Messungen():
    '''Öffnet ein neues Fenster, in dem die Messungen abgelegt werden.'''

    window = tk.Toplevel(root)
    window.title("Messungen")
    root.eval(f'tk::PlaceWindow {str(window)} center')
    window.iconbitmap('prolab (1).ico')
    window.geometry("275x80")

    label = tk.Label(window, text="OBD-Protokoll")
    label.grid(column=0, row=0, sticky="nsew")

    button = tk.Button(window, text="Logfile auswählen", command=lambda: select_obd_file())
    button.grid(column=1, row=0, sticky="nsew")

    label = tk.Label(window, text="Picoscope-Datei")
    label.grid(column=0, row=1, sticky="nsew")

    button = tk.Button(window, text="Messung auswählen", command=lambda: select_scope_file())
    button.grid(column=1, row=1, sticky="nsew")

    button = tk.Button(window, text="schließen", command=window.destroy)
    button.grid(column=2, row=2)

def get_data():

    ''' Funktion zum Auslesen der Eingabefelder der GUI für:

        a = Werkstattname
        b = PLZ
        c = WerkstattID
        d = MitarbeiterID

    '''
    a = name.get()
    b = plz.get()
    c = plz.get()
    d = MitarbeiterID.get()

    return a, b, c, d
    
def data_to_json(root):
    ''' Sammelt Daten aus Eingabefeldern. Diese Daten werden in ein JSON File gelegt (data)'''
    a,b,c,d = get_data()
    global di
    global scope_data
    global VIN
    global Date
    global Kilometerstand

    if a == "": #wenn eingabefeld leer ist, wird eine Fehlermeldung ausgegeben
        messagebox.showinfo("", "Eingabefelder leer, bitte ausfüllen! ")
        return

    data = {'Datum': Date,
            'VIN': VIN,
            'Kilometerstand': Kilometerstand,
            'Werkstattname':a, 
            'PLZ':b,
            'WerkstattID':c, 
            'MitarbeiterID':d,
            'Symptome':di,
            'Fehlercodes':obd_codes,
            'Abtastrate':len(scope_data),
            'Messdaten':scope_data,
            }
    ## Pfad in dem das skript liegt herausfinden
    cur = pathlib.Path(__file__).parent.resolve()

    Messdatenordner = str(cur) + "\\Messdaten"
    Messdatenordner_Pfad = pathlib.Path(Messdatenordner)


    if not os.path.exists(Messdatenordner_Pfad):
        os.makedirs(Messdatenordner_Pfad)
    
    datum = datetime.today().strftime('%Y-%m-%d')

    Messordner_datum = str(Messdatenordner_Pfad) + "\\" +str(datum)
    Messordner_datum_Pfad = pathlib.Path(Messordner_datum)

    if not os.path.exists(Messordner_datum_Pfad):
        os.makedirs(Messordner_datum_Pfad)

    ## neuen json file namen generieren
    json_file_name = str(Messordner_datum_Pfad) + "\\" +  str(VIN) + "_"+str(a) +".json"

    save_dir = Path(json_file_name)

    with open(save_dir, 'a') as f:
        json.dump(data, f)

    root.destroy()



    

######################################## - Hauptfenster - ########################################
''' Hauptfenster wird geöffnet und definiert'''

root = tk.Tk()
root.title("AW40")
root.geometry("350x180")
root.iconbitmap('prolab (1).ico')

root.eval('tk::PlaceWindow . center')


image=Image.open('aw40_lmis.png')
img=image.resize((80, 80))
my_img=ImageTk.PhotoImage(img)
label = tk.Label(root, image=my_img)
label.grid(column=3, row=3, rowspan= 3, padx = 1, columnspan= 2)

label = tk.Label(root, text="Werkstattname")
label.grid(column=0, row=0, sticky="nsew")

Werkstattname = tk.StringVar()
name = tk.Entry(root, textvariable=Werkstattname)
name.grid(column=1, row=0, sticky="nsew")


label = tk.Label(root, text="PLZ")
label.grid(column=0, row=2, sticky="nsew")


plz = tk.Entry(root, )
plz.grid(column=1, row=2, sticky="nsew")


label = tk.Label(root, text="WerksstattID")
label.grid(column=0, row=3, sticky="nsew")


plz = tk.Entry(root)
plz.grid(column=1, row=3, sticky="nsew")


label = tk.Label(root, text="Mitarbeiter ID")
label.grid(column=0, row=4, sticky="nsew")


MitarbeiterID = tk.Entry(root)
MitarbeiterID.grid(column=1, row=4, sticky="nsew")


label = tk.Label(root, text="Symptome")
label.grid(column=0, row=5, sticky="nsew")


button = tk.Button(root, text="Symptome", command=lambda: symptome())
button.grid(column=1, row=5, sticky="nsew")


label = tk.Label(root, text="Messungen")
label.grid(column=0, row=6, sticky="nsew")


button = tk.Button(root, text="Messungen", command=lambda: Messungen())
button.grid(column=1, row=6, sticky="nsew")


button = tk.Button(root, text="Speichern und beenden", command=lambda: data_to_json(root))
button.grid(column=3, row=9, sticky="nsew")

root.mainloop()