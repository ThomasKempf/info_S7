"""
:author: Thomas Krempf-Driesbach
:date: 2025-11-06
:description:

    Ce scrypte contient la classe permetant creer une fenetre de creation de projet

    Cette fenetre ce décompose par des boutons next et precedent permetant de passer de page en page
    et une fenetre d'attente de creation de page

    C'est dans la classe FenetreCreationProjet dans next_page() que va etre créer le projet
    le fichier xlsx et les parametres correspondant
"""

import modeles2 as mod
from outil_gui import Fenetre
import xlsx_reducteur as xlsx
from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg,
    QtCore as qtc
)


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
                'Vitesse':{'unitee':'RPM','valeur_defaut':'4000','validator':qtg.QDoubleValidator(0.0, 10000.0, 6),'parent':'block_gauche'},
                'Puissance':{'unitee':'W','valeur_defaut':'1500','validator':qtg.QDoubleValidator(0.0, 10000.0, 6),'parent':'block_gauche'},
                'Couple':{'unitee':'Nm','valeur_defaut':'380','validator':qtg.QDoubleValidator(0.0, 10000.0, 6),'parent':'block_droit'}
            },
    'labels':['Reducteur','Choix Parametre Global'],
    'styleSheet': '''
                QWidget {
                    background: #fff;           /* Couleur de fond blanche */
                    border: 2px solid #222;     /* Bordure */
                    border-radius: 6px;         /* Coins arrondis */
                    padding: 60px;              /* Rembourrage interne */
                    font-size: 18px;             /* Taille de la police */
                    font-weight: bold;           /* Gras */
                }
                QLineEdit {
                    border: 1px solid #222;
                    border-radius: 6px;
                }
        '''
}


PAGE_1 = {
    'labels_unitee':{
                'entraxe':{'unitee':'mm','valeur_defaut':'400','validator':qtg.QIntValidator(0, 10000)},
                'σ_max':{'unitee':'Mpa','valeur_defaut':'1500','validator':qtg.QIntValidator(0, 10000)},
            },
    'labels':['nombre d’étage :','1'],
    'comboboxes':{'type_engrenage':['  Engrenage droit', '  Engrenage hélicoïdal'],
                  'type_train':['  Train Simple', '  Train Epicicloïdale']},
    'styleSheet': '''
                QWidget {
                    background: #fff; /* Couleur de fond blanche */
                }
                QWidget#sous_block {
                    border: 1px solid #222;
                    border-radius: 6px;
                }
                QLineEdit {
                    border: 1px solid #222;
                    border-radius: 3px;
                    height: 22px;
                }
                QComboBox {
                    border: 1px solid #222;
                    border-radius: 3px;
                    height: 22px;
                }
            '''
}


ATTENTE_CREATION = {
    'geometrie': [200, 60],
    'titre': 'Creation Projet',
    'labels':['creation projet','.','..','...',' '],
    'styleSheet':'''
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                font-size: 12px; /* Taille de police */
                font-weight: bold; /* Poids de police */
                padding: 10px 0; /* Rembourrage */
                margin-bottom: 12px; /* Espace entre les boutons */
        '''
}


