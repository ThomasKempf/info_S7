# Fichier: modeles.py
import math 

# --- Définition des classes de base ---


class Global():
    def __init__(self) -> None:
        self.titre = 'parametre globale'
        self.description = {'vitesse_entree': 0,
                            'puissance_entree': 0,
                            'couple_sortie': 0
                    }
        self.unitee = ['RPM','W','Nm']
        self.error = 0


class Engrenage(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'engrenage {num}'
        super().__init__()
        self.description = {
            'resistance_elastique': 0,
            '_Diametre' : 0
        }
        self.unitee = [
            'Mpa',
            'm'
            ]
        


class Train_global(Global):
    def __init__(self) -> None:
        super().__init__()
        self.titre = 'train global'
        self.description = {
            'vitesse_entree': 0,
            'puissance_entree': 0,
            'couple_sortie': 0,
            '_couple_entree': 0,
            'entraxe': 0,
		    '_vitesse_sortie_calculee': 0,
            '_force_tangentielle_calculee': 0,
            '_rapport_reduction':0,
		    '_module': 0,
            'alpha': 20,
            'beta':0,
        }
        self.unitee = [
            'RPM',
            'W',
            'Nm',
            'Nm',
            'm',
            'RPM',
            'N',
            ' ',
            ' ',
            '°',
            '°'
            ]


class Train(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'train_{num}'
        self.description =  {
            'global': Train_global(),
            'pignon': Engrenage(0),
            'roue': Engrenage(1)
        }
        self.description['pignon'].titre = 'pignon'
        self.description['roue'].titre = 'roue'
        self.unitee = None


# Classe Engrenage (ajoutée à partir de votre exemple)
class Calcule_Engrenage:
    """Représente un Calcule_Engrenage avec ses paramètres géométriques."""
    def __init__(self, nbr_dents: int, rayon_prim: float = 0.0, alpha: float = 0.0, beta: float = 0.0, module: float = 0.0):
        self.nbr_dents = nbr_dents
        self.rayon_prim = rayon_prim
        self.alpha = alpha
        self.beta = beta
        self.module = module 

# Classe Train 
class Calcule_train:
    """Classe de base pour les trains d'Calcule_Engrenages."""
    def __init__(self):
        # Initialisation par défaut, nécessaire pour la sous-classe
        self._rapport_reduction: float = 0.0 
        self.error = 0

    def calculer_rapport(self):
        """La méthode 'calculer_rapport' doit être implémentée par la sous-classe."""
        raise NotImplementedError("La methode 'calculer_rapport' doit être implementee par la sous-classe.")

    @property
    def rapport_reduction(self) -> float:
        """Propriété publique (getter) du rapport de reduction."""
        return self._rapport_reduction

# --- Classe TrainSimple (Cinématique P/C/V) ---

class Calcule_train_simple(Calcule_train):
    
    # Représente un train d'Calcule_Engrenages droits.
    
    def __init__(self, 
                 vitesse_entree: float, 
                 puissance_entree: float, 
                 couple_sortie: float, 
                 entraxe: float, 
                 res_elastique: float):
        """
        Initialise le train d'Calcule_Engrenages simple avec ses paramètres d'entrée/sortie.
        """
        super().__init__() # Appel de l'initialisation de la classe parente
        # initialisation de l'objet
        # Initialisation l'objet train
        self.train_1 = Train(1)
        self._param_global = self.train_1.description['global'].description
        self._param_pignon = self.train_1.description['pignon'].description
        self._param_roue = self.train_1.description['roue'].description
        # implemente variable liee a Train_global
        self._param_global['vitesse_entree'] = vitesse_entree
        self._param_global['puissance_entree'] = puissance_entree
        self._param_global['couple_sortie'] = couple_sortie
        self._param_global['entraxe'] = entraxe
        # implemente variable liee au engrenages
        self._param_pignon['resistance_elastique'] = res_elastique
        self._param_roue['resistance_elastique'] = res_elastique

       # self._vitesse_sortie = None 

        # Le calcul est basé sur P, C et la conversion de rad/s en tr/min
        # ne pas oublier d'ajouter "self.methode" ici dès qu'on ajoute une nouvelle méthode
        self.calculer_parametres()

##############################################################################################################################

    def calculer_parametres(self):
        self.calculer_vitesse_sortie()
        self.calculer_couple_entree()
        self.calculer_force_tangentielle()
        self.calculer_module()
        self.calculer_rapport()
        self.calculer_diametres_primitifs()



    def calculer_vitesse_sortie(self):
        """
        Calcule la vitesse de sortie en tr/min à partir de la puissance (P) et du couple de sortie (Cs).
        Formule utilisée : V_out [tr/min] = (P / Cs) * (60 / 2*pi).
        Cette formule suppose un rendement de 1 (idéal) et que P est en Watts, Cs en Nm.
        """
        P_entree = self._param_global['puissance_entree']
        Couple_sortie = self._param_global['couple_sortie']

        if Couple_sortie <= 0:
            print("Erreur : Le couple de sortie doit être positif.")
            self.train_1.error = 1 # exemple comment utiliser error
            vitesse_sortie = 0.0
        else: 
            # Calcul : (P_entree / Couple_sortie) donne la vitesse en rad/s (omega)
            #           ... * (60 / 2*pi) convertit de rad/s à tr/min
            vitesse_sortie = (P_entree / Couple_sortie) * (60 / (2 * math.pi))
            
        # Mise à jour du dictionnaire 'description'
        self._param_global['_vitesse_sortie_calculee'] = vitesse_sortie

        
######################################################################################################################################

    def calculer_couple_entree(self):
            # Calcule le couple d'entrée à partir de la puissance et de la vitesse d'entrée
            P_entree = self._param_global['puissance_entree']
            V_entree = self._param_global['vitesse_entree']

            self._param_global['_couple_entree'] = P_entree / (V_entree * (2 * math.pi / 60))  # Convertir tr/min en rad/s
    
######################################################################################################################################

    def calculer_force_tangentielle(self):
        # Calcule la force tangentielle à partir du couple de sortie et de l'entraxe
        Ce = self._param_global['_couple_entree']
        r = self._param_global['entraxe']  # En mètres
        a = self._param_global['alpha']

        if r <= 0:
            print("Erreur : L'entraxe doit être positif.")
            force_tangentielle = 0.0
        else:
            force_tangentielle = Ce / (r *math.cos(a)) 

        self._param_global['_force_tangentielle_calculee'] = force_tangentielle

######################################################################################################################################

    # Calcul du module du système

    def calculer_module(self):

        FT = self._param_global['_force_tangentielle_calculee']
        RES = self._param_pignon['resistance_elastique'] # il n'est pas le meme pour les deux engrenages?

        self._param_global['_module'] = 2.34 * math.sqrt(FT / (RES*10))
    

######################################################################################################################################

    # Calcul des diamètres primitifs, il estr nécessaire de demander à l'utilisateur de donner 
    # un des diamètres dans la classe Calcule_Engrenage et aussi un nb de dents pour pouvoir le calculer

        # Calcul des diamètres primitifs, il est nécessaire de demander à l'utilisateur de donner 
    # un des diamètres dans la classe Calcule_Engrenage et aussi un nb de dents pour pouvoir le calculer
    def calculer_diametres_primitifs(self):
        e = self._param_global['entraxe']
        r = self._param_global['_rapport_reduction']
        D1 = (2 * e) / (1 + r)
        D2 = r * D1         

        self._param_pignon['_Diametre'] = D1
        self._param_roue['_Diametre'] = D2

    ######################################################################################################################################

    # Implémentation requise de la classe Train
    def calculer_rapport(self) -> float:
        """
        Calcule le rapport de réduction i = V_entree / V_sortie.
        Nécessite que V_entree et V_sortie soient dans les MÊMES unités (ici tr/min).
        """
        vitesse_sortie = self._param_global['_vitesse_sortie_calculee']
        if vitesse_sortie is None:
            # S'assurer que la vitesse de sortie est calculée
            self.calculer_vitesse_sortie()
            
        if vitesse_sortie == 0:
            print("Erreur : La vitesse de sortie calculée est nulle.")
            rapport_reduction = 0.0
        else:
            # i = V_entree / V_sortie
            vitesse_entree = self._param_global['vitesse_entree']
            rapport_reduction = vitesse_entree / vitesse_sortie
        
        self._param_global['_rapport_reduction'] = rapport_reduction

    ###########################################################################################

    



    
    
