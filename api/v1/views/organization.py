from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from emailVerification import Email
from database import storage
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, \
    jwt_required
from smtplib import SMTPConnectError
import pytz


@app_look.route('/countries', methods=['GET'], strict_slashes=False)
@jwt_required()
def supported_Countries():
    """Returns a dictionary containing country names and
       respective timezones.
    """
    countries = []
    for country_code, country in pytz.country_names.items():
        try:
            timezones = pytz.country_timezones(country_code)
        except KeyError:
            timezones = []
        country_data = {
            "country": country,
            "timezones": timezones
        }
        countries.append(country_data)
    return jsonify(countries)


@app_look.route('/organizations', methods=['GET', 'POST'],
                strict_slashes=False)
@jwt_required()
def organizations():
    """Handles the creating an organization by the user and retrieving
       list of those they belong to
    """
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid JSON token"}), 401
    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Invalid JSON token claims"}), 401
    if request.method == "POST":
        kwargs = {
            "name": request.form.get('name'),
            "country": request.form.get('country'),
            "address": request.form.get('address'),
            "description": request.form.get('description'),
            "mobile": request.form.get('mobile'),
            "timezone": request.form.get('timezone'),
            "image": request.form.get('image'),
            "user_id": user_id
        }
        if not kwargs['name'] or not kwargs['country'] or not \
                kwargs['timezone']:
            return jsonify({"message": "Incomplete parameters"})
        org = storage.create_organization(**kwargs)
        resp = {
            "message": "Organization succesfully created",
            "name": org.name,
            "id": org.id,
            "created_at": org.created_at_local_time_strf(),
            "image": org.image,
            "country": org.country
        }
        return jsonify(resp)
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
        resp = {
            "message": "Returning user organizations",
            "organizations": org
        }
        return jsonify(resp)


