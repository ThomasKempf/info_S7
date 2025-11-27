#♦ New file for being able to modify every single parameters
import math 

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
        #commm test

        
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

        # Calcul des diamètres primitifs

    def calculer_diametres_primitifs(self):
        e = self._param_global['entraxe']
        r = self._param_global['_rapport_reduction']
        D1 = (2 * e) / (1 + r)
        D2 = r * D1         

        self._param_pignon['_Diametre'] = D1
        self._param_roue['_Diametre'] = D2
        
        print("affichage e",e)
        print("affichage r",r)
        print(f"Diametre primitif pignon : {D1:.4f} m")
        print(f"Diametre primitif roue   : {D2:.4f} m")

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

    



    
    

