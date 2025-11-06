# Fichier: modeles.py
import math 

# --- Définition des classes de base ---

# Classe Engrenage (ajoutée à partir de votre exemple)
class Engrenage:
    """Représente un engrenage avec ses paramètres géométriques."""
    def __init__(self, nbr_dents: int, rayon_prim: float = 0.0, alpha: float = 0.0, beta: float = 0.0, module: float = 0.0):
        self.nbr_dents = nbr_dents
        self.rayon_prim = rayon_prim
        self.alpha = alpha
        self.beta = beta
        self.module = module 

# Classe Train 
class Train:
    """Classe de base pour les trains d'engrenages."""
    def __init__(self):
        # Initialisation par défaut, nécessaire pour la sous-classe
        self._rapport_reduction: float = 0.0 

    def calculer_rapport(self):
        """La méthode 'calculer_rapport' doit être implémentée par la sous-classe."""
        raise NotImplementedError("La methode 'calculer_rapport' doit être implementee par la sous-classe.")

    @property
    def rapport_reduction(self) -> float:
        """Propriété publique (getter) du rapport de reduction."""
        return self._rapport_reduction

# --- Classe TrainSimple (Cinématique P/C/V) ---

class TrainSimple(Train):
    
    # Représente un train d'engrenages droits.
    
    def __init__(self, 
                 vitesse_entree: float, 
                 puissance_entree: float, 
                 couple_sortie: float, 
                 entraxe: float, 
                 res_elastique: float):
        """
        Initialise le train d'engrenages simple avec ses paramètres d'entrée/sortie.
        """
        super().__init__() # Appel de l'initialisation de la classe parente
        
        self.vitesse_entree = vitesse_entree
        self.puissance_entree = puissance_entree
        self.couple_sortie = couple_sortie
        self.entraxe = entraxe
        self.res_elastique = res_elastique
        self.alpha = 20.0  # angle de pression
        
        # Initialisation du dictionnaire
        self.description = {}

        # Remplissage du dictionnaire avec les données d'entrée
        self.description['vitesse_entree'] = vitesse_entree
        self.description['puissance_entree'] = puissance_entree 
        self.description['couple_sortie'] = couple_sortie
        self.description['entraxe'] = entraxe
        self.description['res_elastique'] = res_elastique
        self.description['alpha'] = 20.0 # anglede pression
        self.description['beta'] = 0.0   # angle de spirale

       # self._vitesse_sortie = None 

        # Le calcul est basé sur P, C et la conversion de rad/s en tr/min
        # ne pas oublier d'ajouter "self.methode" ici dès qu'on ajoute une nouvelle méthode
        self.calculer_vitesse_sortie()
        self.calculer_couple_entree()
        self.calculer_force_tangentielle()
        self.calculer_module()

##############################################################################################################################

    def calculer_vitesse_sortie(self):
        """
        Calcule la vitesse de sortie en tr/min à partir de la puissance (P) et du couple de sortie (Cs).
        Formule utilisée : V_out [tr/min] = (P / Cs) * (60 / 2*pi).
        Cette formule suppose un rendement de 1 (idéal) et que P est en Watts, Cs en Nm.
        """
        P_entree = self.puissance_entree
        Couple_sortie = self.couple_sortie

        if Couple_sortie <= 0:
            print("Erreur : Le couple de sortie doit être positif.")
            self._vitesse_sortie = 0.0
        else: 
            # Calcul : (P_entree / Couple_sortie) donne la vitesse en rad/s (omega)
            #           ... * (60 / 2*pi) convertit de rad/s à tr/min
            self._vitesse_sortie = (P_entree / Couple_sortie) * (60 / (2 * math.pi))
            
        # Mise à jour du dictionnaire 'description'
        self.description['vitesse_sortie_calculee'] = self._vitesse_sortie
        
        return self._vitesse_sortie

        
######################################################################################################################################

    def calculer_couple_entree(self):
            # Calcule le couple d'entrée à partir de la puissance et de la vitesse d'entrée
            P_entree = self.puissance_entree
            V_entree = self.vitesse_entree

            self._couple_entree = P_entree / (V_entree * (2 * math.pi / 60))  # Convertir tr/min en rad/s
            # Mise à jour du dictionnaire 'description'
            self.description['couple_entree_calcule'] = self._couple_entree
            return self._couple_entree
    
######################################################################################################################################

    def calculer_force_tangentielle(self):
        # Calcule la force tangentielle à partir du couple de sortie et de l'entraxe
        Ce = self._couple_entree
        r = self.entraxe  # En mètres
        a = self.alpha

        if r <= 0:
            print("Erreur : L'entraxe doit être positif.")
            self._force_tangentielle = 0.0
        else:
            self._force_tangentielle = Ce / (r *math.cos(a)) 

        # Mise à jour du dictionnaire 'description'
        self.description['force_tangentielle_calculee'] = self._force_tangentielle
        return self._force_tangentielle

######################################################################################################################################

    # Calcul du module du système

    def calculer_module(self):

        FT = self._force_tangentielle
        RES = self.res_elastique

        self.module = 2.34 * math.sqrt(FT / (RES*10))
        self.description['module_calcule'] = self.module
        return self.module
    

######################################################################################################################################

    # Calcul des diamètres primitifs, il estr nécessaire de demander à l'utilisateur de donner 
    # un des diamètres dans la classe engrenage et aussi un nb de dents pour pouvoir le calculer

    ######################################################################################################################################

    # Implémentation requise de la classe Train
    def calculer_rapport(self) -> float:
        """
        Calcule le rapport de réduction i = V_entree / V_sortie.
        Nécessite que V_entree et V_sortie soient dans les MÊMES unités (ici tr/min).
        """
        if self._vitesse_sortie is None:
            # S'assurer que la vitesse de sortie est calculée
            self.calculer_vitesse_sortie()
            
        if self._vitesse_sortie == 0:
            print("Erreur : La vitesse de sortie calculée est nulle.")
            self._rapport_reduction = 0.0
        else:
            # i = V_entree / V_sortie
            self._rapport_reduction = self.vitesse_entree / self._vitesse_sortie
        
        # Mise à jour du dictionnaire 'description'
        self.description['rapport_reduction_par_vitesses'] = self._rapport_reduction
        
        return self._rapport_reduction

    ###########################################################################################

        
    # NOUVELLE COMMANDE : Méthode pour afficher le dictionnaire
    def afficher_description(self):
        """
        Affiche le contenu du dictionnaire 'description' dans le terminal.
        """
        print("\n--- Description Détaillée du Train d'Engrenages ---")
        for cle, valeur in self.description.items():
            # Formatage pour une meilleure lisibilité dans le terminal
            # Si c'est un flottant, on le formate à deux décimales, sinon on imprime la valeur brute
            if isinstance(valeur, float):
                print(f"{cle.replace('_', ' ').capitalize():<30}: {valeur:.2f}")
            else:
                print(f"{cle.replace('_', ' ').capitalize():<30}: {valeur}")
        print("-------------------------------------------------")



    
    