class FenetreCreationProjet(Fenetre):
    def __init__(self) -> None:
        '''
        creer la fenetre de creation de page avec les boutons next et suivant
        et un stack permetant de defiler les differentes pages 
        l'objectif est de donner les parametre primaire permetant la creation d'un projet reducteur
        
        **Préconditions :**
        - ``CREATION_PROJET`` contient les parametres pincipale de la page, doit etre sous la bonne forme
        '''
        elements = {
            'layouts':{'main':'v','button':'h'},
            'buttons':['precedent','next'],
            'stack':['stack']
        }
        super().__init__(CREATION_PROJET,elements)
        self.generer_widget_page(nbr_page=2)
        self.layouts['button'].insertStretch(0, 1)
        self.generer_bouton_next_precedent(self.layouts['button'])
        self.ajoute_composants()


    def generer_widget_page(self, nbr_page:int) -> None:
        '''
        creer un objet pour chaque page avec la bonne classe et ajoute le au stack permetant le defilement
        
        **Préconditions :**
        - ``Page_i`` les classe de page doivent exister
        '''
        page = []
        self._page = [0]*nbr_page
        for i in range(nbr_page):
            self._page[i] = globals()[f'Page_{i}'](self)
            page_instance = self._page[i].genere_page()
            self.stack['stack'].addWidget(page_instance)
            page.append(page_instance)



    def generer_bouton_next_precedent(self, layout:qtw.QHBoxLayout) -> None:
        '''
        adapte les boutons et les lie au fonction a appeler
        
        **Préconditions :**
        - ``self.buttons`` doit etre valide avec les bonnes key
        - les fonction decrite dans ``fonction`` doivent exister
        '''
        taille = [210,50] # taille des boutons
        fonction = ['precedente_page','next_page'] # nom des fonction a appeler pour chaque bouton
        for i, key in enumerate(self.buttons):
            self.buttons[key].setFixedSize(*taille)
            self.buttons[key].clicked.connect(getattr(self, fonction[i]))
            layout.addWidget(self.buttons[key])
        self.buttons['precedent'].hide()


    def ajoute_composants(self) -> None:
        '''
        ajoute les composants de la page constituer des boutons et du stack permetant le changement de page
        
        **Préconditions :**
        - ``self.stack['stack']``,``self.layouts['button']`` et ``self.layouts['main']`` doit etre valide
        '''
        liste = [self.stack['stack'],self.layouts['button']]
        self.ajoute(self.layouts['main'],liste)
        self.setLayout(self.layouts['main'])


    def precedente_page(self) -> None:
        '''
        permet de passer a la page precedente
        
        **Préconditions :**
        - ``self.stack['stack']`` doit etre valide
        '''
        i = self.stack['stack'].currentIndex()
        if i == 1:
            self.buttons['precedent'].hide()
            self.buttons['next'].setText(CREATION_PROJET['buttons'][1])
        if i > 0:
            self.stack['stack'].setCurrentIndex(i - 1)


    def next_page(self) -> None:
        '''
        a chaque appel, passe à la page suivante, si on est à la derniere page:
            creer une fenetre d'attente pour ensuite creer le projet (objet train et fichier xlsx)

        **Préconditions :**
        - ``self.stack['stack']`` doit etre valide
        '''
        i = self.stack['stack'].currentIndex()
        if i == 0:
            self.buttons['precedent'].show()
            self.buttons['next'].setText("Créer Projet")
        if i < self.stack['stack'].count() - 1:
            self.stack['stack'].setCurrentIndex(i + 1)
        else:
            # ouvre fenetre attente
            fenetre_attente = FenetreAttenteCreation()
            fenetre_attente.show()
            self.showMinimized()
            # prendre les dernieres valeurs
            self.genere_projet()
            self.genere_xlsx()
            fenetre_attente.close()
            self.close()


    def genere_projet(self) -> None:
        '''
        extrait les données des pages pour ensuite les mettre en arguments et creer un objet train

        **Préconditions :**
        - il est important de les laisser en instance courante pour pouvoir les lire juste avant la fermeture de la page
        - ``self._page[0].variables`` doit etre valide de 0 a 1
        '''
        
        description_global =  self._page[0].variables
        self._description_global = mod.Global()
        self._description_global.description =  description_global
        self._description_train = self._page[1].variables
        values_global = [int(val) for val in description_global.values()]
        values_train = [int(val) for val in self._description_train.values()]
        self._train = mod.Calcule_train_simple(*values_global, *values_train)
    
        
    def genere_xlsx(self) -> None:
        '''
        genere les differents instance utilisant la classe xlsx.
        xlsx_param est une liste contenant tout les parametres du projet
        en utilisant des classe tamplate pour etre sur d'avoir la bonne structure
        xlsx_file contient toute les metodes lier au ficher xlsx, permetant de le modifier et le sauvegrader

        **Préconditions :**
        - il est important de les laisser en instance courante pour pouvoir les lire juste avant la fermeture de la page
        - ``self._description_global`` doit etre valide et contenir la description global (vitesse,puissance,couple)
        - ``self._description_global`` doit etre un objet train
        '''
        # creation du fichier
        self.xlsx_file = xlsx.ProjetXlsx(self._description_global)
        self.xlsx_file.ecrire_description_ogjet_multiple(self._train.train_1,1)
        self.xlsx_file.save()


