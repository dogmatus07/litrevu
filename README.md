
# LitReview

## Description

LitReview est une application qui permet de: 

- Créer des demandes de critiques sur des oeuvres littéraires  
ou des articles
- Créer des critiques en répondant à ces articles
- Créer un billet et une critique en une fois
- Suivre un utilisateur spécifique
- Ne plus suivre un utilisateur
- Avoir un aperçu des abonnements : utilisateurs suivis, abonnés
- Avoir un espace pour voir les activités de l'utilisateur  
et des membres qu'il suit

## Terminologie

- Billets : Demande de critiques sur des articles  
ou oeuvres littéraires
- Critiques : avis sur un billet
- User : utilisateur
- Flux : Feed d'activités

## Prérequis

Les dépendances requises pour installer et configurer cette application sont dans le fichier requirements.txt.  
Cette application nécessite Python 3.8 ou version ultérieure.  
Vous pouvez télécharger Python depuis le site officiel.

### Dépendances

- Django==5.0.6 : framework requis pour construire l'application
- Pillow==10.3.0 : bibliothèque pour gérer les téléchargements d'images
- sqlparse==0.5.0 : analyseur SQL pour Python
- tzdata==2024.1 : Base de données de fuseaux horaires pour Python
- asgiref==3.8.1 : utilie pour la fonction asynchrone de Django

## Configuration initiale

### Cloner le dépôt Git
Vous devez cloner le dépôt Git avec la commande suivante :

git clone https://github.com/dogmatus07/litrevu.git

### Installation des dépendances

Afin d'installer les dépendances, vous devez d'abord activer votre environnement virtuel.

#### Windows

python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt

#### Mac & Linux

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Lancement de l'application

Pour lancer l'application, accédez au dossier du projet où il y a le fichier manage.py : 

cd litrevu

### Configuration de la base de données

Un fichier db.sqlite3 est déjà inclus dans le projet et contient déjà toutes les tables  
et les données nécessaires pour un démarrage rapide.

### Informations de connexion

Une fois le serveur lancé, vous pouvez utiliser ces identifiants pour tester l'application.

<table>
    <thead>
        <th scope="col">Nom d'utilisateur</th>
        <th scope="col">Mot de passe</th>
        <th scope="col">Type de compte</th>
    </thead>
    <tbody>
        <tr scope="row">
            <td>admin@litreview.com</td>
            <td>p9OpenC]24)</td>
            <td>Super Utilisateur</td>
        </tr>
        <tr scope="row">
            <td>cecile@lynkevo.com</td>
            <td>p9OpenC]24)</td>
            <td>Utilisateur</td>
        </tr>
        <tr scope="row">
            <td>david@lynkevo.com</td>
            <td>p9OpenC]24)</td>
            <td>Utilisateur</td>
        </tr>
        <tr scope="row">
            <td>isabelle@lynkevo.com</td>
            <td>p9OpenC]24)</td>
            <td>Utilisateur</td>
        </tr>
        <tr scope="row">
            <td>marc@lynkevo.com</td>
            <td>p9OpenC]24)</td>
            <td>Utilisateur</td>
        </tr>
        <tr scope="row">
            <td>kim@lynkevo.com</td>
            <td>p9OpenC]24)</td>
            <td>Utilisateur</td>
        </tr>
        <tr scope="row">
            <td>aurelie@lynkevo.com</td>
            <td>p9OpenC]24)</td>
            <td>Utilisateur</td>
        </tr>
        <tr scope="row">
            <td>elodie@lynkevo.com</td>
            <td>p9OpenC]24)</td>
            <td>Utilisateur</td>
        </tr>
    </tbody>
</table>

### Démarrage du serveur de développement

Cette commande doit être exécutée depuis le dossier où se trouve le fichier manage.py.

python manage.py runserver

### Informations complémentaires

La page Home affiche une page d'inscription et de connexion.  
Vous pouvez créer autant d'utilisateurs que vous le souhaitez.  
Une fois l'utilisateur créé, il est redirigé sur la page Flux (feed). 
Il a accès à toutes les fonctionnalités du site :  
- Création de billets
- Création de critiques
- Création en une seule fois de billet et sa critique
- Suivi d'autres utilisateurs
- Aperçu de ses propres billets et critiques
