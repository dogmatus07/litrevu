# LitReview

## Description

LitReview est une application web qui permet aux utilisateurs de :
- Créer des demandes de critiques sur des oeuvres littéraires ou des articles.
- Répondre à ces demandes par des critiques.
- Suivre l'activité littéraire d'autres utilisateurs.
- Gérer les abonnements aux profils des autres utilisateurs.

## Terminologie

- **Billets** : Demandes de critiques sur des articles ou oeuvres littéraires.
- **Critiques** : Avis et évaluations détaillées sur les billets.
- **User** : Utilisateur de l'application.
- **Flux** : Flux d'activités montrant les dernières actions des utilisateurs suivis.

## Prérequis

Assurez-vous que votre système dispose de Python 3.8 ou ultérieur pour exécuter cette application. Vous pouvez télécharger Python depuis le [site officiel](https://www.python.org/downloads/).

### Dépendances

Les dépendances requises sont listées dans le fichier `requirements.txt`. Installez-les en utilisant la commande suivante après avoir activé votre environnement virtuel :

```
pip install -r requirements.txt
```

## Configuration initiale

### Cloner le dépôt Git
Vous devez cloner le dépôt Git avec la commande suivante :

```
git clone https://github.com/dogmatus07/litrevu.git
```

### Installation des dépendances

Afin d'installer les dépendances, vous devez d'abord activer votre environnement virtuel.

#### Sous Windows

```
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt
```

#### Sous Mac & Linux

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Lancement de l'application

Pour lancer l'application, accédez au dossier du projet contenant le fichier manage.py et exécutez la commande suivante : 

```
py manage.py runserver
```

### Configuration de la base de données

Un fichier `db.sqlite3` est déjà inclus dans le projet avec des données de démonstration.  

Si vous souhaite réinitialiser la base de données, exécutez la commande suivante : 

```
py manage.py migrate
```

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

### Utilisation

La page Home affiche une page d'inscription et de connexion.  
Vous pouvez créer autant d'utilisateurs que vous le souhaitez.  
Une fois l'utilisateur créé, il est redirigé sur la page Flux (feed). 
Il a accès à toutes les fonctionnalités du site :  
- Création de billets
- Création de critiques
- Création en une seule fois de billet et sa critique
- Suivi d'autres utilisateurs
- Aperçu de ses propres billets et critiques
