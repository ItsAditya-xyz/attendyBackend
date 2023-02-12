import requests
from app.function import (
    encrypt_message,
    decrypt_message,
    getDiamondsForPosts,
    getPosterPublicKey,
)
import json
import re
import pyrebase
from datetime import datetime
from pytz import timezone


def signUp(request, jsonify, MYSQL, FIREBASE):
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        name = data["name"]
        # check for email regex and password length
        reg = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if not re.search(reg, email):
            return jsonify({"status": "failed", "message": "Invalid email"})
        if len(password) < 8 or len(password) >= 18:
            return jsonify(
                {
                    "status": "failed",
                    "message": "Password must be atleast 8 characters long or less than 18 characters long",
                }
            )
        email = email.replace("@", "_AT").replace(".", "_")

        # cur = MYSQL.connection.cursor()
        # cur.execute(f'SELECT * FROM attendyAccount WHERE emailVal = "{email}"')
        # result = cur.fetchall()
        # if len(result) > 0:
        #     return jsonify({"status": "failed", "message": "Email already exists"})
        # cur.execute(
        #     f'INSERT INTO attendyAccount (emailVal, passwordVal, name) VALUES ("{email}", "{password}", "{name}")'
        # )
        # MYSQL.connection.commit()

        firebaseConfig = {
            "apiKey": FIREBASE["apiKey"],
            "authDomain": FIREBASE["authDomain"],
            "projectId": FIREBASE["projectId"],
            "storageBucket": FIREBASE["storageBucket"],
            "messagingSenderId": FIREBASE["messagingSenderId"],
            "appId": FIREBASE["appId"],
            "databaseURL": FIREBASE["databaseURL"],
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()

        if db.child("attendyAccount").child(email).get().val() != None:
            return jsonify({"status": "failed", "message": "Email already exists"})
        db.child("attendyAccount").child(email).set(
            {"passwordVal": password, "name": name}
        )

        admin_data = {
            "classes": {},
            "organisation": name,
        }
        db.child(email).set(admin_data)

        return jsonify({"status": "success", "message": "Successfully signed up"})
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "message": f"Something went wrong {e}"})


def login(request, jsonify, MYSQL, FIREBASE):
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        email = email.replace("@", "_AT").replace(".", "_")
        # cur = MYSQL.connection.cursor()
        # cur.execute(f'SELECT * FROM attendyAccount WHERE emailVal = "{email}"')
        # result = cur.fetchall()
        # # print(result)
        # if len(result) == 0:
        #     return jsonify({"status": "failed", "message": "Email does not exist"})
        # if result[0][1] != password:
        #     return jsonify({"status": "failed", "message": "Password is incorrect"})

        firebaseConfig = {
            "apiKey": FIREBASE["apiKey"],
            "authDomain": FIREBASE["authDomain"],
            "projectId": FIREBASE["projectId"],
            "storageBucket": FIREBASE["storageBucket"],
            "messagingSenderId": FIREBASE["messagingSenderId"],
            "appId": FIREBASE["appId"],
            "databaseURL": FIREBASE["databaseURL"],
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()

        result = db.child("attendyAccount").child(email).get().val()
        if result == None:
            return jsonify({"status": "failed", "message": "Email does not exist"})

        if result["passwordVal"] != password:
            return jsonify({"status": "failed", "message": "Password is incorrect"})

        return jsonify(
            {
                "status": "success",
                "message": "Successfully logged in",
                "data": {"name": result["name"], "email": email},
            }
        )
    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "message": f"Something went wrong {e}"})


