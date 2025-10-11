import math

from shiboken6.Shiboken import Object


class Train(Composant) :
 
def __init__(self, vitesse_enree: int,vitesse_sortie: int): 

from abc import ABC, abstractmethod


class Train(ABC):
    """
    Classe Abstraite pour les systèmes de trains d'engrenages.

    Elle définit l'attribut commun 'rapport_reduction' et oblige les 
    sous-classes à implémenter la méthode pour le calculer.
    """
    def __init__(self):
        # L'attribut '_rapport_reduction' est conventionnellement protégé 
        # (seules les sous-classes y accèdent directement pour l'écriture).
        self._rapport_reduction: float = 0.0

    @abstractmethod
    def calculer_rapport(self):
        """
        Méthode abstraite. Les sous-classes doivent fournir leur propre
        logique de calcul du rapport de réduction (formule simple ou épicicloïdale).
        """
        pass

    @property
    def rapport_reduction(self) -> float:
        """
        Propriété publique (getter) pour lire le rapport de réduction.
        C'est l'attribut '+ rapport_reduction: int' de votre diagramme UML.
        """
        return self._rapport_reduction
    