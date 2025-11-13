from PySide6.QtWidgets import (
    QApplication, QWidget, QFrame, QLabel, QPushButton, QGridLayout, QVBoxLayout
)
from PySide6.QtCore import Qt


app = QApplication([])

# --- Fenêtre principale ---
fenetre = QWidget()
layout_principal = QVBoxLayout(fenetre)

# --- Création du QFrame ---
frame = QFrame()
frame.setStyleSheet("""
    QFrame {
        background-color: #f0f7ff;
        border: 2px solid #4a90e2;
        border-radius: 10px;
    }
""")

# --- Layout en grille à l'intérieur du frame ---
grid = QGridLayout()

# Ajout de widgets dans la grille (ligne, colonne)
grid.addWidget(QLabel("Vitesse :"), 0, 0)
grid.addWidget(QLabel("120 km/h"), 0, 1)

grid.addWidget(QLabel("Puissance :"), 1, 0)
grid.addWidget(QLabel("250 kW"), 1, 1)

grid.addWidget(QLabel("Température :"), 2, 0)
grid.addWidget(QLabel("85 °C"), 2, 1)

# Bouton sur la dernière ligne
grid.addWidget(QPushButton("Actualiser"), 3, 0, 1, 2, alignment=Qt.AlignCenter)
# ↑ paramètres : (widget, ligne, colonne, rowspan, colspan, alignment)

# --- Attacher le layout au frame ---
frame.setLayout(grid)

# --- Ajouter le frame au layout principal ---
layout_principal.addWidget(frame)

fenetre.resize(300, 200)
fenetre.show()
app.exec()
