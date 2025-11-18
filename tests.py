from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
import sys
import os


# -------------------------------------------------------------------------
#  Backstage (petite fenêtre type "menu fichier" comme Word)
# -------------------------------------------------------------------------
class BackstagePopup(qtw.QWidget):
    def __init__(self, parent=None, callbacks=None):
        super().__init__(parent, qtc.Qt.Window | qtc.Qt.FramelessWindowHint)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.setWindowFlag(qtc.Qt.Tool)
        self.callbacks = callbacks or {}
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName("backstage")
        self.setStyleSheet("""
        QWidget#backstage {
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

        layout = qtw.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = qtw.QLabel("<b>Fichier</b>")
        layout.addWidget(title)

        options = [
            ("Nouveau", "new"),
            ("Ouvrir...", "open"),
            ("Enregistrer", "save"),
            ("Enregistrer sous...", "save_as"),
            ("Imprimer...", "print"),
        ]

        for text, key in options:
            btn = qtw.QPushButton(text)
            btn.clicked.connect(self._make_handler(key))
            layout.addWidget(btn)

        layout.addStretch(1)

    def _make_handler(self, key):
        def handler():
            self.hide()
            if key in self.callbacks:
                self.callbacks[key]()
        return handler

    def show_at_top_left(self, main_window):
        top_left = main_window.mapToGlobal(main_window.rect().topLeft())
        x = top_left.x() + 4
        y = top_left.y() + 40
        self.adjustSize()
        self.move(x, y)
        self.show()


# -------------------------------------------------------------------------
#  Fenêtre principale
# -------------------------------------------------------------------------
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exemple — Bande supérieure + Backstage")
        self.resize(900, 600)

        self.current_file = None

        self._create_toolbar()
        self._create_backstage()

        self.editor = qtw.QTextEdit()
        self.setCentralWidget(self.editor)

        self.installEventFilter(self)

    # ---------------------------------------------------------------------
    # Toolbar unique (ligne du haut)
    # ---------------------------------------------------------------------
    def _create_toolbar(self):
        toolbar = qtw.QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(qtc.Qt.TopToolBarArea, toolbar)

        # Bouton : Fichier
        fichier_btn = qtw.QPushButton("Fichier")
        fichier_btn.clicked.connect(self.open_backstage)
        fichier_btn.setFlat(True)
        toolbar.addWidget(fichier_btn)

        # Icône enregistrer
        save_icon = qtg.QIcon.fromTheme("document-save")
        save_action = toolbar.addAction(save_icon, "Enregistrer", self.save)

        # Bouton : Aide
        aide_btn = qtw.QPushButton("Aide")
        aide_btn.clicked.connect(self.about)
        aide_btn.setFlat(True)
        toolbar.addWidget(aide_btn)

    # ---------------------------------------------------------------------
    # Backstage
    # ---------------------------------------------------------------------
    def _create_backstage(self):
        self.backstage = BackstagePopup(self, callbacks={
            "new": self.new_file,
            "open": self.open_file,
            "save": self.save,
            "save_as": self.save_as,
            "print": self.print_dialog,
        })

    def open_backstage(self):
        self.backstage.show_at_top_left(self)

    # Cacher le backstage si clic en dehors
    def eventFilter(self, obj, event):
        if event.type() == qtc.QEvent.MouseButtonPress:
            if self.backstage.isVisible():
                pos = event.globalPosition().toPoint()
                if not self.backstage.geometry().contains(pos):
                    self.backstage.hide()
        return super().eventFilter(obj, event)

    # ---------------------------------------------------------------------
    # Actions fichier
    # ---------------------------------------------------------------------
    def new_file(self):
        if self.maybe_save():
            self.editor.clear()
            self.current_file = None
            self.setWindowTitle("Nouveau - Exemple")

    def open_file(self):
        if not self.maybe_save():
            return
        path, _ = qtw.QFileDialog.getOpenFileName(self, "Ouvrir un fichier", os.path.expanduser("~"),
                                                  "Texte (*.txt);;Tous les fichiers (*)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.editor.setPlainText(f.read())
                self.current_file = path
                self.setWindowTitle(os.path.basename(path))
            except Exception as e:
                qtw.QMessageBox.warning(self, "Erreur", str(e))

    def save(self):
        if self.current_file:
            return self._save_path(self.current_file)
        return self.save_as()

    def save_as(self):
        path, _ = qtw.QFileDialog.getSaveFileName(self, "Enregistrer sous", os.path.expanduser("~"),
                                                  "Texte (*.txt);;Tous les fichiers (*)")
        if path:
            return self._save_path(path)
        return False

    def _save_path(self, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.current_file = path
            self.setWindowTitle(os.path.basename(path))
            return True
        except Exception as e:
            qtw.QMessageBox.warning(self, "Erreur", str(e))
            return False

    def maybe_save(self):
        if not self.editor.document().isModified():
            return True

        msg = qtw.QMessageBox.question(
            self, "Enregistrer ?",
            "Le document a été modifié. Voulez-vous enregistrer ?",
            qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel
        )

        if msg == qtw.QMessageBox.Yes:
            return self.save()
        if msg == qtw.QMessageBox.No:
            return True
        return False

    # Impression
    def print_dialog(self):
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == qtw.QDialog.Accepted:
            self.editor.print(printer)

    # A propos
    def about(self):
        qtw.QMessageBox.information(self, "Aide", "Exemple de Backstage PySide6.\nInspiré de Microsoft Office.")

    # Fermeture propre
    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()


# -------------------------------------------------------------------------
# Lancement
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
