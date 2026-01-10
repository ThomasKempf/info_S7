# Fichier: Parametres_dyna.py
import math 

class Calcule_train:
    """Classe de base pour les calculs physiques des trains d'engrenages."""
    
    def __init__(self, Train_1):
        self.train_1 = Train_1
        self._rapport_reduction: float = 0.0 
        self.error = 0

        self._param_global = self.train_1.description['global'].description
        
        # Gestion sécurisée des dictionnaires
        obj_pignon = self.train_1.description.get('pignon')
        self._param_pignon = obj_pignon.description if obj_pignon else {}

        obj_roue = self.train_1.description.get('roue')
        self._param_roue = obj_roue.description if obj_roue else {}

        obj_satelite = self.train_1.description.get('satelite')
        self._param_satelite = obj_satelite.description if obj_satelite else {}

        obj_couronne = self.train_1.description.get('couronne')
        self._param_couronne = obj_couronne.description if obj_couronne else {}

    def calculer_mise_a_jour_complete(self):
        """Met à jour tout le système."""
        self.calculer_vitesse_sortie()
        self.calculer_rapport_reduction()
        self.calculer_couple_entree()
        self.calculer_force_tangentielle()
        self.calculer_module()
        self.calculer_diametres_specifiques() # Calcule diamètres primitifs ET nombre de dents
        self.calculer_arbres() # NOUVEAU : Calcule les diamètres des arbres

    # --- Méthodes Physiques ---

    def calculer_vitesse_sortie(self, param=None):
        P_entree = self._param_global['puissance_entree']
        Couple_sortie = self._param_global['couple_sortie']
        if Couple_sortie <= 0:
            vitesse_sortie = 0.0
        else: 
            vitesse_sortie = (P_entree / Couple_sortie) * (60 / (2 * math.pi))
        self._param_global['_vitesse_sortie'] = vitesse_sortie

    def calculer_couple_entree(self, param=None):
        P_entree = self._param_global['puissance_entree']
        V_entree = self._param_global['vitesse_entree']
        if V_entree > 0:
            self._param_global['_couple_entree'] = P_entree / (V_entree * (2 * math.pi / 60))
        else:
            self._param_global['_couple_entree'] = 0

    def calculer_rapport_reduction(self, param=None):
        v_out = self._param_global['_vitesse_sortie']
        v_in = self._param_global['vitesse_entree']
        if v_out > 0:
            self._param_global['_rapport_reduction'] = v_in / v_out
        else:
            self._param_global['_rapport_reduction'] = 0

    def calculer_force_tangentielle(self, param=None):
        Ce = self._param_global['_couple_entree']
        r = self._param_global['entraxe']/1000 
        alpha_deg = self._param_global.get('alpha', 20)
        a_rad = math.radians(alpha_deg) 
        if r > 0:
            self._param_global['_force_tangentielle'] = Ce / (r * math.cos(a_rad))
        else:
            self._param_global['_force_tangentielle'] = 0

    def calculer_module(self, param=None):
        FT = self._param_global['_force_tangentielle']
        RES = self._param_global['resistance_elastique']
        if RES > 0:
            self._param_global['_module'] = 2.34 * math.sqrt(FT / (RES * 10))
        else:
             self._param_global['_module'] = 0

    def calculer_arbres(self):
        """
        NOUVEAU : Calcule le diamètre minimal des arbres d'entrée et de sortie
        Basé sur la torsion : d = (16 * C / (pi * Rpg))^(1/3)
        Avec Rpg (Resistance glissement) approx Re / 2
        """
        Re = self._param_global.get('resistance_elastique', 0)
        if Re <= 0: 
            self._param_global['_diametre_arbre_entree'] = 0
            self._param_global['_diametre_arbre_sortie'] = 0
            return

        Rpg = Re * 0.5 # Approximation courante pour l'acier (cisaillement)
        
        # Couple en Nm, Re en MPa (N/mm²). 
        # Formule homogène en mm : d = (16 * C*1000 / (pi * Rpg))^(1/3)
        
        C_in = self._param_global.get('_couple_entree', 0)
        C_out = self._param_global.get('couple_sortie', 0)

        if C_in > 0:
            d_in = (16 * C_in * 1000 / (math.pi * Rpg))**(1/3)
            self._param_global['_diametre_arbre_entree'] = d_in
        
        if C_out > 0:
            d_out = (16 * C_out * 1000 / (math.pi * Rpg))**(1/3)
            self._param_global['_diametre_arbre_sortie'] = d_out

    def get_puissance_sortie_reelle(self):
        eta = self._param_global.get('rendement', 1.0) 
        return self._param_global['puissance_entree'] * eta

    def calculer_diametres_specifiques(self):
        raise NotImplementedError("Surchargé par les enfants")
    
    # Méthodes de compatibilité (param=None)
    def calculer_parametres(self, param=None): self.calculer_mise_a_jour_complete()
    def calculer_diametre(self, param=None): self.calculer_diametres_specifiques()


# --- Classes Spécifiques ---

class Calcule_train_simple(Calcule_train):
    
    def calculer_diametres_specifiques(self):
        e = self._param_global['entraxe']/1000 # Converti en m
        r = self._param_global['_rapport_reduction']
        m = self._param_global['_module']

        if r > 0 and e > 0:
            D1 = (2 * e) / (1 + r)
            D2 = r * D1         
            
            # Stockage Diamètres (en mm pour affichage standard dans l'objet engrenage)
            self._param_pignon['_diametre'] = D1 * 1000
            self._param_roue['_diametre'] = D2 * 1000

            # CALCUL NBR DENTS (NOUVEAU) : Z = D / m
            if m > 0:
                self._param_pignon['_nbr_dents'] = int(round((D1 * 1000) / m))
                self._param_roue['_nbr_dents'] = int(round((D2 * 1000) / m))
            else:
                self._param_pignon['_nbr_dents'] = 0
                self._param_roue['_nbr_dents'] = 0


class Calcule_train_epi(Calcule_train):
    
    def calculer_diametres_specifiques(self):
        r_red = self._param_global['_rapport_reduction']
        entraxe = self._param_global['entraxe']/1000
        m = self._param_global['_module']

        if r_red > 1 and entraxe > 0:
            k = r_red - 1 
            D_solaire = (4 * entraxe) / (k + 1)
            D_couronne = k * D_solaire
            D_satellite = (D_couronne - D_solaire) / 2
            
            # Stockage Diamètres (mm)
            if self._param_pignon: self._param_pignon['_diametre'] = D_solaire*1000
            if self._param_couronne: self._param_couronne['_diametre'] = D_couronne*1000
            if self._param_satelite: self._param_satelite['_diametre'] = D_satellite*1000

            # CALCUL NBR DENTS (NOUVEAU)
            if m > 0:
                if self._param_pignon: self._param_pignon['_nbr_dents'] = int(round((D_solaire*1000)/m))
                if self._param_couronne: self._param_couronne['_nbr_dents'] = int(round((D_couronne*1000)/m))
                if self._param_satelite: self._param_satelite['_nbr_dents'] = int(round((D_satellite*1000)/m))