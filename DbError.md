Il y a plusieurs étapes à vérifier lorsque l'erreur **DPI-1047** persiste après l'installation de l'Instant Client et son ajout au `PATH`. Si ta base de données est dans SQL Developer et que tu utilises l'Instant Client pour te connecter avec `cx_Oracle`, voici ce que tu peux faire pour configurer correctement l'Instant Client :

### 1. **Vérifier l'installation de l'Instant Client**
   - Assure-toi que tu as bien téléchargé la version **64 bits** de l'Instant Client, car cx_Oracle nécessite une correspondance entre l'architecture du client Oracle et celle de Python.
   - Ouvre une fenêtre de terminal (ou CMD) et tape la commande suivante pour vérifier que le chemin est bien ajouté :
     ```bash
     echo %PATH%  # Pour Windows
     echo $PATH    # Pour macOS ou Linux
     ```
   - Vérifie si le chemin de l'Instant Client est bien présent. Par exemple :
     ```
     C:\oracle\instantclient_19_8
     ```

### 2. **Télécharger les bibliothèques manquantes pour Windows**
   - Sur **Windows**, il est possible que certaines **bibliothèques Microsoft Visual C++ Runtime** soient manquantes.
   - Tu peux télécharger le **Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, and 2019** [ici](https://aka.ms/vs/17/release/vc_redist.x64.exe).
   - Installe-le et redémarre ton ordinateur pour être sûr que tout est pris en compte.

### 3. **Configurer les variables d'environnement**
   - En plus de la variable `PATH`, il est parfois nécessaire de définir une autre variable d'environnement spécifique pour Oracle.
   - **ORACLE_HOME** : Configure cette variable d'environnement pour pointer vers ton dossier Instant Client :
     - **Windows** :
       1. Clique droit sur "Ce PC" > Propriétés > Paramètres système avancés > Variables d'environnement.
       2. Sous Variables Système, clique sur "Nouveau" et ajoute une variable :
          - **Nom** : `ORACLE_HOME`
          - **Valeur** : Le chemin complet vers le dossier Instant Client, par exemple : `C:\oracle\instantclient_19_8`
     - **Linux/macOS** : Ajoute ceci à ton `.bashrc` ou `.zshrc` :
       ```bash
       export ORACLE_HOME=/chemin/vers/instantclient
       ```
     - Redémarre ton terminal ou ta session pour que les changements soient appliqués.

### 4. **Créer un fichier `tnsnames.ora` (si nécessaire)**
   - Si tu utilises un connecteur Oracle Net (par exemple via SQL*Net ou OCI), tu devrais créer un fichier `tnsnames.ora` dans le dossier de l'Instant Client ou dans un sous-dossier `network/admin`.
   - Ce fichier contient les informations de connexion à la base de données, par exemple :
     ```ini
     ORCL =
       (DESCRIPTION =
         (ADDRESS = (PROTOCOL = TCP)(HOST = your-db-host)(PORT = 1521))
         (CONNECT_DATA =
           (SERVICE_NAME = your-service-name)
         )
       )
     ```
   - Une fois créé, assure-toi que l'Instant Client peut y accéder en ajoutant son chemin à la variable d'environnement `TNS_ADMIN` :
     ```bash
     export TNS_ADMIN=/chemin/vers/tnsnames
     ```

### 5. **Connexion sans TNS (par connexion directe)**

Si tu ne veux pas configurer `tnsnames.ora`, tu peux utiliser une connexion directe (easy connect) avec `cx_Oracle`. Dans ton script Python, spécifie la chaîne de connexion comme suit :
```python
import cx_Oracle

connection = cx_Oracle.connect('username/password@host:port/service_name')
```
Par exemple :
```python
connection = cx_Oracle.connect('scott/tiger@localhost:1521/orclpdb1')
```

### 6. **Vérifier que l'Instant Client fonctionne**
   - Dans une console ou un terminal, tape :
     ```bash
     sqlplus /nolog
     ```
   - Si tu arrives à cette étape, cela veut dire que l'Instant Client est bien installé et fonctionnel.
   - Ensuite, essaye de te connecter :
     ```bash
     connect username/password@host:port/service_name
     ```
   - Si la connexion réussit, ton installation est correcte.

### 7. **Vérifier la compatibilité de cx_Oracle**
   - Assure-toi que la version de `cx_Oracle` que tu utilises est bien compatible avec la version d'Oracle Client que tu as installée. Si besoin, mets à jour cx_Oracle :
     ```bash
     pip install cx_Oracle --upgrade
     ```

Si après ces vérifications, l'erreur persiste, essaye de supprimer l'installation actuelle d'Instant Client et de recommencer avec une installation propre.