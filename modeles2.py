# Fichier: modeles.py
from Parametres_dyna import Calcule_train_simple, Calcule_train_epi
import math

# --- Définition des classes de données ---

class Global():
    def __init__(self) -> None:
        self.titre = 'parametre globale'
        self.description = {'vitesse_entree': 0, 'puissance_entree': 0, 'couple_sortie': 0}
        self.unitee = ['RPM','W','Nm']
        self.error = 0
            
class Engrenage(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'engrenage {num}'
        self.description = {'_diametre' : 0}
        self.unitee = ['mm']

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
            'rendement': 0.95 # NOUVEAU : Rendement par défaut (95%)
        }
        # Unités correspondantes (simplifiées pour l'affichage)
        self.unitee = ['RPM', 'W', 'Nm', 'Nm', 'mm', 'RPM', 'N', ' ', 'mm', '°', '°', 'MPa', '%']

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

class Train_epi(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'train_epi_{num}'
        self.description =  {
            '_mode_blocage':'couronne', 
            'global': Train_global(),
            'pignon': Engrenage(0), # Solaire = planétaire
            'satelite': Engrenage(1),
            'couronne': Engrenage(2)
        }
        # change les titres des sous-objets
        self.description['pignon'].titre = 'solaire'
        self.description['satelite'].titre = 'satellite'
        self.description['couronne'].titre = 'couronne'
        # ajoute le nombre de satellite par defaut a la description global
        self.description['global'].description = {**{'nb_satelite':3}, **self.description['global'].description}
        self.description['global'].unitee.insert(0, ' ') # ajoute l'unitee pour le nombre de satellite
        self.unitee = None

# --- Classe Principale Réducteur ---

class Reducteur():
    def __init__(self, listeTrain: list) -> None:
        self.titre = 'reducteur'
        self.listeTrain = listeTrain
        self.calc_objects = [] # Stocke les objets calculateurs
        
        # Initialisation du premier calcul
        if len(self.listeTrain) > 0:
            self.calculer_systeme_complet()

    def calculer_RR_global_vise(self):
        """Calcule le rapport total visé basé sur les entrées/sorties du système."""
        if not self.listeTrain: return 1
        
        P_in = self.listeTrain[0].description['global'].description['puissance_entree']
        V_in = self.listeTrain[0].description['global'].description['vitesse_entree']
        C_out_desire = self.listeTrain[-1].description['global'].description['couple_sortie']
        
        if C_out_desire == 0: return 1 # On return 1 mais on peut return ce qu'on veut ici
        
        omega_in = V_in * 2 * math.pi / 60
        # Estimation grossière du omega_out idéal (sans rendement global pour le ciblage géométrique)
        omega_out = P_in / C_out_desire 
        
        if omega_out == 0: return 0 ###
        return omega_in / omega_out

    def calculer_systeme_complet(self):
        """Méthode principale qui met à jour toute la chaîne."""
        n = len(self.listeTrain)
        if n == 0: return

        #  Récupération des conditions initiales du premier étage
        P_actuelle = self.listeTrain[0].description['global'].description['puissance_entree']
        V_actuelle = self.listeTrain[0].description['global'].description['vitesse_entree']
        
        #  Calcul du ratio équilibré par étage ( tous les étages ont le même ratio, me dire si tu veux u truc plus optimisé)
        rr_total = self.calculer_RR_global_vise()
        if rr_total > 0:
            r_etage_target = rr_total ** (1/n)
        else:
            r_etage_target = 1

        self.calc_objects = [] # Reset des calculateurs

        #  Boucle 
        for i, train in enumerate(self.listeTrain):
            
            # Mise à jour des entrées de l'étage i
            train.description['global'].description['puissance_entree'] = P_actuelle
            train.description['global'].description['vitesse_entree'] = V_actuelle
            
            # Injection du ratio cible (Sera recalibré par la physique ensuite si besoin)
            # Pour un dimensionnement, on fixe la sortie désirée virtuelle pour calculer la géométrie
            C_out_local_estime = (P_actuelle / (V_actuelle/r_etage_target)) / (2*math.pi/60)
            
            # Si c'est le dernier étage, on respecte impérativement le couple de sortie demandé par l'utilisateur
            # (Ca forcera le ratio de ce dernier étage à s'adapter)
            if i == n - 1:
                # On garde le couple_sortie défini manuellement par l'utilisateur pour le dernier étage
                pass 
            else:
                train.description['global'].description['couple_sortie'] = C_out_local_estime

            # Création du calculateur approprié
            if isinstance(train, Train_simple):
                calc = Calcule_train_simple(train)
            elif isinstance(train, Train_epi):
                calc = Calcule_train_epi(train)
            else:
                continue
            
            self.calc_objects.append(calc)
            
            # Lancement du calcul physique de l'étage
            calc.calculer_mise_a_jour_complete()
            
            # Préparation pour l'étage suivant
            V_actuelle = train.description['global'].description['_vitesse_sortie']
            # La puissance diminue à cause du rendement !
            P_actuelle = calc.get_puissance_sortie_reelle()


    # --- Méthodes de Modification Dynamique ---

    def modifier_parametre(self, index_train, sous_objet, cle, valeur):
        """
        Modifie un paramètr spécifique et relance le calcul.
        Ex: modifier_parametre(0, 'global', 'vitesse_entree', 2000)
        """
        if 0 <= index_train < len(self.listeTrain):
            train = self.listeTrain[index_train]
            if sous_objet in train.description:
                if cle in train.description[sous_objet].description:
                    print(f">> Modification Train {index_train+1} [{sous_objet}][{cle}] = {valeur}")
                    train.description[sous_objet].description[cle] = valeur
                    self.calculer_systeme_complet()
                else:
                    print(f"Erreur: Clé {cle} introuvable.")
            else:
                print(f"Erreur: Sous-objet {sous_objet} introuvable.")

    def ajouter_train(self, type_train='simple'):
        num = len(self.listeTrain) + 1
        if type_train == 'epi':
            new_train = Train_epi(num)
        else:
            new_train = Train_simple(num)
        
        # Initialisation avec des valeurs par défaut cohérentes avec le précédent
        new_train.description['global'].description['entraxe'] = 100
        new_train.description['global'].description['resistance_elastique'] = 340
        new_train.description['global'].description['rendement'] = 0.95
        
        self.listeTrain.append(new_train)
        print(f">> Train {type_train} ajouté.")
        self.calculer_systeme_complet()

    def supprimer_dernier_train(self):
        if len(self.listeTrain) > 0:
            self.listeTrain.pop()
            print(">> Dernier train supprimé.")
            self.calculer_systeme_complet()

    def changer_type_train(self, index, nouveau_type):
        if 0 <= index < len(self.listeTrain):
            old_train = self.listeTrain[index]
            
            # Création du nouveau train
            if nouveau_type == 'epi':
                new_train = Train_epi(index+1)
            else:
                new_train = Train_simple(index+1)
            
            # On essaie de conserver les paramètres globaux communs (Entraxe, Résistance, Rendement)
            for key in ['entraxe', 'resistance_elastique', 'rendement', 'couple_sortie']:
                val = old_train.description['global'].description.get(key)
                new_train.description['global'].description[key] = val
            
            # Si c'est le train 0, on garde les inputs
            if index == 0:
                new_train.description['global'].description['vitesse_entree'] = old_train.description['global'].description['vitesse_entree']
                new_train.description['global'].description['puissance_entree'] = old_train.description['global'].description['puissance_entree']

            self.listeTrain[index] = new_train
            print(f">> Train {index+1} changé en type {nouveau_type}.")
            self.calculer_systeme_complet()

# --- Zone de Test ---

if __name__ == '__main__':
    # Initialisation
    t1 = Train_simple(1)
    t1.description['global'].description.update({'entraxe': 80, 'resistance_elastique': 500, 'vitesse_entree': 1500, 'puissance_entree': 5000})
    
    t2 = Train_simple(2)
    t2.description['global'].description.update({'entraxe': 100, 'resistance_elastique': 500, 'couple_sortie': 200}) # Cible finale

    reducteur = Reducteur([t1, t2])

    def afficher_resultats(r):
        print("\n" + "-"*50)
        for i, train in enumerate(r.listeTrain):
            g = train.description['global'].description
            type_t = "EPI" if isinstance(train, Train_epi) else "SIMPLE"
            print(f"ETAGE {i+1} ({type_t}) | In: {g['vitesse_entree']:.0f}rpm | Out: {g['_vitesse_sortie']:.0f}rpm | Ratio: {g['_rapport_reduction']:.2f} | Couple In: {g['_couple_entree']:.1f}Nm")
            if type_t == "EPI":
                print(f"   >>> D_Solaire: {train.description['pignon'].description['_diametre']:.1f}mm | D_Couronne: {train.description['couronne'].description['_diametre']*1000:.1f}mm")
            else:
                print(f"   >>> D_Pignon: {train.description['pignon'].description['_diametre']:.1f}mm")
        print("-"*50)

    afficher_resultats(reducteur)

    # TEST 1 : Modification paramètre
    reducteur.modifier_parametre(0, 'global', 'vitesse_entree', 3000)
    afficher_resultats(reducteur)

    # TEST 2 : Changement de type (Passer l'étage 2 en Épicycloïdal)
    reducteur.changer_type_train(1, 'epi')
    # Pour un épi, il faut souvent un entraxe plus grand pour caser les satellites si le rapport est grand, ajustons-le
    reducteur.modifier_parametre(1, 'global', 'entraxe', 150) 
    afficher_resultats(reducteur)

    # TEST 3 : Ajout d'un train
    reducteur.ajouter_train('epi')
    # On définit le couple de sortie sur le nouveau dernier train
    reducteur.modifier_parametre(2, 'global', 'couple_sortie', 300) 
    afficher_resultats(reducteur)