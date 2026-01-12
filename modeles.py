# --- Définition des classes ---
import math

# classe engrenage 
class Engrenage:
    #Represente  engrenage avec un nombre de dents.
    def __init__(self, nbr_dents: int,rayon_prim: float = 0.0, alpha: int = 0.0, beta: int = 0.0, module: float = 0.0):
        self.nbr_dents = nbr_dents
        self.rayon_prim = rayon_prim
        self.alpha = alpha
        self.beta = beta
        self.module = module 


# Classe Train
class Train:
    #Classe de base pour les trains d'engrenages.
    def __init__(self):
        self._rapport_reduction: float = 0.0

    def calculer_rapport(self):
        raise NotImplementedError(
            #La methode 'calculer_rapport' doit être implementee par la sous-classe.
        )

    @property
    def rapport_reduction(self) -> float:
        #Propriété publique (getter) du rapport de reduction.
        return self._rapport_reduction

# Classe TrainSimple
class TrainSimple(Train):
    """"
    Represente un train d'engrenages droits.
    Calcule le rapport de vitesse (i = Z_entree / Z_sortie).
    """
    def __init__(self, engrenage_entree: Engrenage, engrenage_sortie: Engrenage):
        super().__init__()
        self.engrenage_entree = engrenage_entree
        self.engrenage_sortie = engrenage_sortie
        self.calculer_rapport()

    def calculer_rapport(self):
        Z_entree = self.engrenage_entree.nbr_dents
        Z_sortie = self.engrenage_sortie.nbr_dents
        
        if Z_sortie != 0: 
            self._rapport_reduction = Z_entree / Z_sortie 
        else:
            self._rapport_reduction = 0.0

#################################################
#################################################
#################################################
#################################################

# Classe TrainSimple
class TrainSimple(Train):
    """"
    Represente un train d'engrenages droits.
    Calcule le rapport de vitesse (i = Z_entree / Z_sortie).
    """
    def __init__(self, vitesse_entree: float, puissance_entree: float, couple_sortie: float, entraxe: float, res_elastique: float,):
    
        self.vitesse_entree = vitesse_entree
        self.puissance_entree = puissance_entree
        self.couple_sortie = couple_sortie
        self.entraxe = entraxe
        self.res_elastique = res_elastique

        #Initialisation du dictionnaire et calcul des paramètres 
        self.description = {}

        self.description['_vitesse_entree'] = vitesse_entree
        self.description['_puissance_entree'] = puissance_entree  
        self.description['_couple_sortie'] = couple_sortie
        self.description['entraxe'] = entraxe
        self.description['res_elastique'] = res_elastique

        self.rapport_reduction = None
        self._vitesse_sortie = None

        self.calcul_vitesse_sortie()

    def calculer_vitesse_sortie(self):

        P_entree = self.puissance_entree
        Couple_sortie = self.couple_sortie

        if P_entree != 0: 
            self._vitesse_sortie = (P_entree/Couple_sortie)*(60/(2*math.pi)) 

        self.description['_vitesse_sortie'] = self._vitesse_sortie




