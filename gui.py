"""
.. codeauthor:: Thomas Krempf-Driesbach
.. date:: 2025-10-12
.. description::

    Ce code permet de créer une interface graphique du projet info S7.

    Il utilise la bibliothèque PySide6 pour créer des fenêtres, des boutons et des titres personnalisés.

"""
import sys
from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg,
    QtCore as qtc
)
import xlsx_reducteur as xlsx

# parametres que les fenetres on en commun 
DEFAULT = {
    'titre': {'police': 'Arial', 'taille': 20, 'couleur': '#222','StyleSheet': 'color: #222; margin-bottom: 20px;padding: 8px'}
}

# parametre specifique a la fenetre menu
MENU = {
    'widget_engrenage':{
        'taille': [210, 210],
        'placement_engrenages': [(60, 105), (150, 150), (150, 52)],
        'styleSheet': 'background: transparent; border: none; font-size: 90px; color: #444;'
    },
    'geometrie': [700, 300],
    'titre': 'Menu',
    'styleSheet': '''
        QWidget {
            background-color: #f8f8f8; /* Couleur de fond claire */
            border: 2px solid #222; /* Bordure sombre */
            border-radius: 8px; /* Bords arrondis */
        }
        QPushButton {
            background: #fff; /* Couleur de fond blanche */
            border: 1px solid #222; /* Bordure sombre */
            border-radius: 6px; /* Bords arrondis */
            font-size: 12px; /* Taille de police */
            font-weight: bold; /* Poids de police */
            padding: 10px 0; /* Rembourrage */
            margin-bottom: 12px; /* Espace entre les boutons */
        }
        QPushButton:hover {
            background: #e0e0e0; /* Couleur de fond au survol */
        }
    '''
}

# parametre specifique a la fenetre menu
CREATION_PROJET = {
    'page':{
        'entree_sortie':{
            'label':['Vitess','RPM','Puissance','kW','Reducteur','Couple','Nm'],
        },
        'structure interne':{
            'label':['nombre d’étage :','1','Entraxe','mm','σ max','MPa',],
            'liste_deroulante':['engrenage droit', 'engrenage hélicoïdal', 'conique'],
        }
    },
    'geometrie': [1000, 600],
    'titre': 'Creation Projet',
    'styleSheet': '''
        QWidget {
            background-color: #f8f8f8; /* Couleur de fond claire */
            
        }
        QPushButton {
            background: #fff; /* Couleur de fond blanche */
            border: 1px solid #222; /* Bordure sombre */
            border-radius: 6px; /* Bords arrondis */
            font-size: 12px; /* Taille de police */
            font-weight: bold; /* Poids de police */
            padding: 10px 0; /* Rembourrage */
            margin-bottom: 12px; /* Espace entre les boutons */
        }
        QPushButton:hover {
            background: #e0e0e0; /* Couleur de fond au survol */
        }
    '''
}

ATTENTE_CREATION = {
    'geometrie': [200, 60],
    'titre': 'Creation Projet',
    'label':['creation projet','.','..','...',' '],
    'styleSheet':"""
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                font-size: 12px; /* Taille de police */
                font-weight: bold; /* Poids de police */
                padding: 10px 0; /* Rembourrage */
                margin-bottom: 12px; /* Espace entre les boutons */
        """
}

PROJET = {
    'titre': 'Projet',
    'label':['creation projet','.','..','...',' '],
    'styleSheet':"""
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                font-size: 12px; /* Taille de police */
                font-weight: bold; /* Poids de police */
                padding: 10px 0; /* Rembourrage */
                margin-bottom: 12px; /* Espace entre les boutons */
        """
}



