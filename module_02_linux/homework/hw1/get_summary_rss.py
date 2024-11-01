"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    summ_size = 0
    with open(ps_output_file_path, 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            columns = line.split()
            summ_size += int(columns[5])
        for i in ['Б', 'KiB', 'MiB', 'GiB']:
            if summ_size // 1024:
                summ_size /= 1024
            else:
                result = f'{round(summ_size, 3)} {i}'
                break
        return result


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
