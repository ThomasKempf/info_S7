# test_vitesse_sortie.py

from modeles2 import Calcule_train_simple

# 🔹 Création d'un train d'engrenages avec des valeurs simples
train = Calcule_train_simple(
    vitesse_entree=1500,      # tr/min
    puissance_entree=4000,    # W
    couple_sortie=380,        # Nm
    entraxe=0.02,             # mm
    res_elastique=150         # sans unité
)

print("=== TEST DU CALCUL DE LA VITESSE DE SORTIE ===")

# 🔹 Appel de la méthode de calcul 
vitesse_sortie = train.calculer_vitesse_sortie()
couple_entree = train.calculer_couple_entree()
force_tangentielle = train.calculer_force_tangentielle()
module = train.calculer_module()

# 🔹 Affichage clair
print(f"Puissance d'entrée     : {train.puissance_entree} W")
print(f"Couple de sortie       : {train.couple_sortie} Nm")
print(f"Vitesse de sortie calc : {vitesse_sortie:.2f} tr/min")

# 🔹 Vérification du rapport de réduction correspondant
rapport = train.calculer_rapport_reduction()
print(f"Rapport de réduction   : {rapport:.4f}")

# 🔹 Affichage du dictionnaire complet (optionnel)
train.afficher_description()
