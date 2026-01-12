from Parametres_dyna import Calcule_train_simple, Calcule_train_epi
import math

# --- Définition des classes de données ---

class Global():
    def __init__(self) -> None:
        self.titre = 'parametre globale'
        self.description = {'_vitesse_entree': 0, '_puissance_entree': 0, 'couple_sortie': 0}
        self.unitee = ['RPM','W','Nm']
        self.error = 0
            
class Engrenage(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'engrenage {num}'
        # Données : Diamètre primitif + Nombre de dents calculé
        self.description = {'_diametre' : 0, '_nbr_dents': 0}
        self.unitee = ['mm', ' ']

class Train_global(Global):
    def __init__(self) -> None:
        super().__init__()
        self.titre = 'train global'
        
        # 16 PARAMÈTRES
        self.description = {
            '_vitesse_entree': 0,
            '_puissance_entree': 0,
            'couple_sortie': 100,
            '_couple_entree': 0,
            
            'entraxe': 100,
            'resistance_elastique': 500,
            
            '_vitesse_sortie': 0,
            '_force_tangentielle': 0,
            '_rapport_reduction':0,
            
            'ratio_fixe': 0,             # <--- Paramètre 10
            
            '_module': 0,
            'alpha': 20,
            'beta':0,
            'rendement': 0.95,
            
            '_diametre_arbre_entree': 0,
            '_diametre_arbre_sortie': 0
        }
        
        # (L'ordre doit être STRICTEMENT identique aux clés ci-dessus)
        self.unitee = [
            'RPM',  # vitesse_entree
            'W',    # puissance_entree
            'Nm',   # couple_sortie
            'Nm',   # _couple_entree
            'mm',   # entraxe
            'MPa',  # resistance_elastique
            'RPM',  # _vitesse_sortie
            'N',    # _force_tangentielle
            ' ',    # _rapport_reduction
            ' ',    # ratio_fixe (C'est celle-ci qui manquait probablement !)
            'mm',   # _module
            '°',    # alpha
            '°',    # beta
            '%',    # rendement
            'mm',   # _diametre_arbre_entree
            'mm'    # _diametre_arbre_sortie
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

class Train_epi(Global):
    def __init__(self,num:int) -> None:
        super().__init__()
        self.titre = f'train_epi_{num}'
        self.description =  {
            '_mode_blocage':'couronne', 
            'global': Train_global(),
            'pignon': Engrenage(0),
            'satelite': Engrenage(1),
            'couronne': Engrenage(2)
        }
        self.description['pignon'].titre = 'solaire'
        self.description['satelite'].titre = 'satellite'
        self.description['couronne'].titre = 'couronne'
        self.description['global'].description = {**{'nb_satelite':3}, **self.description['global'].description}
        self.description['global'].unitee.insert(0, ' ') 
        self.unitee = None

# --- Classe Principale Réducteur ---

class Reducteur():
    def __init__(self, listeTrain: list) -> None:
        self.titre = 'reducteur'
        self.listeTrain = listeTrain
        self.calc_objects = [] 
        if len(self.listeTrain) > 0:
            self.calculer_systeme_complet()

    def calculer_RR_global_vise(self):
        if not self.listeTrain: return 1
        P_in = self.listeTrain[0].description['global'].description['_puissance_entree']
        V_in = self.listeTrain[0].description['global'].description['_vitesse_entree']
        C_out_desire = self.listeTrain[-1].description['global'].description['couple_sortie']
        if C_out_desire == 0: return 1 
        omega_in = V_in * 2 * math.pi / 60
        omega_out = P_in / C_out_desire 
        if omega_out == 0: return 0 
        return omega_in / omega_out

    def calculer_systeme_complet(self):
        n = len(self.listeTrain)
        if n == 0: return
        
        P_actuelle = self.listeTrain[0].description['global'].description['_puissance_entree']
        V_actuelle = self.listeTrain[0].description['global'].description['_vitesse_entree']
        
        # 1. Calcul du besoin global théorique
        rr_global_vise = self.calculer_RR_global_vise()
        if rr_global_vise <= 0: rr_global_vise = 1

        # 2. Séparation : Qui est fixe ? Qui est auto ?
        produit_fixes = 1.0
        nb_auto = 0
        
        for train in self.listeTrain:
            rf = train.description['global'].description.get('ratio_fixe', 0)
            if rf > 0:
                produit_fixes *= rf
            else:
                nb_auto += 1
        
        # 3. Calcul du ratio restant pour les étages automatiques
        if produit_fixes == 0: produit_fixes = 1
        rr_restant = rr_global_vise / produit_fixes
        
        r_auto_target = 1
        if nb_auto > 0:
            if rr_restant > 0:
                r_auto_target = rr_restant ** (1 / nb_auto)
            else:
                r_auto_target = 1

        self.calc_objects = [] 

        for i, train in enumerate(self.listeTrain):
            train.description['global'].description['_puissance_entree'] = P_actuelle
            train.description['global'].description['_puissance_entree'] = V_actuelle
            
            # --- CHOIX DU RATIO LOCAL ---
            r_fixe = train.description['global'].description.get('ratio_fixe', 0)
            if r_fixe > 0:
                ratio_a_appliquer = r_fixe
            else:
                ratio_a_appliquer = r_auto_target
            
            # Calcul du couple cible intermédiaire théorique
            if ratio_a_appliquer > 0 and V_actuelle > 0:
                V_out_prevue = V_actuelle / ratio_a_appliquer
                C_out_local_estime = P_actuelle / (V_out_prevue * (2*math.pi/60))
            else:
                C_out_local_estime = 0

            # --- APPLICATION DU COUPLE ---
            # Si c'est le dernier étage ET qu'il est en mode AUTO :
            # On respecte impérativement la demande utilisateur (couple_sortie).
            # Sinon (étage intermédiaire OU ratio fixé), on impose le couple calculé par la géométrie.
            if i == n - 1 and r_fixe == 0:
                pass 
            else:
                train.description['global'].description['couple_sortie'] = C_out_local_estime

            # Lancement calcul physique
            if isinstance(train, Train_simple):
                calc = Calcule_train_simple(train)
            elif isinstance(train, Train_epi):
                calc = Calcule_train_epi(train)
            else:
                continue
            
            self.calc_objects.append(calc)
            calc.calculer_mise_a_jour_complete()
            
            # Préparation étage suivant
            V_actuelle = train.description['global'].description['_vitesse_sortie']
            P_actuelle = calc.get_puissance_sortie_reelle()

    def modifier_parametre(self, index_train, sous_objet, cle, valeur):
        if index_train < 0: index_train = len(self.listeTrain) + index_train
        if 0 <= index_train < len(self.listeTrain):
            train = self.listeTrain[index_train]
            if sous_objet in train.description:
                if cle in train.description[sous_objet].description:
                    print(f">> Modification Train {index_train+1} [{sous_objet}][{cle}] = {valeur}")
                    train.description[sous_objet].description[cle] = valeur
                    self.calculer_systeme_complet()
                else: print(f"Erreur: Clé {cle} introuvable.")
            else: print(f"Erreur: Sous-objet {sous_objet} introuvable.")

    def ajouter_train(self, type_train='simple'):
        couple_cible = 100 
        if len(self.listeTrain) > 0:
            couple_cible = self.listeTrain[-1].description['global'].description['couple_sortie']
        
        num = len(self.listeTrain) + 1
        if type_train == 'epi': new_train = Train_epi(num)
        else: new_train = Train_simple(num)
        
        # Initialisation avec valeurs par défaut "Standard"
        new_train.description['global'].description['entraxe'] = 100
        new_train.description['global'].description['resistance_elastique'] = 500
        new_train.description['global'].description['rendement'] = 0.95
        new_train.description['global'].description['couple_sortie'] = couple_cible
        
        self.listeTrain.append(new_train)
        print(f">> Train {type_train} ajouté. Cible maintenue à {couple_cible} Nm")
        self.calculer_systeme_complet()

    def supprimer_dernier_train(self):
        if len(self.listeTrain) > 0:
            couple_cible = self.listeTrain[-1].description['global'].description['couple_sortie']
            self.listeTrain.pop()
            print(">> Dernier train supprimé.")
            if len(self.listeTrain) > 0:
                self.listeTrain[-1].description['global'].description['couple_sortie'] = couple_cible
                print(f">> Cible de {couple_cible} Nm transférée au train précédent.")
            self.calculer_systeme_complet()

    def changer_type_train(self, index, nouveau_type):
        if 0 <= index < len(self.listeTrain):
            old_train = self.listeTrain[index]
            if nouveau_type == 'epi': new_train = Train_epi(index+1)
            else: new_train = Train_simple(index+1)
            
            # On conserve les paramètres importants
            for key in ['entraxe', 'resistance_elastique', 'rendement', 'couple_sortie', 'ratio_fixe']:
                if key in old_train.description['global'].description:
                    val = old_train.description['global'].description.get(key)
                    new_train.description['global'].description[key] = val
            
            if index == 0:
                new_train.description['global'].description['_puissance_entree'] = old_train.description['global'].description['_puissance_entree']
                new_train.description['global'].description['_puissance_entree'] = old_train.description['global'].description['_puissance_entree']
            self.listeTrain[index] = new_train
            print(f">> Train {index+1} changé en type {nouveau_type}.")
            self.calculer_systeme_complet()


# --- Zone de Test de Validation (Scenario Mixte) ---

if __name__ == '__main__':
    print("=== TEST : SCÉNARIO MIXTE (Fixe + Auto + Fixe) ===")
    
    # Objectif : Ratio Total ~20
    # T1 Fixé à 2.0
    # T3 Fixé à 2.5
    # T2 (Auto) doit trouver 4.0 tout seul (car 2 * 4 * 2.5 = 20)
    
    t1 = Train_simple(1)
    t1.description['global'].description.update({
        '_puissance_entree': 2000, 
        '_puissance_entree': 5000,
        'ratio_fixe': 2.0   # <--- FIXÉ
    })
    
    t2 = Train_simple(2)
    # T2 est en AUTO (ratio_fixe = 0 par défaut)
    
    t3 = Train_simple(3)
    t3.description['global'].description.update({
        'ratio_fixe': 2.5,  # <--- FIXÉ
        'couple_sortie': 477 # Cible pour obtenir ~100 rpm (Ratio total ~20)
    })

    reducteur = Reducteur([t1, t2, t3])

    print("-" * 60)
    for i, train in enumerate(reducteur.listeTrain):
        g = train.description['global'].description
        
        # Détection du mode pour l'affichage
        is_fixe = g.get('ratio_fixe', 0) > 0
        mode_str = "[FIXÉ]" if is_fixe else "[AUTO]"
        
        ratio = g['_rapport_reduction']
        
        print(f"ETAGE {i+1} {mode_str} : Ratio = {ratio:.2f}")

    print("-" * 60)
    
    # Vérification automatique
    r2 = reducteur.listeTrain[1].description['global'].description['_rapport_reduction']
    if 3.9 < r2 < 4.1:
        print("L'étage 2 (Auto) a bien comblé le trou en se mettant à 4")
    else:
        print(f"L'étage 2 a calculé {r2:.2f} au lieu de 4")