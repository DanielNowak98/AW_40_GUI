import os
import pathlib
from tkinter import messagebox
from datetime import datetime
from pathlib import Path
import json


di = {}
obd_codes = []
scope_data = []
VIN = ""
Kilometerstand = ""
Date = ""

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