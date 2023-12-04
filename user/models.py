from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from app import users

class User:

    def signup(self):
        print(request.form)

        user = {
            "_id": request.form.get('username') ,
            "password": request.form.get('password'),
            "confirm_passwprd": request.form.get('confirm_password'),
            "full_name": request.form.get('full_name'),
            "phone_number": request.form.get('phone_number'),
            "hostel": request.form.get('hostel_name'),
            "user_type": request.form.get('user_type')
        }

        #Ecrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        users.users.insert_one(user)

        #for success calls:200, failure calls:400
        return jsonify(user), 200