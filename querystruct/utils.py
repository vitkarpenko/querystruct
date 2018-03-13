""" Различные полезные функции
"""


def isnumber(value):
    """ Проверяет, является ли value представлением числа. """
    try:
        float(value)
    except ValueError:
        return False
    return True


def format_sql_value(value):
    """ Форматирует значение в соответствии со стандартом SQL:
        - Оборачивает строку в одиночные кавычки, если она не является строковым представлением числа.
        - None -> NULL
        - True, False -> TRUE, FALSE
    """
    if value is None:
        return 'NULL'
    elif not isnumber(value):
        return f"'{value}'"
    elif isinstance(value, bool):
        return str(value).upper()
    else:
        return value