class Simulation_train:
    def __init__(self,
                 vitesse_entree: int = 10,
                 puissance_entree: int = 20,
                 couple_sortie: int = 30,
                 entraxe: int = 7,
                 resistance_elastique: int = 9):
        # dictionnaire initial
        self._description = {
            'vitesse_entree': vitesse_entree,
            'puissance_entree': puissance_entree,
            'couple_sortie': couple_sortie,
            'rendement': 5,
            'entraxe': entraxe,
            'resistance_elastique': resistance_elastique,
            'k': 0,
            'effort_tangenciel': 10,
            'module': 5,
            'engrenage1_rayon_p': 9,
            'engrenage1_nbr_dents': 4,
            'engrenage2_rayon_p': 98,
            'engrenage2_nbr_dents': 42,
        }

        # créer dynamiquement une propriété pour chaque clé du dict
        for key in list(self._description.keys()):
            self._make_property_for_key(key)

    @property
    def description(self):
        """Renvoie le dict (toujours à jour)."""
        return self._description

    def _make_property_for_key(self, key):
        """Crée et attache une propriété nommée comme 'key' sur la classe."""
        def getter(self):
            return self._description[key]

        def setter(self, value):
            # mettre à jour la clé demandée
            self._description[key] = value
            # incrémenter toutes les autres clés (selon la demande)
            for other in self._description:
                if other != key:
                    try:
                        # si la valeur est numérique, on incrémente
                        self._description[other] += 1
                    except TypeError:
                        # si ce n'est pas numérique, on l'ignore
                        pass
            # Note : un setter ne peut pas "retourner" une valeur ; après affectation,
            # l'utilisateur doit lire `obj.description` pour obtenir le dict mis à jour.

        # attacher la propriété à la classe (pas à l'instance)
        setattr(self.__class__, key, property(getter, setter))

    def set_and_get(self, key, value):
        """Méthode utilitaire : modifie la clé et retourne immédiatement le dict."""
        if key not in self._description:
            raise KeyError(f"Clé inconnue: {key}")
        setattr(self, key, value)  # utilisera le setter défini plus haut
        return self.description


class Fenetre(qtw.QWidget):
    '''
    classe de base pour les fenetres
    parametre : dictionnaire contenant les parametres de la fenetre, propre a chaque fenetre
    '''
    def __init__(self, param: dict) -> None:
        super().__init__()
        self._parametre = param
        self.setWindowTitle(param['titre'])
        self.setStyleSheet(param['styleSheet'])
        if 'geometrie' in param:
            self.setFixedSize(*param['geometrie'])
        else:
            self.showMaximized()


    def ajoute_widgets(self,layout,list):
        for i in range(len(list)):
            layout.addWidget(list[i])

    def ajoute_layoutes(self,layout,list):
        for i in range(len(list)):
            layout.addLayout(list[i])


    def _ajout_nom_zone_texte_unitee(self,nom:str,unitee:str,text_defaut):
        layout = qtw.QHBoxLayout()
        lbl_nom = qtw.QLabel(nom)
        layout.addWidget(lbl_nom)
        variable = qtw.QLineEdit()
        variable.setText(text_defaut)
        layout.addWidget(variable)
        lbl_unitee = qtw.QLabel(unitee)
        layout.addWidget(lbl_unitee)
        layout.addStretch()
        widget = qtw.QWidget()
        widget.setLayout(layout)
        return widget,variable
    


class FenetreMenu(Fenetre):
    '''
    Classe pour genere uniquement la fenêtre de menu.
    parametre : dictionnaire contenant les parametres de la fenetre, propre a chaque fenetre
    '''
    def __init__(self, param: dict) -> None:
        super().__init__(param)
        self.creer_composant()
        self.genere_layout()


    def creer_composant(self):
        # creer different composant
        self.titre = self.creer_titre()
        # bouton_creer_projet
        self.bouton_creer_projet = qtw.QPushButton('Créer Projet')
        self.bouton_creer_projet.clicked.connect(self._ouvrir_fenetre_creation_projet)
        # bouton_ouvrir_projet
        self.bouton_ouvrir_projet = qtw.QPushButton('Ouvrir Projet')
        # bouton exit
        self.bouton_exit = qtw.QPushButton('EXIT')
        self.bouton_exit.setFixedSize(210,50)
        self.bouton_exit.clicked.connect(self.close)
        # engrenage
        self.widget_engrenage = self._generer_icone_engrenage()


    def genere_layout(self):
        # genere le layoute de droite
        left_layout = qtw.QVBoxLayout()
        liste = [self.titre,self.bouton_creer_projet,self.bouton_ouvrir_projet]
        self.ajoute_widgets(left_layout,liste)
        left_layout.addStretch() # Pour pousser les éléments vers le haut
        # genere le layoute de gauche
        right_layout = qtw.QVBoxLayout()
        right_layout.addWidget(self.widget_engrenage, alignment=qtg.Qt.AlignmentFlag.AlignTop)
        right_layout.addStretch()
        right_layout.addWidget(self.bouton_exit)
        # genere le layoute principale
        main_layout = qtw.QHBoxLayout()
        liste = [left_layout,right_layout]
        self.ajoute_layoutes(main_layout,liste)
        self.setLayout(main_layout) # Définir le layout principal pour la fenêtre
    

    def _generer_icone_engrenage(self) -> None:
        '''
        Fonction pour générer l'icône d'engrenage dans le layout spécifié
        uniquement dans la classe FenetreMenu parce que l'affichage est spécifique au menu.
        layout : Layout dans lequel ajouter les icône d'engrenage
        '''
        param = self._parametre['widget_engrenage']
        widget = qtw.QWidget(self)
        widget.setFixedSize(*param['taille'])  # Taille du conteneur
        for pos in param['placement_engrenages']:
            gear = qtw.QLabel('\u2699', widget)  # Unicode pour l'icône d'engrenage
            gear.setStyleSheet(param['styleSheet'])  # Style de l'icône
            gear.adjustSize()   # Ajuster la taille du QLabel à son contenu
            x = pos[0] - gear.width() // 2
            y = pos[1] - gear.height() // 2
            gear.move(x, y)  # Positionner l'icône
        # Ajouter le widget contenant les engrenages dans ton layout principal
        return widget


    def creer_titre(self):
        titre = qtw.QLabel('Dimensionnement Réducteur')
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        titre.setFont(qtg.QFont('Arial',20, qtg.QFont.Weight.Bold)) 
        titre.setStyleSheet('color: #222; margin-bottom: 20px;padding: 8px') # Style du titre
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement
        return titre


    def _ouvrir_fenetre_creation_projet(self) -> None:
        '''
        Ouvre la fenêtre de création de projet.
        '''
        self.fentre_projet = FenetreCreationProjet(CREATION_PROJET)
        self.fentre_projet.show()
        self.close()


