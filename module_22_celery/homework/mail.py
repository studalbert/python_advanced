import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER


def send_email(receiver: str, filename: str):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = f"Ваши изображения."
        email["From"] = SMTP_USER
        email["To"] = receiver

        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        email.attach(part)
        text = email.as_string()

        server.sendmail(SMTP_USER, receiver, text)


def send_email_weakly(receiver: str):

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = f"Не забывайте о нас. Ждем вас на на нашем сайте!"
        email["From"] = SMTP_USER
        email["To"] = receiver

        # Создаем текстовую часть письма
        text_part = MIMEText(
            "Заходите почаще на наш сайт для обработки фотографии! Ждем вас!", "plain"
        )
        email.attach(text_part)

        # Преобразуем объект email в строку
        text = email.as_string()

        # Отправляем письмо
        server.sendmail(SMTP_USER, receiver, text)
