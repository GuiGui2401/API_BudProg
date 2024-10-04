# API_BUDPROG

This is the documentation for the project that aims to transmit data from the Budprog database of PAD to Maximo for use in Sage. The API uses a Microsoft SQL Server database to store data related to users accessing the API and an Oracle SQL Developer database to retrieve budgetary data.

## SYSTEM REQUIREMENTS

- You must be on Windows Server Datacenter 2019 or a later version.
- Your server must have at least 4 GB of RAM and 10 GB of free space.
- The computer must be connected to the internet.
- You must update Windows drivers before proceeding.

## INSTALLATION OF PREREQUISITES

- Download Python 3.9 from this link: [https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe)
  - Follow the installation instructions.

- Download Microsoft SQL Server 2019 from this link: [https://www.microsoft.com/en-us/sql-server/sql-server-downloads](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
  - Follow the installation instructions.

- Download Oracle SQL Developer from this link: [https://www.oracle.com/database/sqldeveloper/technologies/download/](https://www.oracle.com/database/sqldeveloper/technologies/download/)
  - Follow the installation instructions.

- Download Microsoft C++ Build Tools 14.0 or greater from this link: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Follow the installation instructions.

- Download Microsoft ODBC Driver for SQL Server from this link: [https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows)
  - Follow the installation instructions.
  
## LIBRARIES INSTALLATION AND DATA MIGRATION

- Run the command `pip install -r requirements.txt` in the command prompt opened at the project's location.

- Run the command `py manage.py makemigrations` in the command prompt at the project's location.

- Run the command 'py manage.py migrate' in the command prompt at tje project's location.

- Run the command `py manage.py createsuperuser --username=api@pad.com --email=api@pad.com` and enter your password.

## Generation of tokens

- Run the command py manage.py shell and write this code line by line :

from jose import jwt
from django.contrib.auth.models import User
import datetime

# Clé secrète utilisée pour encoder le token
SECRET_KEY = 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0'

# Récupérer un utilisateur
user = User.objects.get(username='api@pad.com')

# Vérifier que l'utilisateur est actif
if user.is_active:
    # Définir l'expiration du token (par exemple 999 jours à partir d'aujourd'hui)
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=999)

    # Créer le payload du token
    payload = {
        'user': user.username,
        'expiry': expiry.strftime('%d/%m/%Y')  # Format dd/mm/yyyy
    }

    # Générer le token JWT en utilisant l'algorithme HS256
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    print(f"Token généré pour l'utilisateur {user.username} : {token}")
else:
    print(f"L'utilisateur {user.username} n'est pas actif.")

- At the end you obtain a token like this: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYXBpQHBhZC5jb20iLCJleHBpcnkiOiIyMy85LzIwMjYifQ.G9MYgcqxxVogQqqiJJ5zS3fC2QcnyhYEfCDLEuwKKSI` keep them.

## EXECUTION

- Double-click on the `budprog.bat` file located in the root of the project to launch it.

You can now test the APIs at the following addresses:

- `machineipaddress:9500/api/ligne-budgetaire?token=Generated_Token&codestructuremin=0000000000&codestructuremax=9999999999&anneebudgetaire=2023&page=1`

NB: If you have DPI-1047 error follow instructions on BbError.md