class FenetreCreationProjet(Fenetre):
    def __init__(self, param: dict) -> None:
        '''
        Initialise la fenetre en plus des bouton de base et de toute la structure
        param = parametre de la page situee au dessus
        '''
        super().__init__(param)
        self._param = param
        self._widget_pages = self.generer_widget_page(nbr_page=2)
        # Layout vertical pour le stack + boutons
        self._bouton_layout = qtw.QHBoxLayout()
        self._bouton_layout.insertStretch(0, 1)
        self.generer_bouton_next_precedent(self._bouton_layout)
        self.generer_layout_principale()


    def generer_widget_page(self,nbr_page) -> None:
        '''
        Fonction pour générer les pages du QStackedWidget.
        '''
        stack = qtw.QStackedWidget()
        pages = []
        for i in range(nbr_page):
            page_method = getattr(self, f"create_page{i}")
            page_instance = page_method()
            stack.addWidget(page_instance)
            pages.append(page_instance)
        return stack


    def generer_layout_principale(self):
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._widget_pages)
        main_layout.addLayout(self._bouton_layout)
        self.setLayout(main_layout)

    def generer_bouton_next_precedent(self,layout):
        texte = ['Precedent','Next']
        taille = [210,50]
        fonction = ['precedente_page','next_page']
        widget = [0,0]
        for i in range(len(texte)):
            widget[i] = qtw.QPushButton(texte[i])
            widget[i].setFixedSize(*taille)
            widget[i].clicked.connect(getattr(self, fonction[i]))
            layout.addWidget(widget[i])
        


    def create_page0(self) -> qtw.QWidget:
        '''
        generation de la page 0 qui contient le choix des parametre général du reducteur
        retourne la variable de la page
        '''
        special_style = """
                QWidget {
                    background: #fff;           /* Couleur de fond blanche */
                    border: 1px solid #222;     /* Bordure */
                    border-radius: 6px;         /* Coins arrondis */
                    padding: 60px;              /* Rembourrage interne */
                    font-size: 18px;             /* Taille de la police */
                    font-weight: bold;           /* Gras */
                }
        """
        widgets,self._variables = self.genere_widgets_page0()
        # creation fleche
        fleche_gauche = qtw.QLabel()
        fleche_droite = qtw.QLabel()
        pixmap = qtg.QPixmap("./fleche.png")  # ton fichier
        fleche_gauche.setPixmap(pixmap)
        fleche_droite.setPixmap(pixmap)
        # creation block centre
        lbl_5 = qtw.QLabel('Reducteur')
        lbl_5.setStyleSheet(special_style)
        # creation block droite

        # ajout des layoute au layoute principale
        block_gauche = qtw.QVBoxLayout()
        block_gauche.addStretch()
        block_gauche.addWidget(widgets['Vitesse'])
        block_gauche.addWidget(widgets['Puissance'])
        block_gauche.addStretch()

        block_centre = qtw.QVBoxLayout()
        block_centre.addStretch()
        block_centre.addWidget(lbl_5)
        block_centre.addStretch()

        block_droite = qtw.QHBoxLayout()
        block_droite.addStretch()
        block_droite.addWidget(widgets['Couple'])

        layoute_page0 = qtw.QHBoxLayout()
        layoute_page0.addLayout(block_gauche)
        layoute_page0.addWidget(fleche_gauche)
        layoute_page0.addLayout(block_centre)
        layoute_page0.addWidget(fleche_droite)
        layoute_page0.addLayout(block_droite)
        page = qtw.QWidget()
        page.setLayout(layoute_page0)
        return page


    def genere_widgets_page0(self):
        label_param = {
            'Vitesse':{'unitee':'RPM','valeur_defaut':'4000','margin':[122,0,0,0]},
            'Puissance':{'unitee':'kW','valeur_defaut':'1500','margin':[100,0,0,0]},
            'Couple':{'unitee':'Nm','valeur_defaut':'380','margin':[0,0,100,0]}
        }
        widgets = {}
        variables = {}
        for key in (label_param):
            param = label_param[key]
            widgets[key],variables[key] = self._ajout_nom_zone_texte_unitee(key,param['unitee'],param['valeur_defaut'])
            variables[key].setFixedWidth(60)
            variables[key].setValidator(qtg.QIntValidator(0, 100))
            widgets[key].setContentsMargins(*param['margin'])
        return widgets,variables


    def create_page1(self) -> qtw.QWidget:
        '''
        generation de la page 1 qui contient le choix du nombre de train, de leurs type et de leur materiaux
        retourne la variable de la page
        '''
        special_style = """
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                border: 1px solid #222;
                border-radius: 6px;
                padding: 8px;
            }
        """

        layout_page = qtw.QVBoxLayout()
        layout_bloc_gauche = qtw.QHBoxLayout()
        layout_bloc_droit = qtw.QHBoxLayout()
        param_page = self._param['page']['structure interne']
        label = param_page['label']
        texte_ligne_deroutante = param_page['liste_deroulante']
        # creation page et ligne principale
        page = qtw.QWidget()
        ligne = qtw.QHBoxLayout()
        # Bloc 1 : Label + zone de texte
        bloc_gauche = qtw.QWidget()
        lbl_0 = qtw.QLabel(label[0])
        layout_bloc_gauche.addWidget(lbl_0)
         # nombre d’étage :
        nbr_train = qtw.QLineEdit()
        nbr_train.setValidator(qtg.QDoubleValidator(0.0, 9999.99, 2))
        nbr_train.setFixedWidth(60)
        nbr_train.setText('1')
        layout_bloc_gauche.addStretch()
        bloc_gauche.setLayout(layout_bloc_gauche)
        bloc_gauche.setStyleSheet(special_style)
        # Bloc 2 : le reste à droite
        bloc_droit = qtw.QWidget()
        lbl_1 = qtw.QLabel(label[1])
        layout_bloc_droit.addWidget(lbl_1)
        liste_deroulante = qtw.QComboBox()
        liste_deroulante.addItems(texte_ligne_deroutante)
        layout_bloc_droit.addWidget(liste_deroulante)
        lbl_2 = qtw.QLabel(label[2])
        layout_bloc_droit.addWidget(lbl_2)
        # entraxe
        self._varaible_entraxe = qtw.QLineEdit()
        self._varaible_entraxe.setValidator(qtg.QIntValidator(0, 100))
        self._varaible_entraxe.setFixedWidth(80)
        self._varaible_entraxe.setText('20')
        lbl_3 = qtw.QLabel(label[3])
        layout_bloc_droit.addWidget(lbl_3)
        lbl_4 = qtw.QLabel(label[4])
        layout_bloc_droit.addWidget(lbl_4)
        self._varaible_contrainte_max = qtw.QLineEdit()
        self._varaible_contrainte_max.setValidator(qtg.QIntValidator(0, 100))
        self._varaible_contrainte_max.setFixedWidth(80)
        self._varaible_contrainte_max.setText('210000')
        lbl_5 = qtw.QLabel(label[5])
        layout_bloc_droit.addWidget(lbl_5)
        layout_bloc_droit.addStretch()
        bloc_droit.setLayout(layout_bloc_droit)
        bloc_droit.setStyleSheet(special_style)
        # --- Ajout au layout principal
        ligne.addWidget(bloc_gauche)
        ligne.addSpacing(100)  # Espace fixe entre les deux blocs
        ligne.addWidget(bloc_droit)
        ligne.addStretch()
        # ajoute la ligne au layout
        layout_page.addLayout(ligne)
        layout_page.addStretch()
        page.setLayout(layout_page)
        return page


    def next_page(self) -> None:
        '''
        permet de passer a la page suivante
        '''
        i = self._widget_pages.currentIndex()
        if i < self._widget_pages.count() - 1:
            self._widget_pages.setCurrentIndex(i + 1)
        else:
            # ouvre fenetre attente
            fenetre_attente = FenetreAttenteCreation(ATTENTE_CREATION)
            fenetre_attente.show()
            self.close()
            # prendre les dernieres valeurs
            description_global = {}
            description_global['vitesse_entree'] = int(self._variables['Vitesse'].text())
            description_global['puissance_entree'] = int(self._variables['Puissance'].text())
            description_global['couple_sortie'] = int(self._variables['Couple'].text())
            description_train = {}
            entraxe = int(self._varaible_entraxe.text())
            contrainte_max = int(self._varaible_contrainte_max.text())
            train = Simulation_train(description_global['vitesse_entree'],
                                     description_global['puissance_entree'],
                                     description_global['couple_sortie'],
                                     entraxe,
                                     contrainte_max
                                     )
            param_projet = [xlsx.Global(),xlsx.Train(1)]
            param_projet[0].description = description_global
            param_projet[1].description = train.description
            projet_file = xlsx.ProjetXlsx(param_projet[0])
            projet_file.ecrire_description(param_projet[1],1)
            projet_file.save()
            self.fenetre_projet = FenetreProjet(PROJET,param_projet,projet_file,train)
            self.fenetre_projet.show()
            fenetre_attente.close()


    def precedente_page(self) -> None:
        '''
        permet de passer a la page precedente
        '''
        i = self.stack.currentIndex()
        if i > 0:
            self.stack.setCurrentIndex(i - 1)



