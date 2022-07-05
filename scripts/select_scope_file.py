'''
Funktion zum Einlesen des Osciloscope Files.
    Input: CSV-Datei

        Zeit;Kanal A
        (s);(v)
        0,00000;12,00000

    Output: 
        scope_data: Liste bestehend aus den Kanal A Daten des Osciloscopes

        "Messdaten": [["12,30192000"], ["12,30192000"], ["12,30192000"]

'''
from tkinter import filedialog as fd
import pandas as pd
import numpy as np
from pathlib import Path
import tkinter as tk

def select_scope_file():

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
