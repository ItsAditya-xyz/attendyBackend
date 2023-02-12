# Attendy - AWS

<center>

This folder contains a Flask backend which is hosted on Amazon Web Services

</center>

## How to run locally

### Clone the repo

```bash
git clone https://github.com/ItsAditya-xyz/attendyBackend
cd attendyBackend/AWS
```

### Install python requirements

Make sure you have python3 and pip installed and on your system *PATH*

```bash
pip3 install -r requirements.txt
```

### You will need to create a `.env` file at the root of `AWS` folder with the following keys

```bash
vim .env
# OR
code .env
```

```
FIREBASE_API_KEY = <your api key>
FIREBASE_AUTH_DOMAIN = <your auth domain>
FIREBASE_PROJECT_ID = <your project id>
FIREBASE_STORAGE_BUCKET = <your storage bucket>
FIREBASE_MESSAGING_SENDER_ID = <your messaging id>
FIREBASE_APP_ID = <your app id>
FIREBASE_DATABASE_URL = <your database url>
```

These tokens cane be generated using Googles Firebase Realtime database service

### Run the project

```bash
python3 application.py
```