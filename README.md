# chess-rating-system

First after downloading install requirements:
pip install -r requirements.txt

The app is still developing, so yet it's only local. 
Before running the app you should set up PostgreSQL database (migrating to SQLite is in the process).
The database used is local, so there will be no data after initializing the app. Though you the app will work fine.

To run the app:
chcli websrv

To initialize the database:
chcli db init

To clear the database:
chcli db init -c
