------------------------------------------------------------------------------------------------------
PROJET FLASK SQLite
------------------------------------------------------------------------------------------------------
Quelles sont les notions qui vont être abordées au cours de cet atelier ?
Cet atelier a pour objectif de vous apprendre à créer des bases de données grace à Python et SQLite. Vous allez ensuite exploter cette base de données via la construction d'API. Vous allez utiliser et mettre en oeuvre au travers de cet atelier, un serveur Python utilisant le Framework Flask. 
Vous allez créer des API, découvrir les Actions et les Secrets GitHUB pour au final mettre en service et exploiter une base de données.
Large programme mais tout à fait accessible et ne nécessitant pas de base technique particulière. Juste de l'observation et de la rigueur dans votre travail.

-------------------------------------------------------------------------------------------------------
Séquence 1 : GitHUB
-------------------------------------------------------------------------------------------------------
Objectif : Création d'un Repository GitHUB pour travailler avec son projet  
Difficulté : Très facile (~10 minutes)
-------------------------------------------------------------------------------------------------------
GitHUB est une plateforme en ligne utilisée pour stocker le code de son programme.
GitHUB est organisé en "Repository", c'est à dire en répertoire (contenant lui même des sous répertoires et des fichiers). Chaque Repository sera indépendant les un des autres. Un Repository doit être vu comme un projet unique (1 Repository = 1 Projet). GitHUB est une plateforme très utilisée par les informaticiens.

