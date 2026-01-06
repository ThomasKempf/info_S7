import math 

class Calcule_train:
    """Classe de base pour les calculs physiques des trains d'engrenages."""
    
    def __init__(self, Train_1):
        self.train_1 = Train_1
        self._rapport_reduction: float = 0.0 
        self.error = 0

        self._param_global = self.train_1.description['global'].description
        
        # Gestion  des dictionnaires (pour éviter le crash si pas de satellite)
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
        self.calculer_diametres_specifiques()

    # --- Méthodes Physiques (Avec param=None pour compatibilité) ---

    def calculer_parametres(self, param=None):
        """
        Ancienne méthode principale. 
        On ignore 'param', mais on garde l'argument pour ne pas casser l'appli externe.
        """
        self.calculer_mise_a_jour_complete()

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
        r = self._param_global['entraxe'] 
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

    def calculer_diametre(self, param=None):
        # Redirection vers la nouvelle méthode spécifique
        self.calculer_diametres_specifiques()

    def get_puissance_sortie_reelle(self):
        eta = self._param_global.get('rendement', 1.0) 
        return self._param_global['puissance_entree'] * eta

    def calculer_diametres_specifiques(self):
        raise NotImplementedError("Surchargé par les enfants")


# --- Classes Spécifiques ---

class Calcule_train_simple(Calcule_train):
    
    def calculer_diametres_specifiques(self):
        e = self._param_global['entraxe']
        r = self._param_global['_rapport_reduction']
        
        if r > 0 and e > 0:
            D1 = (2 * e) / (1 + r)
            D2 = r * D1         
            self._param_pignon['_diametre'] = D1
            self._param_roue['_diametre'] = D2


class Calcule_train_epi(Calcule_train):
    
    def calculer_diametres_specifiques(self):
        r_red = self._param_global['_rapport_reduction']
        entraxe = self._param_global['entraxe']
        
        if r_red > 1 and entraxe > 0:
            k = r_red - 1 
            D_solaire = (4 * entraxe) / (k + 1)
            D_couronne = k * D_solaire
            D_satellite = (D_couronne - D_solaire) / 2
            
            if self._param_pignon: self._param_pignon['_diametre'] = D_solaire
            if self._param_couronne: self._param_couronne['_diametre'] = D_couronne
            if self._param_satelite: self._param_satelite['_diametre'] = D_satellite