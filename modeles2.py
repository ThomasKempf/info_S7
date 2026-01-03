# Fichier: modeles.py
from Parametres_dyna import Calcule_train
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
            '_diametre' : 0
        }
        self.unitee = [
            'mm'
            ]

class Train_global(Global):
    def __init__(self) -> None:
        super().__init__()
        self.titre = 'train global'
        self.description = {
            'vitesse_entree': 0,
            'puissance_entree': 0,
            'couple_sortie': 100,
            '_couple_entree': 0,
            'entraxe': 0,
		    '_vitesse_sortie': 0,
            '_force_tangentielle': 0,
            '_rapport_reduction':0,
		    '_module': 0,
            'alpha': 20,
            'beta':0,
            'resistance_elastique': 0,
        }
        self.unitee = [
            'RPM',
            'W',
            'Nm',
            'Nm',
            'mm',
            'RPM',
            'N',
            ' ',
            ' ',
            '°',
            '°',
            'MPa'
            ]


class Train_simple(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'train_simple_{num}'
        self.description =  {
            'global': Train_global(),
            'pignon': Engrenage(0),
            'roue': Engrenage(1)
        }
        self.description['pignon'].titre = 'pignon'
        self.description['roue'].titre = 'roue'
        self.unitee = None



# --- Classe TrainEpi (Cinématique P/C/V) ---
class Train_epi(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'train_epi_{num}'
        self.description =  {
            'global': Train_global(),
            'pignon': Engrenage(0),
            'satelite': Engrenage(1),
            'couronne': Engrenage(2),
            '_nb_satelite':3,
            'mode_blocage':'couronne' # ou pignon
        }
        self.description['pignon'].titre = 'pignon'
        self.description['satelite'].titre = 'roue'
        self.description['couronne'].titre = 'couronne'
        self.unitee = None


class Reducteur():
    # def __init__(self, listeTrain:list[Train_simple]) -> None:
    #     # Objectif est de renvoyer les valeurs de dimensionnement en recevant une liste contenant les différents trains de réductions
    #     self.titre = 'reducteur'
    #     self.listeTrain = listeTrain
    #     self.calculer_RR()
        

    #     self.calc_train = []
    #     for i in range (len(listeTrain)):
    #         self.calc_train.append(Calcule_train_simple(listeTrain[i]))
    def __init__(self, listeTrain: list[Train_simple]) -> None:
        self.titre = 'reducteur'
        self.listeTrain = listeTrain

        self.P_totale = listeTrain[0].description['global'].description['puissance_entree']             # Nouveau paramètre
        self.V_entree_totale = listeTrain[0].description['global'].description['vitesse_entree'] # Nouveau paramètre
        self.rr_global_vise = self.calculer_RR_global()  # Calcul du RR global visé
        
        # Étape 1 : On définit les rapports de réduction par étage
        self.calculer_RR()

        # Étape 2 : On crée les calculateurs et on injecte les données
        self.calc_train = []
        v_actuelle = self.V_entree_totale 

        for i in range(len(listeTrain)):
            # On respecte l'objectif 1 : un seul argument (le train)
            calculateur = Calcule_train_simple(listeTrain[i])
            self.calc_train.append(calculateur)
            
            # Injection dynamique avant le calcul pour éviter ZeroDivisionError
            calculateur._param_global['puissance_entree'] = self.P_totale
            calculateur._param_global['vitesse_entree'] = v_actuelle
            
            # Déclenchement manuel du calcul
            calculateur.calculer_parametres()
            
            # Mise à jour de la vitesse pour l'étage suivant (Cascade)
            v_actuelle = calculateur._param_global['_vitesse_sortie']
        
        
    def calculer_RR_global(self):
        '''
        calcule le le rapport de réduction global du réducteur
        
        :return: rapport de réduction global
        '''
        couple_sortie = self.listeTrain[-1].description['global'].description['couple_sortie']      
        omega_entree = self.V_entree_totale * 2 * math.pi / 60
        omega_sortie = self.P_totale / couple_sortie
        return omega_entree / omega_sortie


    def calculer_RR(self):
        n = len(self.listeTrain)
        if n > 0:
            # Calcul du rapport équilibré
            r_etage = self.rr_global_vise ** (1/n)
            
            for train in self.listeTrain:
                # Injection dans le dictionnaire de description
                train.description['global'].description['_rapport_reduction'] = r_etage
        

    # Rajouter dans paramdyna, une méthode de calcul pour les différents attributs nécessaires (type Vitesse entree, entraxe, etc...)
        

        

# Classe Engrenage (ajoutée à partir de votre exemple)
class Calcule_Engrenage:
    """Représente un Calcule_Engrenage avec ses paramètres géométriques."""
    def __init__(self, nbr_dents: int, rayon_prim: float = 0.0, alpha: float = 0.0, beta: float = 0.0, module: float = 0.0):
        self.nbr_dents = nbr_dents
        self.rayon_prim = rayon_prim
        self.alpha = alpha
        self.beta = beta
        self.module = module 

# --- Classe TrainSimple (Cinématique P/C/V) ---

class Calcule_train_simple(Calcule_train):
    
    # Représente un train d'Calcule_Engrenages droits.
    
    # def __init__(self,train: Train_simple) -> None:
    #     """
    #     Initialise le train d'Calcule_Engrenages simple avec ses paramètres d'entrée/sortie.
    #     """

    #     super().__init__(train) # Appel de l'initialisation de la classe parente
    #     self.calculer_parametres()

    def __init__(self, train: Train_simple) -> None:
        # On initialise seulement les dictionnaires via le parent
        super().__init__(train) 
        # SUPPRESSION de : self.calculer_parametres()

# if __name__ == '__main__':
#     print('hello')

#     # Exemple d'utilisation
#     listeTrain = [Train_simple(1), Train_simple(2)]
#     for i in range(len(listeTrain)):
#         listeTrain[i].description['global'].description['resistance_elastique'] = 340  # Exemple de puissance
#         listeTrain[i].description['global'].description['entraxe'] = 100      # Exemple de couple de sortie
       
#     listeTrain[0].description['global'].description['vitesse_entree'] = 340 
#     listeTrain[0].description['global'].description['puissance_entree'] = 340 
#     listeTrain[1].description['global'].description['couple_sortie'] = 340 
#     print('hello')
#     reducteur = Reducteur(listeTrain)
#     print(listeTrain)

if __name__ == '__main__':
    mes_etages = [Train_simple(1), Train_simple(2), Train_simple(3)] # On peut rajouter ici pour faire des essais
    
    for t in mes_etages:
        # Données de base indispensables pour le dimensionnement
        t.description['global'].description['resistance_elastique'] = 340
        t.description['global'].description['entraxe'] = 100 # en mm
    mes_etages[0].description['global'].description['vitesse_entree'] = 1500  # en RPM
    mes_etages[0].description['global'].description['puissance_entree'] = 4000  # en Watts
    mes_etages[-1].description['global'].description['couple_sortie'] = 380  # en Nm

    # Lancement avec les 3 inputs : Rapport global, Puissance, Vitesse In
    reducteur = Reducteur(mes_etages)

    #  AJOUT DES PRINTS POUR VOIR LES RÉSULTATS
    print("\n" + "="*40)
    print("      RÉSULTATS DU DIMENSIONNEMENT")
    print("="*40)

    for i, train in enumerate(mes_etages):
        # Accès aux données calculées dans le dictionnaire
        global_data = train.description['global'].description
        pignon_data = train.description['pignon'].description
        roue_data = train.description['roue'].description

        print(f"\nÉTAGES N°{i+1} ({train.titre}) :")
        print(f"  - Rapport de réduction local : {global_data['_rapport_reduction']:.2f}")
        print(f"  - Vitesse Entrée : {global_data['vitesse_entree']:.1f} RPM")
        print(f"  - Vitesse Sortie : {global_data['_vitesse_sortie']:.1f} RPM")
        print(f"  - Module calculé : {global_data['_module']:.4f} mm")
        print(f"  - Diamètre Pignon (D1) : {pignon_data['_diametre']:.2f} mm")
        print(f"  - Diamètre Roue (D2)   : {roue_data['_diametre']:.2f} mm")
    
    print("\n" + "="*40)

