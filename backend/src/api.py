import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import requires_auth, AuthError

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


# ROUTES
@app.route('/drinks', methods=["GET"])
def get_drinks():
    data = Drink.query.all()
    drinks = [drink.short() for drink in data]

    return jsonify({
        "success": True,
        "drinks": drinks
    }), 200


@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail():
    data = Drink.query.all()
    drinks = [drink.long() for drink in data]

    return jsonify({
        "success": True,
        "drinks": drinks
    }), 200


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def post_drinks():
    data_json = request.get_json()

    if not data_json:
        abort(422)

    if "recipe" not in data_json and "title" not in data_json and "id" not in data_json:
        abort(422)

    try:
        new_drink = Drink(title=data_json["title"],
                          recipe=data_json["recipe"]
                          )
        new_drink.insert()

        return jsonify({
            "success": True,
            "drinks": [new_drink.long()]
        }), 200
    except exc:
        print(exc)
        db.session.rollback()
    finally:
        db.session.close()


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drink(id: int):
    drink = Drink.query.filter_by(id=id).one_or_none()
    data_json = request.get_json()

    if not drink:  # if drink does not exist user probably typed URL by himself
        abort(404)

    if data_json["id"] != id:  # check if link's and json ID data are identical
        abort(422)

    # Check if it has all the components
    if "recipe" not in data_json and "title" not in data_json and "id" not in data_json:
        abort(422)

    if not (data_json["recipe"] is list):
        abort(422)

    try:
        drink.title = data_json["title"]
        drink.recipe = data_json["recipe"]
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200
    except exc:
        print(exc)
        db.session.rollback()
    finally:
        db.session.query()


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drinks(id):
    drink: Drink = Drink.query.filter_by(id=id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()

        return jsonify({
            "success": True,
            "delete": id
        }), 200
    except exc:
        print(exc)
        db.session.rollback()
    finally:
        db.session.close()


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        "success": False,
        "error": AuthError,
        "message": "Authentication Error"
    }), 401
