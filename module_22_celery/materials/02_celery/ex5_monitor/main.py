from tasks import heavy_task


def get_factorial(arg):
    result = heavy_task.apply_async(args=(arg,))

    while not result.ready():
        # Задача еще выполняется
        pass

    if result.successful():
        result_value = result.get()
    else:
        # Информация об ошибке
        result_value = result.result

    print(result_value)


get_factorial(50)
# 608281864034267560872252163321295376887552831379210240000000000
get_factorial("Сейчас будет ошибка")
# 'str' object cannot be interpreted as an integer

for i in range(100):
    get_factorial(10 * i)
