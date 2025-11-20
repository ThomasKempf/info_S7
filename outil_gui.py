"""
:author: Thomas Krempf-Driesbach
:date: 2025-11-12
:description:

    Ce scrypte contient la classe permetant creer une fenetre a l'aide de PySide6

    Elle permet aussi de faire des fonctionalitee de base pour structurer sa fenetre 
    a l'aide de ces methodes qui permette de simplifier les teches repetitive et recurente dans la plupart des fenetres
"""

from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg,
    QtCore as qtc
)


class Fenetre(qtw.QWidget):
    def __init__(self, param: dict,elements:dict) -> None:
        '''
        genere une fenetre vide et contient des methode de base pour la parametrer
        
        :param param: contient les parametre de base de la fenetre avec le titre le style la geometrie...
        :param elements: contient un dict avce les elements de base a generer, voir structure dans genere_elements(self)
        '''
        super().__init__()
        # met en place les parametres de base de la fenetre
        self._param = param
        self.valeur_precedente = {}
        self.setWindowTitle(param['titre'])
        self.setStyleSheet(param['styleSheet'])
        if 'geometrie' in param:
            self.setFixedSize(*param['geometrie'])
        else:
            self.showMaximized()
        # genere elements de base de la fenetre
        result =self.genere_elements(elements,param)
        for key in result:
            setattr(self, key, result[key])


    def genere_elements(self,elements:dict,textes:list) -> dict:
        """
        Génère les éléments de base constituant la fenêtre à partir de la description donnée.

        Cette méthode crée les layouts, boutons, labels, zones de saisie et autres composants
        décrits dans le dictionnaire `elements`. Les textes et listes déroulantes sont définis
        dans le dictionnaire `textes`.

        Parameters
        ----------
        elements : dict
            Contient la description de tous les éléments à créer et leurs caractéristiques.
            Exemple :
            {
                "layouts": {"main": "v", "button": "h"},
                "buttons": ["next", "precedent"],
                "stack": ["stack"]
            }
        textes : dict
            Contient les noms des labels et des listes déroulantes.
            Exemple :
            {
                "labels": ["nombre d’étage :", "1"],
                "comboboxes": {
                    "liste_deroulante": ["engrenage droit", "engrenage hélicoïdal", "conique"]
                }
            }

        Returns
        -------
        dict
            Un dictionnaire contenant les mêmes clés que `elements`, mais associées
            aux objets graphiques créés (QWidgets, boutons, layouts, etc.).
        """
        constructors = {
        'layouts': lambda spec: qtw.QVBoxLayout() if spec == 'v' else qtw.QHBoxLayout(),
        'widgets': lambda _: qtw.QWidget(),
        'labels': lambda text: qtw.QLabel(text),
        'lineedits': lambda _: qtw.QLineEdit(),
        'comboboxes': lambda _: qtw.QComboBox(),
        'buttons': lambda text: qtw.QPushButton(text),
        'stack': lambda _: qtw.QStackedWidget(),
        'frames': lambda _: qtw.QFrame(),
        'toolbars': lambda _: qtw.QToolBar(),
        'scrolls': lambda _: qtw.QScrollArea()
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
    

    def _genere_lable_image(self,name_and_path:str) -> qtw.QLabel:
        '''
        genere un label contenant une image
        
        :param name_and_path: nom et chemain de l'image
        :return: retourne le label contenant l'image
        '''
        pixmap = qtg.QPixmap(name_and_path)
        label = qtw.QLabel()
        label.setPixmap(pixmap)
        return label


    def ajoute(self,layout:qtw.QLayout,list_element:list) -> None:
        '''
        ajoute une liste d'elements au layout en parametre tout en verifiant si les elements sont les layouts ou non
        si ce ne sont pas des layouts ils sont considérer comme des widget
        
        :param layout: layout dans le quelle seront ajouter les elements
        :param list_elements: liste d'element a ajouter dans le layout
        '''
        for i in range(len(list_element)):
            if isinstance(list_element[i], qtw.QLayout):
                layout.addLayout(list_element[i])
            elif isinstance(list_element[i], int):
                layout.addSpacing(list_element[i])
            else:
                layout.addWidget(list_element[i])


    def _ajout_nom_zone_texte_unitee(self,nom:str,unitee:str,text_defaut:str) -> tuple[qtw.QWidget, qtw.QLineEdit]:
        '''
        genere un widget avec deux label et un qtw.QLineEdit, un pour le nom un pour l'unitee et une zone de texte,
        
        :param nom: nom de la variable
        :param unitee: unitee associée au parametre
        :param test_defaut: texte par defaut ecris dans la zone de texte
        :return: retourne un widgets contenant la structure et une variable contenant l'objet  qtw.QLineEdit
        '''
        layout = qtw.QHBoxLayout()
        # ajoute le label du nom
        lbl_nom = qtw.QLabel(nom)
        layout.addWidget(lbl_nom)
        # ajoute la zone de texte
        variable = qtw.QLineEdit()
        variable.setText(text_defaut)
        self.valeur_precedente[str(variable)] = text_defaut
        variable.setStyleSheet('QLineEdit {border: 1px solid #222; border-radius: 3px;}')
        variable.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        variable.editingFinished.connect(lambda w=variable : self.control_0(w))
        layout.addWidget(variable)
        # ajoute le label de l'unitee
        lbl_unitee = qtw.QLabel(unitee)
        layout.addWidget(lbl_unitee)
        # ajoute le layout principale au widget principale
        widget = qtw.QWidget()
        widget.setLayout(layout)
        return widget,variable
    
    

    def _genere_variables_unitees(self,param_labels_unitee:dict) -> tuple[dict[qtw.QWidget], dict[qtw.QLineEdit]]:
        '''
        genere un dict de widget avec deux label et un qtw.QLineEdit, un pour le nom un pour l'unitee et une zone de texte,
        ceci pour chaque key
        
        :param param_labels_unitee: contient les parametre de chaque variable que eu meme doivent contenir les clef suivante
            'unitee' 'valeur_defaut' et 'validator'
        :return: retourne un dict widgets avec les widgets de chaque parametres 
            et un dict variables avec les objet qtw.QLineEdit de chaque parametre
        '''
        # creer variable temporaire
        widgets = {}
        variables = {}
        for key in (param_labels_unitee):
            param = param_labels_unitee[key]
            # genere les variables contenant les linedit et les widget associee
            widgets[key],variables[key] = self._ajout_nom_zone_texte_unitee(key,param['unitee'],param['valeur_defaut'])
            # ajoute un validator qui permet de restraindre les possiblitee d'ecriture dans la zone de texte
            variables[key].setValidator(param['validator'])
            # modifie leurs taille
        return widgets,variables
    

    def creer_getters_variables_lineedits(self, objet, variables:dict[qtw.QLineEdit]) -> None:
        '''
        creer un getters pour un dict constituer d'objet de type qtw.QLineEdit
        un getter est créer a la fois pour le dict entier et pour chaque key

        :param objet: objet dans le quelle le dict de qtw.QLineEdit ce situe
        :param variables: dict contenant les objet de type qtw.QLineEdit a retourner
        '''
        if isinstance(variables, dict):
            # cas ou l'ont appel le dict entier de ariable
            prop_name = "variables" 
            def _getter(objet) -> dict[str]:
                # incorpore les texte dans une variable temporaire pour la retourner par la suite
                text = {}
                for key in variables:
                    text[key] = variables[key].text()
                return text
            # genere le getter pour le dict entier
            setattr(objet.__class__, prop_name, property(_getter))
        else:
            # cas ou l'ont appel une key en particulier
            for key in variables:
                prop_name = key.lower()
                def _getter(objet, k=key) -> str:
                    # return directement la valeur de la key de variable
                    return variables[k].text()
                # genere pour chaque key un getter
                setattr(objet.__class__, prop_name, property(_getter))


    def style_titre(self,titre:qtw.QLabel) -> None:
            """
            Configure le style et du titre.

            :param titre: label contenant le titre
            """
            titre.setFont(qtg.QFont('Arial', 20, qtg.QFont.Weight.Bold))
            titre.setObjectName("titre")
            titre.setStyleSheet("""
                    QLabel#titre {
                        color: #222;
                        margin-bottom: 20px;
                        padding: 8px;
                        background-color: #f8f8f8; /* Couleur de fond claire */
                        border: 2px solid #222; /* Bordure sombre */
                        border-radius: 8px; /* Bords arrondis */
                    }
            """)
            titre.adjustSize()

    
    def adapte_frames(self,frames:dict[qtw.QFrame],taille:list[tuple[int]]) -> None:
        '''
        definit la taille, le type et le style des frames utiliser

        :param frames: dictionnaire contenant les frames
        :param taille: list contenant la taille des frames dans le meme ordre que les key du dict
        '''
        for i, key in enumerate(frames):
           frames[key].setObjectName("frame")
           frames[key].setFrameShape(qtw.QFrame.Box)
           frames[key].setStyleSheet("""
                    QFrame#frame {
                        background: #fff; /* Couleur de fond blanche */
                        border: 1px solid #222;     /* Bordure */
                        border-radius: 6px;         /* Coins arrondis */
                    }
            """)
           frames[key].setFixedSize(*taille[i])


    def control_0(self,lineedits:qtw.QLineEdit,nouvelle_valeur = None) -> None:
        '''
        controle si la valeur du lineedits n'est pas egal a 0,
        sinon elle est slignaler et modifier par soit la valeur donnée, soit la précedente

        :param lineedits: objet lineedits a modifier
        :param nouvelle_valeur: nouvelle valeur correcte à lui assignée
        '''
        if lineedits.text() == '0':
            if nouvelle_valeur == None:
                nouvelle_valeur = self.valeur_precedente[str(lineedits)]
            self.signaler_lineedits_erreur(lineedits,nouvelle_valeur)
            return
        self.valeur_precedente[str(lineedits)] = lineedits.text()
        

    def signaler_lineedits_erreur(self,lineedits:qtw.QLineEdit,nouvelle_valeur:str) -> None:
        '''
        change le fond du lineedits en rouge pour signaler une erreur,
        pour ensuite le basculer a nouveau dans sa couleur initial.
        
        :param lineedits: objet lineedits a modifier
        :param nouvelle_valeur: nouvelle valeur correcte à lui assignée
        '''
        TEMPS_MAINTIENT = 500 # ms
        color = lineedits.palette().color(lineedits.backgroundRole())
        lineedits.setStyleSheet("color: red; background-color: #ffe6e6;")
        qtw.QApplication.processEvents()
        qtc.QTimer.singleShot(TEMPS_MAINTIENT, lambda: lineedits.setStyleSheet(f"background: {color};"))
        lineedits.setText(nouvelle_valeur)


class BackstagePopup(qtw.QWidget):
    def __init__(self, parent, callbacks, button) -> None:
        '''
        créeer une petite liste qui peut etre ratachée à un evenement comme le click d'un bouton
        '''
        super().__init__(parent, qtc.Qt.Window | qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.callbacks = callbacks
        self.button = button
        self._setup_ui()


    def _setup_ui(self) -> None:
        '''
        met en forme la liste constituée d'un layoute avec des boutons

        **Préconditions :**
        - ``self.callbacks`` doit avoir les memes clef que options
        '''
        # adapte le style
        self.setStyleSheet("""
        QWidget {
            background: white;
            border: 1px solid #bbb;
            border-radius: 6px;
        }
        QPushButton {
            padding: 8px 12px;
            text-align: left;
            font-size: 13px;
        }
        QPushButton:hover {
            background: #e5e5e5;
        }
        """)
        # definit les texte de chaque bouton
        options = [
            ("Nouveau", "new"),
            ("Ouvrir...", "open"),
            ("Enregistrer", "save"),
            ("Enregistrer sous...", "save_as"),
            ("Imprimer...", "print"),
        ]
        # creer et ajoute chaque bouton au layoute
        layout = qtw.QVBoxLayout(self)
        for text, key in options:
            btn = qtw.QPushButton(text)
            btn.clicked.connect(lambda checked=False, k=key: (self.hide(), self.callbacks[k]()))
            layout.addWidget(btn)


    def ouvrir_liste(self) -> None:
        '''
        rend la liste visible et connecte la methode permetant de la fermer

        **Préconditions :**
        - ``self.button`` doit rediriger vers les un bouton
        '''    
        self.adjustSize()
        self.show()
        self.button.clicked.disconnect()
        self.button.clicked.connect(self._fermer_liste)


    def _fermer_liste(self) -> None:
        '''
        ferme cache la liste et connecte la methode permetant de l'ouvrir a nouveau

        **Préconditions :**
        - ``self.button`` doit rediriger vers les un bouton
        '''
        self.button.clicked.disconnect()
        self.button.clicked.connect(self.ouvrir_liste)
        self.hide()


    def positionner_list(self,main_widget:qtw.QWidget) -> None:
        '''
        positionne la list par rapport a la taille de la fenetre

        :param main_widget: widget de la fenetre dans la quelle est ajoutee la liste
        '''
        top_left = main_widget.mapToGlobal(main_widget.rect().topLeft())
        x = top_left.x() + 4
        y = top_left.y() + 40
        self.move(x, y)


class CloseWatcher(qtc.QObject):
    def __init__(self, methode_a_appeler) -> None:
        '''
        la classe permet de mettre en place un tracker pour controler prevenir quand une fenetre ce ferme 
        et recuperer des instances de la fenetre avant qu'elle soit detruite

        :param methode_a_appeler: methode qui seras appeler lors de la detection de l'evenement
        '''
        super().__init__()
        self._methode_a_appeler = methode_a_appeler

    def eventFilter(self, objet: qtc.QObject, event: qtc.QEvent) -> bool:
        '''
        rattache l'evenement de fermer la fenetre à event pour traquer cette evenement
        et execute la fonction definit precedement dans le cas ou l'evenement ce passe

        :param objet: objet sur le quelle est traquer l'envenement
        :param event: instance de la classe QEvent qui décrit ce qui s’est passé
        :return: True si l'événement est consommé (intercepté et non transmis à l'objet),
                False pour laisser Qt continuer le traitement normal de l'événement. 

        **Préconditions :**
        - ``self._fonction_a_appeler`` doit etre valide
        '''
        if event.type() == qtc.QEvent.Close: # ratache la fonction à l'evenement .close
            try:
                self._methode_a_appeler(objet)
            except Exception as e:
                print("Erreur dans le handler de fermeture :", e)
        return super().eventFilter(objet, event) # permet de finir le traitement et de reprendre le comportement normal
