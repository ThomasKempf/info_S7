
from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg,
    QtCore as qtc
)

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
            widgets[key],variables[key] = self._ajout_nom_zone_texte_unitee(key,param['unitee'],param['valeur_defaut'])
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


class CloseWatcher(qtc.QObject):
    def __init__(self, handler):
        super().__init__()
        # handler = fonction à appeler quand on détecte la fermeture
        self._handler = handler

    def eventFilter(self, obj, event):
        # qtc.QEvent.Close est émis juste avant la fermeture (avant destruction)
        if event.type() == qtc.QEvent.Close:
            try:
                # Appelle la fonction de traitement en lui passant l'objet fenêtre
                self._handler(obj)
            except Exception as e:
                print("Erreur dans le handler de fermeture :", e)
        # on laisse l'événement continuer (ne pas bloquer la fermeture)
        return super().eventFilter(obj, event)