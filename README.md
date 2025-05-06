# OC-Projet10 : Créez une API sécurisée RESTful en utilisant Django REST.

Cette application est une API qui permet de :<br>
- Servir des données (utilisateurs, projets, tickets, commentaires) <br>
- Ajouter, modifier ou supprimer des données dans la base de données en fonction des permissions accordées <br>
<br>

> [!NOTE]
> Testé sous Ubuntu 24.04 - Python 3.12.3 - Navigateur Mozilla Firefox - Postman

## ✅ Prérequis

Pour installer ce programme, vous aurez besoin d'une connexion internet. Le programme est ensuite exécuté en local et ne nécessite pas de connexion internet pour fonctionner.<br>
<br>
Python doit être installé sur votre ordinateur (version 3.12.3 ou supérieur).<br>
<br>
L'installateur **pip** doit également être disponible sur votre machine pour installer les dépendances.
Il est possible d'utiliser **pipenv** pour centraliser la gestion des modules, dépendances et environnement virtuel.

## 📦 Installation et exécution du programme

<details>
<summary>📍 Etape 1 - Installer git</summary><br>

Pour télécharger ce programme, vérifiez que git est bien installé sur votre poste.<br>
Vous pouvez l'installer en suivant les instructions fournies sur le site [git-scm.com](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

</details>

<details>
<summary>📍 Etape 2 - Cloner le dépôt contenant le programme</summary><br>


Placez-vous dans le dossier souhaité et utilisez la commande suivante :

``git clone https://github.com/Guillaume-Gillon/OC_Projet10.git``

</details>

<details>
<summary>📍 Etape 3 - Créer et activer un evironnement virtuel</summary>

#### Sans pipenv
Créez un environnement virtuel avec la commande<br>
``python3 -m venv env``<br>

Activez cet environnement avec la commande<br>
``source env/bin/activate``

#### Avec pipenv
Placez-vous dans le dossier SoftDesk_API et exécutez la commande<br>
``pipenv install``
Cette commande crée l'environnement virtuel et installe les modules listés dans le fichier Pipfile.

</details>

<details>
<summary>📍 Etape 4 - Installer les dépendances</summary>

#### Sans pipenv
Pour que ce programme s'exécute, vous aurez besoin de plusieurs packages additionnels listés dans le fichier requirements.txt.<br>

Exécutez la commande <br>
``pip install -r requirements.txt``

#### Avec pipenv
L'installation des dépendances a été réalisée à l'étape 3.

</details>

<details>
<summary>📍 Etape 5 - Lancer un serveur local</summary><br>

#### Sans pipenv
Placez vous dans le dossier **SoftDesk_API** puis exécutez la commande <br>
``python3 manage.py runserver``

#### Avec pipenv
Placez vous dans le dossier **SoftDesk_API** puis exécutez la commande <br>
``pipenv run python manage.py runserver``

</details>

<details>
<summary>📍 Etape 6 - Ouvrez l'application</summary><br>

Dans la barre d'adresse de votre navigateur, entrez l'un des endpoints suivants :<br>
``http://127.0.0.1:8000/users/``
``http://127.0.0.1:8000/users/ID``
``http://127.0.0.1:8000/create-users/``
``http://127.0.0.1:8000/projects/``
``http://127.0.0.1:8000/projects/ID``
``http://127.0.0.1:8000/issues/``
``http://127.0.0.1:8000/issues/ID``
``http://127.0.0.1:8000/comments/``
``http://127.0.0.1:8000/comments/ID``

Remplacer **ID** par la valeur de l'entrée souhaitée.

</details>

## ⚙️ Fonctionnement du programme

L'application comporte différentes sections accessibles sur permission :
- Endpoint USERS : Permissions pour administrateurs uniquement<br>
- Endpoint CREATE-USERS : Permissions en écriture pour utilisateurs non-authentifiés, permissions en lecture et écriture pour administrateurs<br>
- Endpoints PROJECTS, ISSUES, COMMENTS : Permissions en lecture pour utilisateurs authentifiés et en écriture pour contributeurs et administrateurs<br>
<br><br>

L'utilisateur a la possibilité de :
- Créer un compte personnel
- Se connecter / se déconnecter
- Supprimer son compte personnel
- Créer un projet
- Modifier un projet dont il est contributeur
- Créer un ticket associé à un projet dont il est contributeur
- Modifier un ticket dont il est auteur
- Créer un commentaire associé à un projet dont il est contributeur
- Modifier un commentaire dont il est auteur
<br><br>

> [!NOTE]
> L'application est fournie avec une base de données contenant les informations suivantes : <br>
> - 4 utilisateurs : AdminDatabase - deleted_user - GuillaumeGillon - CamilleDupont <br>
> - Les mots de passe de ces utilisateurs sont : DefaultPassword1 <br>
> - Seul l'utilisateur AdminDatabase a les droits "superuser" <br>
> - Des projets, tickets et commentaires sont également présents. <br>

## Utilisation de POSTMAN

Il est possible de générer des JWT dans Postman depuis ``http://127.0.0.1:8000/api/token/``<br>
Le JWT généré peut être utilisé pour accéder aux différents fonctionnalités de l'API.<br>
