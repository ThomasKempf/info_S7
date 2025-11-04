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
    QtGui as qtg
)
from outil_gui import (Fenetre,CloseWatcher)
from fenetres_creation import FenetreCreationProjet
from fenetres_projet import FenetreProjet

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


def next_fenetre(fenetre_depart,fenetre_suivante):
    fenetre_depart.close()
    fenetre_suivante.show()


def detecte_fermeture_fenetre(fenetre):
    """
    Cette fonction sera appelée *avant* que la fenêtre soit détruite.
    Tu peux y accéder aux attributs de fenetre_creation en toute sécurité.
    """
    try:
        param_xlsx = getattr(fenetre, "_param_xlsx")
        projet_file = getattr(fenetre, "_projet_file")
        train = getattr(fenetre, "_train")
        fenetre_projet = FenetreProjet(param_xlsx,projet_file,train)
        fenetre_projet.show()
    except Exception as e:
        print("Impossible de récupérer les attributs :", e)

if __name__ == '__main__':
    # Variable globale pour stocker l'instance de la fenêtre
    app = qtw.QApplication(sys.argv)
    
    # Créer et afficher la fenêtre menu
    fenetre_menu = FenetreMenu(MENU)
    fenetre_creation = FenetreCreationProjet()

    watcher = CloseWatcher(detecte_fermeture_fenetre)
    fenetre_creation.installEventFilter(watcher)

    fenetre_menu.buttons['creer_projet'].clicked.connect(lambda checked=False: next_fenetre(fenetre_menu, fenetre_creation))
    fenetre_menu.show()
    
    sys.exit(app.exec())