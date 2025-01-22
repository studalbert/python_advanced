import random
from threading import Thread

from flask import Flask, request, jsonify
from celery import Celery, group
import time

app = Flask(__name__)

# Конфигурация Celery
celery = Celery(
    app.name,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Хранение информации о задачах и очередях
control_info = {}


def update_control_info():
    global control_info
    while True:
        inspect = celery.control.inspect()
        control_info["active"] = inspect.active() or {}
        control_info["registered"] = inspect.registered() or {}
        control_info["stats"] = inspect.stats() or {}
        time.sleep(10)  # Обновление информации каждые 10 секунд


# Задача Celery для обработки изображения
@celery.task
def process_image(image_id):
    # В реальной ситуации здесь может быть обработка изображения
    # В данном примере просто делаем задержку для демонстрации
    time.sleep(random.randint(5, 15))
    return f"Image {image_id} processed"


@app.route("/process_images", methods=["POST"])
def process_images():
    images = request.json.get("images")

    if images and isinstance(images, list):
        # Создаем группу задач
        task_group = group(process_image.s(image_id) for image_id in images)

        # Запускаем группу задач и сохраняем ее
        result = task_group.apply_async()
        result.save()

        # Возвращаем пользователю ID группы для отслеживания
        return jsonify({"group_id": result.id}), 202
    else:
        return jsonify({"error": "Missing or invalid images parameter"}), 400


@app.route("/status/<group_id>", methods=["GET"])
def get_group_status(group_id):
    result = celery.GroupResult.restore(group_id)

    if result:
        # Если группа с таким ID существует,
        # возвращаем долю выполненных задач
        status = result.completed_count() / len(result)
        return jsonify({"status": status}), 200
    else:
        # Иначе возвращаем ошибку
        return jsonify({"error": "Invalid group_id"}), 404


@app.route("/cancel/<group_id>", methods=["GET"])
def cancel_group(group_id):
    result = celery.GroupResult.restore(group_id)
    if result:
        # Если группа с таким ID существует,
        # отменяем группу задач
        for task in result:
            task.revoke(terminate=True)
        return jsonify({"message": "task group canceled"}), 200
    else:
        # Иначе возвращаем ошибку
        return jsonify({"error": "Invalid group_id"}), 404


@app.route("/control", methods=["GET"])
def control_tasks():
    # Запуск потока для обновления информации о задачах и очередях
    thread = Thread(target=update_control_info)
    thread.daemon = True  # Завершить поток при завершении основного приложения
    thread.start()
    return jsonify(control_info), 200


if __name__ == "__main__":
    app.run(debug=True)
