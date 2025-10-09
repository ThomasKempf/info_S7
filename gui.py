import sys

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg


menu = {
    "geometrie": [100, 100, 400, 300],
    "titre": "Menu"
}
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
        self.setWindowTitle(parametre["titre"])
        self.setGeometry(*parametre["geometrie"])
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
                border: 2px solid #222;
                border-radius: 8px;
            }
            QPushButton {
                background: #fff;
                border: 2px solid #222;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 0;
                margin-bottom: 12px;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
        """)

        main_layout = qtw.QHBoxLayout()
        left_layout = qtw.QVBoxLayout()
        titre = Titre("Dimensionnement Réducteur", self)
        left_layout.addWidget(titre)
        self.bouton1 = Bouton("Créer Projet", self)
        self.bouton2 = Bouton("Ouvrir Projet", self)
        left_layout.addWidget(self.bouton1)
        left_layout.addWidget(self.bouton2)
        left_layout.addStretch()

        # Gears icon (using Unicode as placeholder)
        gears_label = qtw.QLabel("\u2699\u2699\u2699", self)
        gears_label.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter)
        gears_label.setStyleSheet("font-size: 60px; color: #444;")
        main_layout.addLayout(left_layout)
        main_layout.addWidget(gears_label)
        self.setLayout(main_layout)

if __name__ == "__main__":

    class Bouton(qtw.QPushButton):
        def __init__(self, texte, parent=None):
            super().__init__(texte, parent)

    app = qtw.QApplication(sys.argv)
    fenetre = Fenetre(menu)
    fenetre.show()
    sys.exit(app.exec())
    