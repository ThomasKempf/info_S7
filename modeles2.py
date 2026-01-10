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
        # AJOUT : _nbr_dents
        self.description = {'_diametre' : 0, '_nbr_dents': 0}
        self.unitee = ['mm', ' ']

class Train_global(Global):
    def __init__(self) -> None:
        super().__init__()
        self.titre = 'train global'
        self.description = {
            '_vitesse_entree': 0,
            '_puissance_entree': 0,
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
            'rendement': 0.95,
            # AJOUT : Diamètres des arbres (Entrée et Sortie du train)
            '_diametre_arbre_entree': 0,
            '_diametre_arbre_sortie': 0
        }
        self.unitee = ['RPM', 'W', 'Nm', 'Nm', 'mm', 'RPM', 'N', ' ', 'mm', '°', '°', 'MPa', '%', 'mm', 'mm']

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
        
        rr_total = self.calculer_RR_global_vise()
        if rr_total > 0:
            r_etage_target = rr_total ** (1/n)
        else:
            r_etage_target = 1
        
        self.calc_objects = [] 
        for i, train in enumerate(self.listeTrain):
            train.description['global'].description['_puissance_entree'] = P_actuelle
            train.description['global'].description['_vitesse_entree'] = V_actuelle
            
            C_out_local_estime = (P_actuelle / (V_actuelle/r_etage_target)) / (2*math.pi/60)
            if i == n - 1:
                pass 
            else:
                train.description['global'].description['couple_sortie'] = C_out_local_estime

            if isinstance(train, Train_simple):
                calc = Calcule_train_simple(train)
            elif isinstance(train, Train_epi):
                calc = Calcule_train_epi(train)
            else:
                continue
            
            self.calc_objects.append(calc)
            calc.calculer_mise_a_jour_complete()
            
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
        
        new_train.description['global'].description['entraxe'] = 100
        new_train.description['global'].description['resistance_elastique'] = 340
        new_train.description['global'].description['rendement'] = 0.95
        new_train.description['global'].description['couple_sortie'] = couple_cible # Transfert de la cible
        
        self.listeTrain.append(new_train)
        print(f">> Train {type_train} ajouté. Cible maintenue à {couple_cible} Nm")
        self.calculer_systeme_complet()

    def supprimer_dernier_train(self):
        if len(self.listeTrain) > 0:
            couple_cible = self.listeTrain[-1].description['global'].description['couple_sortie']
            self.listeTrain.pop()
            print(">> Dernier train supprimé.")
            if len(self.listeTrain) > 0:
                self.listeTrain[-1].description['global'].description['couple_sortie'] = couple_cible # Transfert de la cible
                print(f">> Cible de {couple_cible} Nm transférée au train précédent.")
            self.calculer_systeme_complet()

    def changer_type_train(self, index, nouveau_type):
        if 0 <= index < len(self.listeTrain):
            old_train = self.listeTrain[index]
            if nouveau_type == 'epi': new_train = Train_epi(index+1)
            else: new_train = Train_simple(index+1)
            for key in ['entraxe', 'resistance_elastique', 'rendement', 'couple_sortie']:
                val = old_train.description['global'].description.get(key)
                new_train.description['global'].description[key] = val
            if index == 0:
                new_train.description['global'].description['_vitesse_entree'] = old_train.description['global'].description['_vitesse_entree']
                new_train.description['global'].description['_puissance_entree'] = old_train.description['global'].description['_puissance_entree']
            self.listeTrain[index] = new_train
            print(f">> Train {index+1} changé en type {nouveau_type}.")
            self.calculer_systeme_complet()


# --- Zone de Test Complète ---

if __name__ == '__main__':
    print("=== INITIALISATION DU TEST COMPLET ===")
    t1 = Train_simple(1)
    t1.description['global'].description.update({'entraxe': 80, 'resistance_elastique': 500, '_vitesse_entree': 1500, '_puissance_entree': 5000})
    
    t2 = Train_simple(2)
    # CIBLE INITIALE : 250 Nm
    t2.description['global'].description.update({'entraxe': 100, 'resistance_elastique': 500, 'couple_sortie': 250}) 

    reducteur = Reducteur([t1, t2])

    def afficher_resultats(r, titre=""):
        print(f"\n--- {titre} ---")
        for i, train in enumerate(r.listeTrain):
            g = train.description['global'].description
            type_t = "EPI   " if isinstance(train, Train_epi) else "SIMPLE"
            
            # Données Clés
            c_out = g.get('couple_sortie', 0)
            ratio = g.get('_rapport_reduction', 0)
            d_arb_in = g.get('_diametre_arbre_entree', 0)
            
            # 1. On affiche le Couple Cible (Test de robustesse)
            print(f"ETAGE {i+1} ({type_t}) | Ratio: {ratio:.2f} | CIBLE: {c_out:.1f} Nm")
            
            # 2. On affiche les nouvelles données (Arbre & Dents)
            print(f"    > Arbre Entrée min: {d_arb_in:.1f} mm")
            
            if type_t == "EPI   ":
                d_s = train.description['pignon'].description['_diametre']
                z_s = train.description['pignon'].description['_nbr_dents']
                d_c = train.description['couronne'].description['_diametre']
                z_c = train.description['couronne'].description['_nbr_dents']
                print(f"    > Solaire : {d_s:.1f}mm ({z_s} dents) | Couronne : {d_c:.1f}mm ({z_c} dents)")
            else:
                d_p = train.description['pignon'].description['_diametre']
                z_p = train.description['pignon'].description['_nbr_dents']
                d_r = train.description['roue'].description['_diametre']
                z_r = train.description['roue'].description['_nbr_dents']
                print(f"    > Pignon : {d_p:.1f}mm ({z_p} dents) | Roue : {d_r:.1f}mm ({z_r} dents)")
        print("-" * 40)

    afficher_resultats(reducteur, "1. État Initial")

    # TEST CRITIQUE 1 : AJOUT (Doit garder 250 Nm)
    reducteur.ajouter_train('epi') 
    afficher_resultats(reducteur, "2. APRÈS AJOUT (Cible 250 Nm sur Etage 3 ?)")

    # TEST CRITIQUE 2 : SUPPRESSION (Doit garder 250 Nm)
    reducteur.supprimer_dernier_train()
    afficher_resultats(reducteur, "3. APRÈS SUPPRESSION (Cible 250 Nm sur Etage 2 ?)")

    # TEST 3 : MODIFICATION
    reducteur.modifier_parametre(0, 'global', '_vitesse_entree', 3000)
    afficher_resultats(reducteur, "4. APRÈS CHANGEMENT VITESSE (Recalcul complet)")