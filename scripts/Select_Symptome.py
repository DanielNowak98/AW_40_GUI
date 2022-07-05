'''
Funktion, welche eine Auswahl von Symptomen ermöglicht.
Als Ausgabe dieser Funktion wird ein Dictionary zurückgegeben, welches die Symptome als Keys und einen boolean als Values enthält.
Diese sind per default auf False gesetzt.
'''


di = {}
PROLAB_ICON = '/img/prolab.ico'


import tkinter as tk
import pathlib
from pathlib import Path
from PIL import ImageTk, Image


def change_symptom_value(i,di):
    '''Checkfunktion. Diese Funktion stellt den Dictionary-Eintrag von "No" auf "Yes".'''
    if di[i] == False:
        di [i] = True
    return di


def symptome(root):
    """
    Öffnet ein neues Fenster, in dem die Symptome zur Checkbox Auswahl liegen.
    """
    global di

    window = tk.Toplevel(root)
    window.title("Symptome")
    window.geometry("400x400")
    root.eval(f'tk::PlaceWindow {str(window)} center')
    img = ImageTk.PhotoImage(file=str(pathlib.Path(__file__).parent.resolve()) + PROLAB_ICON)
    window.tk.call('wm', 'iconphoto', root._w, img)

    symptome = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    # Symtpome innerhalb des dictionarys werden auf "No" gesetzt.
    for i in symptome:
        di[i] = False

    # 12 Checkboxen werden in 3 Spalten gesetzt
    for i in range(0, 12):
        if i % 3 == 0:
            checkbox = tk.Checkbutton(window, text=symptome[i], variable=i,
                                      command=lambda i=symptome[i]: change_symptom_value(i, di))
            checkbox.grid(row=i // 3, column=0)
        elif i % 3 == 1:
            checkbox = tk.Checkbutton(window, text=symptome[i], variable=i,
                                      command=lambda i=symptome[i]: change_symptom_value(i, di))
            checkbox.grid(row=i // 3, column=1)
        else:
            checkbox = tk.Checkbutton(window, text=symptome[i], variable=i,
                                      command=lambda i=symptome[i]: change_symptom_value(i, di))
            checkbox.grid(row=i // 3, column=2)

    # Knopf zum schließen des Fensters
    button = tk.Button(window, text="Close", command=window.destroy)
    button.grid(column=3, row=9)

    return di
