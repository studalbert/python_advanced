from datetime import datetime
import json
import shlex
import subprocess
from logging import logMultiprocessing


def time_func():
    cmd_str = 'grep \'"message": "Enter measure_me"\' measure_me.log'
    cmd = shlex.split(cmd_str)
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    stdout, stderr = proc.communicate()
    logs = stdout.split("\n")
    logs_enter = [json.loads(log) for log in logs if log != ""]

    cmd_str = 'grep \'"message": "Leave measure_me"\' measure_me.log'
    cmd = shlex.split(cmd_str)
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    stdout, stderr = proc.communicate()
    logs = stdout.split("\n")
    logs_leave = [json.loads(log) for log in logs if log != ""]

    res_time = None

    for log_leave, log_enter in zip(logs_leave, logs_enter):
        time_leave, time_enter = log_leave["time"], log_enter["time"]
        time_leave_strptime, time_enter_strptime = datetime.strptime(
            time_leave, "%H:%M:%S.%f"
        ), datetime.strptime(time_enter, "%H:%M:%S.%f")
        if res_time is None:
            res_time = time_leave_strptime - time_enter_strptime
        else:
            res_time += time_leave_strptime - time_enter_strptime

    return res_time / 15


if __name__ == "__main__":

    print(f"среднее время выполнения функции measure_me: {time_func()}")
