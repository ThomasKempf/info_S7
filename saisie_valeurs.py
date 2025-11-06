# --- Saisie simple des variables Puissance, B et C ---
import math

Puissance = int(input("Veuillez entrer une valeur de Puissance : "))
Cs = int(input("Veuillez entrer une valeur pour le couple de sortie  : "))
Omega_E = int(input("Veuillez entrer une valeur pour la vitesse d'entrée : "))

# Afficher les valeurs enregistrées pour confirmation
print("\n Valeurs assignées :")
print(f"Puissance : {Puissance}")
print(f"Couple de sortie : {Cs}")
print(f"Vitesse d'entrée : {Omega_E}")

Omega_S = (Puissance/Cs)*(60/(2*math.pi)) # le math.pi m'aura fait chier mdr
print(f"La vitesse de sortie Omega_S est de : {Omega_S} tr/min")

Omega_E_rad_s = Omega_E * (2 * math.pi / 60)

Ce =  Puissance / Omega_E_rad_s
print(f"Le couple d'entree est de : {Ce} N.m")

Rapport_reduc = Omega_E/Omega_S
print(f"Le rapport de reduction est de : {Rapport_reduc}")

nb_etages = int(input("Veuillez entrer le nombre d'étages de réduction entre 1 et 3: "))

if nb_etages == 1:
    i1 = Rapport_reduc
    print(f"Le rapport de réduction pour l'étage 1 est de : {i1:.2f}")

elif nb_etages == 2:
    print("\n--- Définition des rapports pour 2 étages ---")
    
    # L'utilisateur choisit i1
    while True:
        try:
            i1_input = float(input(f"Entrez le rapport i1 pour l'étage 1 : "))
            if i1_input == 0:
                print(" Le rapport de réduction ne peut pas être zéro.")
                continue
            break
        except ValueError:
            print(" Erreur : Veuillez entrer un nombre valide.")

    i1 = i1_input
    
    # Calcul automatique de i2 pour garantir que i1 * i2 = Rapport_reduc
    i2 = Rapport_reduc / i1
    
    print(f"\nLe rapport i1 (choisi) est de : {i1:.2f}")
    print(f"Le rapport i2 (calculé) est de : {i2:.2f}")
    print(f"Vérification : i1 * i2 = {i1 * i2:.2f} (Doit être {Rapport_reduc:.2f})")

elif nb_etages == 3:
    print("\n--- Définition des rapports pour 3 étages ---")
    
    # 1. Saisie de i1u
    while True:
        try:
            i1 = float(input(f"Entrez le rapport i1 pour l'étage 1 : "))
            if i1 == 0:
                print(" Le rapport de réduction ne peut pas être zéro.")
                continue
            break
        except ValueError:
            print(" Erreur : Veuillez entrer un nombre valide.")
            
    # 2. Saisie de i2
    while True:
        try:
            i2 = float(input(f"Entrez le rapport i2 pour l'étage 2 : "))
            if i2 == 0:
                print(" Le rapport de réduction ne peut pas être zéro.")
                continue
            break
        except ValueError:
            print(" Erreur : Veuillez entrer un nombre valide.")

    # Calcul automatique de i3 pour garantir que i1 * i2 * i3 = Rapport_reduc
    if i1 * i2 != 0:
        i3 = Rapport_reduc / (i1 * i2)
    else:
        i3 = 0.0 # Évite la division par zéro

    print(f"\nLe rapport i1 (choisi) est de : {i1:.2f}")
    print(f"Le rapport i2 (choisi) est de : {i2:.2f}")
    print(f"Le rapport i3 (calculé) est de : {i3:.2f}")
    print(f"Vérification : i1 * i2 * i3 = {i1 * i2 * i3:.2f} (Doit être {Rapport_reduc:.2f})")
    
else:
    print("Erreur : Nombre d'étages invalide. Veuillez entrer une valeur entre 1 et 3.") 



