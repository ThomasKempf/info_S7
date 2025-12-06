"""
.. codeauthor:: Thomas Krempf-Driesbach
.. date:: 2025-10-12
.. description::

    Ce code permet de créer une interface graphique du projet info S7. le main permet de lancer le projet

    Il utilise la bibliothèque PySide6 pour créer des fenêtres, des boutons et des titres personnalisés.
    La creation de la premiere fenetre est dans ce scripte, les autres fenetres sont repartie dans d'autres fichier

    Les outils utiliser pour generer la fenetres sont dans la classe Fenetre

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

def next_fenetre(fenetre_depart: qtw.QWidget, fenetre_suivante: qtw.QWidget) -> None:
    """
    Ferme la fenêtre de départ et affiche la fenêtre suivante.

    :param fenetre_depart: fenetre anterieur a fermer
    :param fenetre_suivante: nouvelle fenetre à mettre en avant
    """
    fenetre_depart.close()
    fenetre_suivante.show()


def detecte_fermeture_fenetre(fenetre: qtw.QWidget) -> None:
    """
    Cette fonction sera appelée *avant* que la fenêtre soit détruite.
    Tente de récupérer des attributs spécifiques de la fenêtre et
    ouvre la FenetreProjet si possible.

    :param fenetre: contient l'objet de la fenetre, qui est de pres ou de loin un widget
    """
    try:
        xlsx_file = getattr(fenetre, "xlsx_file")
        train = getattr(fenetre, "_train")
        fenetre_projet = FenetreProjet(xlsx_file, train)
        fenetre_projet.show()
    except Exception as e:
        print("Impossible de récupérer les attributs :", e)


class FenetreMenu(Fenetre):
    def __init__(self, param: dict) -> None:
        """
        Classe pour générer uniquement la fenêtre de menu.

        :param param: dictionnaire contenant les paramètres de la fenêtre, propre à chaque fenêtre
        """
        super().__init__(param, {
            'layouts': {'main': 'h', 'left': 'v', 'right': 'v'},
            'widgets': ['engrenages'],
            'labels': ['titre'],
            'buttons': ['creer_projet', 'ouvrir_projet', 'exit']
        })
        self.adapt_composant()
        self.add_left()
        self.add_right()
        self.add_main()


    def adapt_composant(self) -> None:
        """
        Crée et adapte les composants de la fenêtre (titres, boutons, widgets).
        """
        self._adapte_titre()
        self.buttons['exit'].setFixedSize(210, 50)
        self.buttons['exit'].clicked.connect(self.close)
        self._generer_icone_engrenage(self.widgets['engrenages'])


    def add_left(self) -> None:
        """
        Ajoute les elements du layout de gauche contenant les boutons creer projet et ouvrir projet
        """
        liste = [self.labels['titre'], self.buttons['creer_projet'], self.buttons['ouvrir_projet']]
        self.ajoute(self.layouts['left'], liste)
        self.layouts['left'].addStretch()


    def add_right(self) -> None:
        """
        Ajoute les element du layoute de droite contenant les engrenages et le bouton exite
        """
        self.layouts['right'].addWidget(self.widgets['engrenages'], alignment=qtg.Qt.AlignmentFlag.AlignTop)
        self.layouts['right'].addStretch()
        self.layouts['right'].addWidget(self.buttons['exit'])


    def add_main(self) -> None:
        """
        Compose le layout principal à partir des sous-layouts gauche et droit.
        """
        liste = [self.layouts['left'], self.layouts['right']]
        self.ajoute(self.layouts['main'], liste)
        self.setLayout(self.layouts['main'])


    def _generer_icone_engrenage(self, widget: qtw.QWidget) -> None:
        """
        Génère l'icône d'engrenage dans le widget fourni et retourne ce widget.

        :param widget: widegt dans la quelle sont ajouter les label d'engrenages
        """
        param = self._param['widget_engrenage']
        widget.setFixedSize(*param['taille'])
        for pos in param['placement_engrenages']:
            gear = qtw.QLabel('\u2699', widget)
            gear.setStyleSheet(param['styleSheet'])
            gear.adjustSize()
            x = pos[0] - gear.width() // 2
            y = pos[1] - gear.height() // 2
            gear.move(x, y)

    def _adapte_titre(self) -> None:
        """
        Configure le style et l'alignement du titre.
        """
        self.style_titre(self.labels['titre'])
        self.labels['titre'].setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop)
        self.labels['titre'].setAlignment(qtg.Qt.AlignmentFlag.AlignCenter)


if __name__ == '__main__':
    # Variable globale pour stocker l'instance de la fenêtre
    app = qtw.QApplication(sys.argv)
    # Créer les fenetres
    fenetre_menu = FenetreMenu(MENU)
    fenetre_creation = FenetreCreationProjet()
    # Surveille la femerture de la fenetre_creation
    watcher = CloseWatcher(detecte_fermeture_fenetre)
    fenetre_creation.installEventFilter(watcher)
    # lie le bouton créer projet à la mise en avant de fenetre_creation
    fenetre_menu.buttons['creer_projet'].clicked.connect(lambda checked=False: next_fenetre(fenetre_menu, fenetre_creation))
    
    fenetre_menu.show()
    sys.exit(app.exec())