class FenetreAttenteCreation(Fenetre):
    def __init__(self, param: dict) -> None:
        super().__init__(param)
        self._param = param

        # --- Création du layout principal ---
        layout_main = qtw.QHBoxLayout()
        self.setStyleSheet(param['styleSheet'])

        # Label principal
        label_texte = qtw.QLabel(param['label'][0])
        layout_main.addWidget(label_texte)
        # Label des points qui clignote
        self.label_points = qtw.QLabel("")
        layout_main.addWidget(self.label_points)
        self.setLayout(layout_main)
        # --- Animation des points ---
        self._points = param['label'][1:]  # ['.', '..', '...',' ']
        self._index = 0
        # Timer pour l’animation
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.clignoter)
        self.timer.start(400)  # toutes les 400 ms

    def clignoter(self):
        """Fait alterner le texte du label pour simuler un clignotement."""
        self.label_points.setText(self._points[self._index])
        self._index = (self._index + 1) % len(self._points)


class FenetreProjet(Fenetre):
    def __init__(self, param_feuille: dict,param:list,file:xlsx.ProjetXlsx,train) -> None:
        super().__init__(param_feuille)
        self._train = train
        self._param_feuille = param_feuille
        self._param = param
        self._file = file
        self. genere_laoute_train()

    def genere_laoute_train(self):
        layout_main = qtw.QHBoxLayout()
        self.setStyleSheet(self._param_feuille['styleSheet'])
        # crer 
        layout_train1 = qtw.QVBoxLayout()
        layout_train1.addStretch()
        titre = qtw.QLabel('Train_1')
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        titre.setFont(qtg.QFont('Arial',20, qtg.QFont.Weight.Bold)) 
        titre.setStyleSheet('color: #222; margin-bottom: 20px;padding: 8px') # Style du titre
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement
        layout_train1.addWidget(titre) 
        self._zone_text_train = {'widget':{},'variable':{}}
        for i, (key, value) in enumerate(self._param[1].description.items()):
            unitee  = self._param[1].unitee[i]
            self._zone_text_train['widget'][key],self._zone_text_train['variable'][key] = self._ajout_nom_zone_texte_unitee(key,unitee,str(value))
            self._zone_text_train['variable'][key].setFixedWidth(60)
            self._zone_text_train['variable'][key].setValidator(qtg.QIntValidator())
            self._zone_text_train['variable'][key].editingFinished.connect(lambda k=key: self.modifie_parametre(self._zone_text_train['variable'][k].text(), k))  
            layout_train1.addWidget(self._zone_text_train['widget'][key]) 
        layout_train1.addStretch()
        layout_main.addLayout(layout_train1)
        self.setLayout(layout_main)

    def modifie_parametre(self, nouvelle_valeur, value_name):
        setattr(self._train, value_name, int(nouvelle_valeur))
        self._param[1].description = self._train.description
        self._file.ecrire_description(self._param[1],1)
        self._file.save()
        for key in self._zone_text_train['variable']:
            if key != value_name:
                self._zone_text_train['variable'][key].setText(str(self._param[1].description[key]))

if __name__ == '__main__':

    app = qtw.QApplication(sys.argv)
    fenetre = FenetreMenu(MENU)
    fenetre.show()
    sys.exit(app.exec())
    