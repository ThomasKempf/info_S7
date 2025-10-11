

#Ce programme contient les classes et fonctions nécessaires au cimensionnement d'un train de réduction

class Train:
   
    # Classe de base concrète pour les systèmes de trains d'engrenages.

 
    
    def __init__(self):
        # L'attribut est toujours utilisé pour stocker le résultat du calcul
        self._rapport_reduction: float = 0.0

    def calculer_rapport(self):
        
        raise NotImplementedError(
            "La méthode 'calculer_rapport' doit être implémentée par la sous-classe (TrainSimple, TrainEpicicloidale)."
        )

    @property
    def rapport_reduction(self) -> float:
        """
        Propriété publique (getter) qui retourne le rapport de réduction.
        """
        return self._rapport_reduction
    
class Engrenage:
    """Représente un engrenage avec un nombre de dents."""
    def __init__(self, nbr_dents: int):
        self.nbr_dents = nbr_dents

# ---
    
class TrainSimple(Train):
   
    def __init__(self, engrenage_entree: Engrenage, engrenage_sortie: Engrenage):
        super().__init__()
        self.engrenage_entree = engrenage_entree
        self.engrenage_sortie = engrenage_sortie
        # Calcule le rapport immédiatement après l'initialisation
        self.calculer_rapport()

    def calculer_rapport(self):
        """
        Implémentation concrète de la méthode abstraite.
        Rapport = Z_sortie / Z_entree (si couple), ou Z_entree / Z_sortie (si vitesse)
        Nous utiliserons ici le rapport de vitesse (sortie/entrée).
        """
        Z_entree = self.engrenage_entree.nbr_dents
        Z_sortie = self.engrenage_sortie.nbr_dents
        
        if Z_entree != 0:
            # Rapport de vitesse (Réduction si < 1.0)
            self._rapport_reduction = Z_entree / Z_sortie 
        else:
            self._rapport_reduction = 0.0