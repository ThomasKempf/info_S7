"""
.. codeauthor:: Thomas Krempf-Driesbach
.. date:: 2025-10-12
.. description::

    Ce code permet de créer une interface graphique du projet info S7.

    Il utilise la bibliothèque PySide6 pour créer des fenêtres, des boutons et des titres personnalisés.

"""

import sys
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

# parametres que les fenetres on en commun 
DEFAULT = {
    'titre': {'police': 'Arial', 'taille': 20, 'couleur': '#222','StyleSheet': 'color: #222; margin-bottom: 20px;padding: 8px'}
}

# parametre specifique a la fenetre menu
MENU = {
    'layout': {
        'left_layout':{
            'bouttons': {'Créer Projet', 'Ouvrir Projet'}
        },
        'right_layout':{
            'bouttons': {'EXIT':[210, 50]}
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
            border: 2px solid #222; /* Bordure sombre */
            border-radius: 6px; /* Bords arrondis */
            font-size: 16px; /* Taille de police */
            font-weight: bold; /* Poids de police */
            padding: 10px 0; /* Rembourrage */
            margin-bottom: 12px; /* Espace entre les bouttons */
        }
        QPushButton:hover {
            background: #e0e0e0; /* Couleur de fond au survol */
        }
    '''
}


class Boutton(qtw.QPushButton):
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
    def __init__(self, parametre: dict) -> None:
        super().__init__()
        self._parametre = parametre
        self.setWindowTitle(self._parametre['titre'])
        self.setFixedSize(*self._parametre['geometrie'])
        self.setStyleSheet(self._parametre['styleSheet'])
        self.generer_layouts()


    def generer_boutton(self,layout_name: str) -> None:
        '''
        fonction de base pour generer les bouttons pour chaque fenetre
        layout_name : nom du layout dans lequel ajouter les bouttons
        '''
        self.bouttons = {}
        bouttons_param = self._parametre['layout'][layout_name]['bouttons']
        for texte_boutton in bouttons_param:
            # verifier si il y a une taille specifique
            if isinstance(bouttons_param, set):
                taille = None
            else:
                taille = bouttons_param[texte_boutton]
            # creer le boutton et l'ajouter au layout
            self.bouttons[texte_boutton] = Boutton(texte_boutton,taille)
            self.layouts[layout_name].addWidget(self.bouttons[texte_boutton])


    def generer_layouts(self) -> None:
        '''
        Fonction de base pour générer les layouts de chaque fenêtre.
        '''
        self.main_layout = qtw.QHBoxLayout() # Layout horizontal principal
        self.layouts = {}
        for name in self._parametre['layout']:
            self.layouts[name] = qtw.QVBoxLayout()


class FenetreMenu(Fenetre):
    '''
    Classe pour genere uniquement la fenêtre de menu.
    parametre : dictionnaire contenant les parametres de la fenetre, propre a chaque fenetre
    '''
    def __init__(self, parametre: dict) -> None:
        super().__init__(parametre)
        self._generer_titre()
        # ajoute la partie gauche avec les bouttons
        self.generer_boutton('left_layout')  # Ajouter les bouttons au layout gauche
        self.layouts['left_layout'].addStretch() # Pour pousser les éléments vers le haut
        self.main_layout.addLayout(self.layouts['left_layout']) # Ajouter le layout gauche au layout principal
        # ajoute la partie droite avec les icones et le boutton exit
        self._generer_icone_engrenage(self.layouts['right_layout'])
        self.layouts['right_layout'].addStretch()
        self.generer_boutton('right_layout') # Ajouter les bouttons au layout droit
        self.main_layout.addLayout(self.layouts['right_layout'])
        self.setLayout(self.main_layout) # Définir le layout principal pour la fenêtre


    def _generer_titre(self) -> None:
        '''
        Fonction pour générer le titre de la fenêtre
        uniquement dans la classe FenetreMenu parce que les autres fenêtres n'en ont pas besoin.
        '''
        titre = Titre('Dimensionnement Réducteur') # Titre personnalisé
        self.layouts['left_layout'].addWidget(titre)  # Ajouter le titre au layout gauche
    

    def _generer_icone_engrenage(self,layout : qtw.QVBoxLayout) -> None:
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


if __name__ == '__main__':

    app = qtw.QApplication(sys.argv)
    fenetre = FenetreMenu(MENU)
    fenetre.show()
    sys.exit(app.exec())
    