def add_student(request, jsonify, FIREBASE):
    try:
        data = request.get_json()

        admin_email = data["admin_email"]
        admin_password = data["admin_password"]
        class_name = data["class_name"]
        student_roll = data["student_roll"]
        student_name = data["student_name"]
        guardian_number = data["guardian_number"]
        wallet_address = data["wallet_address"]

        admin_email = admin_email.replace("@", "_AT").replace(".", "_")

        firebaseConfig = {
            "apiKey": FIREBASE["apiKey"],
            "authDomain": FIREBASE["authDomain"],
            "projectId": FIREBASE["projectId"],
            "storageBucket": FIREBASE["storageBucket"],
            "messagingSenderId": FIREBASE["messagingSenderId"],
            "appId": FIREBASE["appId"],
            "databaseURL": FIREBASE["databaseURL"],
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()

        admin_data = db.child("attendyAccount").child(admin_email).get().val()
        if admin_data == None:
            return jsonify({"status": "failed", "message": "Admin does not exist"})
        if admin_data["passwordVal"] != admin_password:
            return jsonify({"status": "failed", "message": "Password is incorrect"})

        db.child(admin_email).child("classes").child(class_name).child(
            student_roll
        ).set(
            {
                "name": student_name,
                "guardian_number": guardian_number,
                "wallet_address": wallet_address,
            }
        )

        return jsonify({"status": "success", "message": "Successfully added student"})

    except Exception as e:
        print(e)
        return jsonify({"status": "failed", "message": f"Something went wrong {e}"})


def get_details(request, jsonify, FIREBASE):
    data = request.get_json()
    admin_email = data["admin_email"]
    # admin_password = data["admin_password"]

    admin_email = admin_email.replace("@", "_AT").replace(".", "_")

    firebaseConfig = {
        "apiKey": FIREBASE["apiKey"],
        "authDomain": FIREBASE["authDomain"],
        "projectId": FIREBASE["projectId"],
        "storageBucket": FIREBASE["storageBucket"],
        "messagingSenderId": FIREBASE["messagingSenderId"],
        "appId": FIREBASE["appId"],
        "databaseURL": FIREBASE["databaseURL"],
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    admin_data = db.child("attendyAccount").child(admin_email).get().val()

    if admin_data == None:
        return jsonify({"status": "failed", "message": "Admin does not exist"})

    return jsonify(
        {
            "status": "success",
            "message": "Successfully fetched details",
            "data": db.child(admin_email).get().val(),
        }
    )


def delete_student(request, jsonify, FIREBASE):
    data = request.get_json()
    admin_email = data["admin_email"]
    admin_password = data["admin_password"]

    class_name = data["class_name"]
    student_roll = data["student_roll"]

    admin_email = admin_email.replace("@", "_AT").replace(".", "_")

    firebaseConfig = {
        "apiKey": FIREBASE["apiKey"],
        "authDomain": FIREBASE["authDomain"],
        "projectId": FIREBASE["projectId"],
        "storageBucket": FIREBASE["storageBucket"],
        "messagingSenderId": FIREBASE["messagingSenderId"],
        "appId": FIREBASE["appId"],
        "databaseURL": FIREBASE["databaseURL"],
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    admin_data = db.child("attendyAccount").child(admin_email).get().val()
    if admin_data == None:
        return jsonify({"status": "failed", "message": "Admin does not exist"})
    if admin_data["passwordVal"] != admin_password:
        return jsonify({"status": "failed", "message": "Password is incorrect"})

    db.child(admin_email).child("classes").child(class_name).child(
        student_roll
    ).remove()


def delete_class(request, jsonify, FIREBASE):
    data = request.get_json()
    admin_email = data["admin_email"]
    admin_password = data["admin_password"]

    class_name = data["class_name"]

    admin_email = admin_email.replace("@", "_AT").replace(".", "_")

    firebaseConfig = {
        "apiKey": FIREBASE["apiKey"],
        "authDomain": FIREBASE["authDomain"],
        "projectId": FIREBASE["projectId"],
        "storageBucket": FIREBASE["storageBucket"],
        "messagingSenderId": FIREBASE["messagingSenderId"],
        "appId": FIREBASE["appId"],
        "databaseURL": FIREBASE["databaseURL"],
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    admin_data = db.child("attendyAccount").child(admin_email).get().val()
    if admin_data == None:
        return jsonify({"status": "failed", "message": "Admin does not exist"})
    if admin_data["passwordVal"] != admin_password:
        return jsonify({"status": "failed", "message": "Password is incorrect"})

    db.child(admin_email).child("classes").child(class_name).remove()


def mark_attendance(request, jsonify, FIREBASE):
    data = request.get_json()
    admin_email = data["admin_email"]
    admin_password = data["admin_password"]

    class_name = data["class_name"]
    student_roll = data["student_roll"]
    is_present = data["is_present"] in ("true", "True", "TRUE", "1", 1, True)

    admin_email = admin_email.replace("@", "_AT").replace(".", "_")
    date = datetime.now(timezone("Asia/Kolkata")).strftime("%d_%m_%Y")
    hour = datetime.now(timezone("Asia/Kolkata")).strftime("%I%p")

    firebaseConfig = {
        "apiKey": FIREBASE["apiKey"],
        "authDomain": FIREBASE["authDomain"],
        "projectId": FIREBASE["projectId"],
        "storageBucket": FIREBASE["storageBucket"],
        "messagingSenderId": FIREBASE["messagingSenderId"],
        "appId": FIREBASE["appId"],
        "databaseURL": FIREBASE["databaseURL"],
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    admin_data = db.child("attendyAccount").child(admin_email).get().val()
    if admin_data == None:
        return jsonify({"status": "failed", "message": "Admin does not exist"})
    if admin_data["passwordVal"] != admin_password:
        return jsonify({"status": "failed", "message": "Password is incorrect"})

    student_name = (
        db.child(admin_email)
        .child("classes")
        .child(class_name)
        .child(student_roll)
        .child("name")
        .get()
        .val()
    )

    db.child("attendances").child(date).child(hour).child(admin_email).child(
        class_name
    ).child(student_roll).set(
        {
            "present": is_present,
            "name": student_name,
            "markTime": datetime.now(timezone("Asia/Kolkata")).strftime("%H:%M:%S"),
        }
    )

    return jsonify(
        {
            "status": "success",
            "message": "Successfully marked attendance",
        }
    )


def get_attendance(request, jsonify, FIREBASE):
    data = request.get_json()
    admin_email = data["admin_email"]
    date = data["date"]
    hour = date.split("/")[-1]
    if hour == date:
        hour = None

    admin_email = admin_email.replace("@", "_AT").replace(".", "_")

    print(date, hour, admin_email)
    firebaseConfig = {
        "apiKey": FIREBASE["apiKey"],
        "authDomain": FIREBASE["authDomain"],
        "projectId": FIREBASE["projectId"],
        "storageBucket": FIREBASE["storageBucket"],
        "messagingSenderId": FIREBASE["messagingSenderId"],
        "appId": FIREBASE["appId"],
        "databaseURL": FIREBASE["databaseURL"],
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    admin_data = db.child("attendyAccount").child(admin_email).get().val()
    if admin_data == None:
        return jsonify({"status": "failed", "message": "Admin does not exist"})

    if date == "all":
        return_data = db.child(f"attendances").get().val()
    else:
        if db.child(f"attendances/{date}").get().val() == None:
            return jsonify(
                {
                    "status": "failed",
                    "message": "Attendance does not exist for this date",
                }
            )
        if hour == None:
            return_data = db.child(f"attendances").child(date).get().val()
        else:
            return_data = (
                db.child(f"attendances")
                .child(date)
                .child(admin_email)
                .get()
                .val()
            )

    return jsonify(
        {
            "status": "success",
            "message": "Successfully fetched attendance",
            "data": return_data,
        }
    )