class Page_0():
    def __init__(self, fenetre: Fenetre) -> None:
        '''
        genere la page 0 qui contient le choix des parametres globales: puissance vitesse couple...

        :param fenetre: objet de classe fenetre permetant d'atteindre les methode outils de celle ci
        '''
        self._fenetre = fenetre
        # genere les elements
        elements = {
            'layouts':{'main':'h','block_gauche':'v','block_centre':'v','block_droit':'h'},
            'labels':['reducteur','titre'],
            'frames':['block_gauche','block_droit']
        }
        result = fenetre.genere_elements(elements,PAGE_0)
        # lie les elements a des instances courantes
        self.layouts = result['layouts']
        self.labels = result['labels']
        self.labels['reducteur'].setStyleSheet(PAGE_0['styleSheet'])
        self.frames = result['frames']
        taille = [[170, 120],[170, 60]]
        self._fenetre.adapte_frames(self.frames,taille)
        self._widgets,self._variables = self._genere_widgets_unitee()
        self._labels_fleches = self._genere_fleches_page0(2)
        self._fenetre.style_titre(self.labels['titre'])
        # ajoute les elements
        self._add_element_block_gauche_et_droite()
        self._add_element_block_centre()
        fenetre.creer_getters_variables_lineedits(self,self._variables)
         

    def _genere_widgets_unitee(self) -> tuple[dict[qtw.QWidget], dict[qtw.QLineEdit]]:
        '''
        genere les widgets des parametre a unitee, 
        chaque widget contien le nom, un QLineEdit et une unitee

        :return: un dict contenant les widget de chaque parametre
        :return: un dict contenant les QLineEdit pour lire ou modifier sa valeur

        **Préconditions :**
        - ``(PAGE_0['labels_unitee']`` doit exister et avoir la bonne structure
        - ``self._fenetre`` et ``self.frames`` doit etre un objet de la classe Fenetre
        - _adapte_frames(self) doit etre appeler avant cette methode
        '''
        widgets,variables = self._fenetre._genere_variables_unitees(PAGE_0['labels_unitee'])
        for key in (PAGE_0['labels_unitee']):
            parent = PAGE_0['labels_unitee'][key]['parent']
            widgets[key].setParent(self.frames[parent])
            widgets[key].setStyleSheet('background: #fff')
            variables[key].setFixedWidth(40)
            widgets[key].adjustSize()
        return widgets,variables
    

    def _genere_fleches_page0(self, nbr_fleche:int) -> list[qtw.QLabel]:
        '''
        genere une liste contenant les labels des flèches

        :param nbr_fleche: definit le nombre de label generer
        :return: liste de labels contenant la flèche

        **Préconditions :**
        - ``./fleche.png`` doit exister
        - ``fenetre`` doit etre un objet de la classe Fenetre
        '''
        label = [0]*nbr_fleche
        for i in range(nbr_fleche):
            label[i] = self._fenetre._genere_lable_image('./fleche.png')
        return label
        

    def _add_element_block_gauche_et_droite(self) -> None:
        '''
        place les elements contenu dans les farmes du block gauche et droit pour ensuite les ajouter à leurs layout

        **Préconditions :**
        - ``self.layouts`` et ``self._widgets`` doivent etre valide et contenir les bonne key
        '''
        widgets_pose = [[21,10],[5,62],[20,10]]
        for i, key in enumerate(self._widgets):
            self._widgets[key].move(*widgets_pose[i])
        key_liste = ['block_gauche','block_droit']
        for i in range(len(key_liste)):
            self.layouts[key_liste[i]].addWidget(self.frames[key_liste[i]])


    def _add_element_block_centre(self) -> None:
        '''
        ajoute les elements du block centre constituee du label reducteur

        **Préconditions :**
        - ``self.layouts`` et ``self.reducteur`` doivent etre valide
        '''
        self.layouts['block_centre'].addStretch()
        self.layouts['block_centre'].addWidget(self.labels['reducteur'])
        self.layouts['block_centre'].addStretch()


    def genere_page(self) -> qtw.QWidget:
        '''
        ajoute les composants au layoute de la page pour ensuite l'integrer au widget de la page

        :return: widget de la page

        **Préconditions :**
        - ``self.layouts`` doivent etre valide et contenir les bonnes clef
        - ``fenetre`` doit etre un objet de la classe Fenetre
        '''

        self.layouts['main'].addStretch()
        liste = [self.layouts['block_gauche'],self._labels_fleches[0],
                 self.layouts['block_centre'],self._labels_fleches[1],self.layouts['block_droit']]
        self._fenetre.ajoute(self.layouts['main'],liste)
        self.layouts['main'].addStretch()
        self.layouts['main'].setSpacing(40)
        page = qtw.QWidget()
        page.setLayout(self.layouts['main'])
        self.labels['titre'].setParent(page)
        self.labels['titre'].move(60, 10)
        return page



