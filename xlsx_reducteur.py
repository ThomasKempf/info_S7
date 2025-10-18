import os
from openpyxl import Workbook

NAME = 'reducteur'
PATH = '.\\'
LIGNE_TITRE = 2
COLONE_DEPART = 2

GLOBAL = {
    'titre': 'parametre globale',
    'description': ['vitesse entree','puissance entree','couple sortie'],
    'unitee': ['RPM','kW','Nm']

}

class Xlsx_file():
    def __init__(self) -> None:
        self._fichier_excel = os.path.join(PATH, f"{NAME}.xlsx")
        self._wb = Workbook()
        self._ws = self._wb.active

    def ecrire_liste_colonne(self, liste, ligne_depart, colonne):
        for i, valeur in enumerate(liste):
            self._ws.cell(row=ligne_depart + i, column=colonne, value=valeur)

    def save(self):
        self._wb.save(self._fichier_excel)


class ProjetXlsx(Xlsx_file):
    def __init__(self,vitesse_entree,puissance_entree,couple_sortie) -> None:
        super().__init__()
        # ecriture des parametre globale
        valeur = [vitesse_entree,puissance_entree,couple_sortie]
        self._ecrire_valeur(GLOBAL,valeur,COLONE_DEPART)
        self.save
    

    def _ecrire_valeur(self,param,liste_valeur,colone_description):
        liste_globale = [param['titre']] + param['description']
        self.ecrire_liste_colonne(liste_globale,LIGNE_TITRE,colone_description)
        self.ecrire_liste_colonne(liste_valeur,LIGNE_TITRE+1,colone_description+1)
        self.ecrire_liste_colonne(param['unitee'],LIGNE_TITRE+1,colone_description+2)

if __name__ == '__main__':

    test = ProjetXlsx(1,1,1)
    test.save()
