# Chrate

## Setup tutorial

First run:
```bash
pyton3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

To initialize a local database:
```bash
chcli db init
```

To run the app:
```bash
chcli websrv
```

Then the app will be available at [127.0.0.1:5000/](http://127.0.0.1:5000/)