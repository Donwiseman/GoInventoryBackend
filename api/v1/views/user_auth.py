#!/usr/bin/python3
from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from emailVerification import Email
from database import storage
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, \
    jwt_required
from smtplib import SMTPConnectError, SMTPRecipientsRefused
Mail = Email()


@app_look.route('/signup', methods=['POST'], strict_slashes=False)
def reg_users():
    """Registers a user"""
    kwargs = {
        "first_name": request.form.get('firstName'),
        "last_name": request.form.get('lastName'),
        "email": request.form.get('email'),
        "password": request.form.get('password'),
        "mobile": request.form.get('mobile')
    }
    if kwargs["email"] is None or kwargs["password"] is None or\
            kwargs['first_name'] is None or kwargs['last_name'] is None:
        return jsonify({'message': 'Signup details is incomplete'}), 400
    user = storage.get_user_by_email(kwargs["email"])
    if user:
        return jsonify({'message': "email already exits"}), 400
    message = "Signup successful. Verification email sent."
    try:
        passW = Mail.generate_password()
        Mail.send_mail(kwargs['email'], passW)
    except SMTPConnectError:
        message = "Signup successful but verification email could not be sent"
    except SMTPRecipientsRefused:
        message = "Signup unsuccessful as Email is Invalid"
        return jsonify({"message": message}), 400
    new_user = storage.register_user(**kwargs)
    new_user.active_token = passW
    new_user.token_expiry = datetime.utcnow() + timedelta(minutes=10)
    access_token = create_access_token(identity=new_user.id)
    storage.save()
    org = []
    for asso in new_user.org_associations:
        organization = storage.get_org_by_id(asso.org_id)
        org_detail = {
            "name": organization.name,
            "id": organization.id,
            "user_role": organization.get_user_role(new_user.id)
        }
        org.append(org_detail)
    resp = {
        'message': message,
        "jwt": access_token,
        "id": new_user.id,
        "fullName": f"{new_user.first_name} {new_user.last_name}",
        "email_verified": new_user.email_verified,
        "mobile_verified": new_user.mobile_verified,
        "organizations": org
    }
    return jsonify(resp), 200


@app_look.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Logs the user to the site"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = storage.get_user_by_email(email)
    if not user:
        return jsonify({'message': "Wrong email"}), 401
    if not user.validate_password(password):
        return jsonify({'message': "Wrong password"}), 401
    access_token = create_access_token(identity=user.id)
    org = []
    for asso in user.org_associations:
        organization = storage.get_org_by_id(asso.org_id)
        org_detail = {
            "name": organization.name,
            "id": organization.id,
            "user_role": organization.get_user_role(user.id)
        }
        org.append(org_detail)
    resp = {
        'message': "Login Succesful",
        "jwt": access_token,
        "id": user.id,
        "fullName": f"{user.first_name} {user.last_name}",
        "email_verified": user.email_verified,
        "mobile_verified": user.mobile_verified,
        "organizations": org
    }
    return jsonify(resp), 200


@app_look.route('/reset', methods=['POST'], strict_slashes=False)
def password_reset():
    """Resets a given user password with valid token"""
    email = request.form.get('email')
    code = request.form.get('code')
    passowrd = request.form.get('password')
    user = storage.get_user_by_email(email)
    if not user:
        return jsonify({"message": "email does not belong to any user"})
    if user.token_expiry < datetime.utcnow():
        try:
            passW = Mail.generate_password()
            Mail.send_mail(user.email, passW)
            user.active_token = passW
            user.token_expiry = datetime.utcnow() + timedelta(minutes=10)
            msg = "Verification code expired, new code has been resent"
            storage.save()
        except SMTPConnectError:
            msg = "Verification code expired but error occurred resending code"
        return jsonify({"message": msg}), 400
    if code != user.active_token:
        return jsonify({"message": "Wrong verification code"}), 400
    user.set_password(passowrd)
    user.token_expiry = None
    user.active_token = None
    return jsonify({"message": "User password has been updated"})


@app_look.route('/verify', methods=['POST'], strict_slashes=False)
@jwt_required()
def get_code():
    """Gets the verification code"""
    code = request.form.get('code')
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid JSON token"}), 401
    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Invalid JSON token claims"}), 401
    if user.email_verified:
        return jsonify({"message": "User email is already verified"}), 400
    if user.token_expiry < datetime.utcnow():
        try:
            passW = Mail.generate_password()
            Mail.send_mail(user.email, passW)
            user.active_token = passW
            user.token_expiry = datetime.utcnow() + timedelta(minutes=10)
            msg = "Verification code expired, new code has been resent"
            storage.save()
        except SMTPConnectError:
            msg = "Verification code expired but error occurred resending code"
        return jsonify({"message": msg}), 400
    if code != user.active_token:
        return jsonify({"message": "Wrong verification code"}), 400
    user.email_verified = True
    user.active_token = None
    user.token_expiry = None
    storage.save()
    return jsonify({"message": "Email Verified"}), 200


@app_look.route('/token', methods=['POST'], strict_slashes=False)
def send_code():
    """Resends the verification code"""
    email = request.form.get('email')
    if not email:
        return jsonify({"message": "Email details not sent"}), 400
    user = storage.get_user_by_email(email)
    if not user:
        return jsonify({"message": "Email does not belong to any user"}), 400
    try:
        passW = Mail.generate_password()
        Mail.send_mail(user.email, passW)
        user.active_token = passW
        user.token_expiry = datetime.utcnow() + timedelta(minutes=10)
        msg = "Verification code has been sent"
        storage.save()
    except SMTPConnectError:
        msg = "Error occurred sending verification code"
    return jsonify(msg)


@app_look.route('/validate-token', methods=['GET'], strict_slashes=False)
@jwt_required()
def validate_token():
    """Check if JWT is valid"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid JSON token"}), 401
    user = storage.get_user_by_id(user_id)
    if user:
        return jsonify({"message": "JWT is valid"}), 204
    return jsonify({"message": "Invalid JSON token"}), 401
