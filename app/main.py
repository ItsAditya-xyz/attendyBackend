from flask import Flask, request, jsonify
import requests
from flask_mysqldb import MySQL
from decouple import config
from flask_cors import CORS
from app.routeFiles import attendy



application = Flask(__name__)
CORS(application)

application.config['MYSQL_DB'] = DB_NAME
api_key = config('FIREBASE_API_KEY')
auth_domain = config('FIREBASE_AUTH_DOMAIN')
proj_id = config('FIREBASE_PROJECT_ID')
storage_bucket = config('FIREBASE_STORAGE_BUCKET')
messaging_sender_id = config('FIREBASE_MESSAGING_SENDER_ID')
database_url = config('FIREBASE_DATABASE_URL')
app_id = config('FIREBASE_APP_ID')

firebase_auth = {
    "apiKey": api_key,
    "authDomain": auth_domain,
    "projectId": proj_id,
    "storageBucket": storage_bucket,
    "messagingSenderId": messaging_sender_id,
    "appId": app_id,
    "databaseURL": database_url
}




@application.route("/")
def index():
    return jsonify({'status': 'success', 'message': 'Welcome to the API'})





# APIs for AttendyApp

application.add_url_rule(
    '/attendy-login', view_func=attendy.login, methods=['POST'], defaults={'jsonify': jsonify, 'MYSQL': mysql, 'request': request, 'FIREBASE': firebase_auth})

application.add_url_rule(
    '/attendy-signup', view_func=attendy.signUp, methods=['POST'], defaults={'jsonify': jsonify, 'MYSQL': mysql, 'request': request, 'FIREBASE': firebase_auth})

application.add_url_rule(
    '/add-student', view_func=attendy.add_student, methods=['POST'], defaults={'jsonify': jsonify, 'FIREBASE': firebase_auth, 'request': request})

application.add_url_rule(
    '/get-details', view_func=attendy.get_details, methods=['POST'], defaults={'jsonify': jsonify, 'FIREBASE': firebase_auth, 'request': request})


