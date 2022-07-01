import re
import pandas as pd

"""
@edit: Daniel
"""


class Parse_OBD:

    def __init__(self):
        self.filenames = None
        self.Fahrzeugident = None
        self.Kilometerstand = None
        self.Fahrzeugtyp = None
        self.Fehlercodes = []
        self.filename = None
        self.iso_filename = None

    def get_Datetime(self, filename):
        self.filename = filename

        with open(filename) as f:
            for line in f:
                datum = line
                break
        return datum

    def get_Fahrzeugident(self, filename):
        self.filename = filename
        V_IN = 'Fahrzeug-Ident.-Nr.:'

        with open(filename) as f:
            for line in f:
                if V_IN in line:
                    VIN = line.split(' ')
                    VIN = VIN[1]
                    # print("VIN = " + VIN)
                    break
        return VIN

    def get_Kilometerstand(self, filename):
        self.filenames = filename
        km = 'Kilometerstand:'

        with open(filename) as f:

            for line in f:
                if km in line:
                    km = line.split(' ')
                    km = km[5]
                    km = re.sub('km', '', km)
                    break
        return km

    def get_Fahrzeugtyp(self, filename):
        self.filename = filename
        FT = 'Fahrzeugtyp:'

        with open(filename) as f:

            for line in f:
                if FT in line:
                    FT = line.split(' ')
                    FT = FT[1]
                    print("Fahrzeugtyp = " + FT)
                    break

    def get_Fehlercodes(self, filename):

        codes = []
        self.filename = filename
        B_Codes = 'B' + '\d\d\d\d'
        P_Codes = 'P' + '\d\d\d\d'
        C_Codes = 'C' + '\d\d\d\d'
        U_Codes = 'U' + '\d\d\d\d'

        with open(filename) as f:

            for line in f:
                match_B = re.search(B_Codes, line)
                match_P = re.search(P_Codes, line)
                match_C = re.search(C_Codes, line)
                match_U = re.search(U_Codes, line)

                if match_B is not None:
                    codes.append(match_B.group())

                if match_P is not None:
                    codes.append(match_P.group())

                if match_C is not None:
                    codes.append(match_C.group())

                if match_U is not None:
                    codes.append(match_U.group())

        return codes

    def get_iso_df(self, iso_filename):

        self.iso_filename = iso_filename

        df1 = pd.read_csv(iso_filename)
        df1.columns = ["Error Codes", "ISO", "Sensor"]
        return df1

    def get_errorcode_df(self, filename):

        self.filename = filename
        codes = self.get_Fehlercodes(filename)

        df2 = pd.DataFrame(list(zip(codes)))
        df2.columns = ["Error Codes"]

        return df2

    def compare_df(self, iso_filename, filename):
        df1 = self.get_iso_df(iso_filename)
        df = self.get_errorcode_df(filename)

        new = df1[df1['Error Codes'].isin(df['Error Codes'])]

        new = new[['Error Codes', 'ISO']]

        return new
