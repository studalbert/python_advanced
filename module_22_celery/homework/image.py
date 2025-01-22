"""
Здесь происходит логика обработки изображения
"""

from typing import Optional
from PIL import Image, ImageFilter
import os
import zipfile


def blur_image(src_filename: str, dst_filename: Optional[str] = None):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    if not dst_filename:
        dst_filename = f"blur_{src_filename}"

    with Image.open(src_filename) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        new_img.save(dst_filename)

    zip_filename = "blurred_images.zip"
    with zipfile.ZipFile(zip_filename, "a") as zipf:
        zipf.write(
            dst_filename, os.path.basename(dst_filename)
        )  # Добавляем файл в архив

    print(f"Blurred image saved as {dst_filename} and added to {zip_filename}")
