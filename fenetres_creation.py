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

# validator pour les float
validator = qtg.QDoubleValidator()
validator.setLocale(qtc.QLocale(qtc.QLocale.C))

CREATION_PROJET = {
    'buttons':['Précedent','Next'],
    'geometrie': [940, 600],
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
                'Vitesse':{'unitee':'RPM','valeur_defaut':'4000','validator':validator,'parent':'block_gauche'},
                'Puissance':{'unitee':'W','valeur_defaut':'1500','validator':validator,'parent':'block_gauche'},
                'Couple':{'unitee':'Nm','valeur_defaut':'380','validator':validator,'parent':'block_droit'}
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
    'labels':['nombre d’étage :'],
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


LIGNE_TRAIN = {
    'labels_unitee':{
                'entraxe':{'unitee':'mm','valeur_defaut':'400','validator':validator},
                'σ_max':{'unitee':'Mpa','valeur_defaut':'1500','validator':validator},
            },
    'labels':['1'],
    'comboboxes':{'type_engrenage':['  Engrenage droit', '  Engrenage hélicoïdal'],
                  'type_train':['  Train Simple', '  Train Epicicloïdal']},
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
        self._generer_widget_page(nbr_page=2)
        self.layouts['button'].insertStretch(0, 1)
        self._generer_bouton_next_precedent(self.layouts['button'])
        self._ajoute_composants()


    def _generer_widget_page(self, nbr_page:int) -> None:
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



    def _generer_bouton_next_precedent(self, layout:qtw.QHBoxLayout) -> None:
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


    def _ajoute_composants(self) -> None:
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
            fenetre_attente.close()
            self.close()
            self.precedente_page()


    def genere_projet(self) -> None:
        '''
        extrait les données des pages pour ensuite les mettre en arguments et creer un objet train

        **Préconditions :**
        - il est important de les laisser en instance courante pour pouvoir les lire juste avant la fermeture de la page
        - ``self._page[0].variables`` doit etre valide de 0 a 1
        '''
        # cette fonction est encore en prototype le temps que les differentes classes de calcul soit implementée
        # extrait les description des pages
        description_global =  self._page[0].variables
        variables_lignes = self._page[1].variables_lignes
        # lis des données des linedits et des differentes variables
        values_global = [float(val) for val in description_global.values()]
        mes_etages = []
        for num_train in range(len(variables_lignes)):
            values_train = []
            variables_train = variables_lignes[num_train]
            # creation du train
            if variables_train['type_train'] == '  Train Simple':
                mes_etages.append(mod.Train_simple(num_train + 1))
            elif variables_train['type_train'] == '  Train Epicicloïdal':
                mes_etages.append(mod.Train_epi(num_train + 1))
            if variables_train['type_engrenage'] == '  Engrenage hélicoïdal':
                mes_etages[num_train].description['global'].description['beta'] = 20 # angle d'hélice par defaut
            # incorporation des valeur
            for key in variables_train:
                if isinstance(variables_train[key],str):
                    values_train.append(variables_train[key]) # cas des combobox
                else:
                    values_train.append(float(variables_train[key].text())) # cas des linedits
            mes_etages[num_train].description['global'].description['entraxe'] = values_train[0]
            mes_etages[num_train].description['global'].description['resistance_elastique'] = values_train[1]
        # ajout des parametres globals
        mes_etages[0].description['global'].description['vitesse_entree'] = values_global[0]
        mes_etages[0].description['global'].description['puissance_entree'] = values_global[1]
        mes_etages[-1].description['global'].description['couple_sortie'] = values_global[2]
        self._reducteur = mod.Reducteur(mes_etages)


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
            par_defaut = PAGE_0['labels_unitee'][key]['valeur_defaut']
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
        self.labels['titre'].move(10, 10)
        return page



class Page_1():
    def __init__(self, fenetre: Fenetre) -> None:
        '''
        generation de la page 1 qui contient le choix du nombre de train, de leurs type et de leur materiaux

        :param fenetre: objet de classe fenetre permetant d'atteindre les methode outils de celle ci
        '''
        self._fenetre = fenetre
        self._nbr_lignes_precedent = 1
        self._genere_elements()
        self._add_element_block_gauche()
        self._genere_premiere_ligne()
        self._add_element_block_ligne()


    @property
    def variables_lignes(self):
        '''
        retourne une liste contenant le dict des variables lineedit de chaque ligne
        '''
        liste_variable = []
        for i in range(len(self._lignes)):
            liste_variable.append(self._lignes[i].variables)
        return liste_variable
        

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
            'layouts':{'page':'v','premiere_ligne':'h','bloc_gauche':'h','ligne':'h','ligne_vertical':'v'},
            'widgets':['bloc_gauche'],
            'labels':['nbr_etage'],
            'lineedits':['nbr_train'],
        }
        result = self._fenetre.genere_elements(elements,PAGE_1)
        # assoicie les elements avec des instance courante
        self.layouts = result['layouts']
        self.widgets = result['widgets']
        self.labels = result['labels']
        self.nbr_train = result['lineedits']['nbr_train']
        # genere les elements restant
        self.nbr_train.setValidator(qtg.QIntValidator(0, 9))
        self.nbr_train.setFixedWidth(30)
        self.nbr_train.setText('1')
        self.nbr_train.editingFinished.connect(self._refresh_ligne)
        self.nbr_train.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.widgets['bloc_gauche'].setStyleSheet(PAGE_1['styleSheet'])


    def _genere_premiere_ligne(self):
        '''
        reactualise le nombre de ligne, relis la variable associée 
        pour ensuite suprimmer ou ajouter une par une les lignes
        '''
        # genere premiere ligne
        self._lignes =[]
        self._lignes.append(LigneTrain(self._fenetre,1))
        self.widgets['premiere_ligne'] = self._lignes[0].widget
        # adapte et ajoute widget des lignes suivante qui n'existe pas encore
        self.layouts['ligne_vertical'].setSpacing(15)
        widget = qtw.QWidget()
        widget.setLayout(self.layouts['ligne_vertical'])
        self.layouts['ligne'].addStretch()
        self.layouts['ligne'].addWidget(widget)
        self._variables = self._lignes[0].variables


    def _refresh_ligne(self) -> None:
        '''
        reactualise le nombre de ligne, relis la variable associée 
        pour ensuite suprimmer ou ajouter une par une les lignes
        '''
        # verifie la valeur
        MAX = 7
        nouveau_nbr_ligne = int(self.nbr_train.text())
        if nouveau_nbr_ligne > MAX or nouveau_nbr_ligne == 0:
            if nouveau_nbr_ligne > MAX:
                nouveau_nbr_ligne = MAX
            else:
                nouveau_nbr_ligne = 1
            self._fenetre.signaler_lineedits_erreur(self.nbr_train,str(nouveau_nbr_ligne))
        # reactualise les lignes
        difference = nouveau_nbr_ligne - self._nbr_lignes_precedent
        if difference < 0:
            for i in range(abs(difference)):
                self._suprime_une_ligne(self._nbr_lignes_precedent - i - 1)
        elif difference > 0:
            for i in range(difference):
                self._ajoute_une_ligne(self._nbr_lignes_precedent + i)
        self._nbr_lignes_precedent = nouveau_nbr_ligne
        

    def _ajoute_une_ligne(self,num) -> None:
        '''
        ajoute un nouvelle objet de Ligne_train à la liste et au layouts asscociée

        :param num: numero de la nouvelle ligne de train dans la liste
        '''
        self._lignes.append(LigneTrain(self._fenetre,num+1))
        self.layouts['ligne_vertical'].addWidget(self._lignes[num].widget)

    
    def _suprime_une_ligne(self,num) -> None:
        '''
        suprimme un objet de Ligne_train à la liste et au layouts asscociée

        :param num: numero de la ligne de train dans la liste
        '''
        self.layouts['ligne_vertical'].removeWidget(self._lignes[num].widget)
        self._lignes[num].widget.deleteLater()
        self._lignes.pop(num)


    def _add_element_block_gauche(self) -> None:
        '''
        ajoute les elements du block gauche constituee du choix des nombres de train

        **Préconditions :**
        - les self.labels, layouts et widgets doivent etre valide
        '''
        liste = [self.labels['nbr_etage'],self.nbr_train]
        self._fenetre.ajoute(self.layouts['bloc_gauche'],liste)
        self.widgets['bloc_gauche'].setLayout(self.layouts['bloc_gauche'])
        self.widgets['bloc_gauche'].setObjectName("sous_block")



    def _add_element_block_ligne(self) -> None:
        '''
        ajoute les elements du block ligne constituer du block gauche avec le nbr de train 
        et le block droit avec les differents parametre de train

        **Préconditions :**
        - ``self.layouts['premiere_ligne'], self.widgets['bloc_gauche'], self.widgets['bloc_droit'] `` doivent etre valide
        '''
        self.layouts['premiere_ligne'].addWidget(self.widgets['bloc_gauche'])
        self.layouts['premiere_ligne'].addSpacing(93)  # Espace fixe entre les deux blocs
        self.layouts['premiere_ligne'].addWidget(self.widgets['premiere_ligne'])
        self.layouts['premiere_ligne'].addStretch()


    def genere_page(self) -> qtw.QWidget:
        '''
        ajoute les composants au layoute de la page pour ensuite l'integrer au widget de la page

        :return: widget de la page

        **Préconditions :**
        - ``self.layouts['page'], self.layouts['premiere_ligne'] `` doivent etre valide
        '''
        self.layouts['page'].addLayout(self.layouts['premiere_ligne'])
        self.layouts['page'].addLayout(self.layouts['ligne'])
        self.layouts['page'].addStretch()
        page = qtw.QWidget()
        page.setLayout(self.layouts['page'])
        return page


class LigneTrain():
    def __init__(self,fenetre,numero) -> None:
        '''
        genere un widget avec tout les elements necessaire à la partie droite d'un train

        :param fenetre: objet de classe fenetre permetant d'atteindre les methode outils de celle ci
        :param numero: numero du train dans l'ordre croissant du reducteur
        '''
        self._fenetre = fenetre
        self._numero = numero
        self._genere_elements()
        self._add_element_block_droite()
    

    @property
    def variables(self) -> dict[str]:
        '''
        au varaibles 
        '''
        variables = self._variables
        for key in self.comboboxes:
            variables[key] = self.comboboxes[key].currentText()
        return variables


    @property
    def widget(self) -> qtw.QWidget:
        '''
        acces au widget du module entier
        '''
        return self._widgets['main']
    

    def _genere_elements(self) -> None:
        '''
        genere tout les elements utiliser dans la partie droite de la page necessaire pour un train

        **Préconditions :**
        - ``self._fenetre et PAGE_1`` doit etre valide
        '''
        elements = {
            'layouts':{'main':'h','list':'h'},
            'widgets':['main','list'],
            'labels':['1'],
            'comboboxes':['type_engrenage','type_train']
        }
        result = self._fenetre.genere_elements(elements,LIGNE_TRAIN)
        self.layouts = result['layouts']
        self._widgets = result['widgets']
        self.numero_train = result['labels']['1']
        self.numero_train.setText(str(self._numero))
        self.comboboxes = result['comboboxes']
        # genere les elements restant
        self._genere_elements_a_unitee()
        self._widgets['main'].setStyleSheet(LIGNE_TRAIN['styleSheet'])


    def _genere_elements_a_unitee(self) -> None:
        '''
        genere les elements avec unitée, l'entraxe et la resistance elastique
        '''
        widgets,self._variables = self._fenetre._genere_variables_unitees(LIGNE_TRAIN['labels_unitee'])
        for key in self._variables:
            widgets[key].setObjectName("sous_block")
            self._variables[key].setFixedWidth(40)
            par_defaut = LIGNE_TRAIN['labels_unitee'][key]['valeur_defaut']
        self._widgets.update(widgets)


    def _add_element_block_droite(self) -> None:
        '''
        ajoute les elements du block droit constituee des parametres d'un train

        **Préconditions :**
        - les self.labels , layoute liste_deroulante et widgets doivent etre valide
        '''
        # ajoute les combobox au layout list
        for key in self.comboboxes:
            self.layouts['list'].addWidget(self.comboboxes[key])
        self._widgets['list'].setLayout(self.layouts['list'])
        self._widgets['list'].setObjectName("sous_block")
        # ajoute tout les elements au layout main
        liste_widgets = [3,self.numero_train,self._widgets['list'],30,self._widgets['entraxe'],self._widgets['σ_max'],3]
        self._fenetre.ajoute(self.layouts['main'],liste_widgets)
        # adapte le widget principal
        self._widgets['main'].setLayout(self.layouts['main'])
        self._widgets['main'].setObjectName("sous_block")
        self._widgets['main'].setFixedHeight(55)
        # adapte le label numero train
        self.numero_train.setObjectName("sous_block")
        self.numero_train.setFixedWidth(45)
        self.numero_train.setAlignment(qtc.Qt.AlignCenter)



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
        self._genere_fenetre()
        self._genere_changement_dynamique()


    def _genere_fenetre(self) -> None:
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


    def _genere_changement_dynamique(self) -> None:
        '''
        creer un timer pour appeler de maniere cyclique self.clignoter

        **Préconditions :**
        - ``self._param['labels']`` doit être contenir un liste de str
        '''
        self._points = self._param['labels'][1:]  # ['.', '..', '...',' ']
        self._index = 0
        # Timer pour l’animation
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self._clignoter)
        self.timer.start(400)  # toutes les 400 ms


    def _clignoter(self) -> None:
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