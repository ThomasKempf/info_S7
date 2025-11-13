#♦ New file for being able to modify every single parameters

class Calcule_train:
    """Classe de base pour les trains d'Calcule_Engrenages."""
    def __init__(self,Train_1):
        # Initialisation par défaut, nécessaire pour la sous-classe
        self.train_1 = Train_1
        self._rapport_reduction: float = 0.0 
        self.error = 0

        self._param_global = self.train_1.description['global'].description
        self._param_pignon = self.train_1.description['pignon'].description
        self._param_roue = self.train_1.description['roue'].description

    def calculer_rapport(self):
        """La méthode 'calculer_rapport' doit être implémentée par la sous-classe."""
        raise NotImplementedError("La methode 'calculer_rapport' doit être implementee par la sous-classe.")

    @property
    def rapport_reduction(self) -> float:
        """Propriété publique (getter) du rapport de reduction."""
        return self._rapport_reduction

    # On ajoute ici les différentes méthodes qui vont permettre de modifier les paramètres du train 


    def setparameters(self, a: str):
        # Construit dynamiquement le nom de la méthode
        nom_methode = f"calculer_{a}"
        methode = getattr(self, nom_methode, None)

        # Vérifie si elle existe et si elle est appelable
        if callable(methode):
            methode()
        else:
            print(f"Aucune méthode trouvée pour '{nom_methode}'")

