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

# parametres que les fenetres on en commun 
DEFAULT = {
    'titre': {'police': 'Arial', 'taille': 20, 'couleur': '#222','StyleSheet': 'color: #222; margin-bottom: 20px;padding: 8px'}
}

# parametre specifique a la fenetre menu
MENU = {
    'layout': {
        'main_layout':{
            'sens': 'horizontal',
        },
        'left_layout':{
            'sens': 'vertical',
            'boutons': {'Créer Projet':{'taille': None, 'action': 'ouvrir_fenetre_creation_projet'},
                         'Ouvrir Projet':{'taille': None, 'action': 'ouvrir_fenetre_creation_projet'}}
        },
        'right_layout':{
            'sens': 'vertical',
            'boutons': {'EXIT':{'taille': [210, 50], 'action': 'close'}}
        }
    },
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
            'zone_texte':{
                'puissance_entree':{
                    'variable':None,
                    'validator': qtg.QIntValidator(0, 100),
                    'largeur':60,
                    'param_defaut':None
                },
                'vitesse_entree':{
                    'variable':None,
                    'validator': qtg.QIntValidator(0, 100),
                    'largeur':60,
                    'param_defaut':None
                },
                'rapport_reduction':{
                    'variable':None,
                    'validator': qtg.QIntValidator(0, 100),
                    'largeur':60,
                    'param_defaut':None
                },
                'couple_sortie':{
                    'variable':None,
                    'validator': qtg.QIntValidator(0, 100),
                    'largeur':60,
                    'param_defaut':None
                }
            },
            'label':['Vitess','RPM','Puissance','kW','Rapport réduction','Reducteur','Couple','Nm'],
        },
        'structure interne':{
            'zone_texte':{
                'nbr_train':{
                    'variable':None,
                    'validator': qtg.QDoubleValidator(0.0, 9999.99, 2),
                    'largeur':60,
                    'param_defaut':'1'
                },
                'entraxe':{
                    'variable':None,
                    'validator': qtg.QIntValidator(0, 100),
                    'largeur':80,
                    'param_defaut':'20'
                },
                'contrainte_max':{
                    'variable':None,
                    'validator': qtg.QIntValidator(0, 100),
                    'largeur':80,
                    'param_defaut':'210 000'
                }
            },
            'label':['nombre d’étage :','1','Entraxe','mm','σ max','MPa',],
            'liste_deroulante':['engrenage droit', 'engrenage hélicoïdal', 'conique'],
        }
    },
    'layout': {
        'main_layout':{
            'sens': 'vertical',
        },
        'boutons_layout':{
            'sens': 'horizontal',
            'boutons': {'Precedent':{'taille': [210, 50], 'action': 'precedente_page'},
                         'Next':{'taille': [210, 50], 'action': 'next_page'}}
        },
        'page1_layout':{
            'sens': 'hvertical'
        },
        'page1_bloc_gauche_layout':{
            'sens': 'horizontal'
        },
        'page1_bloc_droit_layout':{
            'sens': 'horizontal'
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
    ''',
    'special_style':"""
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                border: 1px solid #222;
                border-radius: 6px;
                padding: 8px;
            }
        """
}


ATTENTE_CREATION = {
    'geometrie': [200, 60],
    'titre': 'Creation Projet',
    'layout': {
        'main_layout':{
            'sens': 'horizontal',
        }
    },
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


class bouton(qtw.QPushButton):
    '''
    Classe pour les boutons avec une taille optionnelle.
    '''
    def __init__(self, texte: str, taille: list = None) -> None:
        super().__init__(texte)
        if taille:
            self.setFixedSize(*taille)  # Définir une taille fixe si spécifiée


class Titre(qtw.QLabel):
    '''
    Classe pour les titres avec un style personnalisé.
    texte : Texte du titre a afficher
    param : Dictionnaire contenant les paramètres de style, voir DEFAULT
    '''
    def __init__(self, texte: str) -> None:
        param = DEFAULT['titre']
        super().__init__(texte)
        self.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        font = qtg.QFont(param['police'], param['taille'], qtg.QFont.Weight.Bold) # Police personnalisée
        self.setFont(font) 
        self.setStyleSheet(param['StyleSheet']) # Style du titre
        self.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement


class Fenetre(qtw.QWidget):
    '''
    classe de base pour les fenetres
    parametre : dictionnaire contenant les parametres de la fenetre, propre a chaque fenetre
    '''
    def __init__(self, param: dict) -> None:
        super().__init__()
        self._parametre = param
        self.setWindowTitle(self._parametre['titre'])
        self.setFixedSize(*self._parametre['geometrie'])
        self.setStyleSheet(self._parametre['styleSheet'])
        self.generer_layouts()


    def generer_bouton(self,layout_name: str) -> None:
        '''
        fonction de base pour generer les boutons pour chaque fenetre
        layout_name : nom du layout dans lequel ajouter les boutons
        '''
        self.boutons = {}
        boutons_param = self._parametre['layout'][layout_name]['boutons']
        for texte_bouton in boutons_param:
            # creer le bouton et l'ajouter au layout
            self.boutons[texte_bouton] = bouton(texte_bouton, boutons_param[texte_bouton]['taille'])
            self.boutons[texte_bouton].clicked.connect(getattr(self, boutons_param[texte_bouton]['action']))
            self.layouts[layout_name].addWidget(self.boutons[texte_bouton])


    def generer_layouts(self) -> None:
        '''
        Fonction de base pour générer les layouts de chaque fenêtre.
        '''
        self.layouts = {}
        for name in self._parametre['layout']:
            if self._parametre['layout'][name]['sens'] == 'horizontal':
                self.layouts[name] = qtw.QHBoxLayout()
            else:
                self.layouts[name] = qtw.QVBoxLayout()


    def _generer_zone_texte(self,ligne:qtw.QHBoxLayout,param_zone_text:dict) -> qtw.QLineEdit:
        '''
        genere une zone de texte ne fonction des parametre
        ligne = ligne sur la quelle la zone est ajoutee
        param_zone = parametre de la zone de texte, voir la structure si dessus dans les constante de parametre fenetre
        retourne la varable contenant la zone de texte
        '''
        variable = qtw.QLineEdit()
        variable.setValidator(param_zone_text['validator'])  # seulement des entiers
        variable.setFixedWidth(param_zone_text['largeur'])
        variable.setText(param_zone_text['param_defaut'])
        ligne.addWidget(variable)
        return variable
    

    def _generer_label(slef,ligne:qtw.QHBoxLayout,texte:str) -> None:
        '''
        genere un label, du texte prédéfinie sur le quelle l'ont ne peut pas interragire
        ligne = ligne sur la quelle le label est ajoutee
        text = texte aui sera afficher sur la ligne
        '''
        lbl_nbr = qtw.QLabel(texte)
        ligne.addWidget(lbl_nbr)
        return lbl_nbr


    def _generer_liste_deroulante(self,ligne:qtw.QHBoxLayout,choix:list[str]) -> qtw.QComboBox:
        '''
        genere une liste deroulante de str
        ligne = ligne sur la quelle la liste est ajoutéee
        choix = liste contenant les differents choix
        retourne la variable contenant la liste_deroulante
        '''
        liste_deroulante = qtw.QComboBox()
        liste_deroulante.addItems(choix)
        ligne.addWidget(liste_deroulante)
        return liste_deroulante


    def _ajout_nom_et_zone_texte_et_unitee(self,nom:str,unitee:str,param_zone_texte):
        layout = qtw.QHBoxLayout()
        widget = qtw.QWidget()
        self._generer_label(layout, nom)
        variable = self._generer_zone_texte(layout, param_zone_texte)
        self._generer_label(layout, unitee) 
        layout.addStretch()
        widget.setLayout(layout)
        return widget,variable


class FenetreMenu(Fenetre):
    '''
    Classe pour genere uniquement la fenêtre de menu.
    parametre : dictionnaire contenant les parametres de la fenetre, propre a chaque fenetre
    '''
    def __init__(self, param: dict) -> None:
        super().__init__(param)
        self._generer_titre()
        # ajoute la partie gauche avec les boutons
        self.generer_bouton('left_layout')  # Ajouter les boutons au layout gauche
        self.layouts['left_layout'].addStretch() # Pour pousser les éléments vers le haut
        self.layouts['main_layout'].addLayout(self.layouts['left_layout']) # Ajouter le layout gauche au layout principal
        # ajoute la partie droite avec les icones et le bouton exit
        self._generer_icone_engrenage(self.layouts['right_layout'])
        self.layouts['right_layout'].addStretch()
        self.generer_bouton('right_layout') # Ajouter les boutons au layout droit
        self.layouts['main_layout'].addLayout(self.layouts['right_layout'])
        self.setLayout(self.layouts['main_layout']) # Définir le layout principal pour la fenêtre


    def _generer_titre(self) -> None:
        '''
        Fonction pour générer le titre de la fenêtre
        uniquement dans la classe FenetreMenu parce que les autres fenêtres n'en ont pas besoin.
        '''
        titre = Titre('Dimensionnement Réducteur') # Titre personnalisé
        self.layouts['left_layout'].addWidget(titre)  # Ajouter le titre au layout gauche
    

    def _generer_icone_engrenage(self,layout:qtw.QVBoxLayout) -> None:
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
        layout.addWidget(widget, alignment=qtg.Qt.AlignmentFlag.AlignTop)


    def ouvrir_fenetre_creation_projet(self) -> None:
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
        self.generer_widget_page()
        self.layouts['boutons_layout'].insertStretch(0, 1)
        # Layout vertical pour le stack + boutons
        self.generer_bouton('boutons_layout')
        self.layouts['main_layout'].addLayout(self.layouts['boutons_layout'])
        self.setLayout(self.layouts['main_layout'])


    def generer_widget_page(self) -> None:
        '''
        Fonction pour générer les pages du QStackedWidget.
        '''
        self.stack = qtw.QStackedWidget()
        self.pages = []
        for i in range(len(self._param['page'])):
            page_method = getattr(self, f"create_page{i}")
            page_instance = page_method()
            self.stack.addWidget(page_instance)
            self.pages.append(page_instance)
        self.layouts['main_layout'].addWidget(self.stack)


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

        param_page = self._param['page']['entree_sortie']
        param_zone_texte = param_page['zone_texte']
        label = param_page['label']
        # creation page et ligne principale
        page = qtw.QWidget()
        # creation block de gauche
        block_gauche = qtw.QVBoxLayout()
        block_gauche.addStretch()
        # widget vitess
        widget_vitesse,variable_vitesse = self._ajout_nom_et_zone_texte_et_unitee(label[0],label[1],param_zone_texte['vitesse_entree'])
        widget_vitesse.setContentsMargins(122, 0, 0, 0)
        block_gauche.addWidget(widget_vitesse)
        # widget puissance
        widget_puissance,variable_puissance = self._ajout_nom_et_zone_texte_et_unitee(label[2],label[3],param_zone_texte['puissance_entree'])
        widget_puissance.setContentsMargins(100, 0, 0, 0)
        block_gauche.addWidget(widget_puissance)
        block_gauche.addStretch()
        # creation fleche
        fleche_gauche = qtw.QLabel()
        fleche_droite = qtw.QLabel()
        pixmap = qtg.QPixmap("./fleche.png")  # ton fichier
        fleche_gauche.setPixmap(pixmap)
        fleche_droite.setPixmap(pixmap)
        # creation block centre
        block_centre = qtw.QVBoxLayout()
        block_centre.addStretch()
        widget_centre = self._generer_label(block_centre,label[5])
        widget_centre.setStyleSheet(special_style)
        block_centre.addStretch()
        # creation block droite
        block_droite = qtw.QHBoxLayout()
        # widget couple
        block_droite.addStretch()
        widget_couple,variqble_couple = self._ajout_nom_et_zone_texte_et_unitee(label[6],label[7],param_zone_texte['couple_sortie'])
        widget_couple.setContentsMargins(0, 0, 100, 0)
        block_droite.addWidget(widget_couple)
        # ajout des layoute au layoute principale
        layoute_page0 = qtw.QHBoxLayout()
        layoute_page0.addLayout(block_gauche)
        layoute_page0.addWidget(fleche_gauche)
        layoute_page0.addLayout(block_centre)
        layoute_page0.addWidget(fleche_droite)
        layoute_page0.addLayout(block_droite)
        page.setLayout(layoute_page0)
        return page



    def create_page1(self) -> qtw.QWidget:
        '''
        generation de la page 1 qui contient le choix du nombre de train, de leurs type et de leur materiaux
        retourne la variable de la page
        '''
        param_page = self._param['page']['structure interne']
        param_zone_texte = param_page['zone_texte']
        label = param_page['label']
        texte_ligne_deroutante = param_page['liste_deroulante']
        special_style = self._param['special_style']
        # creation page et ligne principale
        page = qtw.QWidget()
        ligne = qtw.QHBoxLayout()
        # Bloc 1 : Label + zone de texte
        bloc_gauche = qtw.QWidget()
        self._generer_label(self.layouts['page1_bloc_gauche_layout'], label[0])  # nombre d’étage :
        param_zone_texte['nbr_train']['varaible'] = self._generer_zone_texte(self.layouts['page1_bloc_gauche_layout'], param_zone_texte['nbr_train'])
        self.layouts['page1_bloc_gauche_layout'].addStretch()
        bloc_gauche.setLayout(self.layouts['page1_bloc_gauche_layout'])
        bloc_gauche.setStyleSheet(special_style)
        # Bloc 2 : le reste à droite
        bloc_droit = qtw.QWidget()
        self._generer_label(self.layouts['page1_bloc_droit_layout'], label[1])  # 1
        liste_deroulante = self._generer_liste_deroulante(self.layouts['page1_bloc_droit_layout'], texte_ligne_deroutante)
        self._generer_label(self.layouts['page1_bloc_droit_layout'], label[2])  # entraxe
        param_zone_texte['entraxe']['varaible'] = self._generer_zone_texte(self.layouts['page1_bloc_droit_layout'], param_zone_texte['entraxe'])
        self._generer_label(self.layouts['page1_bloc_droit_layout'], label[3])  # mm
        self._generer_label(self.layouts['page1_bloc_droit_layout'], label[4])  # σ max
        param_zone_texte['contrainte_max']['varaible'] = self._generer_zone_texte(self.layouts['page1_bloc_droit_layout'], param_zone_texte['contrainte_max'])
        self._generer_label(self.layouts['page1_bloc_droit_layout'], label[5])  # MPa
        self.layouts['page1_bloc_droit_layout'].addStretch()
        bloc_droit.setLayout(self.layouts['page1_bloc_droit_layout'])
        bloc_droit.setStyleSheet(special_style)
        # --- Ajout au layout principal
        ligne.addWidget(bloc_gauche)
        ligne.addSpacing(100)  # Espace fixe entre les deux blocs
        ligne.addWidget(bloc_droit)
        ligne.addStretch()
        # ajoute la ligne au layout
        self.layouts['page1_layout'].addLayout(ligne)
        self.layouts['page1_layout'].addStretch()
        page.setLayout(self.layouts['page1_layout'])
        return page



    def create_page2(self) -> qtw.QWidget:
        page = qtw.QWidget()
        self.close()
        return page

    def next_page(self) -> None:
        '''
        permet de passer a la page suivante
        '''
        i = self.stack.currentIndex()
        if i < self.stack.count() - 1:
            self.stack.setCurrentIndex(i + 1)
        else:
            self.fenetre_attente = FenetreAttenteCreation(ATTENTE_CREATION)
            self.fenetre_attente.show()
            self.close()

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
        self.label_texte = qtw.QLabel(param['label'][0])
        layout_main.addWidget(self.label_texte)
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



if __name__ == '__main__':

    app = qtw.QApplication(sys.argv)
    fenetre = FenetreMenu(MENU)
    fenetre.show()
    sys.exit(app.exec())
    