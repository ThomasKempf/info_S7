from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
)
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assistant d'installation")

        # --- Créer les pages ---
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()
        self.page3 = self.create_page3()

        # --- Créer le QStackedWidget ---
        self.stack = QStackedWidget()
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)

        # --- Boutons de navigation ---
        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Previous")

        self.next_button.clicked.connect(self.next_page)
        self.prev_button.clicked.connect(self.prev_page)

        # --- Layout principal ---
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_page1(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenue dans l'installation !"))
        layout.addWidget(QLabel("Ceci est la première étape."))
        page.setLayout(layout)
        return page

    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Étape 2 : Configuration"))
        layout.addWidget(QLabel("Ici tu peux configurer ton application."))
        page.setLayout(layout)
        return page

    def create_page3(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Installation terminée 🎉"))
        layout.addWidget(QLabel("Clique sur 'Previous' pour revenir."))
        page.setLayout(layout)
        return page

    def next_page(self):
        current = self.stack.currentIndex()
        if current < self.stack.count() - 1:
            self.stack.setCurrentIndex(current + 1)

    def prev_page(self):
        current = self.stack.currentIndex()
        if current > 0:
            self.stack.setCurrentIndex(current - 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
