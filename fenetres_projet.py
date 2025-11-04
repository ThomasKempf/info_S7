from outil_gui import Fenetre
import xlsx_reducteur as xlsx
from PySide6 import (
    QtWidgets as qtw,
    QtGui as qtg
)


PROJET = {
    'titre': 'Projet',
    'labels':['Train_1'],
    'styleSheet':"""
            QWidget {
                background: #fff; /* Couleur de fond blanche */
                font-size: 12px; /* Taille de police */
                font-weight: bold; /* Poids de police */
                padding: 10px 0; /* Rembourrage */
                margin-bottom: 12px; /* Espace entre les boutons */
        """
}


class FenetreProjet(Fenetre):
    def __init__(self,param_xlsx:list,file:xlsx.ProjetXlsx,train) -> None:
        elements = {
            'layouts':{'main':'h','train1':'v'},
        }
        super().__init__(PROJET,elements)
        self._train = train
        self._param_xlsx = param_xlsx
        self._file = file
        self.setStyleSheet(self._param['styleSheet'])
        layout = self.genere_train()
        self.layouts['main'].addLayout(layout)
        self.setLayout(self.layouts['main'])


    def genere_train(self):
        titre = self.genere_titre_train()
        self._zone_text_train = self.genere_widget_train()
        return self.genere_layout_train(titre)


    def genere_titre_train(self):
        titre = qtw.QLabel(*self._param['labels'])
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignLeft | qtg.Qt.AlignmentFlag.AlignTop) # Alignement à gauche et en haut
        titre.setFont(qtg.QFont('Arial',20, qtg.QFont.Weight.Bold)) 
        titre.setStyleSheet('color: #222; margin-bottom: 20px;padding: 8px') # Style du titre
        titre.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter) # Centrer le texte horizontalement
        return titre


    def genere_widget_train(self):
        train = {'widget':{},'variable':{}}
        for i, (key, value) in enumerate(self._param_xlsx[1].description.items()):
            unitee  = self._param_xlsx[1].unitee[i]
            train['widget'][key],train['variable'][key] = self._ajout_nom_zone_texte_unitee(key,unitee,str(value))
            train['variable'][key].setFixedWidth(60)
            train['variable'][key].setValidator(qtg.QIntValidator())
            train['variable'][key].editingFinished.connect(lambda k=key: self.modifie_parametre(self._zone_text_train['variable'][k].text(), k))  
        return train
    

    def genere_layout_train(self,titre):
        layout = qtw.QVBoxLayout()
        layout.addStretch()
        layout.addWidget(titre) 
        layout.addStretch()
        self.ajoute(layout, list(self._zone_text_train['widget'].values()))
        return layout


    def modifie_parametre(self, nouvelle_valeur, value_name):
        # met a jour l'objet train
        setattr(self._train, value_name, int(nouvelle_valeur))
        # met a jour le xlsx
        self._param_xlsx[1].description = self._train.description
        self._file.ecrire_description(self._param_xlsx[1],1)
        self._file.save()
        # met a jour la fenetre
        for key in self._zone_text_train['variable']:
            if key != value_name:
                self._zone_text_train['variable'][key].setText(str(self._param_xlsx[1].description[key]))