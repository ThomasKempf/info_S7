import sys

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

menu = {
    "geometrie": [700, 300],
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
        self.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        font = qtg.QFont("Arial", 20, qtg.QFont.Weight.Bold) # Police personnalisée
        self.setFont(font) 
        self.setStyleSheet("color: #222; margin-bottom: 20px;padding: 8px") # Style du titre
        self.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement


class Fenetre(qtw.QWidget):
    def __init__(self, parametre):
        super().__init__()
        self._parametre = parametre
        self.setWindowTitle(self._parametre["titre"])
        self.setFixedSize(*self._parametre["geometrie"])
        self.setStyleSheet(self._parametre["styleSheet"])
        self.main_layout = qtw.QHBoxLayout() # Layout horizontal principal
        self.layouts = {}
        self.layouts["child"] = qtw.QVBoxLayout() # Layout vertical pour les boutons et le titre

    def ajouter_bouton(self,layout):
        self.boutons = {}
        for texte_bouton in self._parametre["buttons"]:
            self.boutons[texte_bouton] = Bouton(texte_bouton, self)
            layout.addWidget(self.boutons[texte_bouton])

class FenetreMenu(Fenetre):
    def __init__(self, parametre):
        super().__init__(parametre)
        self._generer_titre()
        self.ajouter_bouton(self.layouts["child"])  # Ajouter les boutons au layout gauche
        self.layouts["child"].addStretch() # Pour pousser les éléments vers le haut
        self._generer_icone_engrenage()
        self.setLayout(self.main_layout) # Définir le layout principal pour la fenêtre

    def _generer_titre(self):
        titre = Titre("Dimensionnement Réducteur", self) # Titre personnalisé
        self.layouts["child"].addWidget(titre)  # Ajouter le titre au layout gauche
    
    def _generer_icone_engrenage(self):
        self.gears_widget = qtw.QWidget(self)
        self.gears_widget.setFixedSize(210, 210)  # Taille du conteneur
        placement_engreanes = [(60, 105), (150, 150), (150, 52)] 
        for pos in placement_engreanes:
            gear = qtw.QLabel("\u2699", self.gears_widget)  # Unicode pour l'icône d'engrenage
            gear.setStyleSheet(f"background: transparent; border: none; font-size: 90px; color: #444;")  # Style de l'icône
            gear.adjustSize()   # Ajuster la taille du QLabel à son contenu
            x = pos[0] - gear.width() // 2
            y = pos[1] - gear.height() // 2
            gear.move(x, y)  # Positionner l'icône
        # Ajouter le widget contenant les engrenages dans ton layout principal
        self.main_layout.addLayout(self.layouts["child"])
        self.main_layout.addWidget(self.gears_widget, alignment=qtg.Qt.AlignmentFlag.AlignTop)
        


if __name__ == "__main__":


    app = qtw.QApplication(sys.argv)
    fenetre = FenetreMenu(menu)
    fenetre.show()
    sys.exit(app.exec())
    