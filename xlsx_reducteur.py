import os
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

NAME = 'reducteur'
PATH = '.\\'
LIGNE_TITRE = 2
COLONE_DEPART = 2


class Xlsx_file():
    def __init__(self) -> None:
        self._fichier_excel = os.path.join(PATH, f"{NAME}.xlsx")
        self._wb = Workbook()
        self._ws = self._wb.active


    def _ecrire_liste_colonne(self, liste, ligne_depart, colonne):
        for i, valeur in enumerate(liste):
            self._ws.cell(row=ligne_depart + i, column=colonne, value=valeur)


    def _fusionner_cells(self, ligne, colone_depart, colone_fin):
        start_letter = get_column_letter(colone_depart)
        end_letter = get_column_letter(colone_fin)

        self._ws.merge_cells(f"{start_letter}{ligne}:{end_letter}{ligne}")

    def save(self):
        self._wb.save(self._fichier_excel)


class Global():
    def __init__(self) -> None:
        self._titre = 'parametre globale'
        self._description = {'vitesse entree': 0,
                            'puissance entree': 0,
                            'couple sortie': 0
                    }
        self._unitee = ['RPM','kW','Nm']


    def _make_property(attr_name):   
        def getter(self):
            return getattr(self, f"_{attr_name}") # Retourne la valeur
        def setter(self, value):
            setattr(self, f"_{attr_name}", value) # Modifie la valeur
        return property(getter, setter)
    titre = _make_property("titre") 
    description = _make_property("description") 
    unitee = _make_property("unitee")


class ProjetXlsx(Xlsx_file):
    def __init__(self,param_global:Global) -> None:
        super().__init__()
        # ecriture des parametre globale
        self._param = [param_global]
        self._ecrire_valeur( self._param[0],COLONE_DEPART)
        self.save
    

    def ecrire_train(self,description,num):
        if num == len(self._description): # si num est égal à la longueur c'est que le train n'est pas incorporé
            self._description.append(description)
            self._param.append(description)
            self._ecrire_valeur()
             


    def _ecrire_valeur(self,param,colone_description):
        liste_valeur = list(param.description.values())
        liste_description = list(param.description.keys())
        liste_globale = [param.titre] + liste_description
        self._ecrire_liste_colonne(liste_globale,LIGNE_TITRE,colone_description) # ecrit titre + description
        self._fusionner_cells(LIGNE_TITRE,colone_description,colone_description+2)
        self._ecrire_liste_colonne(liste_valeur,LIGNE_TITRE+1,colone_description+1)
        self._ecrire_liste_colonne(param.unitee,LIGNE_TITRE+1,colone_description+2)

if __name__ == '__main__':

    param_global = Global()
    param_global.description['vitesse entree'] = 3
    test = ProjetXlsx(param_global)
    test.save()
