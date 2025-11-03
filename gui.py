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
    'labels':['Dimensionnement Réducteur'],
    'buttons':['Créer Projet','Ouvrir Projet','EXIT'],
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
    'buttons':['Next','Précedent'],
    'page':{
        'entree_sortie':{
            'labels_unitee':{
                'Vitesse':{'unitee':'RPM','valeur_defaut':'4000','margin':[122,0,0,0]},
                'Puissance':{'unitee':'kW','valeur_defaut':'1500','margin':[100,0,0,0]},
                'Couple':{'unitee':'Nm','valeur_defaut':'380','margin':[0,0,100,0]}
            },
            'labels':['Reducteur']
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
    def __init__(self, param: dict,elements:dict) -> None:
        super().__init__()
        self._param = param
        self.setWindowTitle(param['titre'])
        self.setStyleSheet(param['styleSheet'])
        if 'geometrie' in param:
            self.setFixedSize(*param['geometrie'])
        else:
            self.showMaximized()
        result =self.genere_elements(elements,param)
        for key in result:
            setattr(self, key, result[key])


    def genere_elements(self,elements:dict,textes):
        constructors = {
        'layouts': lambda spec: qtw.QVBoxLayout() if spec == 'v' else qtw.QHBoxLayout(),
        'widgets': lambda _: qtw.QWidget(),
        'labels': lambda text: qtw.QLabel(text),
        'lineedits': lambda _: qtw.QLineEdit(),
        'comboboxes': lambda _: qtw.QComboBox(),
        'buttons': lambda text: qtw.QPushButton(text),
        'stack': lambda _: qtw.QStackedWidget()
        }
        result = {}
        for key in constructors:
            result[key] = {}  # initialiser chaque type d'élément avec un dict vide
        for key, valeur_result in result.items():
            # vérifie si le type d'élément est présent dans elements
            if key not in elements:
                continue
            # crée variables temporaires
            valeur = elements[key]
            text_list = textes.get(key, [])
            # créer les éléments
            if key == 'layouts':
                # Cas spécial : layouts est un dict (nom: 'v' ou 'h')
                for name, spec in valeur.items():
                    valeur_result[name] = constructors[key](spec)
            else:
                # Cas général : listes d'éléments
                for i, name in enumerate(valeur):
                    if i < len(text_list):
                        text = text_list[i]
                    else:
                        text = ""
                    if key in ('labels', 'buttons'):
                        arg = text
                    else:
                        arg = None
                    valeur_result[name] = constructors[key](arg)
        return result

    def _genere_lable_image(self,name):
        pixmap = qtg.QPixmap(name)
        label = qtw.QLabel()
        label.setPixmap(pixmap)
        return label


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
        elements = {
            'layouts':{'main':'h','left':'v','right':'v'},
            'widgets':['engrenages'],
            'labels':['titre'],
            'buttons':['creer_projet','ouvrir_projet','exit']
        }
        super().__init__(param,elements)
        self.adapt_composant()
        self.ajoute_composants()


    def adapt_composant(self):
        # creer different composant
        self.adapter_titre()
        # bouton_creer_projet
        self.buttons['creer_projet'].clicked.connect(self._ouvrir_fenetre_creation_projet)
        # bouton_ouvrir_projet
        # bouton exit
        self.buttons['exit'].setFixedSize(210,50)
        self.buttons['exit'].clicked.connect(self.close)
        # engrenage
        self.widget_engrenage = self._generer_icone_engrenage(self.widgets['engrenages'])


    def ajoute_composants(self):
        liste = [self.labels['titre'],self.buttons['creer_projet'],self.buttons['ouvrir_projet']]
        self.ajoute_widgets(self.layouts['left'],liste)
        self.layouts['left'].addStretch() # Pour pousser les éléments vers le haut
        self.layouts['right'].addWidget(self.widget_engrenage, alignment=qtg.Qt.AlignmentFlag.AlignTop)
        self.layouts['right'].addStretch()
        self.layouts['right'].addWidget(self.buttons['exit'])
        liste = [self.layouts['left'],self.layouts['right']]
        self.ajoute_layoutes(self.layouts['main'],liste)
        self.setLayout(self.layouts['main']) # Définir le layout principal pour la fenêtre
    

    def _generer_icone_engrenage(self,widget) -> None:
        '''
        Fonction pour générer l'icône d'engrenage dans le layout spécifié
        uniquement dans la classe FenetreMenu parce que l'affichage est spécifique au menu.
        layout : Layout dans lequel ajouter les icône d'engrenage
        '''
        param = self._param['widget_engrenage']
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


    def adapter_titre(self):
        self.labels['titre'].setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        self.labels['titre'].setFont(qtg.QFont('Arial',20, qtg.QFont.Weight.Bold)) 
        self.labels['titre'].setStyleSheet('color: #222; margin-bottom: 20px;padding: 8px') # Style du titre
        self.labels['titre'].setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement


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
        elements = {
            'layouts':{'main':'v','button':'h'},
            'buttons':['next','precedent'],
            'stack':['stack']
        }
        super().__init__(param,elements)
        self.generer_widget_page(nbr_page=2)
        # Layout vertical pour le stack + boutons
        self.layouts['button'].insertStretch(0, 1)
        self.generer_bouton_next_precedent(self.layouts['button'])
        self.ajoute_composants()


    def generer_widget_page(self,nbr_page) -> None:
        '''
        Fonction pour générer les pages du QStackedWidget.
        '''
        pages = []
        for i in range(nbr_page):
            if i == 0:
                page_0 = Page_0(self)
                page_instance = page_0.genere_page()
            else:
                page_method = getattr(self, f"create_page{i}")
                page_instance = page_method()
            self.stack['stack'].addWidget(page_instance)
            pages.append(page_instance)


    def generer_bouton_next_precedent(self,layout):
        taille = [210,50]
        fonction = ['precedente_page','next_page']
        for i, key in enumerate(self.buttons):
            self.buttons[key].setFixedSize(*taille)
            self.buttons[key].clicked.connect(getattr(self, fonction[i]))
            layout.addWidget(self.buttons[key])


    def ajoute_composants(self):
        self.layouts['main'].addWidget(self.stack['stack'])
        self.layouts['main'].addLayout(self.layouts['button'])
        self.setLayout(self.layouts['main'])

    # --- Création page 0 ---


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
        param_page = self._param['page']['structure interne']
        texte_ligne_deroutante = param_page['liste_deroulante']

        elements = {
            'layouts':{'page':'v','ligne':'h','bloc_gauche':'h','bloc_droit':'h'},
            'widgets':['page','bloc_gauche','bloc_droit'],
            'labels':['nbr_etage','1','entraxe','mm','σ_max','mpa'],
            'lineedits':['nbr_train','entraxe','contrainte_max'],
            'comboboxes':['liste_deroulante']
        }
        result =self.genere_elements(elements,{'labels':param_page['label']})
        layouts = result['layouts']
        widgets = result['widgets']
        labels = result['labels']
        self._lineedits = result['lineedits']
        liste_deroulante = result['comboboxes']['liste_deroulante']
        liste_deroulante.addItems(texte_ligne_deroutante)


        
        text = ['1','20','210000']
        for i, key in enumerate(self._lineedits):
            self._lineedits[key].setValidator(qtg.QDoubleValidator())
            self._lineedits[key].setFixedWidth(80)
            self._lineedits[key].setText(text[i])
        # bloc gauche
        layouts['bloc_gauche'].addWidget(labels['nbr_etage'])
        widgets['bloc_gauche'].setLayout(layouts['bloc_gauche'])
        widgets['bloc_gauche'].setStyleSheet(special_style)
        layouts['bloc_gauche'].addWidget(self._lineedits['nbr_train'])
        # bloc droit
        widgets['bloc_droit'].setStyleSheet(special_style)
        liste_widgets = [labels['1'],liste_deroulante,labels['entraxe'],self._lineedits['entraxe'],labels['mm'],
                         labels['σ_max'],self._lineedits['contrainte_max'],labels['mpa']]
        self.ajoute_widgets(layouts['bloc_droit'],liste_widgets)
        widgets['bloc_droit'].setLayout(layouts['bloc_droit'])
        # page
        layouts['ligne'].addWidget(widgets['bloc_gauche'])
        layouts['ligne'].addSpacing(100)  # Espace fixe entre les deux blocs
        layouts['ligne'].addWidget(widgets['bloc_droit'])
        layouts['ligne'].addStretch()
        layouts['page'].addLayout(layouts['ligne'])
        layouts['page'].addStretch()
        widgets['page'].setLayout(layouts['page'])
        return widgets['page']


    def next_page(self) -> None:
        '''
        permet de passer a la page suivante
        '''
        i = self.stack['stack'].currentIndex()
        if i < self.stack['stack'].count() - 1:
            self.stack['stack'].setCurrentIndex(i + 1)
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
            entraxe = int(self._lineedits['entraxe'].text())
            contrainte_max = int(self._lineedits['contrainte_max'].text())
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
        i = self.stack['stack'].currentIndex()
        if i > 0:
            self.stack['stack'].setCurrentIndex(i - 1)



class Page_0():
    def __init__(self, fenetre: Fenetre) -> None:
        self._fenetre = fenetre
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
        elements = {
            'layouts':{'main_0':'h','block_gauche_0':'v','block_centre_0':'v','block_droit_0':'h'},
            'labels':['reducteur'],
        }
        result = fenetre.genere_elements(elements,{'labels':fenetre._param['page']['entree_sortie']['labels']})
        self.layouts = result['layouts']
        self.labels = result['labels']
        self._widgets,self._variables = self._genere_widgets_page0()
        self._labels_fleches = self._genere_fleches_page0(2)
        self.labels['reducteur'].setStyleSheet(special_style)
        self._layout_enfant = self._genere_layoute_page0() 


    def _genere_widgets_page0(self):
        label_param = {
            'Vitesse':{'unitee':'RPM','valeur_defaut':'4000','margin':[122,0,0,0]},
            'Puissance':{'unitee':'kW','valeur_defaut':'1500','margin':[100,0,0,0]},
            'Couple':{'unitee':'Nm','valeur_defaut':'380','margin':[0,0,100,0]}
        }
        widgets = {}
        variables = {}
        for key in (label_param):
            param = label_param[key]
            widgets[key],variables[key] = fenetre._ajout_nom_zone_texte_unitee(key,param['unitee'],param['valeur_defaut'])
            variables[key].setFixedWidth(60)
            variables[key].setValidator(qtg.QIntValidator(0, 100))
            widgets[key].setContentsMargins(*param['margin'])
        return widgets,variables


    def _genere_fleches_page0(self,nbr_fleche):
        label = [0]*nbr_fleche
        for i in range(nbr_fleche):
            label[i] = self._fenetre._genere_lable_image('./fleche.png')
        return label

    def _genere_layoute_page0(self):
        self.layouts['block_gauche_0'].addStretch()
        self.layouts['block_gauche_0'].addWidget(self._widgets['Vitesse'])
        self.layouts['block_gauche_0'].addWidget(self._widgets['Puissance'])
        self.layouts['block_gauche_0'].addStretch()
        self.layouts['block_centre_0'].addStretch()
        self.layouts['block_centre_0'].addWidget(self.labels['reducteur'])
        self.layouts['block_centre_0'].addStretch()
        self.layouts['block_droit_0'].addStretch()
        self.layouts['block_droit_0'].addWidget(self._widgets['Couple'])
        return [self.layouts['block_gauche_0'],self.layouts['block_centre_0'],self.layouts['block_droit_0']]


    def genere_page(self):
        self.layouts['main_0'].addLayout(self._layout_enfant[0])
        self.layouts['main_0'].addWidget(self._labels_fleches[0])
        self.layouts['main_0'].addLayout(self._layout_enfant[1])
        self.layouts['main_0'].addWidget(self._labels_fleches[1])
        self.layouts['main_0'].addLayout(self._layout_enfant[2])
        page = qtw.QWidget()
        page.setLayout(self.layouts['main_0'])
        return page


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
    