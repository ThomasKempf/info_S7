# Fichier : tests.py

# --- Importation des Classes depuis le module 'modeles' ---
from modeles import Engrenage, Train, TrainSimple

# --- Fonction de Test ---

def run_tests():
    print("--- Demarrage des tests du modele Train via Importation ---")

    # 1. Test du Train Simple (Réduction)
    print("\n[1] Test du Train Simple (Reduction)")
    e_petit = Engrenage(nbr_dents=20)
    e_grand = Engrenage(nbr_dents=50)
    train_1 = TrainSimple(e_petit, e_grand)
    
    expected_rapport = 20 / 50
    
    print(f"  Entree: {e_petit.nbr_dents} | Sortie: {e_grand.nbr_dents}")
    print(f"  Rapport Calcule: {train_1.rapport_reduction:.2f}")
    
    if train_1.rapport_reduction == expected_rapport:
        print("  RESULTAT: Succes. Le rapport est correct (0.25).")
    else:
        print(f"  REULTAT: Echec. Le rapport ne correspond pas ({train_1.rapport_reduction} != {expected_rapport}).")

    # 2. Test du Train Simple 
    print("\n[2] Test du Train Simple ")
    e_entree_rapide = Engrenage(nbr_dents=60)
    e_sortie_lente = Engrenage(nbr_dents=20)
    train_2 = TrainSimple(e_entree_rapide, e_sortie_lente)
    
    expected_rapport_2 = 60 / 20
    
    print(f"  Entree: {e_entree_rapide.nbr_dents} | Sortie: {e_sortie_lente.nbr_dents}")
    print(f"  Rapport Calcule: {train_2.rapport_reduction:.2f}")
    
    if train_2.rapport_reduction == expected_rapport_2:
        print("  RESULTAT: Succes. Le rapport est correct (2.00).")
    else:
        print(f"  RESULTAT: Echec. Le rapport ne correspond pas ({train_2.rapport_reduction} != {expected_rapport_2}).")

    # 3. Test de l'obligation d'implémentation (Méthode de la classe mère Train)
    print("\n[3] Test de l'heritage (Tentative d'utilisation directe)")
    try:
        train_mere = Train()
        train_mere.calculer_rapport()
    except NotImplementedError as e:
        print(f"  RESULTAT: Succes. Erreur levee : '{e}'")
    except Exception as e:
        print(f"  RESULTAT: Echec. Une autre erreur s'est produite : {e}")

        

# --- Exécution du script de test ---
if __name__ == "__main__":
    run_tests()