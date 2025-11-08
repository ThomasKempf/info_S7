import os
import copy
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from modeles2 import Global

NAME = 'reducteur'
PATH = '.\\'
LIGNE_TITRE = 2
colonne_DEPART = 2 # numero de colonne de la premiere valeur
NBR_colonne_SEPRARATION = 1 # nombre de colonne separant les train
NBR_colonne_TRAIN = 3 # nombre de colonne pris par un train


class Xlsx_file():
    def __init__(self) -> None:
        self._fichier_excel = os.path.join(PATH, f"{NAME}.xlsx")
        self._wb = Workbook()
        self._ws = self._wb.active


    def _ecrire_liste_colonne(self, liste, ligne_depart, colonne):
        for i, valeur in enumerate(liste):
            self._ws.cell(row=ligne_depart + i, column=colonne, value=valeur)


    def _fusionner_cells(self, ligne, colonne_depart, colonne_fin):
        start_letter = get_column_letter(colonne_depart)
        end_letter = get_column_letter(colonne_fin)

        self._ws.merge_cells(f"{start_letter}{ligne}:{end_letter}{ligne}")

    def save(self):
        self._wb.save(self._fichier_excel)


class Global():
    def __init__(self) -> None:
        self.titre = 'parametre globale'
        self.description = {'vitesse_entree': 0,
                            'puissance_entree': 0,
                            'couple_sortie': 0
                    }
        self.unitee = ['RPM','kW','Nm']


    def _make_property(attr_name):   
        def getter(self):
            return getattr(self, f"_{attr_name}") # Retourne la valeur
        def setter(self, value):
            setattr(self, f"_{attr_name}", value) # Modifie la valeur
        return property(getter, setter)
    titre = _make_property("titre") 
    description = _make_property("description") 
    unitee = _make_property("unitee")


class Train(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'train_{num}'
        self.description = {
            'vitesse_entree': 0,
            'puissance_entree': 0,
            'couple_sortie': 0,
            'rendement': 0,
            'entraxe': 0,
            'resistance_elastique': 0,
            'k': 0,
            'effort_tangenciel': 0,
            'module':0,
            'engrenage1_rayon_p': 0,
		    'engrenage1_nbr_dents': 0,
		    'engrenage2_rayon_p': 0,
		    'engrenage2_nbr_dents': 0,
        }
        self.unitee = [
            'RPM',
            'W',
            'Nm',
            '%',
            'mm',
            'Mpa',
            ' ',
            'N',
            ' ',
            'mm',
            ' ',
            'mm',
            ' '
            ]


class ProjetXlsx(Xlsx_file):
    def __init__(self,param_global:Global) -> None:
        super().__init__()
        # ecriture des parametre globale
        self._param = [copy.deepcopy(param_global)]
        self._ecrire_valeur(self._param[0],colonne_DEPART)
        self.save
    

    def ecrire_description_simple(self,param,num):
        colonne_unitee = colonne_DEPART + num*(NBR_colonne_SEPRARATION + NBR_colonne_TRAIN)
        colonne_valeur = colonne_unitee + 1
        if num == len(self._param): # si num est égal à la longueur c'est que le train n'est pas incorporé
            self._param.append(copy.deepcopy(param))
            self._ecrire_valeur(self._param[num],colonne_unitee)
        elif num < len(self._param):
            for i, key in enumerate(param.description, start=1):
                if param.description[key] != self._param[num].description[key]:
                    ligne = LIGNE_TITRE + i
                    self._ws.cell(row=ligne, column=colonne_valeur, value=param.description[key])
                    self._param[num].description[key] = param.description[key]

    
    def ecrire_description_ogjet_multiple(self,param,num):  
        colonne_unitee = colonne_DEPART + num*(NBR_colonne_SEPRARATION + NBR_colonne_TRAIN)
        colonne_valeur = colonne_unitee + 1                   
        decalage = 0    
        if num == len(self._param): # si num est égal à la longueur c'est que le train n'est pas incorporé     
            self._param.append(copy.deepcopy(param.description))
            for key in self._param[num]:
                self._ecrire_valeur(self._param[num][key],colonne_unitee,decalage)
                decalage = decalage + len(self._param[num][key].unitee) + 1
            self._ws.cell(row=LIGNE_TITRE, column=colonne_unitee, value=param.titre)
        elif num < len(self._param):
            param_des = param.description
            for global_key in self._param[num]:
                print('selfparam:',self._param[num][global_key].description)  
                print('param',param.description[global_key].description)
                for i, key in enumerate(param_des[global_key].description, start=1):
                    print(global_key,key)
                    if param_des[global_key].description[key] != self._param[num][global_key].description[key]:
                        print('hello')
                        ligne = LIGNE_TITRE + decalage +i
                        self._ws.cell(row=ligne, column=colonne_valeur, value=param_des[global_key].description[key])
                        self._param[num][global_key].description[key] = param_des[global_key].description[key]
                decalage = decalage + len(self._param[num][global_key].unitee) + 1


    def _ecrire_valeur(self,param:dict[int],colonne_description:int,decalage_ligne:int=0):
        ligne = LIGNE_TITRE + decalage_ligne
        liste_valeur = list(param.description.values())
        liste_description = list(param.description.keys())
        liste_globale = [param.titre] + liste_description
        self._ecrire_liste_colonne(liste_globale,ligne,colonne_description) # ecrit titre + description
        self._fusionner_cells(ligne,colonne_description,colonne_description+2)
        self._ecrire_liste_colonne(liste_valeur,ligne+1,colonne_description+1)
        self._ecrire_liste_colonne(param.unitee,ligne+1,colonne_description+2)

if __name__ == '__main__':

    param_global = Global()
    param_global.description['vitesse_entree'] = 3
    test = ProjetXlsx(param_global)
    train_1 = Train(1)
    test.ecrire_description_simple(train_1,1)
    train_1.description['vitesse_entree'] = 4
    test.ecrire_description_simple(train_1,1)
    train_2 = Train(2)
    train_2.description['rendement'] = 8
    test.ecrire_description_simple(train_2,2)
    test.save()