**Procedure à suivre :**  
1° - Créez vous un compte sur GitHub : https://github.com/  
Si besoin, une vidéo pour vous aider à créer votre propre compte GitHUB : [Créer un compte GitHUB](https://docs.github.com/fr/get-started/onboarding/getting-started-with-your-github-account)  
A noter que **si vous possédez déjà un compte GitHUB, vous pouvez le conserver pour réaliser cet atelier**. Pas besion d'en créer un nouveau.  
Remarque importante : **Lors de votre inscription, utilisez une adresse mail valide. GitHUB n'accepte pas les adresses mails temporaires**  

2° - Faites un Fork du Repository suivant : [https://github.com/OpenRSI/Flask_Projet_SQLite](https://github.com/OpenRSI/Flask_Projet_SQLite)  
Voici une vidéo d'accompagnement pour vous aider dans les "Forks" : [Forker ce projet](https://youtu.be/p33-7XQ29zQ)    
  
**Travail demandé :** Créé votre compte GitHUB, faites le fork de ce projet et **copier l'URL de votre Repository GitHUB dans la discussion public**.

Notion acquise lors de cette séquence :  
Vous avez appris lors de cette séquence à créer des Repository pour stocker et travailler avec votre code informatique. Vous pourez par la suite travailler en groupe sur un projet. Vous avez également appris à faire des Forks. C'est à dire, faire des copies de projets déjà existant dans GitHUB que vous pourrez ensuite adapter à vos besoins.
  
---------------------------------------------------
Séquence 2 : Création d'un hébergement en ligne
---------------------------------------------------
Objectif : Créer un hébergement sur Alawaysdata  
Difficulté : Faible (~10 minutes)
---------------------------------------------------

Rendez-vous sur **https://www.alwaysdata.com/fr/**  
  
Remarque : **Attention à bien vous rappeler de vos Login/Password** lors de la création de votre compte site car vous en aurez besoin plus tard pour la création de vos Secrets GitHUB.  
  
Voici une vidéo d'accompagnement pour vous aider dans cette séquence de création d'un site sur Alwaysdata : [Vidéo Alwaysdata](https://youtu.be/6cuHjy8n968)  
  
**Procédure :**  
1° - Créez votre compte Alwaysdata (gratuit jusqu'à 100Mo, aucune carte nécéssaire).  
2° - Depuis la console d'administration (Le panel d'administration de Alwaysdata) :  
 . 2.1 - Cliquez sur "Sites" (Colonne de gauche) puis **supprimer votre site PHP** (via l'icone de la Poubelle).  
 . 2.2 - **Installer ensuite une application Flask** (Bouton **+ Installer une application**).  
 . . 2.2.1 Adresses = utilisez le sous-domaine qui vous appartient que vous trouverez dans l'information " Les sous-domaines suivants vous appartiennent et sont actuellement inutilisés : {Site}.alwaysdata.net  
 . . 2.2.2 Répertoire d'installation = **/www/flask**  
 . 2.2.3 N'oubliez pas d'Accepter les conditions.  
3° - Autoriser les connexions SSH :  
 . 3.1 - Cliquez sur SSH (Accès distant).  
 . 3.2 - Modifier les paramètres de votre utilisateur.  
 . 3.3 - Définissez si besion un nouveau mot de passe.  
 . 3.4 - Cliquez sur **Activer la connexion par mot de passe**.  
  
**Travail demandé :** Mettre en ligne votre application Flask "Hello World !" et **copier l'URL de votre site dans la discussion public**.  
  
Notions acquises lors de cette séquence :  
Vous avez créer un hébergement (gratuit) et découvert également que vous pouvez installer bien d'autres applications (Django, Drupal, Jenkins, Magento, Symphony, etc...). Les perspectives sont nombreuses.

---------------------------------------------------------------------------------------------
Séquence 3 : Les Actions GitHUB (Industrialisation Continue)
---------------------------------------------------------------------------------------------
Objectif : Automatiser la mise à jour de votre hébergement Alwaysdata  
Difficulté : Moyenne (~15 minutes)
---------------------------------------------------------------------------------------------
Dans le Repository GitHUB que vous venez de créer précédemment lors de la séquence 1, vous avez un fichier intitulé CICD.yml et qui est déposé dans le répertoire .github/workflows. Ce fichier a pour objectif d'automatiser le déploiement de votre code sur votre site Alwaysdata. Pour information, c'est ce que l'on appel des Actions GitHUB. Ce sont des scripts qui s'exécutent automatiquement lors de chaque Commit dans votre projet (C'est à dire à chaque modification de votre code). Ces scripts (appelés actions) sont au format yml qui est un format structuré proche de celui d'XML.  

Pour utiliser cette Action (CICD.yml), **vous avez besoin de créer des secrets dans GitHUB** afin de ne pas divulguer des informations sensibles aux internautes de passage dans votre Repository comme vos login et password par exemple.  

Pour ce projet Métriques, **vous avez 4 secrets à créer** dans votre Repository GitHUB :  
**USERNAME** = Le login qui est utilisé pour la connexion SSH.  
**PASSWORD** = Le mot de passe qui est utilisé pour la connexion SSH.  
**ALWAYSDATA_TOKEN** = Le token est à créer depuis l'interface d'administration Alwaysdata. Cliquez sur votre profil en haut à droite, puis sur 'Profil' puis sur 'Gérer les tokens'. Laissez le champ "Adresses IP autorisées" vide. Dans le cas contraire vous limiteriez les connexions seulement à une adresse IP. Pour le champ Application* mettez "Monprojet" par exemple.  
**ALWAYSDATA_SITE_ID** = Vous trouverez l'ID de votre site depuis l'interface d'administration Alwaysdata dans les paramètres de votre site, c'est à dire la petite roue crantée à "droite" puis dans le titre #XXXXX. XXXXX étant l'ID de votre site. Ne prenez pas le # mais juste les chiffres.  
  
Voici une vidéo pour vous expliquer le processus de création de vos secrets dans GitHUB : [Création des secrets](https://youtu.be/pi80zRdrJyQ)  
Vous pouvez à présent **lancer une action pour mettre en ligne votre solution**.  
  
Notions acquises de cette séquence :  
Vous avez vu dans cette séquence comment créer des secrets GiHUB afin de mettre en place de l'industrialisation continue.  
L'utilité des scripts d'actions (C'est à dire des scripts exécutés lors des Commits) est très importante mais sortes malheureusement du cadre de cet atelier faute de temps. Toutefois, je vous invites à découvrir cet outil via les différentes sources du Web (Google, ChatGPT, etc..).  

---------------------------------------------------
Séquence 4 : Créer la base de données sur votre serveur
---------------------------------------------------
Objectif : Créer la base de données SQLite sur votre serveur  
Difficulté : Faible (~10 minutes)
---------------------------------------------------
1° - Connectez vous en SSH à votre serveur Alwaysdata via l'adresse suivante :**https://ssh-{compte}.alwaysdata.net**. Remarque importante, {compte] est à remplacer par votre compte Alwaysdata. C'est à dire le compte que vous avez utilisé pour renseigner votre secret GitHUB USERNAME.   
2° - Une fois connecté, depuis de la console SSH, executez la commande suivante : **cd www/flask** puis **python3 create_db.py**  
Votre base de données est à présent opérationnelle sur votre serveur (Le fichier database.db à été créé dans votre répertoire sur le serveur)
Vous pouvez, si vous le souhaitez, tappez la commande **ls** dans votre console pour voir la présence de la base de données.

LES ROUTES (API)
-------------------------------------------
Votre solution est à présent opérationnelle. Vous pouvez testez les routes (API) comme suit :  
  
https://{Votre_URL}**/**  
Pointe sur le fichier helloWorld d'accueil  

https://{Votre_URL}**/lecture**  
L'accès est conditionné à un contrôle d'accès  

https://{Votre_URL}**/authentification**  
Page d'authentification (admin, password)  

https://{Votre_URL}**/fiche_client/1**  
Permet de faire un filtre sur un client. Vous pouvez changer la valeur de 1 par le N° du client de votre choix  

https://{Votre_URL}**/consultation/**  
Permet de consutler la base de données  

https://{Votre_URL}**/enregistrer_client**  
API pour enregistrer un nouveau client  

---------------------------------------------------
Séquence 5 : Exercices
---------------------------------------------------
Objectif : Travailler votre code  
Difficulté : Moyenne (~60 minutes)
---------------------------------------------------
**Exercice 1 : Création d'une nouvelle fonctionnalité**    
Créer une nouvelle route dans votre application afin de faire une recherche sur la base du nom d'un client.  
Cette fonctionnalité sera accéssible via la route suivante : **/fiche_nom/**  

**Exercice 2 : Protection**  
Cette nouvelle route "/fiche_nom/" est soumise à un contrôle d'accès User. C'est à dire différent des login et mot de passe administrateur.  
Pour accéder à cette fonctionnalité, l'utilisateur sera authentifié sous les login et mot de passe suivant : **user/12345**
  
---------------------------------------------------
Séquence 6 : Le projet de bibliothèque
---------------------------------------------------
Objectif : Créer une application de biliothèque  
Difficulté : Moyenne (~180 minutes)
---------------------------------------------------
Votre projet consiste à present à concevoir et développer une application de gestion de bibliothèque moderne qui simplifie le processus de prêt et de retour de livres. Les fonctionnalités attendues dans le cadre de ce projet sont les suivantes :  
•	L’enregistrement et la suppression de livres.  
•	La recherche de livres disponibles.  
•	L'emprunt possible d'un livre par un utilisateur.  
•	La gestion des utilisateurs.  
•	La gestion des stocks.  
Votre travail est de modifier votre code afin de répondre aux besoins définis ci-dessus.
L'application exploitera des API pour interagir avec la base de données et un contrôle d'accès Utilisateur/Administrateur doit être mis en place.  
L’application pourra être enrichie avec des fonctionnalités supplémentaires telles que des recommandations de livres, des notifications pour les retours en retard, ou encore des rapports statistiques sur l'utilisation des livres pour améliorer l'expérience utilisateur et la gestion de la bibliothèque.  

------------------/!\ MODIFICATIONS EFFECTUEES /!\------------------------
Séquence suivante — Évolution de l’application Flask (explication détaillée)

Dans les premières séquences du projet, l’application Flask était volontairement très simple.
Elle servait surtout à comprendre les bases : lancer un serveur Flask et afficher une page HTML.

1. Rappel : ce que faisait le code de base
Le code initial se limitait à :
- créer une application Flask,
- définir une seule route /,
- afficher une page HTML (hello.html).

Limite de cette version :
- aucune base de données,
- aucune authentification,
- aucune logique métier,
- aucune API.
L’application ne faisait qu’afficher une page, sans interaction réelle.

2. Objectif des modifications apportées

Les modifications réalisées ont pour but de transformer cette application basique en une application web plus réaliste, intégrant :
- une base de données SQLite,
- une API REST,
- deux types d’authentification,
- une logique métier simple (gestion d’une bibliothèque).
L’objectif reste pédagogique : comprendre comment une vraie application Flask est structurée, sans complexité excessive.

3. Ajout d’une base de données SQLite
Pourquoi une base de données ?

Une application réelle doit pouvoir stocker des informations :
- des utilisateurs, des livres, et des emprunts.
SQLite a été choisie car :
- elle est simple, elle ne nécessite pas de serveur, et elle est parfaitement adaptée aux TP.
- 
Chemin absolu vers la base :
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
Ce point est très important :
le chemin absolu évite le problème classique où Flask crée une base vide par erreur selon le dossier depuis lequel l’application est lancée.

4. Fonction utilitaire pour accéder à la base
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
Cette fonction :
- ouvre une connexion vers la base SQLite,
- permet d’accéder aux colonnes par leur nom (row["title"]) plutôt que par index (row[0]),
- centralise l’accès à la base pour éviter la duplication de code.

5. Mise en place de l’authentification
Deux types d’authentification ont été ajoutés pour illustrer deux approches différentes.

5.1 Authentification “utilisateur” (Basic Auth + base de données)
Cette authentification est utilisée pour accéder à l’API publique de la bibliothèque.
Principe :
- l’utilisateur fournit un login / mot de passe,
- ces informations sont vérifiées dans la table users,
- seul un utilisateur ayant le rôle user est autorisé.

def require_user_auth_db():
    auth = request.authorization
    if not auth:
        return Response("Auth requise", 401, {"WWW-Authenticate": 'Basic realm="User Area"'})
Si l’utilisateur n’est pas authentifié :
- le serveur renvoie une erreur 401, et le navigateur affiche automatiquement une fenêtre de login.
Cette méthode permet de comprendre : les codes HTTP, le fonctionnement du header Authorization, et la protection d’une API.

5.2 Authentification “admin” via session Flask
- Cette authentification est différente :
- elle passe par un formulaire HTML,
- l’état de connexion est stocké dans la session Flask.

session["authentifie"] = True
Elle permet d’accéder aux fonctionnalités administrateur : ajout de livres, suppression de livres.
Cette séparation montre qu’il peut exister plusieurs niveaux d’accès dans une même application.

6. Réorganisation des routes existantes
Les anciennes routes liées aux “clients” du TP initial ont été volontairement :
- soit désactivées,
- soit redirigées vers les nouvelles routes API.
Cela permet de :
- conserver la structure du TP, éviter la confusion, montrer comment une application peut évoluer sans tout casser.

7. Création d’une API de bibliothèque
7.1 Liste des livres disponibles
Route : GET /api/books
Fonctionnalités : authentification obligatoire, affichage uniquement des livres disponibles, possibilité de recherche par titre, auteur ou ISBN.
Cette route illustre : l’utilisation des paramètres URL (?search=), les requêtes SQL conditionnelles, le retour de données au format JSON.

7.2 Emprunter un livre
Route : POST /api/borrow/<book_id>

Logique : vérifier que l’utilisateur est authentifié, vérifier que le livre existe, vérifier que le stock est suffisant, enregistrer l’emprunt, décrémenter le stock.
Cette route introduit :
- la notion de logique métier,
- la gestion des erreurs (404, 409),
- les transactions SQL.

7.3 Rendre un livre
Route : POST /api/return/<book_id>

Fonctionnement inverse :
- recherche d’un emprunt actif,
- mise à jour de la date de retour,
- incrémentation du stock.

8. API administrateur
Les routes administrateur sont protégées par la session.
Ajouter un livre : POST /api/admin/books
- données envoyées en JSON,
- validation minimale des champs,
- initialisation du stock.
Supprimer un livre : DELETE /api/admin/books/<id>
Ces routes permettent de comprendre :
- les méthodes HTTP (POST / DELETE),
- la distinction utilisateur / administrateur,
- la sécurisation des actions sensibles.

9. Route de diagnostic (debug)
/api/debug/counts
Cette route retourne : le nombre de livres, le nombre d’utilisateurs, le nombre d’emprunts.
Elle sert uniquement à : vérifier que la base n’est pas vide, diagnostiquer rapidement un problème de données.

10. Conclusion pédagogique
Grâce à ces évolutions, l’application est passée : d’une simple page Flask à une application web complète de niveau débutant/intermédiaire, intégrant :
- base de données,
- API REST,
- authentification,
- logique métier,
- séparation des rôles.

L’objectif n’est pas de faire une application “production”, mais de comprendre les briques fondamentales d’un backend Flask moderne.

Chemins à utiliser pour vérifications :
1. Vérifier que Flask fonctionne (application en ligne)
https://oceanaquatique.alwaysdata.net > Base de l’application (hébergement AlwaysData). Sert à vérifier : que Flask démarre correctement, que le serveur répond, et que le template hello.html est bien chargé.

2. Vérifier l’authentification admin (session Flask)
https://oceanaquatique.alwaysdata.net/authentification > Sert à vérifier : que les routes GET/POST fonctionnent, que le formulaire HTML s’affiche, et que les sessions Flask fonctionnent.
Test :
- identifiant : admin
- mot de passe : password
Si correct, redirection vers : https://oceanaquatique.alwaysdata.net/lecture

3. Vérifier que la base de données n’est pas vide :
https://oceanaquatique.alwaysdata.net/api/debug/counts > Sert à vérifier : que Flask pointe vers la bonne base SQLite, que les tables existent, et que les données sont bien présentes.
Si tout est à 0 : soit la base est vide, soit Flask pointe vers une mauvaise DB (erreur de chemin).

4. Vérifier l’API utilisateur (bibliothèque) (Ces routes nécessitent une authentification Basic Auth (login / mot de passe stockés dans la table users)).
https://oceanaquatique.alwaysdata.net/api/books > Lister les livres disponibles
Ce qui se passe : le navigateur demande un login / mot de passe, Flask vérifie dans la DB, si OK ➜ liste JSON des livres disponibles.
Sert à vérifier : l’authentification Basic Auth, la requête SQL, le format JSON.



