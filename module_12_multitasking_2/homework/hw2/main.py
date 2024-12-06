import subprocess
import os


def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    try:
        command_str = f"ps -u {username} -o pid --no-headers | wc -l"
        result = subprocess.run(command_str, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Ошибка при выполнении команды: {result.stderr}")
            return 0
        output = result.stdout.strip()
        return int(output) if output.isdigit() else 0
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return 0


def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    try:
        # Команда для получения всех PID в дереве процессов, включая root_pid
        pgrep_command = f"pgrep --parent {root_pid} -d ','"
        result = subprocess.run(
            pgrep_command, shell=True, capture_output=True, text=True
        )
        if result.returncode != 0:  # Если команда завершилась с ошибкой
            print(f"Ошибка при выполнении команды pgrep: {result.stderr}")
            return 0.0

        # Добавляем root_pid к списку потомков
        child_pids = result.stdout.strip()
        all_pids = f"{root_pid},{child_pids}" if child_pids else str(root_pid)
        # Команда для получения использования памяти указанными процессами
        ps_command = f"ps -o pmem --no-headers -p {all_pids}"
        result = subprocess.run(ps_command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:  # Если команда завершилась с ошибкой
            print(f"Ошибка при выполнении команды ps: {result.stderr}")
            return 0.0

        # Читаем результат и суммируем использование памяти
        memory_usage_lines = result.stdout.strip().splitlines()
        memory_usage = sum(float(line) for line in memory_usage_lines if line.strip())

        return memory_usage
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return 0.0


if __name__ == "__main__":
    username = "user"
    current_pid = os.getpid()

    # Количество процессов пользователя
    user_process_count = process_count(username)
    print(f"Количество процессов пользователя {username}: {user_process_count}")

    # Суммарное потребление памяти
    memory_usage = total_memory_usage(current_pid)
    print(
        f"Суммарное потребление памяти для дерева процессов с корнем {current_pid}: {memory_usage:.2f}%"
    )
