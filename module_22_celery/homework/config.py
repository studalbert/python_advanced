"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""

# https://yandex.ru/support/mail/mail-clients/others.html
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_HOST = "smtp.yandex.ru"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_PORT = 587
