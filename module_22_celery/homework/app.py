"""
В этом файле будет ваше Flask-приложение
"""

from flask import Flask, request, jsonify
from celery import group, chord
from sqlalchemy.exc import IntegrityError

from tasks import celery_app, task_blur_image, task_send_email
from model import User, session
import os

app = Flask(__name__)


@app.route("/blur", methods=["POST"])
def blur_images():
    images = request.files.getlist("images")
    user_email = request.form.get("email")
    if images and isinstance(images, list):
        images_list = []
        for image in images:
            image.save(f"img/{image.filename}")
            images_list.append(f"img/{image.filename}")

        task_group = group(task_blur_image.s(image) for image in images_list)
        result = chord(
            task_group,
            task_send_email.s(user_email=user_email).set(immutable=True),
        ).apply_async()
        return jsonify({"group_id": result.id}), 202
    else:
        return jsonify({"error": "invalid parameter"}), 400


@app.route("/status/<group_id>", methods=["GET"])
def status_group_id(group_id):
    result = celery_app.AsyncResult(group_id)
    if result:
        return jsonify({'state': result.state, 'info': result.info})
    else:
        return jsonify({"error": "Group not found."}), 404


@app.route("/subscribe", methods=["POST"])
def subscribe_mailing():
    user_email = request.form.get("email")
    new_user = User(email=user_email)
    session.add(new_user)
    try:
        session.commit()
        return jsonify({"message": "Subscription successful"}), 200
    except IntegrityError:
        session.rollback()
        return {"error": f"User with email {user_email} already exists."}, 409


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe_mailing():
    user_email = request.form.get("email")
    del_count = session.query(User).filter(User.email == user_email).delete()
    session.commit()
    if del_count > 0:
        return {"message": f"User with email {user_email} unsubscribe"}, 200
    else:
        return {"error": f"No user found with email {user_email}."}, 404


if __name__ == "__main__":
    app.run(debug=True)
