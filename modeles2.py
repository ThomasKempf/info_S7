# Fichier: modeles.py
from Parametres_dyna import Calcule_train

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
            'm',
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
        }
        self.description['pignon'].titre = 'pignon'
        self.description['satelite'].titre = 'roue'
        self.description['couronne'].titre = 'couronne'
        self.unitee = None


class Reducteur():
    def __init__(self, listeTrain:list[Train_simple]) -> None:
        # Objectif est de renvoyer les valeurs de dimensionnement en recevant une liste contenant les différents trains de réductions
        self.titre = 'reducteur'
        self.listeTrain = listeTrain
        self.calculer_RR()
        

        self.calc_train = []
        for i in range (len(listeTrain)):
            self.calc_train.append(Calcule_train_simple(listeTrain[i]))
        
    def calculer_RR(self):
        #calcul rapport de réduction
        pass

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
    
    def __init__(self,train: Train_simple) -> None:
        """
        Initialise le train d'Calcule_Engrenages simple avec ses paramètres d'entrée/sortie.
        """

        super().__init__(train) # Appel de l'initialisation de la classe parente
        self.calculer_parametres()

if __name__ == '__main__':
    print('hello')

    # Exemple d'utilisation
    listeTrain = [Train_simple(1), Train_simple(2)]
    for i in range(len(listeTrain)):
        listeTrain[i].description['global'].description['resistance_elastique'] = 340  # Exemple de puissance
        listeTrain[i].description['global'].description['entraxe'] = 100      # Exemple de couple de sortie
       
    listeTrain[0].description['global'].description['vitesse_entree'] = 340 
    listeTrain[0].description['global'].description['puissance_entree'] = 340 
    listeTrain[1].description['global'].description['couple_sortie'] = 340 
    print('hello')
    reducteur = Reducteur(listeTrain)
    print(listeTrain)
##