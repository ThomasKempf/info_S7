from outil_gui import (Fenetre,Simulation_train)
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
                'Vitesse':{'unitee':'RPM','valeur_defaut':'4000','validator':qtg.QIntValidator(0, 10000),'margin':[122,0,0,0]},
                'Puissance':{'unitee':'kW','valeur_defaut':'1500','validator':qtg.QIntValidator(0, 10000),'margin':[100,0,0,0]},
                'Couple':{'unitee':'Nm','valeur_defaut':'380','validator':qtg.QIntValidator(0, 10000),'margin':[0,0,100,0]}
            },
    'labels':['Reducteur'],
    'styleSheet': '''
                QWidget {
                    background: #fff;           /* Couleur de fond blanche */
                    border: 1px solid #222;     /* Bordure */
                    border-radius: 6px;         /* Coins arrondis */
                    padding: 60px;              /* Rembourrage interne */
                    font-size: 18px;             /* Taille de la police */
                    font-weight: bold;           /* Gras */
                }
        '''
}


PAGE_1 = {
    'labels_unitee':{
                'entraxe':{'unitee':'mm','valeur_defaut':'400','validator':qtg.QIntValidator(0, 10000)},
                'σ_max':{'unitee':'Mpa','valeur_defaut':'1500','validator':qtg.QIntValidator(0, 10000)},
            },
    'labels':['nombre d’étage :','1'],
    'comboboxes':{'liste_deroulante':['engrenage droit', 'engrenage hélicoïdal', 'conique']},
    'styleSheet': '''
                QWidget {
                    background: #fff; /* Couleur de fond blanche */
                    border: 1px solid #222;
                    border-radius: 6px;
                    padding: 8px;
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
        Initialise la fenetre en plus des bouton de base et de toute la structure
        param = parametre de la page situee au dessus
        '''
        elements = {
            'layouts':{'main':'v','button':'h'},
            'buttons':['next','precedent'],
            'stack':['stack']
        }
        super().__init__(CREATION_PROJET,elements)
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
            self._page[i] = globals()[f'Page_{i}'](self)
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
            fenetre_attente = FenetreAttenteCreation()
            fenetre_attente.show()
            self.showMinimized()
            # prendre les dernieres valeurs
            self.genere_projet()
            self.genere_xlsx()
            fenetre_attente.close()
            self.close()


    def genere_projet(self):
        self._description_global =  self._page[0].variables
        self._description_train = self._page[1].variables
        values_global = [int(val) for val in self._description_global.values()]
        values_train = [int(val) for val in self._description_train.values()]
        self._train = Simulation_train(*values_global, *values_train)
    
        
    def genere_xlsx(self):
        self.xlsx_param = [xlsx.Global(),xlsx.Train(1)]
        self.xlsx_param[0].description = self._description_global
        self.xlsx_param[1].description = self._train.description
        self.xlsx_file = xlsx.ProjetXlsx(self.xlsx_param[0])
        self.xlsx_file.ecrire_description(self.xlsx_param[1],1)
        self.xlsx_file.save()


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
        self._fenetre.ajoute(self.layouts['block_gauche'],liste)
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
        self._fenetre.ajoute(self.layouts['main'],liste)
        page = qtw.QWidget()
        page.setLayout(self.layouts['main'])
        return page



class Page_1():
    def __init__(self, fenetre: Fenetre) -> None:
        '''
        generation de la page 1 qui contient le choix du nombre de train, de leurs type et de leur materiaux
        '''
        self._fenetre = fenetre
        self._genere_variable_elements_variables()
        self._add_element_block_gauche()
        self._add_element_block_droite()
        self._add_element_block_ligne()
        fenetre.creer_getters_variables_lineedits(self, self._variables)
        

    def _genere_variable_elements_variables(self) -> None:
        '''
        genere tout les elements utiliser dans la fenetre tout en les adaptant
        pour ensuite les lier à des instances courante

        **Préconditions :**
        - les self.labels, layouts et widgets doivent etre valide
        - ``self._fenetre et PAGE_1`` doit etre valide
        '''
        # genere les elements principale de la fenetre
        elements = {
            'layouts':{'page':'v','ligne':'h','bloc_gauche':'h','bloc_droit':'h'},
            'widgets':['bloc_gauche','bloc_droit'],
            'labels':['nbr_etage','1'],
            'lineedits':['nbr_train'],
            'comboboxes':['liste_deroulante']
        }
        result = self._fenetre.genere_elements(elements,PAGE_1)
        # assoicie les elements avec des instance courante
        self.layouts = result['layouts']
        self.widgets = result['widgets']
        self.labels = result['labels']
        self.nbr_train = result['lineedits']['nbr_train']
        self.liste_deroulante = result['comboboxes']['liste_deroulante']
        # genere leselements restant
        widgets,self._variables = self._fenetre._genere_variables_unitees(PAGE_1['labels_unitee'])
        self.widgets.update(widgets)
        self.nbr_train.setValidator(qtg.QDoubleValidator())
        self.nbr_train.setFixedWidth(80)
        self.nbr_train.setText('1')
        self.widgets['bloc_gauche'].setStyleSheet(PAGE_1['styleSheet'])
        self.widgets['bloc_droit'].setStyleSheet(PAGE_1['styleSheet'])
        

    def _add_element_block_gauche(self):
        '''
        ajoute les elements du block gauche constituee du choix des nombres de train

        **Préconditions :**
        - les self.labels, layouts et widgets doivent etre valide
        '''
        liste = [self.labels['nbr_etage'],self.nbr_train]
        self._fenetre.ajoute(self.layouts['bloc_gauche'],liste)
        self.widgets['bloc_gauche'].setLayout(self.layouts['bloc_gauche'])


    def _add_element_block_droite(self) -> None:
        '''
        ajoute les elements du block droit constituee des parametres d'un train

        **Préconditions :**
        - les self.labels , layoute liste_deroulante et widgets doivent etre valide
        '''
        liste_widgets = [self.labels['1'],self.liste_deroulante,self.widgets['entraxe'],self.widgets['σ_max']]
        self._fenetre.ajoute(self.layouts['bloc_droit'],liste_widgets)
        self.widgets['bloc_droit'].setLayout(self.layouts['bloc_droit'])


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
        ajoute au les composants au layoute de la page pour ensuite l'integrer au widget de la page

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