# Dimensionnement Reducteur Projet Info S7

## Description
Cette application permet de dimensionner un réducteur à plusieurs étages.
Elle permet de choisir le nombre de trains, le type de train, ainsi que de modifier chaque paramètre de manière individuelle.

## Authors

Thomas KEMPF  
Lucas STEINER

## Installation

````
pip install -r requirements.txt
````


## How to use
Exécuter le fichier .exe ou python gui.py.
Une première fenêtre s’ouvre et vous permet de choisir entre créer un nouveau projet ou en ouvrir un existant.
En cliquant sur Créer un nouveau projet, une fenêtre de dimensionnement s’ouvre.
La première page permet de sélectionner les paramètres globaux.
La seconde page permet de définir le nombre de trains, le type de train, le type d’engrenage, ainsi que la résistance élastique et l’entraxe — soit entre les deux engrenages, soit entre la couronne et le planétaire.
Ensuite, la fenêtre Projet s’ouvre et affiche les différents trains. Pour chaque train, on peut d’abord changer le type de train, puis modifier ses paramètres.
Pour chaque paramètre, on retrouve son nom, sa valeur et son unité.
Les paramètres en gras sont modifiables, les autres ne le sont pas.
En appuyant sur Entrée, les nouveaux paramètres sont mis à jour.
Il est également possible de supprimer ou d’ajouter des trains :
– pour supprimer, cliquer sur le signe « – » en haut du dernier train ;
– pour ajouter, cliquer sur le signe « + » à droite de celui-ci.  

Dans la barre supérieure, on trouve deux boutons :
Celui de droite permet d’enregistrer le projet dans un fichier .xlsx.
Le second ouvre un menu proposant plusieurs options : créer un nouveau projet (qui ouvre une nouvelle fenêtre de dimensionnement), ouvrir un projet existant, enregistrer ou enregistrer sous.  

Une fois le projet enregistré, on peut l’ouvrir soit via le bouton Ouvrir, soit au lancement du programme en sélectionnant Ouvrir un projet au lieu de Créer.


## Project architecture

### gui.py
    contient les classes permettant de générer un projet ainsi que la fenêtre du menu de départ.
### fenetres_creation.py
    contient les classes permettant de générer la fenêtre de création, ainsi que les éléments associés.
### fenetres_projet.py
    contient les classes permettant de générer la fenêtre du projet.
### outil_gui.py
    contient la super classe des fenêtres, ainsi que d'autres classes utiles de manière générale lors de la programmation d'une fenêtre avec PySide6.
### gestion_reducteur.py
    contient les classes descriptives des différents composants d'un réducteur, faisant le lien entre la GUI et les classes de calcul.
### gestion_calcule_train.py
    contient la classe permettant de calculer les différents paramètres d'un train.
### xlsx_reducteur.py
    contient les classes permettant de gérer l'enregistrement d'un projet dans un fichier .xlsx.
### error_description.py
    contient la description des erreurs associées à un code d'erreur. Module non finalisé et non encore totalement intégré.
### .PNG
    contient les fichiers .png utilisés dans la GUI, ne pas les supprimer.