class Page_1():
    def __init__(self, fenetre: Fenetre) -> None:
        '''
        generation de la page 1 qui contient le choix du nombre de train, de leurs type et de leur materiaux
        '''
        self._fenetre = fenetre
        self._genere_elements()
        self._add_element_block_gauche()
        self._add_element_block_droite()
        self._add_element_block_ligne()
        fenetre.creer_getters_variables_lineedits(self, self._variables)
        

    def _genere_elements(self) -> None:
        '''
        genere tout les elements utiliser dans la page tout en les adaptant
        pour ensuite les lier à des instances courante

        **Préconditions :**
        - les self.labels, layouts et widgets doivent etre valide
        - ``self._fenetre et PAGE_1`` doit etre valide
        '''
        # genere les elements principale de la page
        elements = {
            'layouts':{'page':'v','ligne':'h','bloc_gauche':'h','bloc_droit':'h','list':'h'},
            'widgets':['bloc_gauche','bloc_droit','list'],
            'labels':['nbr_etage','1'],
            'lineedits':['nbr_train'],
            'comboboxes':['type_engrenage','type_train']
        }
        result = self._fenetre.genere_elements(elements,PAGE_1)
        # assoicie les elements avec des instance courante
        self.layouts = result['layouts']
        self.widgets = result['widgets']
        self.labels = result['labels']
        self.nbr_train = result['lineedits']['nbr_train']
        self.comboboxes = result['comboboxes']
        # genere les elements restant
        self._genere_elements_a_unitee()
        self.nbr_train.setValidator(qtg.QDoubleValidator())
        self.nbr_train.setFixedWidth(30)
        self.nbr_train.setText('1')
        self.widgets['bloc_gauche'].setStyleSheet(PAGE_1['styleSheet'])
        self.widgets['bloc_droit'].setStyleSheet(PAGE_1['styleSheet'])
        

    def _genere_elements_a_unitee(self):
        widgets,self._variables = self._fenetre._genere_variables_unitees(PAGE_1['labels_unitee'])
        for key in self._variables:
            widgets[key].setObjectName("sous_block")
            self._variables[key].setFixedWidth(40)
        self.widgets.update(widgets)


    def _add_element_block_gauche(self):
        '''
        ajoute les elements du block gauche constituee du choix des nombres de train

        **Préconditions :**
        - les self.labels, layouts et widgets doivent etre valide
        '''
        liste = [self.labels['nbr_etage'],self.nbr_train]
        self._fenetre.ajoute(self.layouts['bloc_gauche'],liste)
        self.widgets['bloc_gauche'].setLayout(self.layouts['bloc_gauche'])
        self.widgets['bloc_gauche'].setObjectName("sous_block")


    def _add_element_block_droite(self) -> None:
        '''
        ajoute les elements du block droit constituee des parametres d'un train

        **Préconditions :**
        - les self.labels , layoute liste_deroulante et widgets doivent etre valide
        '''
        for key in self.comboboxes:
            self.layouts['list'].addWidget(self.comboboxes[key])
        self.widgets['list'].setLayout(self.layouts['list'])
        self.widgets['list'].setObjectName("sous_block")
        liste_widgets = [self.labels['1'],self.widgets['list'],self.widgets['entraxe'],self.widgets['σ_max']]
        self._fenetre.ajoute(self.layouts['bloc_droit'],liste_widgets)
        self.widgets['bloc_droit'].setLayout(self.layouts['bloc_droit'])
        self.widgets['bloc_droit'].setObjectName("sous_block")


    def _add_element_block_ligne(self) -> None:
        '''
        ajoute les elements du block ligne constituer du block gauche avec le nbr de train 
        et le block droit avec les differents parametre de train

        **Préconditions :**
        - ``self.layouts['ligne'], self.widgets['bloc_gauche'], self.widgets['bloc_droit'] `` doivent etre valide
        '''
        self.layouts['ligne'].addWidget(self.widgets['bloc_gauche'])
        self.layouts['ligne'].addSpacing(100)  # Espace fixe entre les deux blocs
        self.layouts['ligne'].addWidget(self.widgets['bloc_droit'])
        self.layouts['ligne'].addStretch()


    def genere_page(self) -> qtw.QWidget:
        '''
        ajoute les composants au layoute de la page pour ensuite l'integrer au widget de la page

        :return: widget de la page

        **Préconditions :**
        - ``self.layouts['page'], self.layouts['ligne'] `` doivent etre valide
        '''
        self.layouts['page'].addLayout(self.layouts['ligne'])
        self.layouts['page'].addStretch()
        page = qtw.QWidget()
        page.setLayout(self.layouts['page'])
        return page


