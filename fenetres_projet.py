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
import os
from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg,
    QtCore as qtc
)


# param global de la fentre generer lors du super init
PROJET = {
    'titre': 'Projet',
    'labels':['Train_1'],
    'buttons':['Fichier',''],
    'styleSheet':"""
                    QFrame#monContainer {
                        background-color: white;       /* fond blanc */
                        border: 2px solid black;       /* bordure de 2px noire */
                        border-radius: 15px;           /* coins arrondis de 15px */
                    }
                    #bp_moins { 
                        background-color: black;
                        padding: 0;
                        border-radius:3;
                        height: 6px; 
                        width: 30px; 
                    }
                    #bp_moins:hover {
                        background-color: red;
                    }
                    #bp_plus { 
                        background: none;          /* pas de fond */
                        border: none;              /* pas de bordure */
                        color: black;              /* texte noir */
                        font-size: 80px;           /* texte très gros, ajuste à ton goût */
                        font-weight: bold;         /* optionnel : texte en gras */
                    }
                    #bp_plus:hover {
                        color: red;
                    }
        """
}

class FenetreProjet(Fenetre):
    def __init__(self, reducteur:md.Reducteur, projet) -> None:
        """
        créer une fenetre Projet tout en construisant les layoutes des trains

        :param reducteur: objet de la classe Reducteur la description de touts les trains
        :param projet: instance de la classe de type Projet pour le passer à la fenetre projet
        """
        elements = {
            'layouts':{'main':'v','train':'h'},
            'widgets': ['toolbar','container'],
            'buttons':['fichier','enregistrer'],
            'scrolls':['train']
        }
        super().__init__(PROJET,elements)
        self.projet = projet
        self.reducteur = reducteur
        self.liste_train = reducteur.listeTrain
        self.setStyleSheet(self._param['styleSheet'])
        self._genere_toolbars()
        self.layouts['main'].addWidget(self.widgets['toolbar'])
        # genere les trains
        self.frames_train = []
        for i in range(len(self.liste_train)):
            self.frames_train.append(Frame_Train(reducteur,self,i))
        self.ajoute(self.layouts['train'],self.frames_train)
        if len(self.frames_train) > 1:
            self.ajoute_bp_moins()
        self.ajoute_bp_plus()
        if len(self.frames_train) >= 7:
            self.bouton_plus.hide()
        self.layouts['train'].addStretch() 
        self.widgets['container'].setLayout(self.layouts['train'])
        self.scrolls['train'].setWidget(self.widgets['container'])
        self.scrolls['train'].setWidgetResizable(True)
        # politiques de barres (facultatif)
        self.scrolls['train'].setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)
        self.scrolls['train'].setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)
        # ajoute la scrollarea au layout principal
        self.layouts['main'].addWidget(self.scrolls['train'])
        self.setLayout(self.layouts['main'])

    
    def _genere_toolbars(self) -> None:
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
    

    def _supprime_frame_train(self) -> None:
        '''
        supprime le dernier fram de train à droite, tout en reduisant aussi la liste le contenant
        
        '''
        self.reducteur.supprimer_dernier_train()
        self.frames_train[len(self.frames_train) - 1].deleteLater()
        self.met_a_jour_parametre_fenetre_entiere()
        self.frames_train.pop()
        if len(self.frames_train) > 1: 
            self.ajoute_bp_moins()
        if len(self.frames_train) < 7:
            self.bouton_plus.show()

    
    def _ajoute_frame_train(self) -> None:
        '''
        ajoute un fram de train à droite, tout en augmentant aussi la liste le contenant
        
        '''
        self.reducteur.ajouter_train('simple')
        self.frames_train[len(self.frames_train)-1].bp_moins.hide()
        self.frames_train.append(Frame_Train(self.reducteur,self,len(self.frames_train)))
        self.layouts['train'].insertWidget(len(self.frames_train)-1, self.frames_train[len(self.frames_train)-1])
        self.ajoute_bp_moins()
        self.met_a_jour_parametre_fenetre_entiere()
        if len(self.frames_train) >= 7:
            self.bouton_plus.hide()


    def met_a_jour_parametre_fenetre_entiere(self, num:int = None, value_name:str = None) -> None:
        '''
        met a jour tout les parametre de la fenetre

        :param num: numero du train qui vient d'etre modifier
        :param value_name: nom du parametre qui vient d'etre modifier
        '''
        for i, frame in enumerate(self.frames_train):
            if i == num:
                frame.met_a_jour_parametre(value_name)
            else:
                frame.met_a_jour_parametre()
        


    def ajoute_bp_moins(self) -> None:
        '''
        ajoute le bouton mois qui permet de supprimer un fram de train
        '''
        self.frames_train[len(self.frames_train)-1].bp_moins.show()
        self.frames_train[len(self.frames_train)-1].bp_moins.setFixedSize(30, 6)


    def ajoute_bp_plus(self) -> None:
        '''
        ajoute le bouton plus qui permet d'ajouter un fram de train
        '''
        self.bouton_plus = qtw.QPushButton('+')
        self.bouton_plus.clicked.connect(self._ajoute_frame_train)
        self.bouton_plus.setObjectName('bp_plus')
        self.layouts['train'].addWidget(self.bouton_plus)
        self.bouton_plus.show()


    def _fichier(self) -> None:
        '''
        fonction ratachée au bouton fichier, son nom permet de le lier autotmatique
        ne pas modifier la structure nie le nom de la methode
        '''
        self.backstage.ouvrir_list()


    def creer_nouveau_projet(self) -> None:
        '''
        genere un nouveau objet projet et ouvre directement la fenetre de creation de projet
        '''
        self.projet.fenetre_creation.showNormal()


    def ouvrir(self) -> None:
        ''' fonction test'''
        self.projet.fenetre_menu._ouvrir_projet()


    def _enregistrer(self) -> None:
        '''
        fonction ratachée au bouton enregistrer, son nom permet de le lier autotmatique
        ne pas modifier la structure nie le nom de la methode
        verifie si un xlsx est deja creer, si oui il le met a jour, sinon il lance la methode save as
        '''
        if hasattr(self, "xlsx_file"):
            for i in range(len(self.liste_train)):
                self.xlsx_file.ecrire_description_ogjet_multiple(self.liste_train[i], i + 1)
            self.xlsx_file.save()
        else:
            self.save_as()


    def save_as(self):
        '''
        ouvre une fenetre de dialogue pour enregistrer le fichier xlsx
        '''
        default_name = os.path.join(
            os.path.expanduser("~"),
            "réducteur.xlsx"
        )
        path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Enregistrer sous",
            default_name,
            "Fichier Excel (*.xlsx);;Tous les fichiers (*)"
        )
        if not path:
            return False
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"
        self.setWindowTitle(str(path))
        return self._genere_xlsx(path)


    def _create_backstage(self) -> None:
        '''
        ratache les methode au key des boutons de la liste, pour ensuite la créer à l'aide de la classse appropriee
        '''
        callbacks={
            "new": self.creer_nouveau_projet,
            "open": self.ouvrir,
            "save": self._enregistrer,
            "save_as": self.save_as,
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

    
    def _genere_xlsx(self,path) -> None:
        '''
        genere les differents instance utilisant la classe xlsx.
        xlsx_param est une liste contenant tout les parametres du projet
        en utilisant des classe tamplate pour etre sur d'avoir la bonne structure
        xlsx_file contient toute les metodes lier au ficher xlsx, permetant de le modifier et le sauvegrader

        :param path: chemain complet du fichier xlsx à creer

        **Préconditions :**
        - il est important de les laisser en instance courante pour pouvoir les lire juste avant la fermeture de la page
        - ``self._description_global`` doit etre valide et contenir la description global (vitesse,puissance,couple)
        - ``self._description_global`` doit etre un objet train
        '''
        # creation du fichier
        self.xlsx_file = xlsx.XlsxReducteur(path)
        self.xlsx_file.creation_espace_travail()
        for i in range(len(self.liste_train)):
            self.xlsx_file.ecrire_description_ogjet_multiple(self.liste_train[i], i + 1)
        self.xlsx_file.save()


class Frame_Train(qtw.QFrame):
    def __init__(self,reducteur:md.Reducteur,fenetre:FenetreProjet,numero:int):
        '''
        creer un frame contenant la representation d'un train

        :param reducteur: objet contenant la description du reducteur
        :param fenetre: fenetre donnant l'accès au methode outil mais aussi au instance de la fenetre
        :param numero: numero du train
        '''
        super().__init__()
        self.largeur_param = 270
        self.num = numero
        self.reducteur = reducteur
        self._train = reducteur.listeTrain[numero]
        self.fenetre = fenetre
        self._zone_text_train = self._genere_widget_train()
        layout = self._genere_layout_train()
        self.setLayout(layout)
        self.setFixedWidth(300)
    

    def _genere_layout_train(self) -> qtw.QVBoxLayout:
        """
        genere le layout vertical principal du train en y ajoutant les labels et widgets

        :return: layoute du train est retournée

        **Préconditions :**
        - ``self._zone_text_train`` doit être valide et contenir la key widget
        """
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self._genere_type_train()) 
        main_layout.addWidget(self._genere_image_train(), alignment=qtc.Qt.AlignCenter)
        self._genere_layoute_parametre(main_layout)
        self.main_layout = main_layout
        return main_layout


    def _genere_layoute_parametre(self,main_layout:qtw.QVBoxLayout) -> None:
        '''
        genere le layout des parametre du train en y ajoutant les labels et widgets
        
        :param main_layout: layout principal du train auquel on ajoute les parametre
        '''
        self.param_containers = []
        for key in self._zone_text_train:
            container = qtw.QFrame()
            container.setFixedWidth(self.largeur_param)
            layout = qtw.QVBoxLayout(container)
            container.setObjectName("monContainer")
            titre = qtw.QLabel(key)
            titre.setStyleSheet("font-weight: bold;")
            widget_list = [titre] + list(self._zone_text_train[key]['widget'].values()) # titre + param
            self.fenetre.ajoute(layout, widget_list)
            main_layout.addWidget(container, alignment=qtc.Qt.AlignHCenter)
            self.param_containers.append(container)
            
        self.stretch_bas = qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        main_layout.addItem(self.stretch_bas)


    def _genere_widget_train(self) -> dict[qtw.QWidget,qtw.QLineEdit]:
        """
        genere un widget et une variable associée à la valeur pour chaque paramatre du train 
        en ce basant sur les keys de la description du train

        :return: dict avec le widget et la variable liée a chaque parametre de chaque sous obj
        """
        taille_max = 0
        train_gui = {}
        description_train = self._train.description
        for global_key in description_train: 
            if global_key.startswith('_'): # parametre interne a ne pas traiter: exemple _nb_satellites
                continue
            sous_obj = {'widget':{},'variable':{},'lbl_nom':{}}
            sous_obj['objet'] = description_train[global_key]
            for i, (key, value) in enumerate(sous_obj['objet'].description.items()):
                unitee  = sous_obj['objet'].unitee[i]   
                train_gui[global_key] = self._genere_un_parametre(sous_obj,key,value,unitee)
                if sous_obj['lbl_nom'][key].sizeHint().width() > taille_max:
                    taille_max = sous_obj['lbl_nom'][key].sizeHint().width()
        # ajuste la largeur des widgets
        for global_key in train_gui:
            for key in train_gui[global_key]['lbl_nom']:
                train_gui[global_key]['lbl_nom'][key].setFixedWidth(taille_max)
                pass
        return train_gui
    

    def _genere_type_train(self) -> None:
        '''
        créer une liste deroulante pour le choix du type de train 

        :return: retourne la combobox pour directment l'ajouter au layout
        '''
        combobox = qtw.QComboBox()
        items = ['Train Simple', 'Train Epicicloïdal']
        for item in items:
            combobox.addItem(item)
            index = combobox.count() - 1
            combobox.setItemData(index, qtc.Qt.AlignCenter, qtc.Qt.TextAlignmentRole)
        if self._train.titre.startswith('train_simple_'):
            combobox.setCurrentIndex(0)
        elif self._train.titre.startswith('train_epi_'):
            combobox.setCurrentIndex(1)
        combobox.currentTextChanged.connect(self._change_type_train)
        self.combobox = combobox
        return combobox

    def _change_type_train(self) -> None:
        '''
        change le type de train en fonction de la selection dans la combobox
        '''
        # supprime les ancien containers et stretch
        for i in range(len(self.param_containers)):
            container = self.param_containers[i]
            self.main_layout.removeWidget(container)  # enlever du layout
            container.setParent(None)            # détacher du parent
            container.deleteLater()
        self.main_layout.removeItem(self.stretch_bas)
        # change le type de train
        index = self.combobox.currentIndex()
        if index == 0: # train simple
            self.reducteur.changer_type_train(self.num, 'simple')
        elif index == 1: # train epi
            self.reducteur.changer_type_train(self.num, 'epi')
        # genere les nouveau containers et ajoute au main layout
        self._train = self.reducteur.listeTrain[self.num]
        self._zone_text_train = self._genere_widget_train()
        self._genere_layoute_parametre(self.main_layout)
        self._defini_image_a_utiliser()        
        # met a jour les parametre de la fenetre et change l'image
        self.fenetre.met_a_jour_parametre_fenetre_entiere()
        


    def _genere_image_train(self):
        """
        Génère un widget contenant l'image et un label supplémentaire avec un nombre.
        """
        # Créer un conteneur pour l'image et le label
        container = qtw.QFrame()
        container.setObjectName("monContainer")
        container.setFixedSize(self.largeur_param, 230)  # Taille du conteneu
        # Label pour l'image
        self.label_image = self.fenetre._genere_lable_image('./epicicloïdale.png')
        self._defini_image_a_utiliser()
        self.label_image.setParent(container)
        self.label_image.setFixedSize(210, 210)
        self.label_image.setScaledContents(True)
        # Label pour le nombre
        label_nombre = qtw.QLabel(str(self.num), container)  # Exemple : nombre à afficher
        label_nombre.setStyleSheet('font-size: 20px; font-weight: bold; color: black; padding-left: 5px;')
        # Label - pour supprimer le train
        self.bp_moins = qtw.QPushButton(container)  # Exemple : nombre à afficher
        self.bp_moins.setObjectName('bp_moins')
        self.bp_moins.clicked.connect(self.fenetre._supprime_frame_train)
        self.label_image.move(30, 10)
        label_nombre.move(10, 5)
        self.bp_moins.move(220, 15)
        self.bp_moins.hide()
        return container
    

    def _defini_image_a_utiliser(self) -> None:
        '''
        defini l'image a utiliser en fonction du type de train
        '''
        if self._train.titre.startswith('train_simple_'):
            image = './simple.png'
        elif self._train.titre.startswith('train_epi_'):
            image = './epicicloïdale.png'
        self.label_image.setPixmap(qtg.QPixmap(image))


    def _genere_un_parametre(self,sous_obj,key,value,unitee):
        '''
        genere un parametre, les labels et le linedit sont integrer dans un widget

        :param sous_obj: sous objet de l'objet train
        :param key: nom du parametre du sous objet train
        :param value: valeur par defaut du parametre
        :param unitee: unitee du parametre
        :return: retourne le sous objet avec l'ajout de la variable linedit et du widget principale
        '''
        if key == 'nbr_satellites':
            validator = qtg.QIntValidator() # cas particulier pour le nombre de satellite
        else:
            validator = qtg.QDoubleValidator()# validator pour forcer l'entrée de nombre flottant avec point decimal
        validator.setLocale(qtc.QLocale(qtc.QLocale.C))
        # supprime le _ pour les parametre interne
        if key.startswith('_'): 
            nom = key[1:]
            if not((key == '_vitesse_entree' or key == '_puissance_entree') and self.num == 0):# ajoute le cas particulier du _vitesse_entree et puissance_entree du premier train
                gras = False
            else:
                gras = True
        else:
            nom = key
            gras = True
        # cas particulier pour le couple beta qui peut etre nul ou nbr de satellite ou un interval de 3 a 12 est vérifié, deux vérification entraine une erreur
        if key == 'beta' or key == 'nbr_satellites':
            controle_0 = False
        else:
            controle_0 = True
        # genere le widget et la variable associée
        new_value = self.arrondie_et_convertie_en_str(value)
        sous_obj['widget'][key],sous_obj['variable'][key],sous_obj['lbl_nom'][key] = self.fenetre._ajout_nom_zone_texte_unitee(nom,unitee,new_value,controle_0,gras)
        if key.startswith('_') and not((key == '_vitesse_entree' or key == '_puissance_entree') and self.num == 0):# ajoute le cas particulier du _vitesse_entree et puissance_entree du premier train
            sous_obj['variable'][key].setReadOnly(True)
        else:
            sous_obj['variable'][key].editingFinished.connect(lambda k=key, variable=sous_obj['variable'][key], obj=sous_obj['objet']:
                self._modifie_parametre(float(variable.text()), k,obj)) # self._zone_text_train n'existe pas encore
            sous_obj['variable'][key].setValidator(validator)
        sous_obj['variable'][key].setFixedWidth(60)
        if key == 'nbr_satellites':
            print('valeur_precedente',self.fenetre.valeur_precedente[str(sous_obj['variable'][key])])
            sous_obj['variable'][key].editingFinished.connect(lambda w=sous_obj['variable'][key] : self.fenetre.control_interval(w,12,3))
        return sous_obj
    

    def _modifie_parametre(self, nouvelle_valeur:int, value_name:str, sous_obj:md.Global) -> None:
        """
        Met à jour un paramètre de l'objet train, puis synchronise les modifications
        dans le fichier Excel et l'interface graphique.

        :param nouvelle_valeur: Nouvelle valeur à assigner à l'attribut spécifié.
        :param value_name: Nom de l'attribut du train à modifier.
        :param sous_obj: sous objet contenant le paramaetre modifier dans sa descritpion, ex: roue type Engrenage du Train

        **Préconditions :**
        - L'attribut ``self._train`` doit contenir la descrpition de l'objet de Type Train.
        - ``self._zone_text_train`` 
          doit être valides et contenir les clés attendues.
        """
        # met a jour l'objet train
        sous_obj.description[value_name] = nouvelle_valeur
        self.reducteur.calculer_systeme_complet()
        print(f"Paramètre '{value_name}' mis à jour à {nouvelle_valeur} pour le train {self.num}.")
        # met a jour la fenetre
        self.fenetre.met_a_jour_parametre_fenetre_entiere(self.num,value_name)


    def met_a_jour_parametre(self,value_name:str = None) -> None:
        '''
        met a jour les parametre de la fenetre en excluant celui qui vient d'etre modifier s'il y en a un
        
        :param value_name: nom du parametre qui vient d'être modifié, que l'ont as pas besoin de remettre à jour
        '''
        for global_key in  self._zone_text_train:
            for key in self._zone_text_train[global_key]['variable']:
                if key != value_name:
                    new_value = self._train.description[global_key].description[key]
                    new_value = self.arrondie_et_convertie_en_str(new_value)
                    self._zone_text_train[global_key]['variable'][key].setText(new_value)

    
    def arrondie_et_convertie_en_str(self,valeur) -> str:
        '''
        arrondie une valeur a 3 chiffre apres la virgule et la convertie en str
        
        :param valeur: valeur a arrondir
        :return: retourne la valeur arrondie en str
        '''
        new_value = round(valeur,3)
        new_value = str(new_value)
        # supprime les 0 superflus
        val = new_value.rstrip("0").rstrip(".")
        new_value = val if val != "" else "0"
        return new_value

        