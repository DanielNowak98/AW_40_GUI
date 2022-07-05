"""
GUI Für das Autowerkstatt 4.0 Projekt

@author DanielNowak98

"""
import json
import os
import pathlib
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog as fd
from tkinter import messagebox
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
from parse import Parse_OBD

LMIS_ICON = '/img/aw40_lmis.png'
PROLAB_ICON = '/img/prolab.ico'

di = {}
obd_codes = []
scope_data = []
VIN = ""
Kilometerstand = ""
Date = ""



def select_obd_file():
    """
    Funktion zum einlesen des OBD-Logfiles. Rückgabewerte sind, bei richtig ausgewählter Datei die obd Fehlercodes
    als Liste, sowie die VIN als String.
    """
    obd = Parse_OBD()
    filename = fd.askopenfilename()
    global obd_codes
    global VIN
    global Date
    global Kilometerstand

    MsgBox = tk.messagebox.askquestion('Exit App', 'Richtige Datei ausgewählt? \n' + filename, icon='question')

    if MsgBox == 'yes':
        # Hier wird die Datei im angegebenen Pfad in ein JSON File gelegt
        obd_codes = obd.get_Fehlercodes(filename)
        VIN = obd.get_Fahrzeugident(filename)
        Date = obd.get_Datetime(filename)
        Kilometerstand = obd.get_Kilometerstand(filename)
    else:
        # Hier wird nach der neuen Datei gefragt, danach wird sie gespeichert.
        filename = fd.askopenfilename()


def select_scope_file():
    """
    Funktion zum einlesen der CSV-Dateien. Bei richtig ausgewählter Datei werden die Messdaten in ein Dataframe
    gelegt, welches weiterhin in ein Dictionary geschrieben wird.
    """
    filename = fd.askopenfilename()
    global scope_data

    MsgBox = tk.messagebox.askquestion('Exit App', 'Richtige Datei ausgewählt? \n' + filename, icon='question')

    if MsgBox == 'yes':
        ## Hier wird die Datei im angegebenen Pfad in ein JSON File gelegt
        path = Path(filename)
        df = pd.read_csv(path, sep=';')  # .values
        df = df.drop('Zeit', 1)
        df = df.drop(0)
        scope_data = df.to_numpy()
        scope_data = np.array(scope_data).tolist()

    else:
        ## Hier wird nach der neuen Datei gefragt, danach wird sie gespeichert.
        filename = fd.askopenfilename()


def Messungen(root):
    """
    Öffnet ein neues Fenster, in dem die Messungen abgelegt werden.
    """
    window = tk.Toplevel(root)
    window.title("Messungen")
    root.eval(f'tk::PlaceWindow {str(window)} center')
    img = ImageTk.PhotoImage(file=str(pathlib.Path(__file__).parent.resolve()) + PROLAB_ICON)
    window.tk.call('wm', 'iconphoto', root._w, img)

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


def get_data(name, plz, MitarbeiterID):
    """
    Funktion zum Auslesen der Eingabefelder der GUI für:
        a = Werkstattname
        b = PLZ
        c = WerkstattID
        d = MitarbeiterID
    """
    a = name.get()
    b = plz.get()
    c = plz.get()
    d = MitarbeiterID.get()

    return a, b, c, d


def data_to_json(root, name, plz, MitarbeiterID):
    """
    Sammelt Daten aus Eingabefeldern. Diese Daten werden in ein JSON File gelegt (data)
    """
    a, b, c, d = get_data(name, plz, MitarbeiterID)
    global di
    global scope_data
    global VIN
    global Date
    global Kilometerstand

    if a == "":  # wenn eingabefeld leer ist, wird eine Fehlermeldung ausgegeben
        messagebox.showinfo("", "Eingabefelder leer, bitte ausfüllen! ")
        return

    data = {'Datum': Date,
            'VIN': VIN,
            'Kilometerstand': Kilometerstand,
            'Werkstattname': a,
            'PLZ': b,
            'WerkstattID': c,
            'MitarbeiterID': d,
            'Symptome': di,
            'Fehlercodes': obd_codes,
            'Abtastrate': len(scope_data),
            'Messdaten': scope_data,
            }
    # Pfad in dem das skript liegt herausfinden
    cur = pathlib.Path(__file__).parent.resolve()


    Messdatenordner = str(cur) + "\\Messdaten"
    Messdatenordner_Pfad = pathlib.Path(Messdatenordner)

    if not os.path.exists(Messdatenordner_Pfad):
        os.makedirs(Messdatenordner_Pfad)

    datum = datetime.today().strftime('%Y-%m-%d')

    Messordner_datum = str(Messdatenordner_Pfad) + "\\" + str(datum)
    Messordner_datum_Pfad = pathlib.Path(Messordner_datum)

    if not os.path.exists(Messordner_datum_Pfad):
        os.makedirs(Messordner_datum_Pfad)

    # neuen json file namen generieren
    json_file_name = str(Messordner_datum_Pfad) + "\\" + str(VIN) + "_" + str(a) + ".json"

    save_dir = Path(json_file_name)

    with open(save_dir, 'a') as f:
        json.dump(data, f)

    root.destroy()


def run_gui():
    """
    Hauptfenster wird geöffnet und definiert
    """
    root = tk.Tk()
    root.title("AW40")
    root.geometry("350x160")

    img = ImageTk.PhotoImage(file=str(pathlib.Path(__file__).parent.resolve()) + PROLAB_ICON)
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.eval('tk::PlaceWindow . center')

    image = Image.open(str(pathlib.Path(__file__).parent.resolve()) + LMIS_ICON)
    img = image.resize((80, 80))
    my_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=my_img)
    label.grid(column=3, row=0, rowspan=6, padx=1,pady=4, columnspan=3)

    label = tk.Label(root, text="Werkstattname")
    label.grid(column=0, row=0, pady=2, sticky="nsew")

    Werkstattname = tk.StringVar()
    name = tk.Entry(root, textvariable=Werkstattname)
    name.grid(column=1, row=0,pady=2, sticky="nsew")

    label = tk.Label(root, text="PLZ")
    label.grid(column=0, row=2,pady=2, sticky="nsew")

    plz = tk.Entry(root, )
    plz.grid(column=1, row=2,pady=2, sticky="nsew")

    label = tk.Label(root, text="WerksstattID")
    label.grid(column=0, row=3,pady=2, sticky="nsew")

    plz = tk.Entry(root)
    plz.grid(column=1, row=3,pady=2, sticky="nsew")

    label = tk.Label(root, text="Mitarbeiter ID")
    label.grid(column=0, row=4,pady=2, sticky="nsew")

    MitarbeiterID = tk.Entry(root)
    MitarbeiterID.grid(column=1, row=4,pady=2, sticky="nsew")

    label = tk.Label(root, text="Messungen")
    label.grid(column=0, row=6,pady=2, sticky="nsew")

    button = tk.Button(root, text="Messungen", command=lambda: Messungen(root))
    button.grid(column=1, row=6,pady=2, sticky="nsew")

    button = tk.Button(root, text="Speichern und beenden", command=lambda: data_to_json(root, name, plz, MitarbeiterID))
    button.grid(column=3, sticky="s")

    root.mainloop()


if __name__ == '__main__':
    run_gui()