@app_look.route('/organizations/<organization_id>',
                methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
@jwt_required()
def organization(organization_id):
    """Handles the resource for a specific organization"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400

    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Token is invalid"}), 400

    org = storage.get_org_by_id(organization_id)
    if not org:
        return jsonify({"message": "Organization dosent exist"}), 404
    user_role = org.get_user_role(user_id)
    if not user_role:
        return jsonify({"message": "User not in Organization"}), 401

    if request.method == 'GET':
        creator_name = "Craetor Account has been deleted"
        if org.creator:
            creator_name = org.creator.full_name()
        resp = {
            "name": org.name,
            "id": org.id,
            "country": org.country,
            "address": org.address,
            "description": org.description,
            "creator": creator_name,
            "image": org.image,
            "time_zone": org.time_zone,
            "created_at": org.created_at_local_time_strf(),
            "mobile": org.mobile,
            "total_products": len(org.items),
            "user_role": user_role
        }
        return jsonify(resp)

    if request.method == 'PUT':
        if user_role != "Admin":
            msg = "Only Admins can update Organization details"
            return jsonify({"message": msg}), 401
        mobile = request.form.get('mobile')
        description = request.form.get('description')
        address = request.form.get('address')
        image = request.form.get('image')
        if not mobile and not description and not address and not image:
            mesg = "Update failed, Empty parameters"
            return jsonify({"message": mesg}), 400
        msg = []
        if mobile:
            org.mobile = mobile
            msg.append("Mobile updated")
        if description:
            org.description = description
            msg.append("Organization description Updated")
        if address:
            org.address = address
            msg.append("Organization address Updated")
        if image:
            org.image = image
            msg.append("Organization image Updated")
        storage.save()
        return jsonify({"message": ", ".join(msg)})

    if request.method == "DELETE":
        if user_role != "Admin":
            msg = "Only Admins can delete this Organization"
            return jsonify({"message": msg}), 401
        storage.delete(org)
        storage.save()
        return jsonify({"message": "Organization account is deleted"})


@app_look.route('/organizations/<organization_id>/sales',
                methods=['GET', 'POST'], strict_slashes=False)
@jwt_required()
def sales(organization_id):
    """Gets and creates sales for an organization"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400
    get_usr = storage.get_user_by_id(user_id)
    if not get_usr:
        return jsonify({"message": "Invalid access"}), 400
    get_org = storage.get_org_by_id(organization_id)
    if not get_org:
        return jsonify({"message": "Invalid access"}), 400

    if request.method == 'POST':
        org = request.get_json()
        items = org.get('items')
        if items is None or not isinstance(items, list):
            msg = "Invalid or missing 'items' in the request JSON"
            return jsonify({"message": msg}), 400
        get_time = get_org.get_local_time()
        list_items = []
        for item in items:
            item_id = item.get('id')
            get_item = storage.get_item_by_id(item_id)
            if not get_item:
                tr = {
                    "status": "failed transaction, wrong product id",
                    "product_id": item_id
                }
                list_items.append(tr)
                continue
            get_quantity = item.get('quantity')
            get_username = get_usr.full_name()
            get_description = item.get('description')
            try:
                make_sale = get_item.remove(get_quantity, get_time,
                                            get_username, get_description)
                tr = make_sale.transaction()
                tr["status"] = "succesful transaction"
                list_items.append(tr)
            except ValueError:
                failed_sale = {
                    "status": "failed transaction, Not enough quantity",
                    "product_id": item_id
                }
                list_items.append(failed_sale)
        return jsonify(list_items), 200
    if request.method == "GET":
        all_sales = get_org.sales
        all_sales.sort(reverse=True, key=lambda p: p.date)
        sales_list = [x.transaction() for x in all_sales]
        page_sent = request.form.get('page')
        try:
            page = int(page_sent)
        except Exception:
            page = 1
        resp = {
            "page": page,
            "data": sales_list,
            "next": None
        }
        if len(sales_list) > 36:
            start = (page - 1) * 36
            end = start + 36
            resp["data"] = sales[start:end]
            resp["next"] = page + 1
        return jsonify(resp)


@app_look.route('/organizations/<organization_id>/purchases',
                methods=['GET'], strict_slashes=False)
@jwt_required()
def purchases(organization_id):
    """Gets and creates sales for an organization"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400
    get_usr = storage.get_user_by_id(user_id)
    if not get_usr:
        return jsonify({"message": "Invalid access"}), 400
    get_org = storage.get_org_by_id(organization_id)
    if not get_org:
        return jsonify({"message": "Invalid access"}), 400
    if request.method == "GET":
        all_purchases = get_org.purchases
        all_purchases.sort(reverse=True, key=lambda p: p.date)
        purchases_list = [x.transaction() for x in all_purchases]
        page_sent = request.form.get('page')
        try:
            page = int(page_sent)
        except Exception:
            page = 1
        resp = {
            "page": page,
            "data": purchases_list,
            "next": None
        }
        if len(purchases_list) > 36:
            start = (page - 1) * 36
            end = start + 36
            resp["data"] = purchases_list[start:end]
            resp["next"] = page + 1
        return jsonify(resp)


@app_look.route('/organizations/<organization_id>/products',
                methods=['GET', 'POST'], strict_slashes=False)
@jwt_required()
def products(organization_id):
    """Handles getting and creating producr resource"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400

    get_usr = storage.get_user_by_id(user_id)
    if not get_usr:
        return jsonify({"message": "Invalid access"}), 400
    org_id = storage.get_org_by_id(organization_id)
    if not org_id:
        return jsonify({"message": "Invalid organization"}), 400

    if request.method == "GET":
        page_sent = request.form.get('page')
        try:
            page = int(page_sent)
        except Exception:
            page = 1
        all_list = []
        for item in org_id.items:
            if item.obsolete is True:
                continue
            all_list.append(item.to_dict())
        all_list.sort(key=lambda p: p['name'])
        resp = {
            "page": page,
            "data": all_list,
            "next": None
        }
        if len(all_list) > 36:
            start = (page - 1) * 36
            end = start + 36
            resp["data"] = all_list[start:end]
            resp["next"] = page + 1
        return jsonify(resp)

    if request.method == 'POST':
        kwarg = {
            'name': request.form.get('name'),
            'cost_price': request.form.get('costPrice'),
            'sale_price': request.form.get('salePrice'),
            'unit': request.form.get('unit'),
            'quantity': request.form.get('quantity'),
            'total_cost': request.form.get('totalCost'),
            'category_id': request.form.get('categoryId'),
            'user_name': get_usr.full_name()
        }

        if not kwarg["name"] or not kwarg["sale_price"] \
                or not kwarg["quantity"]:
            return jsonify({"message": "Incomplete data"}), 400
        item = org_id.create_item(**kwarg)
        return jsonify(item.to_dict())


@app_look.route('/organizations/<organization_id>/products/search',
                methods=['GET'], strict_slashes=False)
@jwt_required()
def product_search(organization_id):
    """Returns a list of items that match the keyword"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400

    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Token is invalid"}), 400

    org = storage.get_org_by_id(organization_id)
    if not org:
        return jsonify({"message": "Organization dosent exist"}), 404
    user_role = org.get_user_role(user_id)
    if not user_role:
        return jsonify({"message": "User not in Organization"}), 401

    if request.method == "GET":
        keyword = request.form.get('keyword')
        page_sent = request.form.get('page')
        try:
            page = int(page_sent)
        except Exception:
            page = 1
        search_items = []
        if not keyword:
            return jsonify({"message": "No search keyword provided"}), 400
        for item in org.items:
            if item.name.lower().startswith(keyword.lower()):
                if item.obsolete:
                    continue
                search_items.append(item.to_dict())
        search_items.sort(key=lambda p: p['name'])
        resp = {
            "page": page,
            "data": search_items,
            "next": None
        }
        if len(search_items) > 36:
            start = (page - 1) * 36
            end = start + 36
            resp["data"] = search_items[start:end]
            resp["next"] = page + 1
        return jsonify(resp)


@app_look.route('/organizations/<organization_id>/products/<product_id>',
                methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
@jwt_required()
def product(organization_id, product_id):
    """Gets and updates a particular product in the inventory"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400

    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Token is invalid"}), 400

    org = storage.get_org_by_id(organization_id)
    if not org:
        return jsonify({"message": "Organization dosent exist"}), 404
    user_role = org.get_user_role(user_id)
    if not user_role:
        return jsonify({"message": "User not in Organization"}), 401
    item = storage.get_item_by_id(product_id)
    if not item:
        return jsonify({"message": "Invalid product id data"}), 400

    if request.method == "PUT":
        # for adding more quantities and updating other values.
        msg = []
        transaction = {}
        quantity_str = request.form.get('quantity')
        purchase_cost_str = request.form.get('purchaseCost')
        description = request.form.get('description')
        name = request.form.get('name')
        cost_price_str = request.form.get('costPrice')
        sale_price_str = request.form.get('salePrice')
        alert_level_str = request.form.get('lowStockLevel')
        category_id = request.form.get('categoryId')
        image = request.form.get('image')
        unit = request.form.get('unit')

        if quantity_str:
            try:
                quantity = int(quantity_str)
            except Exception:
                return jsonify({"message": "Invalid quntity data"}), 400
            try:
                purchase_cost = float(purchase_cost_str)
            except Exception:
                purchase_cost = 0
            pur = item.add(quantity, purchase_cost, org.get_local_time(),
                           description, user.full_name())
            msg.append(f"{item.name} purchase succesfully added")
            transaction = pur.transaction()
        if name:
            item.name = name
            msg.append("Product name succesfully updated")
        if cost_price_str:
            try:
                cost_price = float(cost_price_str)
            except Exception:
                return jsonify({"message": "Invalid costPrice data"}), 400
            item.cost_price = cost_price
            msg.append("Product cost price succesfully updated")
        if sale_price_str:
            try:
                sale_price = float(sale_price_str)
            except Exception:
                return jsonify({"message": "Invalid salePrice data"}), 400
            item.sale_price = sale_price
            msg.append("Product sale price succesfully updated")
        if alert_level_str:
            try:
                alert_level = int(alert_level_str)
            except Exception:
                return jsonify({"message": "Invalid low stock data"}), 400
            item.alert_level = alert_level
            msg.append("Product low stock warning updated")
        if image:
            item.image = image
            msg.append("Product image updated")
        if unit:
            item.unit = unit
            msg.append("Product's unit name succesfully updated")
        if category_id:
            item.category_id = category_id
            msg.append("Product category succesfully updated")
        storage.save()
        resp = {
            "message": ", ".join(msg),
            "transaction": transaction
        }
        return jsonify(resp)
    if request.method == "GET":
        return jsonify(item.to_dict())
    if request.method == "DELETE":
        quantity_str = request.form.get("quantity")
        sale_str = request.form.get("sale")
        description = request.form.get('description')
        if quantity_str:
            try:
                quantity = int(quantity_str)
            except Exception:
                return jsonify({"message": "Invalid quntity data"}), 400
            try:
                sale = float(sale_str)
            except Exception:
                sale = 0
            sale_tr = item.remove(quantity, org.get_local_time(),
                                  user.full_name(), description, sale)
            msg = f"{quantity} unit of {item.name} removed"
            resp = {
                "message": msg,
                "transaction": sale_tr.transaction()
            }
            return jsonify(resp)


@app_look.route('/organizations/<organization_id>/products/category',
                methods=['GET'], strict_slashes=False)
@jwt_required()
def proudct_category(organization_id):
    """Returns products based on their organizaion"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400

    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Token is invalid"}), 400

    org = storage.get_org_by_id(organization_id)
    if not org:
        return jsonify({"message": "Organization dosent exist"}), 404
    user_role = org.get_user_role(user_id)
    if not user_role:
        return jsonify({"message": "User not in Organization"}), 401
    if request.method == "GET":
        category_id = request.form.get('categoryId')
        page_sent = request.form.get('page')
        category = storage.get_category_by_id(category_id)
        if not category:
            return jsonify({"message": "Incorrect category id"}), 400
        cat_items = []
        try:
            page = int(page_sent)
        except Exception:
            page = 0
        for item in category.items:
            if item.obsolete is True:
                continue
            cat_items.append(item.to_dict())
        cat_items.sort(key=lambda p: p['name'])
        resp = {
            "page": page,
            "data": cat_items,
            "next": None
        }
        if len(cat_items) > 36:
            start = (page - 1) * 36
            end = start + 36
            resp["data"] = cat_items[start:end]
            resp["next"] = page + 1
        return jsonify(resp)


@app_look.route('/organizations/<organization_id>/categories',
                methods=['GET', 'POST'], strict_slashes=False)
@jwt_required()
def categories(organization_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Invalid token"}), 400
    user = storage.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Token is invalid"}), 400

    org = storage.get_org_by_id(organization_id)
    if not org:
        return jsonify({"message": "Organization dosent exist"}), 404
    user_role = org.get_user_role(user_id)
    if not user_role:
        return jsonify({"message": "User not in Organization"}), 401

    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            return jsonify({"message": "Incomplete parameters"})
        new_cat = org.add_category(name, description)
        resp = {
            "message": "New category created",
            "category": {
                "name": new_cat.name,
                "id": new_cat.id,
                "description": new_cat.description,
                "created_at": org.localize(new_cat.created_at)
            }
        }
        return jsonify(resp)

    if request.method == "GET":
        resp = []
        for cat in org.categories:
            cat_detail = {
                "name": cat.name,
                "id": cat.id,
                "description": cat.description,
                "created_at": org.localize(cat.created_at)
            }
            resp.append(cat_detail)
        return jsonify(resp)
