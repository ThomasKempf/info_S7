from abc import ABC, abstractmethod

class Train(ABC):
    """
    Classe de base abstraite pour tous les systèmes de trains d'engrenages.

    Elle définit une propriété commune, le rapport de réduction, et 
    exige des classes filles qu'elles implémentent leur propre 
    logique de calcul.
    """
    def __init__(self):
        # L'attribut est protégé (par convention en Python) car il est
        # calculé en interne et non fourni à la création.
        self._rapport_reduction: float = 0.0

    @abstractmethod
    def calculer_rapport(self):
        """
        Méthode abstraite pour calculer le rapport de réduction.
        Chaque sous-classe doit fournir son implémentation.
        """
        pass

    @property
    def rapport_reduction(self) -> float:
        """
        Propriété publique (getter) qui retourne le rapport de réduction.
        """
        return self._rapport_reduction