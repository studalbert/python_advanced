from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from flask import Flask, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func, cast, Text

from models import session, Base, engine, User, Coffee, Session
import requests
import random

from schemas import UserSchema, CoffeeSchema

app = Flask(__name__)
coffee_ids = []


def task1(url):
    sess = Session()
    response = requests.get(url)
    try:
        if response.status_code == 200:
            coffee_data = response.json()
            coffee = Coffee(
                title=coffee_data["blend_name"],
                origin=coffee_data["origin"],
                intensifier=coffee_data["intensifier"],
                notes=coffee_data["notes"],
            )
            sess.add(coffee)
            sess.commit()
            coffee_ids.append(coffee.id)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        sess.rollback()
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
        sess.rollback()
    finally:
        sess.close()


def task2(url):
    sess = Session()
    response = requests.get(url)
    try:
        if response.status_code == 200:
            address_data = response.json()
            user = User(
                name=f"user_{random.randint(1, 1000)}",
                has_sale=random.choice([True, False]),
                address=address_data if address_data else {},  # JSON-адрес
                coffee_id=random.choice(coffee_ids),  # Случайный кофе
            )
            sess.add(user)
            sess.commit()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        sess.rollback()
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
        sess.rollback()
    finally:
        sess.close()


# @app.before_request
# def before_first_request():
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#
#     with ThreadPool(processes=cpu_count() * 5) as pool:
#         result1 = pool.map(
#             task1, ["https://random-data-api.com/api/coffee/random_coffee"] * 10
#         )
#         result2 = pool.map(
#             task2, ["https://random-data-api.com/api/address/random_address"] * 10
#         )


@app.route("/users", methods=["POST"])
def create_user():

    user_schema = UserSchema()
    try:
        data = request.json
        validated_data = user_schema.load(data)

        coffee_id = validated_data.get("coffee_id")
        if coffee_id:
            coffee = session.query(Coffee).get(coffee_id)
            if not coffee:
                return jsonify({"message": "Coffee not found"}), 400

        new_user = User(
            name=validated_data["name"],  # Use validated data
            has_sale=validated_data.get("has_sale", False),
            address=validated_data["address"],
            coffee_id=coffee_id,
        )
        session.add(new_user)
        session.commit()

        dumped_data = user_schema.dump(new_user)
        return jsonify(dumped_data), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/coffee/search", methods=["GET"])
def search_coffee():
    title = request.args.get("title")
    if not title:
        return jsonify({"message": "Title parameter is required"}), 400
    try:
        coffee_schema = CoffeeSchema()
        stmt = select(Coffee).where(Coffee.title.match(title))
        res = session.execute(stmt).scalars().all()
        if res:
            coffees = coffee_schema.dump(res, many=True)
            return jsonify(coffees), 200

    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/coffee/notes", methods=["GET"])
def get_uniq_notes():
    stmt = select(func.distinct(Coffee.notes))
    try:
        result = session.execute(stmt).scalar()
        return jsonify(result), 200
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/users/by_country", methods=["GET"])
def get_users_by_country():
    country = request.args.get("country")

    if not country:
        return jsonify({"message": "country parameter is required"}), 400
    try:
        user_schema = UserSchema()
        stmt = select(User).where(User.address.op("->>")("country") == country)
        res = session.execute(stmt).scalars().all()
        if res:
            users = user_schema.dump(res, many=True)
            return jsonify(users), 200
        else:
            return jsonify({"message": "No users found for this country"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
