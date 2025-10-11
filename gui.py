import sys

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

menu = {
    "geometrie": [100, 100, 400, 300],
    "titre": "Menu",
    "styleSheet": """
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
            margin-bottom: 12px; /* Espace entre les boutons */
        }
        QPushButton:hover {
            background: #e0e0e0; /* Couleur de fond au survol */
        }
    """,
    "buttons": ["Créer Projet", "Ouvrir Projet"]
}

class Bouton(qtw.QPushButton):
    def __init__(self, texte, parent=None):
        super().__init__(texte, parent)


class Titre(qtw.QLabel):
    def __init__(self, texte, parent=None):
        super().__init__(texte, parent)
        self.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop)
        font = qtg.QFont("Arial", 20, qtg.QFont.Weight.Bold)
        self.setFont(font)
        self.setStyleSheet("color: #222; margin-bottom: 20px;")

class Fenetre(qtw.QWidget):
    def __init__(self, parametre):
        super().__init__()
        self._parametre = parametre
        self.setWindowTitle(self._parametre["titre"])
        self.setGeometry(*self._parametre["geometrie"])
        self.setStyleSheet(self._parametre["styleSheet"])
        self.main_layout = qtw.QHBoxLayout() # Layout horizontal principal
        self.left_layout = qtw.QVBoxLayout() # Layout vertical pour les boutons et le titre

    def ajouter_bouton(self,layout):
        self.boutons = {}
        for texte_bouton in self._parametre["buttons"]:
            self.boutons[texte_bouton] = Bouton(texte_bouton, self)
            layout.addWidget(self.boutons[texte_bouton])

class FenetreMenu(Fenetre):
    def __init__(self, parametre):
        super().__init__(parametre)

        titre = Titre("Dimensionnement Réducteur", self) # Titre personnalisé
        self.left_layout.addWidget(titre)  # Ajouter le titre au layout gauche
        self.ajouter_bouton(self.left_layout)  # Ajouter les boutons au layout gauche
        self.left_layout.addStretch() # Pour pousser les éléments vers le haut
        # Conteneur pour les engrenages
        self.gears_widget = qtw.QWidget(self)
        self.gears_widget.setFixedSize(210, 210)  # Taille du conteneur
        placement_engreanes = [(60, 105), (150, 155), (150, 52)] 
        for pos in placement_engreanes:
            gear = qtw.QLabel("\u2699", self.gears_widget)  # Unicode pour l'icône d'engrenage
            gear.setStyleSheet(f"background: transparent; border: none; font-size: 90px; color: #444;")  # Style de l'icône
            gear.adjustSize()   # Ajuster la taille du QLabel à son contenu
            x = pos[0] - gear.width() // 2
            y = pos[1] - gear.height() // 2
            gear.move(x, y)  # Positionner l'icône
        # Ajouter le widget contenant les engrenages dans ton layout principal
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addWidget(self.gears_widget, alignment=qtg.Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

    def creer_projet(self):
        print("Créer Projet clicked")

    def ouvrir_projet(self):
        print("Ouvrir Projet clicked")

if __name__ == "__main__":


    app = qtw.QApplication(sys.argv)
    fenetre = FenetreMenu(menu)
    fenetre.show()
    sys.exit(app.exec())
    