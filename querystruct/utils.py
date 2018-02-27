""" Различные полезные функции
"""


def isnumber(string):
    """ Проверяет, является ли string строковым представлением числа """
    try:
        float(string)
    except ValueError:
        return False
    return True


def quote_alphabetic(string):
    """ Оборачивает строку в одиночные кавычки, если она не является строковым представлением числа.
    """
    return string if isnumber(string) else f"'{string}'"
