from flask import Blueprint, jsonify, request, g
from jwt_utils import token_required
from config import get_connection


products = Blueprint('products', __name__)


@products.route("/api/products", methods=["GET"])
@token_required
def get_products():
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    code,
                    name,
                    description,
                    qty,
                    price
                FROM tblProduct
                WHERE user_id = %s
                """,
                (g.user_id,)
            )
            data = cursor.fetchall()

            if data is None:
                return jsonify({"message": "Products are not found."}), 404

            for prod in data:
                prod["price"] = float(prod["price"])

            return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": "An internal server error occured."}), 500
    finally:
        if conn:
            conn.close()

@products.route("/api/products/<int:id>", methods=["GET"])
@token_required
def get_by_id(id):
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    code,
                    name,
                    description,
                    price,
                    qty
                FROM tblProduct
                WHERE id = %s AND user_id = %s
                """,
                (id, g.user_id)
            )
            data = cursor.fetchone()

            if data is None:
                return jsonify({"message": "Product was not found."}), 404

            data["price"] = float(data["price"])

            return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": "An internal server error occured."}), 500
    finally:
        if conn:
            conn.close()


@products.route("/api/products", methods=["POST"])
@token_required
def add_product():

    data = request.get_json()
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tblProduct
                    (code, name, description, qty, price, user_id)
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
                """,
                (
                    data.get("code"),
                    data.get("name"),
                    data.get("description"),
                    data.get("qty"),
                    data.get("price"),
                    g.user_id
                )
            )
            conn.commit()

            return jsonify({"message": "Added successfully."}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close()


@products.route("/api/products/<int:id>", methods=["PUT"])
@token_required
def update_product(id):
    data = request.get_json()
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id FROM tblProduct WHERE id = %s
                """,
                (id,)
            )
            prod = cursor.fetchone()

            if prod is None:
                return jsonify({"message": "Product was not found."}), 404

            cursor.execute(
                """
                UPDATE tblProduct
                SET
                    code = %s,
                    name = %s,
                    description = %s,
                    qty = %s,
                    price = %s
                WHERE id = %s AND user_id = %s
                """,
                (
                    data.get("code"),
                    data.get("name"),
                    data.get("description"),
                    data.get("qty"),
                    data.get("price"),
                    id,
                    g.user_id
                )
            )
            conn.commit()

            return jsonify({"message": "Updated successfully."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close()
        

