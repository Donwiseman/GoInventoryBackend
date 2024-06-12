from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from emailVerification import Email
from database import storage
from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required
from smtplib import SMTPConnectError, SMTPRecipientsRefused


@app_look.route('/user', methods=['GET', 'PUT', 'DELETE'],
                strict_slashes=False)
@jwt_required()
def user():
    """Endpoint to handle the user resource"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid JSON token"}), 401
    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Invalid JSON token claims"}), 401

    if request.method == "GET":
        org = []
        for asso in user.org_associations:
            organization = storage.get_org_by_id(asso.org_id)
            org_detail = {
                "name": organization.name,
                "id": organization.id,
                "user_role": organization.get_user_role(user.id)
            }
            org.append(org_detail)
        created_org = []
        for organization in user.org_created:
            org_detail = {
                "name": organization.name,
                "id": organization.id,
                "created_at": organization.created_at_local_time_strf()
            }
            created_org.append(org_detail)
        user_dict = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "email_verified": user.email_verified,
            "mobile": user.mobile,
            "mobile_verified": user.mobile_verified,
            "organizations": org,
            "created_at": user.created_at,
            "organizations_created": created_org
        }
        return jsonify(user_dict)

    if request.method == "PUT":
        msg = []
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        if not email and not mobile and not first_name and not last_name:
            mesg = "Update failed, Empty parameters"
            return jsonify({"message": mesg}), 400
        if email:
            mail = Email()
            try:
                code = mail.generate_password()
                mail.send_mail(email, code)
                mesg = "Email updated and verification code sent"
            except SMTPConnectError:
                mesg = "Email updated but verification code could not be sent"
            except SMTPRecipientsRefused:
                mesg = "Update failed, email is invalid"
                return jsonify({"message": mesg}), 400
            user.active_token = code
            user.token_expiry = datetime.utcnow() + timedelta(minutes=10)
            user.email_verified = False
            msg.append(mesg)
        if mobile:
            user.mobile = mobile
            msg.append("Mobile number updated")
        if first_name:
            user.first_name = first_name
            msg.append("First name updated")
        if last_name:
            user.last_name = last_name
            msg.append("Last name updated")
        storage.save()
        return jsonify({"message": ", ".join(msg)})

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({"message": "User account has been deleted"})
