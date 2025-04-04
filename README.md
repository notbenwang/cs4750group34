# cs4750group34

Group Members:
* Benjamin Wang (hgf3jq)
* Conroy Lee (mtg9ny)
* 
* 

## Setting Up Project
1) Clone git repository onto your local machine.
```
  git clone https://github.com/notbenwang/cs4750group34/
```
2) Set up and enter python virtual environment [(reference)](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).
3) Install necessary libraries using 'requirements.txt'.
```
  pip install -r requirements.txt
```
4) Create a file in the 'cs4750group34' directory called '.env' and paste the following:
```
  DB_HOST = <host>
  DB_PORT = <port>
  DB_NAME = <username>
  DB_USER = <username>
  DB_PASSWORD = <password>
```
5) Change all '<>' variables to the  database credentials given by Professor McBurney in his email. For security reasons, the database credentials are not stored within this github repository.
## Running
If in the main directory, simply run:
```
  cd db_project
  python manage.py runserver
```