class FenetreAttenteCreation(Fenetre):
    def __init__(self) -> None:
        '''
        genere une fenetre avec un label texte 'creation projet' et un label dynamique avec des ...

        **Préconditions :**
        - ``ATTENTE_CREATION`` doit exister et avoir la bonne structure 
        '''
        elements = {
            'layouts':{'main':'h'},
            'labels':['texte','points'],
        }
        super().__init__(ATTENTE_CREATION,elements)
        self.genere_fenetre()
        self.genere_changement_dynamique()


    def genere_fenetre(self) -> None:
        '''
        adapte le style du laout main et y ajoute le label texte et celui des points dynamoique
        pour ensuite ajouter le main à la fenetre

        **Préconditions :**
        - ``self.layouts['main'], self._param['styleSheet'], self.labels['points']`` 
            doivent être valide 
        '''
        main = self.layouts['main']
        self.setStyleSheet(self._param['styleSheet'])
        liste = [self.labels['texte'],self.labels['points']]
        self.ajoute(main,liste)
        self.setLayout(main)


    def genere_changement_dynamique(self) -> None:
        '''
        creer un timer pour appeler de maniere cyclique self.clignoter

        **Préconditions :**
        - ``self._param['labels']`` doit être contenir un liste de str
        '''
        self._points = self._param['labels'][1:]  # ['.', '..', '...',' ']
        self._index = 0
        # Timer pour l’animation
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.clignoter)
        self.timer.start(400)  # toutes les 400 ms


    def clignoter(self) -> None:
        '''
        Permet le chamgement du text tu label a chaque appel

        **Préconditions :**
        - ``self.labels['points']`` doit être valide 
        - ``self._points`` doit contenir une liste de str
        - ``self._index`` ne doit etre initialiser à 0
        '''
        # ecriture du prochain text
        self.labels['points'].setText(self._points[self._index])
        # incremente l'indexe et le remet à zero si la taille de la liste est dépassée
        self._index = (self._index + 1) % len(self._points)