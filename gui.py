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
import copy

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
    'buttons':['Précedent','Next'],
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

PAGE_0 = {
    'labels_unitee':{
                'Vitesse':{'unitee':'RPM','valeur_defaut':'4000','validator':qtg.QIntValidator(0, 10000),'margin':[122,0,0,0]},
                'Puissance':{'unitee':'kW','valeur_defaut':'1500','validator':qtg.QIntValidator(0, 10000),'margin':[100,0,0,0]},
                'Couple':{'unitee':'Nm','valeur_defaut':'380','validator':qtg.QIntValidator(0, 10000),'margin':[0,0,100,0]}
            },
    'labels':['Reducteur'],
    'styleSheet': """
                QWidget {
                    background: #fff;           /* Couleur de fond blanche */
                    border: 1px solid #222;     /* Bordure */
                    border-radius: 6px;         /* Coins arrondis */
                    padding: 60px;              /* Rembourrage interne */
                    font-size: 18px;             /* Taille de la police */
                    font-weight: bold;           /* Gras */
                }
        """
}


PAGE_1 = {
    'labels_unitee':{
                'entraxe':{'unitee':'mm','valeur_defaut':'400','validator':qtg.QIntValidator(0, 10000)},
                'σ_max':{'unitee':'Mpa','valeur_defaut':'1500','validator':qtg.QIntValidator(0, 10000)},
            },
    'labels':['nombre d’étage :','1'],
    'comboboxes':{'liste_deroulante':['engrenage droit', 'engrenage hélicoïdal', 'conique']},
    'styleSheet': """
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
    'labels':['creation projet','.','..','...',' '],
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
    'labels':['Train_1'],
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
            elif key == 'comboboxes':
                # Cas spécial : comboboxes avec items
                for name in valeur:
                    combo = constructors[key](None)
                    combo.addItems(textes[key][name])
                    valeur_result[name] = combo
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


    def ajoute(self,layout,list):
        for i in range(len(list)):
            if isinstance(list[i], qtw.QLayout):
                layout.addLayout(list[i])
            else:
                layout.addWidget(list[i])


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
    

    def _genere_variables_unitees(self,param_labels_unitee):
        widgets = {}
        variables = {}
        for key in (param_labels_unitee):
            param = param_labels_unitee[key]
            widgets[key],variables[key] = fenetre._ajout_nom_zone_texte_unitee(key,param['unitee'],param['valeur_defaut'])
            variables[key].setValidator(param['validator'])
        return widgets,variables
    

    def creer_getters_variables_lineedits(self, objet, variables):
        if isinstance(variables, dict):
            prop_name = "variables" 
            def _getter(objet):
                text = {}
                for key in variables:
                    text[key] = variables[key].text()
                return text
            setattr(objet.__class__, prop_name, property(_getter))
        else:
            for key in variables:
                prop_name = key.lower()
                def _getter(objet, k=key):
                    return variables[k].text()
                setattr(objet.__class__, prop_name, property(_getter))


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
        self.add_left()
        self.add_right()
        self.add_main()

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


    def add_left(self):
        liste = [self.labels['titre'],self.buttons['creer_projet'],self.buttons['ouvrir_projet']]
        self.ajoute(self.layouts['left'],liste)
        self.layouts['left'].addStretch() # Pour pousser les éléments vers le haut


    def add_right(self):
        self.layouts['right'].addWidget(self.widget_engrenage, alignment=qtg.Qt.AlignmentFlag.AlignTop)
        self.layouts['right'].addStretch()
        self.layouts['right'].addWidget(self.buttons['exit'])

    
    def add_main(self):
        liste = [self.layouts['left'],self.layouts['right']]
        self.ajoute(self.layouts['main'],liste)
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
        page = []
        self._page = [0]*nbr_page
        for i in range(nbr_page):
            self._page[i] = globals()[f"Page_{i}"](self)
            page_instance = self._page[i].genere_page()
            self.stack['stack'].addWidget(page_instance)
            page.append(page_instance)



    def generer_bouton_next_precedent(self,layout):
        taille = [210,50]
        fonction = ['precedente_page','next_page']
        for i, key in enumerate(self.buttons):
            self.buttons[key].setFixedSize(*taille)
            self.buttons[key].clicked.connect(getattr(self, fonction[i]))
            layout.addWidget(self.buttons[key])


    def ajoute_composants(self):
        liste = [self.stack['stack'],self.layouts['button']]
        self.ajoute(self.layouts['main'],liste)
        self.setLayout(self.layouts['main'])


    def precedente_page(self) -> None:
        '''
        permet de passer a la page precedente
        '''
        i = self.stack['stack'].currentIndex()
        if i > 0:
            self.stack['stack'].setCurrentIndex(i - 1)


    def next_page(self) -> None:
        '''
        permet de passer a la page suivante
        '''
        i = self.stack['stack'].currentIndex()
        if i < self.stack['stack'].count() - 1:
            self.stack['stack'].setCurrentIndex(i + 1)
        else:
            # ouvre fenetre attente
            self.fenetre_attente = FenetreAttenteCreation(ATTENTE_CREATION)
            self.fenetre_attente.show()
            self.close()
            # prendre les dernieres valeurs
            self.genere_projet()
            self.genere_xlsx()
            self.genere_fenetre_projet()


    def genere_projet(self):
        self._description_global =  self._page[0].variables
        self._description_train = self._page[1].variables
        values_global = [int(val) for val in self._description_global.values()]
        values_train = [int(val) for val in self._description_train.values()]
        self._train = Simulation_train(*values_global, *values_train)
    
        
    def genere_xlsx(self):
        self._param_xlsx = [xlsx.Global(),xlsx.Train(1)]
        self._param_xlsx[0].description = self._description_global
        self._param_xlsx[1].description = self._train.description
        self._projet_file = xlsx.ProjetXlsx(self._param_xlsx[0])
        self._projet_file.ecrire_description(self._param_xlsx[1],1)
        self._projet_file.save()


    def genere_fenetre_projet(self):
        self.fenetre_projet = FenetreProjet(PROJET,self._param_xlsx,self._projet_file,self._train)
        self.fenetre_projet.show()
        self.fenetre_attente.close()



class Page_0():
    def __init__(self, fenetre: Fenetre) -> None:
        '''
        generation de la page 0 qui contient le choix des parametre général du reducteur
        retourne la variable de la page
        '''
        self._fenetre = fenetre
        elements = {
            'layouts':{'main':'h','block_gauche':'v','block_centre':'v','block_droit':'h'},
            'labels':['reducteur'],
        }
        result = fenetre.genere_elements(elements,PAGE_0)
        self.layouts = result['layouts']
        self.reducteur = result['labels']['reducteur']
        self._widgets,self._variables = self._genere_widgets_unitee()
        self._labels_fleches = self._genere_fleches_page0(2)
        self.reducteur.setStyleSheet(PAGE_0['styleSheet'])
        self._add_element_block_gauche()
        self._add_element_block_centre()
        self._add_element_block_droit()
        fenetre.creer_getters_variables_lineedits(self,self._variables)
        

    def _genere_widgets_unitee(self):
        widgets,variables = self._fenetre._genere_variables_unitees(PAGE_0['labels_unitee'])
        for key in (PAGE_0['labels_unitee']):
            variables[key].setFixedWidth(60)
            widgets[key].setContentsMargins(*PAGE_0['labels_unitee'][key]['margin'])
        return widgets,variables


    def _genere_fleches_page0(self,nbr_fleche):
        label = [0]*nbr_fleche
        for i in range(nbr_fleche):
            label[i] = self._fenetre._genere_lable_image('./fleche.png')
        return label


    def _add_element_block_gauche(self):
        self.layouts['block_gauche'].addStretch()
        liste = [self._widgets['Vitesse'],self._widgets['Puissance']]
        fenetre.ajoute(self.layouts['block_gauche'],liste)
        self.layouts['block_gauche'].addStretch()


    def _add_element_block_centre(self):
        self.layouts['block_centre'].addStretch()
        self.layouts['block_centre'].addWidget(self.reducteur)
        self.layouts['block_centre'].addStretch()


    def _add_element_block_droit(self):
        self.layouts['block_droit'].addStretch()
        self.layouts['block_droit'].addWidget(self._widgets['Couple'])


    def genere_page(self):
        liste = [self.layouts['block_gauche'],self._labels_fleches[0],
                 self.layouts['block_centre'],self._labels_fleches[1],self.layouts['block_droit']]
        fenetre.ajoute(self.layouts['main'],liste)
        page = qtw.QWidget()
        page.setLayout(self.layouts['main'])
        return page



class Page_1():
    def __init__(self, fenetre: Fenetre) -> None:
        '''
        generation de la page 1 qui contient le choix du nombre de train, de leurs type et de leur materiaux
        retourne la variable de la page
        '''
        PAGE_1['styleSheet'] = """
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                border: 1px solid #222;
                border-radius: 6px;
                padding: 8px;
            }
        """
        self._genere_variable_elements_variables()
        self._add_element_block_gauche()
        self._add_element_block_droite()
        self._add_element_block_ligne()
        fenetre.creer_getters_variables_lineedits(self, self._variables)
        

    def _genere_variable_elements_variables(self):
        elements = {
            'layouts':{'page':'v','ligne':'h','bloc_gauche':'h','bloc_droit':'h'},
            'widgets':['bloc_gauche','bloc_droit'],
            'labels':['nbr_etage','1'],
            'lineedits':['nbr_train'],
            'comboboxes':['liste_deroulante']
        }
        result =fenetre.genere_elements(elements,PAGE_1)
        self.layouts = result['layouts']
        self.widgets = result['widgets']
        self.labels = result['labels']
        self.nbr_train = result['lineedits']['nbr_train']
        self.liste_deroulante = result['comboboxes']['liste_deroulante']
        widgets,self._variables = fenetre._genere_variables_unitees(PAGE_1['labels_unitee'])
        self.widgets.update(widgets)
        # config nbr_train
        self.nbr_train.setValidator(qtg.QDoubleValidator())
        self.nbr_train.setFixedWidth(80)
        self.nbr_train.setText('1')
        

    def _add_element_block_gauche(self):
        liste = [self.labels['nbr_etage'],self.nbr_train]
        fenetre.ajoute(self.layouts['bloc_gauche'],liste)
        self.widgets['bloc_gauche'].setLayout(self.layouts['bloc_gauche'])
        self.widgets['bloc_gauche'].setStyleSheet(PAGE_1['styleSheet'])


    def _add_element_block_droite(self):
        liste_widgets = [self.labels['1'],self.liste_deroulante,self.widgets['entraxe'],self.widgets['σ_max']]
        fenetre.ajoute(self.layouts['bloc_droit'],liste_widgets)
        self.widgets['bloc_droit'].setStyleSheet(PAGE_1['styleSheet'])
        self.widgets['bloc_droit'].setLayout(self.layouts['bloc_droit'])


    def _add_element_block_ligne(self):
        self.layouts['ligne'].addWidget(self.widgets['bloc_gauche'])
        self.layouts['ligne'].addSpacing(100)  # Espace fixe entre les deux blocs
        self.layouts['ligne'].addWidget(self.widgets['bloc_droit'])
        self.layouts['ligne'].addStretch()


    def genere_page(self):
        self.layouts['page'].addLayout(self.layouts['ligne'])
        self.layouts['page'].addStretch()
        page = qtw.QWidget()
        page.setLayout(self.layouts['page'])
        return page


class FenetreAttenteCreation(Fenetre):
    def __init__(self, param: dict) -> None:
        elements = {
            'layouts':{'main':'h'},
            'labels':['texte','points'],
        }
        super().__init__(param,elements)
        self.genere_fenetre()
        self.genere_changement_dynamique()


    def genere_fenetre(self):
        main = self.layouts['main']
        self.setStyleSheet(self._param['styleSheet'])
        liste = [self.labels['texte'],self.labels['points']]
        self.ajoute(main,liste)
        self.setLayout(main)


    def genere_changement_dynamique(self):
        self._points = self._param['labels'][1:]  # ['.', '..', '...',' ']
        self._index = 0
        # Timer pour l’animation
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.clignoter)
        self.timer.start(400)  # toutes les 400 ms


    def clignoter(self):
        """Fait alterner le texte du label pour simuler un clignotement."""
        self.labels['points'].setText(self._points[self._index])
        self._index = (self._index + 1) % len(self._points)


class FenetreProjet(Fenetre):
    def __init__(self, param: dict,param_xlsx:list,file:xlsx.ProjetXlsx,train) -> None:
        elements = {
            'layouts':{'main':'h','train1':'v'},
        }
        super().__init__(param,elements)
        self._train = train
        self._param_xlsx = param_xlsx
        self._file = file
        self.setStyleSheet(self._param['styleSheet'])
        layout = self.genere_train()
        self.layouts['main'].addLayout(layout)
        self.setLayout(self.layouts['main'])


    def genere_train(self):
        titre = self.genere_titre_train()
        self._zone_text_train = self.genere_widget_train()
        return self.genere_layout_train(titre)


    def genere_titre_train(self):
        titre = qtw.QLabel(*self._param['labels'])
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        titre.setFont(qtg.QFont('Arial',20, qtg.QFont.Weight.Bold)) 
        titre.setStyleSheet('color: #222; margin-bottom: 20px;padding: 8px') # Style du titre
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement
        return titre


    def genere_widget_train(self):
        train = {'widget':{},'variable':{}}
        for i, (key, value) in enumerate(self._param_xlsx[1].description.items()):
            unitee  = self._param_xlsx[1].unitee[i]
            train['widget'][key],train['variable'][key] = self._ajout_nom_zone_texte_unitee(key,unitee,str(value))
            train['variable'][key].setFixedWidth(60)
            train['variable'][key].setValidator(qtg.QIntValidator())
            train['variable'][key].editingFinished.connect(lambda k=key: self.modifie_parametre(self._zone_text_train['variable'][k].text(), k))  
        return train
    

    def genere_layout_train(self,titre):
        layout = qtw.QVBoxLayout()
        layout.addStretch()
        layout.addWidget(titre) 
        layout.addStretch()
        self.ajoute(layout, list(self._zone_text_train['widget'].values()))
        return layout


    def modifie_parametre(self, nouvelle_valeur, value_name):
        # met a jour l'objet train
        setattr(self._train, value_name, int(nouvelle_valeur))
        # met a jour le xlsx
        self._param_xlsx[1].description = self._train.description
        self._file.ecrire_description(self._param_xlsx[1],1)
        self._file.save()
        # met a jour la fenetre
        for key in self._zone_text_train['variable']:
            if key != value_name:
                self._zone_text_train['variable'][key].setText(str(self._param_xlsx[1].description[key]))


if __name__ == '__main__':

    app = qtw.QApplication(sys.argv)
    fenetre = FenetreMenu(MENU)
    fenetre.show()
    sys.exit(app.exec())
    