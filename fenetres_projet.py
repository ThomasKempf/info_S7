"""
:author: Thomas Krempf-Driesbach
:date: 2025-11-05
:description:

    Ce scrypte contient la classe permetant de creer et de gerer la fenetre projet

    C'est une sous classe de Fenetre qui doit en premier etre initialiser avec PROJET 
    pour ensuite créer un par un les layouts de chaque train

    Quand un parametre change le train est remis à jours à l'aide de son objet pour ensuite rafraichir la page et le xlsx
"""


from outil_gui import Fenetre
import modeles2 as md
import xlsx_reducteur as xlsx
from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg,
    QtCore as qtc
)


# param global de la fentre generer lors du super init
PROJET = {
    'titre': 'Projet',
    'labels':['Train_1'],
    'buttons':['Fichier','Enregistrer','Aide'],
    'styleSheet':"""
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                font-size: 12px; /* Taille de police */
                font-weight: bold; /* Poids de police */
                padding: 10px 0; /* Rembourrage */
                margin-bottom: 12px; /* Espace entre les boutons */
        """
}


class FenetreProjet(Fenetre):
    def __init__(self, xlsx_file:xlsx.ProjetXlsx, train:md.Calcule_train) -> None:
        """
        créer une fenetre Projet tout en construisant les layoutes des trains

        :param xlsx_param: liste d'ogjet de parametre utiliser par le xlsx, le premier sont les parmetres global, ensuite vienne les trains
        :param xlsx_file: ogjet utiliser pour le xlsx du projet, c'est dans celui si qu'on écris les param precedents
        :param train: objet de la classe Simulation_train contenant les methode de calcule et la descritption du Train
        """
        elements = {
            'layouts':{'main':'v','train1':'v'},
            'buttons':['fichier','enregistrer','aide'],
            'toolbars':['ligne_haut']
        }
        super().__init__(PROJET,elements)
        self._methode_train = train
        self._train = train.train_1 # obj contenant toute la descritption, obj de type Train
        self._xlsx_file = xlsx_file
        self.setStyleSheet(self._param['styleSheet'])
        layout = self.genere_train()
        self.genere_toolbars()
        self.layouts['main'].addWidget(self.toolbar)
        self.layouts['main'].addLayout(layout)
        self.setLayout(self.layouts['main'])

    
    def genere_toolbars(self):
        self.toolbar = self.toolbars['ligne_haut']
        self.toolbar.setMovable(False)
        for key in self.buttons:
            print(key)
            self.buttons[key].setFlat(True)
            self.toolbar.addWidget(self.buttons[key])


    def genere_train(self) -> qtw.QVBoxLayout:
        """
        genere le layout train contenant un titre et les parametre du train

        :return: layout du train
        """
        titre = self.genere_titre_train()
        self._zone_text_train = self.genere_widget_train()
        return self.genere_layout_train(titre)


    def genere_titre_train(self) -> qtw.QLabel:
        """
        genere le label titre et le met en forme

        :return: label du titre

        **Préconditions :**
        - ``self._param['labels']`` doit être valide
        """
        titre = qtw.QLabel(*self._param['labels'])
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        titre.setFont(qtg.QFont('Arial',20, qtg.QFont.Weight.Bold)) 
        titre.setStyleSheet('color: #222; margin-bottom: 20px;padding: 8px') # Style du titre
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement
        return titre
    

    def genere_widget_train(self) -> dict[qtw.QWidget,qtw.QLineEdit]:
        """
        genere un widget et une variable associée à la valeur pour chaque paramatre du train 
        en ce basant sur les key du xlsx

        :return: dict avec le widget et la variable liée a chaque parametre de chaque sous obj

        **Préconditions :**
        - ``self._xlsx_param`` doit être valide
        """
        train_gui = {}
        description_train = self._train.description
        for global_key in description_train:
            sous_obj = {'widget':{},'variable':{}}
            sous_obj['objet'] = description_train[global_key]
            for i, (key, value) in enumerate(sous_obj['objet'].description.items()):
                unitee  = sous_obj['objet'].unitee[i]
                sous_obj['widget'][key],sous_obj['variable'][key] = self._ajout_nom_zone_texte_unitee(key,unitee,str(round(value,4)))
                sous_obj['variable'][key].setFixedWidth(60)
                sous_obj['variable'][key].setValidator(qtg.QIntValidator())
                sous_obj['variable'][key].editingFinished.connect(lambda k=key, variable=sous_obj['variable'][key], obj=sous_obj['objet']:
                    self.modifie_parametre(int(variable.text()), k,obj)) # self._zone_text_train n'existe pas encore
                train_gui[global_key] = sous_obj
        return train_gui


    def genere_layout_train(self, titre:qtw.QLabel) -> qtw.QVBoxLayout:
        """
        genere le layout vertical principal du train en y ajoutant les labels et widgets

        :param titre: label titre incérer dans le layout
        :return: layoute du train est retournée

        **Préconditions :**
        - ``self._zone_text_train`` doit être valide et contenir la key widget
        """
        layout = qtw.QVBoxLayout()
        layout.addStretch()
        layout.addWidget(titre) 
        layout.addStretch()
        for key in self._zone_text_train:
            self.ajoute(layout, list(self._zone_text_train[key]['widget'].values()))
        return layout
    

    def modifie_parametre(self, nouvelle_valeur:int, value_name:str, sous_obj:md.Global) -> None:
        """
        Met à jour un paramètre de l'objet train, puis synchronise les modifications
        dans le fichier Excel et l'interface graphique.

        :param nouvelle_valeur: Nouvelle valeur à assigner à l'attribut spécifié.
        :param value_name: Nom de l'attribut du train à modifier.
        :param sous_obj: sous objet contenant le paramaetre modifier dans sa descritpion, ex: roue type Engrenage du Train

        **Préconditions :**
        - L'attribut ``self._train`` doit contenir la descrpition de l'objet de Type Train.
        - ``_xlsx_file`` et ``self._zone_text_train`` 
          doivent être valides et contenir les clés attendues.
        """
        # met a jour l'objet train
        sous_obj.description[value_name] = nouvelle_valeur
        self._methode_train.calculer_parametres()
        # met a jour le xlsx
        self._xlsx_file.ecrire_description_ogjet_multiple(self._train,1)
        self._xlsx_file.save()
        # met a jour la fenetre
        for global_key in  self._zone_text_train:
            for key in self._zone_text_train[global_key]['variable']:
                if key != value_name:
                    self._zone_text_train[global_key]['variable'][key].setText(str(round(self._train.description[global_key].description[key],4)))
