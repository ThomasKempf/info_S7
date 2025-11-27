"""
:author: Thomas Krempf-Driesbach
:date: 2025-11-05
:description:

    Ce scrypte contient la classe permetant de creer et de gerer la fenetre projet

    C'est une sous classe de Fenetre qui doit en premier etre initialiser avec PROJET 
    pour ensuite créer un par un les layouts de chaque train

    Quand un parametre change le train est remis à jours à l'aide de son objet pour ensuite rafraichir la page et le xlsx
"""


from outil_gui import Fenetre,BackstagePopup
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
    'buttons':['Fichier','','Aide'],
    'styleSheet':"""
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
            'layouts':{'main':'v','train':'h'},
            'widgets': ['toolbar','container'],
            'buttons':['fichier','enregistrer','aide'],
            'scrolls':['train']
        }
        super().__init__(PROJET,elements)
        self._methode_train = train
        self._xlsx_file = xlsx_file
        self._train = train.train_1 # obj contenant toute la descritption, obj de type Train
        self.setStyleSheet(self._param['styleSheet'])
        self.genere_toolbars()
        self.layouts['main'].addWidget(self.widgets['toolbar'])
        for i in range(7):
            frame = Frame_Train(self._train,self,i+1)
            self.layouts['train'].addWidget(frame)
        self.layouts['train'].addStretch() 
        self.widgets['container'].setLayout(self.layouts['train'])
        self.scrolls['train'].setWidget(self.widgets['container'])

        self.scrolls['train'].setWidgetResizable(False)

        # politiques de barres (facultatif)
        self.scrolls['train'].setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)
        self.scrolls['train'].setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)


        # ajoute la scrollarea au layout principal
        self.layouts['main'].addWidget(self.scrolls['train'])
        self.setLayout(self.layouts['main'])

    
    def genere_toolbars(self) -> None:
        '''
        genere une bande en haut de la page avec des boutons à droite
        inspirer par la meme bande que l'ont peut trouver sur word ou exel
        '''
        # adapte le main layout a la toolbars
        self.layouts['main'].setContentsMargins(0, 0, 0, 0)
        self.layouts['main'].setSpacing(0)
        # adapte de widget associée et créer un layoute de support
        self.widgets['toolbar'].setStyleSheet("background: #ddd;")
        tb_layout = qtw.QHBoxLayout(self.widgets['toolbar'])
        tb_layout.setContentsMargins(6, 4, 6, 4)
        tb_layout.setSpacing(10)
        # ajoute les bouttons
        for key in self.buttons:
            self.buttons[key].setFlat(True)
            self.buttons[key].clicked.connect(getattr(self,f'_{key}'))
            tb_layout.addWidget(self.buttons[key])
        # adapte l'apparence du bouton enregistrer
        self.buttons['enregistrer'].setIcon(qtg.QIcon.fromTheme("document-save"))
        tb_layout.addStretch(1)
        self._create_backstage()
    



    def _fichier(self) -> None:
        '''
        fonction ratachée au bouton fichier, son nom permet de le lier autotmatique
        ne pas modifier la structure nie le nom de la methode
        '''
        self.backstage.ouvrir_liste()


    def _enregistrer(self) -> None:
        '''
        fonction ratachée au bouton enregistrer, son nom permet de le lier autotmatique
        ne pas modifier la structure nie le nom de la methode
        '''
        print('enregistrer')


    def _aide(self) -> None:
        '''
        fonction ratachée au bouton aide, son nom permet de le lier autotmatique
        ne pas modifier la structure nie le nom de la methode
        '''
        print('aide')


    def compens(self) -> None:
        ''' fonction test'''
        print('hello')

    def compens_2(self) -> None:
        ''' fonction test'''
        print('helli')

    def _create_backstage(self) -> None:
        '''
        ratache les methode au key des boutons de la liste, pour ensuite la créer à l'aide de la classse appropriee
        '''
        callbacks={
            "new": self.compens,
            "open": self.compens,
            "save": self.compens_2,
            "save_as": self.compens,
            "print": self.compens,
        }
        self.backstage = BackstagePopup(self,callbacks,self.buttons['fichier'])


    def resizeEvent(self, event: qtg.QResizeEvent) -> None:
        '''
        permet de rattacher l'évenement de modifier la taille de la page, au faite de deplacer la liste
        la methode est automatiquement appeler a l'aide de son entete predefinit dans la super classe
        '''
        super().resizeEvent(event)
        event.size()
        if hasattr(self, 'backstage') and self.backstage is not None:
            self.backstage.positionner_list(self)


class Frame_Train(qtw.QFrame):
    def __init__(self,train:md.Train_simple,fenetre:FenetreProjet,numero:int):
        '''
        creer un frame contenant la representation d'un train

        :param train: objet contenant la description du train
        :param fenetre: fenetre donnant l'accès au methode outil mais aussi au instance de la fenetre
        :param numero: numero du train
        '''
        super().__init__()
        self.num = numero
        self._train = train
        self.fenetre = fenetre
        self._zone_text_train = self.genere_widget_train()
        layout = self.genere_layout_train()
        self.setLayout(layout)
        self.setFixedWidth(300)
    

    def genere_layout_train(self) -> qtw.QVBoxLayout:
        """
        genere le layout vertical principal du train en y ajoutant les labels et widgets

        :return: layoute du train est retournée

        **Préconditions :**
        - ``self._zone_text_train`` doit être valide et contenir la key widget
        """
        layout = qtw.QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.genere_type_train()) 
        layout.addWidget(self.genere_image_train(), alignment=qtc.Qt.AlignCenter)
        layout.addStretch()
        for key in self._zone_text_train:
            self.fenetre.ajoute(layout, list(self._zone_text_train[key]['widget'].values()))
        return layout


    def genere_widget_train(self) -> dict[qtw.QWidget,qtw.QLineEdit]:
        """
        genere un widget et une variable associée à la valeur pour chaque paramatre du train 
        en ce basant sur les key du xlsx

        :return: dict avec le widget et la variable liée a chaque parametre de chaque sous obj
        """
        train_gui = {}
        description_train = self._train.description
        print('description_train:',description_train)
        for global_key in description_train:
            print('hello')  
            sous_obj = {'widget':{},'variable':{}}
            sous_obj['objet'] = description_train[global_key]
            print('sous obj:',sous_obj['objet'].description)
            print('unitee',sous_obj['objet'].unitee)
            for i, (key, value) in enumerate(sous_obj['objet'].description.items()):
                print(i)
                unitee  = sous_obj['objet'].unitee[i]   
                train_gui[global_key] = self.genere_un_parametre(sous_obj,key,value,unitee)
        return train_gui
    

    def genere_type_train(self) -> None:
        '''
        créer une liste deroulante pour le choix du type de train 
        '''
        combobox = qtw.QComboBox()
        items = ['Train Simple', 'Train Epicicloïdal']
        for item in items:
            combobox.addItem(item)
            index = combobox.count() - 1
            combobox.setItemData(index, qtc.Qt.AlignCenter, qtc.Qt.TextAlignmentRole)
        return combobox
    



    def genere_image_train(self):
        """
        Génère un widget contenant l'image et un label supplémentaire avec un nombre.
        """
        # Créer un conteneur pour l'image et le label
        container = qtw.QFrame()
        container.setObjectName("monContainer")
        container.setFixedSize(230, 230)  # Taille du conteneu
        container.setStyleSheet("""
                    QFrame#monContainer {
                        background-color: white;       /* fond blanc */
                        border: 2px solid black;       /* bordure de 2px noire */
                        border-radius: 15px;           /* coins arrondis de 15px */
                    }
        """)
        # Label pour l'image
        label_image = self.fenetre._genere_lable_image('./epicicloïdale.png')
        label_image.setParent(container)
        label_image.setFixedSize(210, 210)
        label_image.setScaledContents(True)

        # Label pour le nombre
        label_nombre = qtw.QLabel(str(self.num), container)  # Exemple : nombre à afficher
        label_nombre.setAlignment(qtc.Qt.AlignLeft)
        label_nombre.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: black;
            padding-left: 5px;
        """)


        label_image.move(10, 10)
        label_nombre.move(10, 5)
        return container





    def genere_un_parametre(self,sous_obj,key,value,unitee):
        '''
        genere un parametre, les labels et le linedit sont integrer dans un widget

        :param sous_obj: sous objet de l'objet train
        :param key: nom du parametre du sous objet train
        :param value: valeur par defaut du parametre
        :param unitee: unitee du parametre
        :return: retourne le sous objet avec l'ajout de la variable linedit et du widget principale
        '''
        sous_obj['widget'][key],sous_obj['variable'][key] = self.fenetre._ajout_nom_zone_texte_unitee(key,unitee,str(round(value,4)))
        if key.startswith('_'):
            sous_obj['variable'][key].setReadOnly(True)
        else:
            sous_obj['variable'][key].editingFinished.connect(lambda k=key, variable=sous_obj['variable'][key], obj=sous_obj['objet']:
                self.modifie_parametre(int(variable.text()), k,obj)) # self._zone_text_train n'existe pas encore
            sous_obj['variable'][key].setValidator(qtg.QIntValidator())
        sous_obj['variable'][key].setFixedWidth(60)
        return sous_obj
    

    def modifie_parametre(self, nouvelle_valeur:int, value_name:str, sous_obj:md.Global) -> None:
        """
        Met à jour un paramètre de l'objet train, puis synchronise les modifications
        dans le fichier Excel et l'interface graphique.

        :param nouvelle_valeur: Nouvelle valeur à assigner à l'attribut spécifié.
        :param value_name: Nom de l'attribut du train à modifier.
        :param sous_obj: sous objet contenant le paramaetre modifier dans sa descritpion, ex: roue type Engrenage du Train

        **Préconditions :**
        - L'attribut ``self._train`` doit contenir la descrpition de l'objet de Type Train.
        - ``self.fenetre._xlsx_file`` et ``self._zone_text_train`` 
          doivent être valides et contenir les clés attendues.
        """
        # met a jour l'objet train
        sous_obj.description[value_name] = nouvelle_valeur
        self.fenetre._methode_train.calculer_parametres()
        # met a jour le xlsx
        self.fenetre._xlsx_file.ecrire_description_ogjet_multiple(self._train,1)
        self.fenetre._xlsx_file.save()
        # met a jour la fenetre
        for global_key in  self._zone_text_train:
            for key in self._zone_text_train[global_key]['variable']:
                if key != value_name:
                    self._zone_text_train[global_key]['variable'][key].setText(str(round(self._train.description[global_key].description[key],4)))